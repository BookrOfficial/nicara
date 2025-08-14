from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class AvatarType(str, Enum):
    nick = "nick"
    nicky = "nicky"


class MessageSender(str, Enum):
    user = "user"
    nick = "nick"
    nicky = "nicky"


class MessageType(str, Enum):
    message = "message"
    encouragement = "encouragement"
    advice = "advice"
    update = "update"
    celebration = "celebration"


class AchievementType(str, Enum):
    bronze = "bronze"
    silver = "silver"  
    gold = "gold"


# User Models
class UserBase(BaseModel):
    name: str
    avatar: AvatarType
    
    
class UserCreate(UserBase):
    quit_date: datetime
    smokes_per_day: int
    cost_per_pack: float
    cigarettes_per_pack: int = 20


class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quit_date: datetime
    smokes_per_day: int
    cost_per_pack: float
    cigarettes_per_pack: int
    current_level: int = 1
    xp: int = 0
    streak: int = 0
    longest_streak: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Chat Models
class ChatMessageBase(BaseModel):
    message: str
    

class ChatMessageCreate(ChatMessageBase):
    user_id: str
    

class ChatMessage(ChatMessageBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    sender: MessageSender
    message_type: MessageType = MessageType.message
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context: Optional[Dict[str, Any]] = None


# Achievement Models
class AchievementDefinition(BaseModel):
    id: str
    title: str
    description: str
    achievement_type: AchievementType
    xp_reward: int
    unlock_criteria: Dict[str, Any]
    icon: str = "shield"


class UserAchievement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    achievement_id: str
    earned: bool = False
    earned_date: Optional[datetime] = None
    progress: int = 0
    total_required: int = 1


# Daily Challenge Models
class DailyChallengeDefinition(BaseModel):
    id: str
    title: str
    description: str
    xp_reward: int
    challenge_type: str
    duration: str
    difficulty: int = 1


class UserDailyChallenge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    challenge_id: str
    date: datetime = Field(default_factory=lambda: datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
    completed: bool = False
    completed_at: Optional[datetime] = None
    xp_awarded: int = 0


# Craving Models
class CravingLogCreate(BaseModel):
    user_id: str
    intensity: int  # 1-10 scale
    trigger: Optional[str] = None
    duration_minutes: Optional[int] = None
    coping_strategy: Optional[str] = None
    

class CravingLog(CravingLogCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = True


# Progress Models  
class HealthStats(BaseModel):
    user_id: str
    days_smoke_free: int
    money_saved: float
    cigarettes_avoided: int
    health_score: int  # 0-100
    time_regained_minutes: int
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


class ProgressSnapshot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    date: datetime = Field(default_factory=lambda: datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
    days_smoke_free: int
    money_saved: float
    cigarettes_avoided: int
    health_score: int
    streak: int
    level: int
    xp: int


# Social Models
class SocialStats(BaseModel):
    user_id: str
    friends_helped: int = 0
    encouragements_sent: int = 0
    encouragements_received: int = 0
    community_rank: int = 999
    achievements_shared: int = 0


# Response Models
class QuickActionRequest(BaseModel):
    user_id: str
    action_type: str  # craving, progress, motivation, tip
    context: Optional[Dict[str, Any]] = None


class AchievementUnlockResponse(BaseModel):
    achievement: UserAchievement
    xp_gained: int
    new_level: Optional[int] = None
    message: str


class UserProgressResponse(BaseModel):
    user: User
    health_stats: HealthStats
    daily_challenge: Optional[UserDailyChallenge] = None
    recent_achievements: List[UserAchievement] = []
    social_stats: SocialStats


# Craving Tips (Static for now)
class CravingTip(BaseModel):
    id: str
    title: str
    description: str
    category: str  # breathing, distraction, social, physical
    duration: str
    icon: str


# Level Definitions
class LevelDefinition(BaseModel):
    level: int
    title: str
    xp_required: int
    color: str