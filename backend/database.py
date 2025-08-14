from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

# Database instance
db_instance = Database()

# Collections
async def get_database() -> AsyncIOMotorDatabase:
    return db_instance.database

async def get_users_collection() -> AsyncIOMotorCollection:
    return db_instance.database["users"]

async def get_chat_messages_collection() -> AsyncIOMotorCollection:
    return db_instance.database["chat_messages"]

async def get_achievements_collection() -> AsyncIOMotorCollection:
    return db_instance.database["user_achievements"]

async def get_daily_challenges_collection() -> AsyncIOMotorCollection:
    return db_instance.database["user_daily_challenges"]

async def get_craving_logs_collection() -> AsyncIOMotorCollection:
    return db_instance.database["craving_logs"]

async def get_progress_snapshots_collection() -> AsyncIOMotorCollection:
    return db_instance.database["progress_snapshots"]

async def get_social_stats_collection() -> AsyncIOMotorCollection:
    return db_instance.database["social_stats"]


# Database connection functions
async def connect_to_mongo():
    """Create database connection"""
    db_instance.client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db_instance.database = db_instance.client[os.environ["DB_NAME"].strip('"')]
    print(f"Connected to MongoDB: {os.environ['DB_NAME'].strip('\"')}")


async def close_mongo_connection():
    """Close database connection"""
    if db_instance.client:
        db_instance.client.close()
        print("Disconnected from MongoDB")


# Achievement definitions (static data)
ACHIEVEMENT_DEFINITIONS = [
    {
        "id": "first_day",
        "title": "First Day Victory",
        "description": "Completed your first day smoke-free",
        "achievement_type": "bronze",
        "xp_reward": 100,
        "unlock_criteria": {"days_smoke_free": 1},
        "icon": "shield"
    },
    {
        "id": "week_warrior", 
        "title": "Week Warrior",
        "description": "7 consecutive days smoke-free",
        "achievement_type": "silver",
        "xp_reward": 500,
        "unlock_criteria": {"streak": 7},
        "icon": "shield"
    },
    {
        "id": "month_champion",
        "title": "Month Champion", 
        "description": "30 consecutive days smoke-free",
        "achievement_type": "gold",
        "xp_reward": 2000,
        "unlock_criteria": {"streak": 30},
        "icon": "shield"
    },
    {
        "id": "craving_crusher",
        "title": "Craving Crusher",
        "description": "Successfully managed 10 cravings",
        "achievement_type": "gold", 
        "xp_reward": 750,
        "unlock_criteria": {"cravings_managed": 10},
        "icon": "shield"
    },
    {
        "id": "money_saver",
        "title": "Money Saver",
        "description": "Saved $100 by not smoking",
        "achievement_type": "silver",
        "xp_reward": 300,
        "unlock_criteria": {"money_saved": 100.0},
        "icon": "shield"
    },
    {
        "id": "chat_champion",
        "title": "Chat Champion",
        "description": "Had 50 conversations with your AI coach",
        "achievement_type": "bronze",
        "xp_reward": 200,
        "unlock_criteria": {"chat_sessions": 50},
        "icon": "shield"
    }
]

# Daily challenge definitions
DAILY_CHALLENGE_DEFINITIONS = [
    {
        "id": "deep_breathing",
        "title": "Deep Breathing Master",
        "description": "Practice deep breathing for 2 minutes when you feel a craving",
        "xp_reward": 50,
        "challenge_type": "wellness",
        "duration": "2 minutes",
        "difficulty": 1
    },
    {
        "id": "hydration_hero",
        "title": "Hydration Hero",
        "description": "Drink 8 glasses of water throughout the day",
        "xp_reward": 75,
        "challenge_type": "health", 
        "duration": "All day",
        "difficulty": 2
    },
    {
        "id": "exercise_explorer",
        "title": "Exercise Explorer",
        "description": "Take a 15-minute walk or do light exercise",
        "xp_reward": 100,
        "challenge_type": "physical",
        "duration": "15 minutes",
        "difficulty": 2
    },
    {
        "id": "mindfulness_moment",
        "title": "Mindfulness Moment",
        "description": "Practice mindfulness meditation for 5 minutes",
        "xp_reward": 60,
        "challenge_type": "mental",
        "duration": "5 minutes", 
        "difficulty": 1
    },
    {
        "id": "social_support",
        "title": "Social Support",
        "description": "Reach out to a friend or family member for encouragement",
        "xp_reward": 80,
        "challenge_type": "social",
        "duration": "5 minutes",
        "difficulty": 1
    }
]

# Craving tips definitions
CRAVING_TIPS = [
    {
        "id": "tip_001",
        "title": "The 4-7-8 Technique", 
        "description": "Breathe in for 4 counts, hold for 7, exhale for 8. This activates your body's relaxation response.",
        "category": "breathing",
        "duration": "2 minutes",
        "icon": "wind"
    },
    {
        "id": "tip_002",
        "title": "Drink Cold Water",
        "description": "Cold water can help reduce nicotine cravings and keep your hands and mouth busy.",
        "category": "distraction",
        "duration": "30 seconds",
        "icon": "droplets"
    },
    {
        "id": "tip_003", 
        "title": "Call a Friend",
        "description": "Reach out to someone supportive. Social connection helps overcome difficult moments.",
        "category": "social",
        "duration": "5 minutes",
        "icon": "phone"
    },
    {
        "id": "tip_004",
        "title": "Physical Exercise",
        "description": "Do 10 jumping jacks or take a quick walk. Exercise releases endorphins that fight cravings.",
        "category": "physical", 
        "duration": "3 minutes",
        "icon": "zap"
    },
    {
        "id": "tip_005",
        "title": "Progressive Muscle Relaxation",
        "description": "Tense and relax each muscle group starting from your toes up to your head.",
        "category": "breathing",
        "duration": "5 minutes",
        "icon": "wind"
    },
    {
        "id": "tip_006",
        "title": "Healthy Snack",
        "description": "Eat carrots, celery, or sunflower seeds to satisfy the oral fixation.",
        "category": "distraction",
        "duration": "2 minutes", 
        "icon": "apple"
    }
]

# Level definitions
LEVEL_DEFINITIONS = [
    {"level": 1, "title": "Fresh Start", "xp_required": 0, "color": "#1BC7B1"},
    {"level": 2, "title": "Getting Strong", "xp_required": 250, "color": "#1BC7B1"},
    {"level": 3, "title": "Determined", "xp_required": 500, "color": "#FF6F61"},
    {"level": 4, "title": "Resilient", "xp_required": 1000, "color": "#FF6F61"},
    {"level": 5, "title": "Champion", "xp_required": 2000, "color": "#FFC857"},
    {"level": 6, "title": "Warrior", "xp_required": 3500, "color": "#FFC857"},
    {"level": 7, "title": "Hero", "xp_required": 5500, "color": "#FFC857"},
    {"level": 8, "title": "Legend", "xp_required": 8000, "color": "#FFC857"},
    {"level": 9, "title": "Master", "xp_required": 12000, "color": "#FFC857"},
    {"level": 10, "title": "Grandmaster", "xp_required": 18000, "color": "#FFC857"}
]