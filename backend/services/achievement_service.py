from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models import User, UserAchievement, AchievementUnlockResponse, HealthStats
from database import (
    get_achievements_collection, 
    get_craving_logs_collection,
    get_chat_messages_collection,
    ACHIEVEMENT_DEFINITIONS
)
from services.progress_service import ProgressService


class AchievementService:
    
    @staticmethod
    async def initialize_user_achievements(user_id: str) -> None:
        """Initialize achievement tracking for new user"""
        achievements_collection = await get_achievements_collection()
        
        # Create achievement records for all available achievements
        user_achievements = []
        for achievement_def in ACHIEVEMENT_DEFINITIONS:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement_def["id"],
                total_required=achievement_def["unlock_criteria"].get("days_smoke_free", 
                                achievement_def["unlock_criteria"].get("streak",
                                achievement_def["unlock_criteria"].get("money_saved", 
                                achievement_def["unlock_criteria"].get("cravings_managed",
                                achievement_def["unlock_criteria"].get("chat_sessions", 1)))))
            )
            
            user_achievements.append(user_achievement.dict())
        
        await achievements_collection.insert_many(user_achievements)
    
    @staticmethod
    async def check_and_unlock_achievements(user: User, health_stats: HealthStats) -> List[AchievementUnlockResponse]:
        """Check if user has unlocked any new achievements"""
        achievements_collection = await get_achievements_collection()
        craving_logs_collection = await get_craving_logs_collection()
        chat_messages_collection = await get_chat_messages_collection()
        
        # Get user's current achievement progress
        user_achievements = await achievements_collection.find({"user_id": user.id}).to_list(1000)
        unlocked_achievements = []
        
        for user_achievement_dict in user_achievements:
            if user_achievement_dict["earned"]:
                continue  # Skip already earned achievements
            
            user_achievement = UserAchievement(**user_achievement_dict)
            achievement_def = next((a for a in ACHIEVEMENT_DEFINITIONS if a["id"] == user_achievement.achievement_id), None)
            
            if not achievement_def:
                continue
            
            # Check unlock criteria
            criteria = achievement_def["unlock_criteria"]
            unlocked = False
            new_progress = user_achievement.progress
            
            if "days_smoke_free" in criteria:
                new_progress = health_stats.days_smoke_free
                unlocked = health_stats.days_smoke_free >= criteria["days_smoke_free"]
            
            elif "streak" in criteria:
                new_progress = user.streak
                unlocked = user.streak >= criteria["streak"]
            
            elif "money_saved" in criteria:
                new_progress = int(health_stats.money_saved)
                unlocked = health_stats.money_saved >= criteria["money_saved"]
            
            elif "cravings_managed" in criteria:
                # Count resolved cravings
                craving_count = await craving_logs_collection.count_documents({
                    "user_id": user.id, 
                    "resolved": True
                })
                new_progress = craving_count
                unlocked = craving_count >= criteria["cravings_managed"]
            
            elif "chat_sessions" in criteria:
                # Count unique chat days
                chat_count = await chat_messages_collection.count_documents({
                    "user_id": user.id,
                    "sender": "user"
                })
                new_progress = chat_count
                unlocked = chat_count >= criteria["chat_sessions"]
            
            # Update progress
            if new_progress != user_achievement.progress:
                await achievements_collection.update_one(
                    {"_id": user_achievement_dict["_id"]},
                    {"$set": {"progress": new_progress}}
                )
                user_achievement.progress = new_progress
            
            # Unlock achievement if criteria met
            if unlocked:
                # Award XP and update user
                xp_result = ProgressService.award_xp(user.xp, achievement_def["xp_reward"])
                user.xp = xp_result["new_xp"]
                
                if xp_result["level_up"]:
                    user.current_level = xp_result["new_level"]
                
                # Mark achievement as earned
                earned_date = datetime.utcnow()
                await achievements_collection.update_one(
                    {"_id": user_achievement_dict["_id"]},
                    {
                        "$set": {
                            "earned": True,
                            "earned_date": earned_date
                        }
                    }
                )
                
                user_achievement.earned = True
                user_achievement.earned_date = earned_date
                
                # Create unlock response
                unlock_response = AchievementUnlockResponse(
                    achievement=user_achievement,
                    xp_gained=achievement_def["xp_reward"],
                    new_level=xp_result["new_level"] if xp_result["level_up"] else None,
                    message=f"🎉 Achievement unlocked: {achievement_def['title']}! You earned {achievement_def['xp_reward']} XP!"
                )
                
                unlocked_achievements.append(unlock_response)
        
        return unlocked_achievements
    
    @staticmethod
    async def get_user_achievements(user_id: str) -> List[Dict[str, Any]]:
        """Get all user achievements with definition data"""
        achievements_collection = await get_achievements_collection()
        user_achievements = await achievements_collection.find({"user_id": user_id}).to_list(1000)
        
        # Merge with achievement definitions
        result = []
        for user_achievement_dict in user_achievements:
            achievement_def = next((a for a in ACHIEVEMENT_DEFINITIONS if a["id"] == user_achievement_dict["achievement_id"]), None)
            
            if achievement_def:
                merged = {
                    **user_achievement_dict,
                    **achievement_def,
                    "total": user_achievement_dict["total_required"]
                }
                result.append(merged)
        
        # Sort by earned status (earned first) then by XP reward
        result.sort(key=lambda x: (not x["earned"], -x["xp_reward"]))
        return result
    
    @staticmethod
    async def get_recent_achievements(user_id: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Get recently earned achievements"""
        achievements_collection = await get_achievements_collection()
        
        # Get recently earned achievements
        recent_achievements = await achievements_collection.find({
            "user_id": user_id,
            "earned": True
        }).sort("earned_date", -1).limit(limit).to_list(limit)
        
        # Merge with definitions
        result = []
        for user_achievement_dict in recent_achievements:
            achievement_def = next((a for a in ACHIEVEMENT_DEFINITIONS if a["id"] == user_achievement_dict["achievement_id"]), None)
            
            if achievement_def:
                merged = {
                    **user_achievement_dict,
                    **achievement_def
                }
                result.append(merged)
        
        return result