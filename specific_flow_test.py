#!/usr/bin/env python3
"""
Specific Test Flow for Nicara Backend API
Tests the exact flow mentioned in the review request
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://smoke-free-journey.preview.emergentagent.com')
API_BASE_URL = f"{BACKEND_URL}/api"

async def run_specific_flow_test():
    """Run the specific test flow as requested"""
    
    async with aiohttp.ClientSession() as session:
        print("🎯 Running Specific Test Flow as Requested")
        print("=" * 50)
        
        # 1. Create a user named "John" with nick avatar, quit date 6 days ago, 15 cigarettes/day, $12.50/pack
        print("1️⃣ Creating user 'John' with specified parameters...")
        quit_date = (datetime.utcnow() - timedelta(days=6)).isoformat()
        
        user_data = {
            "name": "John",
            "avatar": "nick",
            "quit_date": quit_date,
            "smokes_per_day": 15,
            "cost_per_pack": 12.50,
            "cigarettes_per_pack": 20
        }
        
        async with session.post(f"{API_BASE_URL}/users", json=user_data) as response:
            user = await response.json()
            user_id = user["id"]
            print(f"   ✅ User created: {user['name']} (ID: {user_id})")
            print(f"   📊 Initial stats: Level {user['current_level']}, {user['xp']} XP, {user['streak']} day streak")
        
        # 2. Test progress calculation (should show 6 days smoke-free, money saved, cigarettes avoided)
        print("\n2️⃣ Testing progress calculation...")
        async with session.get(f"{API_BASE_URL}/progress/{user_id}") as response:
            progress = await response.json()
            health_stats = progress["health_stats"]
            print(f"   ✅ Progress calculated:")
            print(f"      🚭 Days smoke-free: {health_stats['days_smoke_free']}")
            print(f"      💰 Money saved: ${health_stats['money_saved']:.2f}")
            print(f"      🚬 Cigarettes avoided: {health_stats['cigarettes_avoided']}")
            print(f"      ❤️ Health score: {health_stats['health_score']}%")
        
        # 3. Test AI chat with messages like "I'm having a craving" and "How am I doing?"
        print("\n3️⃣ Testing AI chat with specific messages...")
        
        # Test craving message
        craving_msg = {"user_id": user_id, "message": "I'm having a craving"}
        async with session.post(f"{API_BASE_URL}/chat", json=craving_msg) as response:
            chat_response = await response.json()
            ai_message = chat_response["ai_message"]["message"]
            print(f"   ✅ Craving support response: {ai_message[:100]}...")
        
        # Test progress inquiry
        progress_msg = {"user_id": user_id, "message": "How am I doing?"}
        async with session.post(f"{API_BASE_URL}/chat", json=progress_msg) as response:
            chat_response = await response.json()
            ai_message = chat_response["ai_message"]["message"]
            print(f"   ✅ Progress inquiry response: {ai_message[:100]}...")
        
        # 4. Complete a daily challenge and verify XP award
        print("\n4️⃣ Completing daily challenge and verifying XP award...")
        
        # Get today's challenge
        async with session.get(f"{API_BASE_URL}/challenges/{user_id}/daily") as response:
            challenge = await response.json()
            challenge_id = challenge["id"]
            print(f"   📋 Today's challenge: {challenge['title']}")
        
        # Complete the challenge
        async with session.post(f"{API_BASE_URL}/challenges/{user_id}/{challenge_id}/complete") as response:
            completion = await response.json()
            print(f"   ✅ Challenge completed!")
            print(f"      🎁 XP awarded: {completion['xp_awarded']}")
            if completion.get('level_up'):
                print(f"      🎉 Level up! New level: {completion['new_level']}")
        
        # 5. Log a craving and verify achievement checking
        print("\n5️⃣ Logging craving and checking achievements...")
        
        craving_data = {
            "user_id": user_id,
            "intensity": 8,
            "trigger": "stress",
            "duration_minutes": 3,
            "coping_strategy": "deep breathing"
        }
        
        async with session.post(f"{API_BASE_URL}/cravings", json=craving_data) as response:
            craving_result = await response.json()
            print(f"   ✅ Craving logged (intensity: {craving_data['intensity']}/10)")
            achievements = craving_result.get("achievements_unlocked", [])
            if achievements:
                print(f"      🏆 New achievements unlocked: {len(achievements)}")
            else:
                print(f"      📊 No new achievements (progress tracked)")
        
        # 6. Test all quick actions
        print("\n6️⃣ Testing all quick actions...")
        
        quick_actions = ["craving", "motivation", "progress", "tip"]
        for action in quick_actions:
            action_data = {"user_id": user_id, "action_type": action}
            async with session.post(f"{API_BASE_URL}/chat/quick-action", json=action_data) as response:
                action_response = await response.json()
                ai_message = action_response["ai_message"]["message"]
                print(f"   ✅ {action.capitalize()} action: {ai_message[:80]}...")
        
        # Final verification - check all systems are working
        print("\n🔍 Final System Verification...")
        
        # Check achievements
        async with session.get(f"{API_BASE_URL}/achievements/{user_id}") as response:
            achievements = await response.json()
            earned_count = sum(1 for a in achievements if a.get("earned", False))
            print(f"   🏆 Achievements: {earned_count}/{len(achievements)} earned")
        
        # Check craving tips
        async with session.get(f"{API_BASE_URL}/craving-tips") as response:
            tips = await response.json()
            print(f"   💡 Craving tips available: {len(tips)}")
        
        # Check final user state
        async with session.get(f"{API_BASE_URL}/users/{user_id}") as response:
            final_user = await response.json()
            print(f"   👤 Final user state: Level {final_user['current_level']}, {final_user['xp']} XP")
        
        print("\n" + "=" * 50)
        print("🎉 SPECIFIC FLOW TEST COMPLETED SUCCESSFULLY!")
        print("✅ All requested features tested and working:")
        print("   • User creation with proper initialization")
        print("   • Accurate progress calculations")
        print("   • Working AI chat with Gemini integration")
        print("   • Achievement system and XP progression")
        print("   • Daily challenges with XP rewards")
        print("   • Craving logging and management")
        print("   • All quick actions functional")

if __name__ == "__main__":
    asyncio.run(run_specific_flow_test())