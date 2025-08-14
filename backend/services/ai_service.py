import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
from models import User, HealthStats, MessageType, MessageSender
from database import get_chat_messages_collection

load_dotenv()

class AICoachService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _create_system_message(self, user: User, health_stats: HealthStats, context: Optional[Dict[str, Any]] = None) -> str:
        """Create a contextual system message for the AI coach"""
        
        avatar_name = "Nick" if user.avatar == "nick" else "Nicky"
        avatar_personality = {
            "nick": "You are Nick, a friendly, supportive male AI coach who helps people quit smoking. You're encouraging, understanding, and always ready with practical advice.",
            "nicky": "You are Nicky, a warm, caring female AI coach who specializes in helping people quit smoking. You're empathetic, motivational, and offer gentle guidance."
        }
        
        system_message = f"""{avatar_personality[user.avatar]}

USER PROFILE:
- Name: {user.name}
- Quit Date: {user.quit_date.strftime('%Y-%m-%d')}
- Current Streak: {user.streak} days
- Level: {user.current_level} (XP: {user.xp})
- Longest Streak: {user.longest_streak} days

CURRENT PROGRESS:
- Days Smoke-Free: {health_stats.days_smoke_free}
- Money Saved: ${health_stats.money_saved:.2f}
- Cigarettes Avoided: {health_stats.cigarettes_avoided}
- Health Score: {health_stats.health_score}%

COACHING GUIDELINES:
1. Always address the user by their name ({user.name})
2. Be encouraging and celebrate their progress
3. Provide practical, actionable advice for cravings
4. Reference their specific achievements and milestones
5. Keep responses conversational and supportive
6. If they mention cravings, offer immediate coping strategies
7. Use emojis occasionally to keep conversations warm and friendly
8. Remember their streak and acknowledge their commitment

RESPONSE STYLE:
- Keep messages under 150 words unless providing detailed advice
- Be conversational, not clinical
- Show genuine care and understanding
- Offer specific techniques when asked for help
- Celebrate milestones and achievements enthusiastically"""

        if context:
            if context.get('craving_intensity'):
                system_message += f"\n\nIMPORTANT: The user is experiencing a craving (intensity: {context['craving_intensity']}/10). Provide immediate, practical support and coping strategies."
            
            if context.get('achievement_unlocked'):
                system_message += f"\n\nCELEBRATE: The user just unlocked the achievement '{context['achievement_unlocked']}'. Congratulate them enthusiastically!"
                
            if context.get('challenge_completed'):
                system_message += f"\n\nACKNOWLEDGE: The user completed today's challenge: '{context['challenge_completed']}'. Praise their dedication!"
        
        return system_message
    
    async def get_ai_response(self, 
                            user_message: str, 
                            user: User, 
                            health_stats: HealthStats,
                            context: Optional[Dict[str, Any]] = None) -> str:
        """Get AI response for user message"""
        try:
            # Create system message with context
            system_message = self._create_system_message(user, health_stats, context)
            
            # Initialize chat with user-specific session
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"nicara_user_{user.id}",
                system_message=system_message
            ).with_model("gemini", "gemini-2.0-flash")
            
            # Create user message
            message = UserMessage(text=user_message)
            
            # Get AI response
            response = await chat.send_message(message)
            
            return response
            
        except Exception as e:
            print(f"Error getting AI response: {str(e)}")
            # Fallback responses based on context
            fallback_responses = {
                "craving": f"I understand you're having a craving, {user.name}. Remember, this feeling is temporary and will pass. Try taking 5 deep breaths or drinking a glass of cold water. You've been smoke-free for {health_stats.days_smoke_free} days - you're stronger than this craving! 💪",
                "motivation": f"You're doing amazing, {user.name}! {health_stats.days_smoke_free} days smoke-free and ${health_stats.money_saved:.2f} saved. That's incredible progress! Every day you choose not to smoke, you're choosing a healthier, happier you. Keep going! 🌟",
                "progress": f"Let me share your incredible progress, {user.name}! You've been smoke-free for {health_stats.days_smoke_free} days, avoided {health_stats.cigarettes_avoided} cigarettes, and saved ${health_stats.money_saved:.2f}. Your health score is {health_stats.health_score}%. You should be proud! 🎉",
                "general": f"Hi {user.name}! I'm here to support you on your quit-smoking journey. You're doing great with your {user.streak}-day streak! How can I help you today? 😊"
            }
            
            context_type = "general"
            if context:
                if context.get('craving_intensity'):
                    context_type = "craving"
                elif "motivation" in user_message.lower():
                    context_type = "motivation"
                elif "progress" in user_message.lower():
                    context_type = "progress"
            
            return fallback_responses.get(context_type, fallback_responses["general"])
    
    async def handle_quick_action(self, 
                                action_type: str, 
                                user: User, 
                                health_stats: HealthStats,
                                context: Optional[Dict[str, Any]] = None) -> str:
        """Handle quick action buttons in chat"""
        
        action_messages = {
            "craving": "I'm having a craving right now. Can you help me get through this?",
            "progress": "Can you tell me how I'm doing with my quit journey?",
            "motivation": "I could use some motivation and encouragement today.",
            "tip": "Can you share a helpful tip for staying smoke-free?"
        }
        
        message = action_messages.get(action_type, "How can you help me today?")
        
        # Add craving context for immediate support
        if action_type == "craving":
            if not context:
                context = {}
            context['craving_intensity'] = 7  # Assume moderate-high craving
        
        return await self.get_ai_response(message, user, health_stats, context)
    
    def determine_message_type(self, ai_response: str) -> MessageType:
        """Determine the type of AI message based on content"""
        response_lower = ai_response.lower()
        
        if any(word in response_lower for word in ['congratulations', 'celebrate', 'achievement', 'milestone', 'proud']):
            return MessageType.celebration
        elif any(word in response_lower for word in ['try', 'technique', 'strategy', 'breathe', 'exercise', 'tip']):
            return MessageType.advice
        elif any(word in response_lower for word in ['great job', 'amazing', 'fantastic', 'keep going', 'you can do']):
            return MessageType.encouragement
        else:
            return MessageType.message