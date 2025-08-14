import random
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from models import UserDailyChallenge
from database import (
    get_daily_challenges_collection,
    DAILY_CHALLENGE_DEFINITIONS
)


class ChallengeService:
    
    @staticmethod
    async def get_or_create_daily_challenge(user_id: str) -> Optional[Dict[str, Any]]:
        """Get today's challenge or create a new one if it doesn't exist"""
        challenges_collection = await get_daily_challenges_collection()
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check if user already has a challenge for today
        existing_challenge = await challenges_collection.find_one({
            "user_id": user_id,
            "date": today
        })
        
        if existing_challenge:
            # Merge with definition data
            challenge_def = next((c for c in DAILY_CHALLENGE_DEFINITIONS 
                                if c["id"] == existing_challenge["challenge_id"]), None)
            if challenge_def:
                return {**existing_challenge, **challenge_def}
            return existing_challenge
        
        # Create new daily challenge
        available_challenges = DAILY_CHALLENGE_DEFINITIONS.copy()
        
        # Get user's recent challenges to avoid repetition
        recent_challenges = await challenges_collection.find({
            "user_id": user_id,
            "date": {"$gte": today - timedelta(days=7)}
        }).to_list(10)
        
        recent_challenge_ids = [c["challenge_id"] for c in recent_challenges]
        
        # Filter out recent challenges
        available_challenges = [c for c in available_challenges 
                              if c["id"] not in recent_challenge_ids]
        
        # If no challenges available (user did all in past week), allow all
        if not available_challenges:
            available_challenges = DAILY_CHALLENGE_DEFINITIONS
        
        # Select random challenge
        selected_challenge_def = random.choice(available_challenges)
        
        # Create user challenge record
        user_challenge = UserDailyChallenge(
            user_id=user_id,
            challenge_id=selected_challenge_def["id"],
            date=today
        )
        
        # Insert into database
        result = await challenges_collection.insert_one(user_challenge.dict())
        user_challenge_dict = user_challenge.dict()
        user_challenge_dict["_id"] = result.inserted_id
        
        # Return merged data
        return {**user_challenge_dict, **selected_challenge_def}
    
    @staticmethod
    async def complete_daily_challenge(user_id: str, challenge_id: str) -> Dict[str, Any]:
        """Mark daily challenge as completed and award XP"""
        challenges_collection = await get_daily_challenges_collection()
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Find the challenge
        challenge = await challenges_collection.find_one({
            "user_id": user_id,
            "challenge_id": challenge_id,
            "date": today,
            "completed": False
        })
        
        if not challenge:
            return {"success": False, "message": "Challenge not found or already completed"}
        
        # Get challenge definition for XP reward
        challenge_def = next((c for c in DAILY_CHALLENGE_DEFINITIONS 
                            if c["id"] == challenge_id), None)
        
        if not challenge_def:
            return {"success": False, "message": "Challenge definition not found"}
        
        # Mark as completed
        completed_at = datetime.utcnow()
        await challenges_collection.update_one(
            {"_id": challenge["_id"]},
            {
                "$set": {
                    "completed": True,
                    "completed_at": completed_at,
                    "xp_awarded": challenge_def["xp_reward"]
                }
            }
        )
        
        return {
            "success": True,
            "xp_awarded": challenge_def["xp_reward"],
            "challenge_title": challenge_def["title"],
            "completed_at": completed_at,
            "message": f"Challenge completed! You earned {challenge_def['xp_reward']} XP!"
        }
    
    @staticmethod
    async def get_challenge_history(user_id: str, limit: int = 30) -> list:
        """Get user's challenge completion history"""
        challenges_collection = await get_daily_challenges_collection()
        
        challenges = await challenges_collection.find({
            "user_id": user_id,
            "completed": True
        }).sort("completed_at", -1).limit(limit).to_list(limit)
        
        # Merge with definition data
        result = []
        for challenge in challenges:
            challenge_def = next((c for c in DAILY_CHALLENGE_DEFINITIONS 
                                if c["id"] == challenge["challenge_id"]), None)
            if challenge_def:
                merged = {**challenge, **challenge_def}
                result.append(merged)
        
        return result
    
    @staticmethod
    async def get_challenge_stats(user_id: str) -> Dict[str, Any]:
        """Get user's overall challenge statistics"""
        challenges_collection = await get_daily_challenges_collection()
        
        # Count completed challenges
        completed_count = await challenges_collection.count_documents({
            "user_id": user_id,
            "completed": True
        })
        
        # Count total challenges assigned
        total_count = await challenges_collection.count_documents({
            "user_id": user_id
        })
        
        # Calculate completion rate
        completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # Get current streak of completed challenges
        recent_challenges = await challenges_collection.find({
            "user_id": user_id
        }).sort("date", -1).limit(30).to_list(30)
        
        current_streak = 0
        for challenge in recent_challenges:
            if challenge["completed"]:
                current_streak += 1
            else:
                break
        
        return {
            "completed_challenges": completed_count,
            "total_challenges": total_count,
            "completion_rate": round(completion_rate, 1),
            "current_streak": current_streak
        }