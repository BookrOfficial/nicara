from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
from bson import ObjectId

# Import models and services
from models import (
    User, UserCreate, ChatMessage, ChatMessageCreate, MessageSender, MessageType,
    UserAchievement, UserDailyChallenge, CravingLog, CravingLogCreate,
    HealthStats, QuickActionRequest, UserProgressResponse, SocialStats
)
from database import (
    connect_to_mongo, close_mongo_connection,
    get_users_collection, get_chat_messages_collection,
    get_achievements_collection, get_daily_challenges_collection,
    get_craving_logs_collection, get_social_stats_collection,
    CRAVING_TIPS, ACHIEVEMENT_DEFINITIONS, LEVEL_DEFINITIONS
)
from services.ai_service import AICoachService
from services.progress_service import ProgressService
from services.achievement_service import AchievementService
from services.challenge_service import ChallengeService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Nicara API", description="AI-Powered Quit Smoking Coach API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize services
ai_service = AICoachService()

# Startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Helper functions
def convert_objectid_to_str(data):
    """Convert MongoDB ObjectIds to strings for JSON serialization"""
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

async def get_user_by_id(user_id: str) -> User:
    """Get user by ID, raise 404 if not found"""
    users_collection = await get_users_collection()
    user_dict = await users_collection.find_one({"id": user_id})
    if not user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user_dict)

async def update_user(user: User):
    """Update user in database"""
    users_collection = await get_users_collection()
    user.updated_at = datetime.utcnow()
    await users_collection.update_one(
        {"id": user.id},
        {"$set": user.dict()}
    )

# API Routes

@api_router.get("/")
async def root():
    return {"message": "Welcome to Nicara API - Your AI Quit Smoking Coach!"}

