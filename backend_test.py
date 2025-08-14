#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Nicara Quit Smoking Coach
Tests all core features including user management, progress tracking, AI chat, achievements, challenges, and craving management.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import sys

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://smoke-free-journey.preview.emergentagent.com')
API_BASE_URL = f"{BACKEND_URL}/api"

class NicaraAPITester:
    def __init__(self):
        self.session = None
        self.test_user_id = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data if not success else None
        })
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple[bool, Any]:
        """Make HTTP request and return success status and response data"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            
            if method.upper() == "GET":
                async with self.session.get(url, params=params) as response:
                    response_data = await response.json()
                    return response.status < 400, response_data
            elif method.upper() == "POST":
                async with self.session.post(url, json=data, params=params) as response:
                    response_data = await response.json()
                    return response.status < 400, response_data
            elif method.upper() == "PUT":
                async with self.session.put(url, json=data, params=params) as response:
                    response_data = await response.json()
                    return response.status < 400, response_data
                    
        except Exception as e:
            return False, {"error": str(e)}
    
    async def test_api_root(self):
        """Test API root endpoint"""
        success, response = await self.make_request("GET", "/")
        expected_message = "Welcome to Nicara API - Your AI Quit Smoking Coach!"
        
        if success and response.get("message") == expected_message:
            self.log_test("API Root Endpoint", True, "API is accessible and responding correctly")
        else:
            self.log_test("API Root Endpoint", False, "API root not responding as expected", response)
    
    async def test_user_creation(self):
        """Test user creation with proper initialization"""
        # Create user "John" with nick avatar, quit date 6 days ago
        quit_date = (datetime.utcnow() - timedelta(days=6)).isoformat()
        
        user_data = {
            "name": "John",
            "avatar": "nick",
            "quit_date": quit_date,
            "smokes_per_day": 15,
            "cost_per_pack": 12.50,
            "cigarettes_per_pack": 20
        }
        
        success, response = await self.make_request("POST", "/users", user_data)
        
        if success and "id" in response:
            self.test_user_id = response["id"]
            
            # Verify user data
            expected_fields = ["id", "name", "avatar", "quit_date", "smokes_per_day", "cost_per_pack", "current_level", "xp", "streak"]
            missing_fields = [field for field in expected_fields if field not in response]
            
            if not missing_fields:
                self.log_test("User Creation", True, f"User created successfully with ID: {self.test_user_id}")
            else:
                self.log_test("User Creation", False, f"Missing fields: {missing_fields}", response)
        else:
            self.log_test("User Creation", False, "Failed to create user", response)
    
    async def test_user_retrieval(self):
        """Test user profile retrieval"""
        if not self.test_user_id:
            self.log_test("User Retrieval", False, "No test user ID available")
            return
            
        success, response = await self.make_request("GET", f"/users/{self.test_user_id}")
        
        if success and response.get("id") == self.test_user_id:
            self.log_test("User Retrieval", True, "User profile retrieved successfully")
        else:
            self.log_test("User Retrieval", False, "Failed to retrieve user profile", response)
    
    async def test_user_update(self):
        """Test user profile update"""
        if not self.test_user_id:
            self.log_test("User Update", False, "No test user ID available")
            return
            
        # Update user data
        quit_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
        update_data = {
            "name": "John Updated",
            "avatar": "nick",
            "quit_date": quit_date,
            "smokes_per_day": 20,
            "cost_per_pack": 15.00,
            "cigarettes_per_pack": 20
        }
        
        success, response = await self.make_request("PUT", f"/users/{self.test_user_id}", update_data)
        
        if success and response.get("name") == "John Updated":
            self.log_test("User Update", True, "User profile updated successfully")
        else:
            self.log_test("User Update", False, "Failed to update user profile", response)
    
    async def test_progress_tracking(self):
        """Test comprehensive progress data retrieval"""
        if not self.test_user_id:
            self.log_test("Progress Tracking", False, "No test user ID available")
            return
            
        success, response = await self.make_request("GET", f"/progress/{self.test_user_id}")
        
        if success:
            required_sections = ["user", "health_stats", "daily_challenge", "recent_achievements", "social_stats"]
            missing_sections = [section for section in required_sections if section not in response]
            
            if not missing_sections:
                health_stats = response["health_stats"]
                days_free = health_stats.get("days_smoke_free", 0)
                money_saved = health_stats.get("money_saved", 0)
                cigarettes_avoided = health_stats.get("cigarettes_avoided", 0)
                
                self.log_test("Progress Tracking", True, 
                             f"Progress data complete - {days_free} days smoke-free, ${money_saved:.2f} saved, {cigarettes_avoided} cigarettes avoided")
            else:
                self.log_test("Progress Tracking", False, f"Missing sections: {missing_sections}", response)
        else:
            self.log_test("Progress Tracking", False, "Failed to retrieve progress data", response)
    
    async def test_health_stats(self):
        """Test health statistics calculation"""
        if not self.test_user_id:
            self.log_test("Health Stats", False, "No test user ID available")
            return
            
        success, response = await self.make_request("GET", f"/health-stats/{self.test_user_id}")
        
        if success:
            required_fields = ["days_smoke_free", "money_saved", "cigarettes_avoided", "health_score", "time_regained_minutes"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                self.log_test("Health Stats", True, f"Health stats calculated - Health score: {response['health_score']}%")
            else:
                self.log_test("Health Stats", False, f"Missing fields: {missing_fields}", response)
        else:
            self.log_test("Health Stats", False, "Failed to retrieve health stats", response)
    
    async def test_ai_chat_system(self):
        """Test AI chat system with Gemini integration"""
        if not self.test_user_id:
            self.log_test("AI Chat System", False, "No test user ID available")
            return
            
        # Test sending a message about cravings
        chat_data = {
            "user_id": self.test_user_id,
            "message": "I'm having a craving right now. Can you help me?"
        }
        
        success, response = await self.make_request("POST", "/chat", chat_data)
        
        if success:
            required_fields = ["user_message", "ai_message", "achievements_unlocked"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                ai_message = response["ai_message"]["message"]
                self.log_test("AI Chat System", True, f"AI responded successfully: {ai_message[:100]}...")
            else:
                self.log_test("AI Chat System", False, f"Missing fields: {missing_fields}", response)
        else:
            self.log_test("AI Chat System", False, "Failed to get AI response", response)
    
    async def test_chat_history(self):
        """Test chat history retrieval"""
        if not self.test_user_id:
            self.log_test("Chat History", False, "No test user ID available")
            return
            
        success, response = await self.make_request("GET", f"/chat/{self.test_user_id}")
        
        if success and isinstance(response, list):
            self.log_test("Chat History", True, f"Retrieved {len(response)} chat messages")
        else:
            self.log_test("Chat History", False, "Failed to retrieve chat history", response)
    
    async def test_quick_actions(self):
        """Test quick action buttons"""
        if not self.test_user_id:
            self.log_test("Quick Actions", False, "No test user ID available")
            return
            
        quick_actions = ["craving", "motivation", "progress", "tip"]
        
        for action in quick_actions:
            action_data = {
                "user_id": self.test_user_id,
                "action_type": action
            }
            
            success, response = await self.make_request("POST", "/chat/quick-action", action_data)
            
            if success and "ai_message" in response:
                self.log_test(f"Quick Action - {action}", True, f"Action handled successfully")
            else:
                self.log_test(f"Quick Action - {action}", False, f"Failed to handle {action} action", response)
    
    async def test_achievements_system(self):
        """Test achievement system"""
        if not self.test_user_id:
            self.log_test("Achievement System", False, "No test user ID available")
            return
            
        # Get user achievements
        success, response = await self.make_request("GET", f"/achievements/{self.test_user_id}")
        
        if success and isinstance(response, list):
            self.log_test("Get Achievements", True, f"Retrieved {len(response)} achievements")
            
            # Test manual achievement checking
            success2, response2 = await self.make_request("POST", f"/achievements/{self.test_user_id}/check")
            
            if success2:
                unlocked_count = len(response2.get("achievements_unlocked", []))
                self.log_test("Achievement Checking", True, f"Achievement check completed, {unlocked_count} new achievements")
            else:
                self.log_test("Achievement Checking", False, "Failed to check achievements", response2)
        else:
            self.log_test("Get Achievements", False, "Failed to retrieve achievements", response)
    
    async def test_daily_challenges(self):
        """Test daily challenge system"""
        if not self.test_user_id:
            self.log_test("Daily Challenges", False, "No test user ID available")
            return
            
        # Get today's challenge
        success, response = await self.make_request("GET", f"/challenges/{self.test_user_id}/daily")
        
        if success and "id" in response:
            challenge_id = response["id"]
            self.log_test("Get Daily Challenge", True, f"Retrieved challenge: {response.get('title', 'Unknown')}")
            
            # Complete the challenge
            success2, response2 = await self.make_request("POST", f"/challenges/{self.test_user_id}/{challenge_id}/complete")
            
            if success2:
                xp_awarded = response2.get("xp_awarded", 0)
                self.log_test("Complete Challenge", True, f"Challenge completed, {xp_awarded} XP awarded")
            else:
                self.log_test("Complete Challenge", False, "Failed to complete challenge", response2)
        else:
            self.log_test("Get Daily Challenge", False, "Failed to retrieve daily challenge", response)
    
    async def test_craving_management(self):
        """Test craving logging and management"""
        if not self.test_user_id:
            self.log_test("Craving Management", False, "No test user ID available")
            return
            
        # Log a craving
        craving_data = {
            "user_id": self.test_user_id,
            "intensity": 7,
            "trigger": "stress at work",
            "duration_minutes": 5,
            "coping_strategy": "deep breathing"
        }
        
        success, response = await self.make_request("POST", "/cravings", craving_data)
        
        if success and "craving_log" in response:
            self.log_test("Log Craving", True, "Craving logged successfully")
            
            # Get craving history
            success2, response2 = await self.make_request("GET", f"/cravings/{self.test_user_id}")
            
            if success2 and isinstance(response2, list):
                self.log_test("Get Craving History", True, f"Retrieved {len(response2)} craving logs")
            else:
                self.log_test("Get Craving History", False, "Failed to retrieve craving history", response2)
        else:
            self.log_test("Log Craving", False, "Failed to log craving", response)
    
    async def test_craving_tips(self):
        """Test craving tips system"""
        success, response = await self.make_request("GET", "/craving-tips")
        
        if success and isinstance(response, list) and len(response) > 0:
            self.log_test("Get Craving Tips", True, f"Retrieved {len(response)} craving tips")
        else:
            self.log_test("Get Craving Tips", False, "Failed to retrieve craving tips", response)
    
    async def test_utility_endpoints(self):
        """Test utility endpoints"""
        # Test level definitions
        success, response = await self.make_request("GET", "/levels")
        
        if success and isinstance(response, list):
            self.log_test("Get Level Definitions", True, f"Retrieved {len(response)} level definitions")
        else:
            self.log_test("Get Level Definitions", False, "Failed to retrieve level definitions", response)
        
        # Test motivational quotes
        success2, response2 = await self.make_request("GET", "/quotes")
        
        if success2 and "quotes" in response2:
            self.log_test("Get Motivational Quotes", True, f"Retrieved {len(response2['quotes'])} quotes")
        else:
            self.log_test("Get Motivational Quotes", False, "Failed to retrieve quotes", response2)
    
    async def run_all_tests(self):
        """Run all backend API tests"""
        print(f"🚀 Starting Nicara Backend API Tests")
        print(f"📡 Testing API at: {API_BASE_URL}")
        print("=" * 60)
        
        # Core API tests
        await self.test_api_root()
        
        # User management tests
        await self.test_user_creation()
        await self.test_user_retrieval()
        await self.test_user_update()
        
        # Progress tracking tests
        await self.test_progress_tracking()
        await self.test_health_stats()
        
        # AI chat system tests (Critical - Gemini integration)
        await self.test_ai_chat_system()
        await self.test_chat_history()
        await self.test_quick_actions()
        
        # Achievement system tests
        await self.test_achievements_system()
        
        # Daily challenge tests
        await self.test_daily_challenges()
        
        # Craving management tests
        await self.test_craving_management()
        await self.test_craving_tips()
        
        # Utility endpoint tests
        await self.test_utility_endpoints()
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if total - passed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['details']}")
        
        print(f"\n🎯 Overall Success Rate: {(passed/total)*100:.1f}%")
        
        return passed == total

async def main():
    """Main test execution"""
    try:
        async with NicaraAPITester() as tester:
            success = await tester.run_all_tests()
            return 0 if success else 1
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)