from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import math
from models import User, HealthStats, ProgressSnapshot
from database import LEVEL_DEFINITIONS


class ProgressService:
    
    @staticmethod
    def calculate_health_stats(user: User) -> HealthStats:
        """Calculate current health statistics for user"""
        now = datetime.utcnow()
        quit_date = user.quit_date
        days_smoke_free = (now - quit_date).days
        
        if days_smoke_free < 0:
            days_smoke_free = 0
        
        # Calculate money saved
        daily_cost = (user.cost_per_pack / user.cigarettes_per_pack) * user.smokes_per_day
        money_saved = daily_cost * days_smoke_free
        
        # Calculate cigarettes avoided
        cigarettes_avoided = user.smokes_per_day * days_smoke_free
        
        # Calculate time regained (assume 5 minutes per cigarette)
        minutes_per_cigarette = 5
        time_regained_minutes = cigarettes_avoided * minutes_per_cigarette
        
        # Calculate health score (progressive improvement)
        health_score = min(100, 50 + (days_smoke_free * 2))  # Start at 50%, improve 2% per day, max 100%
        
        return HealthStats(
            user_id=user.id,
            days_smoke_free=days_smoke_free,
            money_saved=round(money_saved, 2),
            cigarettes_avoided=cigarettes_avoided,
            health_score=health_score,
            time_regained_minutes=time_regained_minutes
        )
    
    @staticmethod
    def calculate_streak(user: User) -> int:
        """Calculate current streak - for now just use days since quit"""
        now = datetime.utcnow()
        quit_date = user.quit_date
        days = (now - quit_date).days
        return max(0, days)
    
    @staticmethod
    def calculate_level_from_xp(xp: int) -> Dict[str, Any]:
        """Determine level from XP and calculate progress to next level"""
        current_level = 1
        xp_to_next = 250
        
        for level_def in LEVEL_DEFINITIONS:
            if xp >= level_def["xp_required"]:
                current_level = level_def["level"]
            else:
                xp_to_next = level_def["xp_required"] - xp
                break
        
        return {
            "level": current_level,
            "xp_to_next_level": xp_to_next,
            "level_info": next((l for l in LEVEL_DEFINITIONS if l["level"] == current_level), LEVEL_DEFINITIONS[0])
        }
    
    @staticmethod
    def award_xp(current_xp: int, xp_to_award: int) -> Dict[str, Any]:
        """Award XP and check for level up"""
        old_level_info = ProgressService.calculate_level_from_xp(current_xp)
        new_xp = current_xp + xp_to_award
        new_level_info = ProgressService.calculate_level_from_xp(new_xp)
        
        level_up = new_level_info["level"] > old_level_info["level"]
        
        return {
            "new_xp": new_xp,
            "xp_awarded": xp_to_award,
            "old_level": old_level_info["level"],
            "new_level": new_level_info["level"],
            "level_up": level_up,
            "xp_to_next": new_level_info["xp_to_next_level"]
        }
    
    @staticmethod
    def get_health_improvements_by_timeframe(days_smoke_free: int) -> Dict[str, str]:
        """Get health improvement messages based on days smoke-free"""
        improvements = {}
        
        if days_smoke_free >= 1:
            improvements["circulation"] = "Blood circulation is improving"
        if days_smoke_free >= 3:
            improvements["taste_smell"] = "Taste and smell are enhancing"
        if days_smoke_free >= 7:
            improvements["breathing"] = "Breathing is getting easier"
        if days_smoke_free >= 14:
            improvements["lung_function"] = "Lung function is increasing"
        if days_smoke_free >= 30:
            improvements["heart_health"] = "Heart disease risk is decreasing"
        if days_smoke_free >= 90:
            improvements["immune_system"] = "Immune system is strengthening"
        
        return improvements
    
    @staticmethod
    def get_milestone_message(days_smoke_free: int) -> Optional[str]:
        """Get celebratory message for milestones"""
        milestones = {
            1: "🎉 First day complete! You've taken the most important step!",
            3: "💪 Three days strong! The hardest part is behind you!",
            7: "🌟 One week smoke-free! You're building unstoppable momentum!",
            14: "🚀 Two weeks of freedom! Your body is healing rapidly!",
            30: "👑 One month champion! You've proven you can do this!",
            90: "🏆 Three months smoke-free! You're a true warrior!",
            365: "🎊 ONE YEAR SMOKE-FREE! You've achieved something incredible!"
        }
        
        return milestones.get(days_smoke_free)
    
    @staticmethod
    def format_time_regained(minutes: int) -> str:
        """Format time regained in human-readable format"""
        if minutes < 60:
            return f"{minutes}m"
        elif minutes < 1440:  # Less than a day
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {remaining_minutes}m"
        else:  # Days
            days = minutes // 1440
            remaining_hours = (minutes % 1440) // 60
            if remaining_hours == 0:
                return f"{days}d"
            else:
                return f"{days}d {remaining_hours}h"