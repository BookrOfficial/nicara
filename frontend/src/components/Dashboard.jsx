import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import {
  Heart,
  Shield,
  MessageCircle,
  Trophy,
  Flame,
  DollarSign,
  XCircle,
  Clock,
  Target,
  Users
} from "lucide-react";
import { mockHealthStats, mockDailyChallenge, mockAchievements } from "../data/mockData";

const Dashboard = ({ user }) => {
  const [completedChallenge, setCompletedChallenge] = useState(false);

  const daysQuit = Math.floor((new Date() - new Date(user.quitDate)) / (1000 * 60 * 60 * 24));
  const progressToNextLevel = (user.xp / (user.xp + user.xpToNextLevel)) * 100;

  const iconMap = {
    "dollar-sign": DollarSign,
    "x-circle": XCircle,
    "heart": Heart,
    "clock": Clock
  };

  const handleCompleteChallenge = () => {
    setCompletedChallenge(true);
    // Mock XP gain animation could be added here
  };

  const NavCard = ({ to, icon: Icon, title, subtitle, color = "teal" }) => (
    <Link to={to}>
      <Card className={`cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-105 border-0 bg-gradient-to-br ${
        color === 'coral' ? 'from-coral-100 to-coral-50' : 
        color === 'gold' ? 'from-yellow-100 to-yellow-50' : 
        'from-teal-100 to-teal-50'
      }`}>
        <CardContent className="p-6 text-center">
          <Icon className={`w-8 h-8 mx-auto mb-3 ${
            color === 'coral' ? 'text-coral-500' : 
            color === 'gold' ? 'text-yellow-600' : 
            'text-teal-500'
          }`} />
          <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
          <p className="text-sm text-gray-600">{subtitle}</p>
        </CardContent>
      </Card>
    </Link>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Shield className="w-8 h-8 text-teal-500" />
                <Heart className="w-4 h-4 text-coral-500 absolute top-2 left-2" fill="currentColor" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">NICARA</h1>
                <p className="text-sm text-gray-600">Hello, {user.name}</p>
              </div>
            </div>
            <div className="text-right">
              <div className="flex items-center space-x-2">
                <Flame className="w-5 h-5 text-orange-500" />
                <span className="text-2xl font-bold text-gray-800">{user.streak}</span>
              </div>
              <p className="text-sm text-gray-600">{user.streak}-day streak</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-8">
        {/* Progress Overview */}
        <Card className="border-0 shadow-lg bg-gradient-to-r from-teal-500 to-teal-600 text-white">
          <CardHeader>
            <CardTitle className="text-xl">Your Progress Today</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/90">Level {user.currentLevel}</span>
              <span className="text-white/90">{user.xp} XP</span>
            </div>
            <Progress value={progressToNextLevel} className="h-3 bg-white/20">
              <div 
                className="h-full bg-white rounded-full transition-all duration-500"
                style={{ width: `${progressToNextLevel}%` }}
              />
            </Progress>
            <p className="text-sm text-white/90">
              {user.xpToNextLevel} XP to next level
            </p>
          </CardContent>
        </Card>

        {/* Health Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {mockHealthStats.map((stat, index) => {
            const IconComponent = iconMap[stat.icon];
            return (
              <Card key={index} className="border-0 shadow-md bg-white">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <IconComponent className={`w-5 h-5 ${stat.color}`} />
                  </div>
                  <div className="space-y-1">
                    <h3 className="font-bold text-xl text-gray-800">{stat.value}</h3>
                    <p className="text-sm text-gray-600">{stat.title}</p>
                    <p className="text-xs text-green-600">{stat.improvement}</p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Daily Challenge */}
        <Card className="border-0 shadow-md bg-white">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Target className="w-5 h-5 text-coral-500" />
              <CardTitle className="text-lg">Today's Challenge</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">{mockDailyChallenge.title}</h3>
              <p className="text-gray-600 text-sm mb-3">{mockDailyChallenge.description}</p>
              <div className="flex items-center justify-between">
                <Badge variant="outline" className="text-yellow-600 border-yellow-600">
                  +{mockDailyChallenge.xpReward} XP
                </Badge>
                <Button
                  onClick={handleCompleteChallenge}
                  disabled={completedChallenge}
                  className={`${
                    completedChallenge
                      ? 'bg-green-500 hover:bg-green-600'
                      : 'bg-coral-500 hover:bg-coral-600'
                  } text-white`}
                >
                  {completedChallenge ? 'Completed! ✓' : 'Mark Complete'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Access Navigation */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <NavCard
            to="/chat"
            icon={MessageCircle}
            title="Chat with Nick"
            subtitle="Get personalized support"
            color="teal"
          />
          <NavCard
            to="/achievements"
            icon={Trophy}
            title="Achievements"
            subtitle="View your badges"
            color="gold"
          />
          <NavCard
            to="/craving-help"
            icon={Heart}
            title="Craving Help"
            subtitle="Immediate support"
            color="coral"
          />
        </div>

        {/* Recent Achievements Preview */}
        <Card className="border-0 shadow-md bg-white">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Trophy className="w-5 h-5 text-yellow-600" />
                <CardTitle className="text-lg">Recent Achievements</CardTitle>
              </div>
              <Link to="/achievements">
                <Button variant="ghost" className="text-teal-600 hover:text-teal-700">
                  View All
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              {mockAchievements.slice(0, 4).map((achievement) => (
                <div
                  key={achievement.id}
                  className={`text-center p-4 rounded-lg ${
                    achievement.earned
                      ? 'bg-gradient-to-br from-yellow-100 to-yellow-50'
                      : 'bg-gray-100'
                  }`}
                >
                  <Shield
                    className={`w-8 h-8 mx-auto mb-2 ${
                      achievement.earned
                        ? achievement.type === 'gold'
                          ? 'text-yellow-600'
                          : achievement.type === 'silver'
                          ? 'text-gray-500'
                          : 'text-orange-600'
                        : 'text-gray-400'
                    }`}
                    fill="currentColor"
                  />
                  <h4 className={`font-medium text-sm ${
                    achievement.earned ? 'text-gray-800' : 'text-gray-500'
                  }`}>
                    {achievement.title}
                  </h4>
                  {!achievement.earned && achievement.progress && (
                    <p className="text-xs text-gray-500 mt-1">
                      {achievement.progress}/{achievement.total}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;