# User Management
@api_router.post("/users", response_model=User)
async def create_user(user_create: UserCreate):
    """Create a new user and initialize their progress tracking"""
    users_collection = await get_users_collection()
    social_stats_collection = await get_social_stats_collection()
    
    # Create user
    user = User(**user_create.dict())
    user.streak = ProgressService.calculate_streak(user)
    
    # Insert user
    await users_collection.insert_one(user.dict())
    
    # Initialize achievements
    await AchievementService.initialize_user_achievements(user.id)
    
    # Initialize social stats
    social_stats = SocialStats(user_id=user.id)
    await social_stats_collection.insert_one(social_stats.dict())
    
    # Create first daily challenge
    await ChallengeService.get_or_create_daily_challenge(user.id)
    
    return user

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get user profile"""
    return await get_user_by_id(user_id)

@api_router.put("/users/{user_id}", response_model=User)
async def update_user_profile(user_id: str, user_update: UserCreate):
    """Update user profile"""
    user = await get_user_by_id(user_id)
    
    # Update fields
    for field, value in user_update.dict().items():
        setattr(user, field, value)
    
    # Recalculate streak
    user.streak = ProgressService.calculate_streak(user)
    
    await update_user(user)
    return user

# Progress Tracking
@api_router.get("/progress/{user_id}", response_model=UserProgressResponse)
async def get_user_progress(user_id: str):
    """Get comprehensive user progress data"""
    user = await get_user_by_id(user_id)
    social_stats_collection = await get_social_stats_collection()
    
    # Calculate health stats
    health_stats = ProgressService.calculate_health_stats(user)
    
    # Get today's challenge
    daily_challenge = await ChallengeService.get_or_create_daily_challenge(user_id)
    
    # Get recent achievements
    recent_achievements = await AchievementService.get_recent_achievements(user_id, 4)
    
    # Get social stats
    social_stats_dict = await social_stats_collection.find_one({"user_id": user_id})
    social_stats = SocialStats(**social_stats_dict) if social_stats_dict else SocialStats(user_id=user_id)
    
    return UserProgressResponse(
        user=user,
        health_stats=health_stats,
        daily_challenge=daily_challenge,
        recent_achievements=recent_achievements,
        social_stats=social_stats
    )

@api_router.get("/health-stats/{user_id}", response_model=HealthStats)
async def get_health_stats(user_id: str):
    """Get user health statistics"""
    user = await get_user_by_id(user_id)
    return ProgressService.calculate_health_stats(user)

# AI Chat System
@api_router.post("/chat")
async def send_chat_message(message_create: ChatMessageCreate):
    """Send message to AI coach and get response"""
    chat_collection = await get_chat_messages_collection()
    
    # Get user and health stats for context
    user = await get_user_by_id(message_create.user_id)
    health_stats = ProgressService.calculate_health_stats(user)
    
    # Create user message
    user_message = ChatMessage(
        user_id=message_create.user_id,
        sender=MessageSender.user,
        message=message_create.message,
        message_type=MessageType.message
    )
    
    # Save user message
    await chat_collection.insert_one(user_message.dict())
    
    # Get AI response
    try:
        ai_response_text = await ai_service.get_ai_response(
            message_create.message, user, health_stats
        )
        
        # Determine message type
        message_type = ai_service.determine_message_type(ai_response_text)
        
        # Create AI message
        ai_message = ChatMessage(
            user_id=message_create.user_id,
            sender=MessageSender(user.avatar),
            message=ai_response_text,
            message_type=message_type
        )
        
        # Save AI message
        await chat_collection.insert_one(ai_message.dict())
        
        # Check for new achievements after chat interaction
        unlocked_achievements = await AchievementService.check_and_unlock_achievements(user, health_stats)
        
        # Update user if achievements were unlocked
        if unlocked_achievements:
            await update_user(user)
        
        return {
            "user_message": user_message,
            "ai_message": ai_message,
            "achievements_unlocked": unlocked_achievements
        }
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get AI response")

@api_router.get("/chat/{user_id}")
async def get_chat_history(user_id: str, limit: int = 50):
    """Get chat message history"""
    chat_collection = await get_chat_messages_collection()
    
    messages = await chat_collection.find({
        "user_id": user_id
    }).sort("timestamp", -1).limit(limit).to_list(limit)
    
    # Reverse to get chronological order
    messages.reverse()
    
    return [ChatMessage(**msg) for msg in messages]

@api_router.post("/chat/quick-action")
async def handle_quick_action(action_request: QuickActionRequest):
    """Handle quick action buttons in chat"""
    user = await get_user_by_id(action_request.user_id)
    health_stats = ProgressService.calculate_health_stats(user)
    chat_collection = await get_chat_messages_collection()
    
    try:
        ai_response_text = await ai_service.handle_quick_action(
            action_request.action_type, user, health_stats, action_request.context
        )
        
        message_type = ai_service.determine_message_type(ai_response_text)
        
        ai_message = ChatMessage(
            user_id=action_request.user_id,
            sender=MessageSender(user.avatar),
            message=ai_response_text,
            message_type=message_type,
            context={"quick_action": action_request.action_type}
        )
        
        await chat_collection.insert_one(ai_message.dict())
        
        return {
            "ai_message": ai_message,
            "action_type": action_request.action_type
        }
        
    except Exception as e:
        print(f"Error handling quick action: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to handle quick action")

# Achievement System
@api_router.get("/achievements/{user_id}")
async def get_user_achievements(user_id: str):
    """Get all user achievements"""
    achievements = await AchievementService.get_user_achievements(user_id)
    return achievements

@api_router.get("/achievements/available")
async def get_available_achievements():
    """Get all available achievement definitions"""
    return ACHIEVEMENT_DEFINITIONS

@api_router.post("/achievements/{user_id}/check")
async def check_achievements(user_id: str):
    """Manually trigger achievement checking"""
    user = await get_user_by_id(user_id)
    health_stats = ProgressService.calculate_health_stats(user)
    
    unlocked = await AchievementService.check_and_unlock_achievements(user, health_stats)
    
    if unlocked:
        await update_user(user)
    
    return {
        "achievements_unlocked": unlocked,
        "message": f"Checked achievements. {len(unlocked)} new achievements unlocked."
    }

# Daily Challenges
@api_router.get("/challenges/{user_id}/daily")
async def get_daily_challenge(user_id: str):
    """Get today's daily challenge"""
    challenge = await ChallengeService.get_or_create_daily_challenge(user_id)
    return challenge

