// Mock data for Nicara quit-smoking app

export const mockUser = {
  id: "user_001",
  name: "John",
  avatar: "nick", // nick or nicky
  quitDate: "2025-01-08", // 6 days ago from today
  smokesPerDay: 15,
  costPerPack: 12.50,
  cigarettesPerPack: 20,
  currentLevel: 3,
  xp: 750,
  xpToNextLevel: 250,
  streak: 6,
  longestStreak: 12
};

export const mockHealthStats = [
  {
    title: "Money Saved",
    value: "$45.00",
    icon: "dollar-sign",
    color: "text-yellow-600",
    improvement: "+$7.50 today"
  },
  {
    title: "Cigarettes Avoided",
    value: "90",
    icon: "x-circle",
    color: "text-red-500",
    improvement: "+15 today"
  },
  {
    title: "Health Score",
    value: "78%",
    icon: "heart",
    color: "text-green-500",
    improvement: "+5% this week"
  },
  {
    title: "Time Regained",
    value: "3h 45m",
    icon: "clock",
    color: "text-blue-500",
    improvement: "+37m today"
  }
];

export const mockAchievements = [
  {
    id: "first_day",
    title: "First Day Victory",
    description: "Completed your first day smoke-free",
    type: "bronze",
    earned: true,
    earnedDate: "2025-01-08"
  },
  {
    id: "week_warrior",
    title: "Week Warrior",
    description: "7 consecutive days smoke-free",
    type: "silver",
    earned: false,
    progress: 6,
    total: 7
  },
  {
    id: "craving_crusher",
    title: "Craving Crusher",
    description: "Successfully managed 10 cravings",
    type: "gold",
    earned: false,
    progress: 7,
    total: 10
  },
  {
    id: "money_saver",
    title: "Money Saver",
    description: "Saved $100 by not smoking",
    type: "silver",
    earned: false,
    progress: 45,
    total: 100
  }
];

export const mockDailyChallenge = {
  id: "challenge_001",
  title: "Deep Breathing Master",
  description: "Practice deep breathing for 2 minutes when you feel a craving",
  xpReward: 50,
  completed: false,
  timeLimit: "24 hours",
  type: "wellness"
};

export const mockChatMessages = [
  {
    id: "msg_001",
    sender: "nick",
    message: "Hey John! 🌟 Congratulations on your 6-day streak! That's amazing progress. How are you feeling today?",
    timestamp: "2025-01-14T09:00:00Z",
    type: "encouragement"
  },
  {
    id: "msg_002",
    sender: "user",
    message: "Thanks Nick! I'm feeling good but had a small craving this morning.",
    timestamp: "2025-01-14T09:15:00Z",
    type: "update"
  },
  {
    id: "msg_003",
    sender: "nick",
    message: "That's totally normal! Cravings are temporary - they usually last only 3-5 minutes. Here's what you can do: Try the 4-7-8 breathing technique. Breathe in for 4, hold for 7, exhale for 8. Want to try it together?",
    timestamp: "2025-01-14T09:16:00Z",
    type: "advice"
  }
];

export const mockCravingTips = [
  {
    id: "tip_001",
    title: "The 4-7-8 Technique",
    description: "Breathe in for 4 counts, hold for 7, exhale for 8. This activates your body's relaxation response.",
    category: "breathing",
    duration: "2 minutes"
  },
  {
    id: "tip_002",
    title: "Drink Cold Water",
    description: "Cold water can help reduce nicotine cravings and keep your hands and mouth busy.",
    category: "distraction",
    duration: "30 seconds"
  },
  {
    id: "tip_003",
    title: "Call a Friend",
    description: "Reach out to someone supportive. Social connection helps overcome difficult moments.",
    category: "social",
    duration: "5 minutes"
  },
  {
    id: "tip_004",
    title: "Physical Exercise",
    description: "Do 10 jumping jacks or take a quick walk. Exercise releases endorphins that fight cravings.",
    category: "physical",
    duration: "3 minutes"
  }
];

export const mockQuotes = [
  "Every cigarette you don't smoke is doing you good. - Unknown",
  "The best time to quit smoking was 20 years ago. The second best time is now. - Chinese Proverb",
  "You are stronger than your cravings. Keep going! - Nicara Team",
  "Success is the sum of small efforts repeated day in and day out. - Robert Collier"
];

export const mockLevels = [
  { level: 1, title: "Fresh Start", xpRequired: 0, color: "#1BC7B1" },
  { level: 2, title: "Getting Strong", xpRequired: 250, color: "#1BC7B1" },
  { level: 3, title: "Determined", xpRequired: 500, color: "#FF6F61" },
  { level: 4, title: "Resilient", xpRequired: 1000, color: "#FF6F61" },
  { level: 5, title: "Champion", xpRequired: 2000, color: "#FFC857" }
];

export const mockSocialStats = {
  friendsQuit: 3,
  encouragementsSent: 12,
  encouragementsReceived: 8,
  communityRank: 847
};