# Nicara App - Backend Integration Contracts

## API Endpoints to Implement

### 1. User Management
```
POST /api/users - Create/register user
GET /api/users/:id - Get user profile
PUT /api/users/:id - Update user profile
POST /api/users/login - User login (if needed)
```

### 2. Progress Tracking
```
GET /api/progress/:userId - Get user progress data
PUT /api/progress/:userId - Update progress metrics
GET /api/health-stats/:userId - Get health statistics
```

### 3. AI Chat Integration
```
POST /api/chat - Send message to AI coach
GET /api/chat/:userId - Get chat history
POST /api/chat/quick-action - Handle quick action responses
```

### 4. Achievements System
```
GET /api/achievements/:userId - Get user achievements
POST /api/achievements/:userId/unlock - Unlock achievement
GET /api/achievements/available - Get all available achievements
```

### 5. Daily Challenges
```
GET /api/challenges/:userId/daily - Get today's challenge
POST /api/challenges/:userId/complete - Mark challenge complete
GET /api/challenges/history/:userId - Get challenge history
```

### 6. Craving Management
```
POST /api/cravings - Log a craving incident
GET /api/cravings/:userId - Get craving history
GET /api/craving-tips - Get available tips
POST /api/craving-tips/:tipId/used - Track tip usage
```

## Mock Data to Replace

### From `mockData.js`:
1. **mockUser** → Real user data from MongoDB
2. **mockHealthStats** → Calculated from user's quit date and smoking habits
3. **mockAchievements** → Achievement progress based on user actions
4. **mockDailyChallenge** → Dynamic daily challenges
5. **mockChatMessages** → Real AI conversations with Gemini
6. **mockCravingTips** → Static tips (can remain, but usage tracking needed)
7. **mockSocialStats** → Real community statistics

## Backend Implementation Plan

### 1. MongoDB Models
```javascript
- User: { name, avatar, quitDate, smokingHabits, level, xp, streak }
- ChatMessage: { userId, sender, message, timestamp, type }
- Achievement: { userId, achievementId, earned, earnedDate, progress }
- DailyChallenge: { userId, challengeId, date, completed, xpAwarded }
- CravingLog: { userId, timestamp, intensity, tipUsed, duration }
- ProgressSnapshot: { userId, date, daysSmokeFree, moneySaved, healthScore }
```

### 2. Core Business Logic
- **Health Calculations**: Days smoke-free, money saved, cigarettes avoided
- **XP System**: Award XP for achievements, challenges, milestones
- **Achievement Unlocking**: Automatic achievement checking and unlocking
- **Streak Management**: Calculate and maintain quit streaks
- **Level Progression**: XP-based leveling system

### 3. Gemini AI Integration
- **Real-time Coaching**: Contextual responses based on user progress
- **Craving Support**: Emergency AI support during cravings
- **Motivational Messages**: Personalized encouragement
- **Progress Celebrations**: AI celebrates user milestones

## Frontend Integration Changes

### Files to Modify:
1. **App.js** - Replace localStorage with API calls
2. **Dashboard.jsx** - Fetch real progress data
3. **ChatCoach.jsx** - Integrate with Gemini AI API
4. **Achievements.jsx** - Load real achievement progress
5. **CravingHelp.jsx** - Log cravings and fetch personalized tips

### API Integration Pattern:
```javascript
// Replace mock data calls like:
import { mockUser } from '../data/mockData';

// With API calls like:
const fetchUserData = async () => {
  const response = await axios.get(`${API}/users/${userId}`);
  return response.data;
};
```

## Key Features Implementation

### 1. User Onboarding Flow
- Save avatar selection and quit details
- Initialize user progress tracking
- Set up first daily challenge
- Award "Fresh Start" achievement

### 2. Real-time Progress Updates
- Calculate health improvements in real-time
- Update XP and levels based on actions
- Automatic achievement checking
- Streak maintenance and recovery

### 3. AI Coach Intelligence
- Context-aware responses based on:
  - User's current streak
  - Recent craving patterns
  - Achievement progress
  - Time since last interaction
- Emergency craving support protocols
- Celebration of milestones

### 4. Gamification Engine
- Daily XP opportunities
- Progressive challenge difficulty
- Social features and sharing
- Badge collection mechanics

## Data Flow Architecture

```
Frontend Components → API Calls → Backend Controllers → Business Logic → MongoDB
                                                    ↓
                   Gemini AI ← AI Service Layer ←──┘
```

## Testing Strategy
1. Test all API endpoints individually
2. Verify AI coaching responses are contextual
3. Ensure achievement system works correctly
4. Test progress calculations accuracy
5. Validate craving logging and support features

## Security & Performance
- Rate limiting for AI API calls
- User data validation
- Efficient caching for frequent calculations
- Proper error handling for AI service downtime