@api_router.post("/challenges/{user_id}/{challenge_id}/complete")
async def complete_daily_challenge(user_id: str, challenge_id: str):
    """Mark daily challenge as completed"""
    user = await get_user_by_id(user_id)
    
    # Complete challenge
    result = await ChallengeService.complete_daily_challenge(user_id, challenge_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    # Award XP to user
    xp_result = ProgressService.award_xp(user.xp, result["xp_awarded"])
    user.xp = xp_result["new_xp"]
    
    if xp_result["level_up"]:
        user.current_level = xp_result["new_level"]
    
    await update_user(user)
    
    # Check for achievements
    health_stats = ProgressService.calculate_health_stats(user)
    unlocked = await AchievementService.check_and_unlock_achievements(user, health_stats)
    
    if unlocked:
        await update_user(user)
    
    return {
        **result,
        "level_up": xp_result["level_up"],
        "new_level": xp_result["new_level"] if xp_result["level_up"] else None,
        "achievements_unlocked": unlocked
    }

@api_router.get("/challenges/{user_id}/history")
async def get_challenge_history(user_id: str, limit: int = 30):
    """Get challenge completion history"""
    return await ChallengeService.get_challenge_history(user_id, limit)

@api_router.get("/challenges/{user_id}/stats")
async def get_challenge_stats(user_id: str):
    """Get challenge statistics"""
    return await ChallengeService.get_challenge_stats(user_id)

# Craving Management
@api_router.post("/cravings")
async def log_craving(craving: CravingLogCreate):
    """Log a craving incident"""
    cravings_collection = await get_craving_logs_collection()
    
    craving_log = CravingLog(**craving.dict())
    await cravings_collection.insert_one(craving_log.dict())
    
    # Check for achievements (craving management)
    user = await get_user_by_id(craving.user_id)
    health_stats = ProgressService.calculate_health_stats(user)
    unlocked = await AchievementService.check_and_unlock_achievements(user, health_stats)
    
    if unlocked:
        await update_user(user)
    
    return {
        "craving_log": craving_log,
        "achievements_unlocked": unlocked,
        "message": "Craving logged successfully. You're doing great managing your cravings!"
    }

@api_router.get("/cravings/{user_id}")
async def get_craving_history(user_id: str, limit: int = 50):
    """Get craving log history"""
    cravings_collection = await get_craving_logs_collection()
    
    cravings = await cravings_collection.find({
        "user_id": user_id
    }).sort("timestamp", -1).limit(limit).to_list(limit)
    
    return [CravingLog(**craving) for craving in cravings]

@api_router.get("/craving-tips")
async def get_craving_tips():
    """Get all available craving tips"""
    return CRAVING_TIPS

@api_router.post("/craving-tips/{tip_id}/used")
async def track_tip_usage(tip_id: str, user_id: str):
    """Track when a user uses a specific tip"""
    # For now, just return success. Can be extended to track usage statistics
    return {
        "success": True,
        "message": f"Tip usage tracked for tip {tip_id}"
    }

# Utility endpoints
@api_router.get("/levels")
async def get_level_definitions():
    """Get all level definitions"""
    return LEVEL_DEFINITIONS

@api_router.get("/quotes")
async def get_motivational_quotes():
    """Get motivational quotes"""
    quotes = [
        "Every cigarette you don't smoke is doing you good. - Unknown",
        "The best time to quit smoking was 20 years ago. The second best time is now. - Chinese Proverb", 
        "You are stronger than your cravings. Keep going! - Nicara Team",
        "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
        "Don't give up what you want most for what you want now. - Richard G. Scott",
        "The groundwork for all happiness is good health. - Leigh Hunt"
    ]
    return {"quotes": quotes}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
