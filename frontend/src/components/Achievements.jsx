import React from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import {
  ArrowLeft,
  Shield,
  Heart,
  Trophy,
  Star,
  Award,
  Target,
  Users,
  Share2
} from "lucide-react";
import { mockAchievements, mockSocialStats } from "../data/mockData";

const Achievements = ({ user }) => {
  const earnedCount = mockAchievements.filter(a => a.earned).length;
  const totalCount = mockAchievements.length;
  const completionPercentage = (earnedCount / totalCount) * 100;

  const getBadgeIcon = (type, earned) => {
    const baseClass = "w-16 h-16 mx-auto mb-4";
    if (!earned) {
      return <Shield className={`${baseClass} text-gray-400`} />;
    }

    switch (type) {
      case 'gold':
        return <Shield className={`${baseClass} text-yellow-600`} fill="currentColor" />;
      case 'silver':
        return <Shield className={`${baseClass} text-gray-500`} fill="currentColor" />;
      case 'bronze':
        return <Shield className={`${baseClass} text-orange-600`} fill="currentColor" />;
      default:
        return <Shield className={`${baseClass} text-teal-500`} fill="currentColor" />;
    }
  };

  const getBadgeColor = (type) => {
    switch (type) {
      case 'gold':
        return 'from-yellow-100 to-yellow-50';
      case 'silver':
        return 'from-gray-100 to-gray-50';
      case 'bronze':
        return 'from-orange-100 to-orange-50';
      default:
        return 'from-teal-100 to-teal-50';
    }
  };

  const handleShare = (achievement) => {
    // Mock social sharing
    if (navigator.share) {
      navigator.share({
        title: 'Nicara Achievement!',
        text: `I just earned "${achievement.title}" on my quit-smoking journey! 🏆`,
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`I just earned "${achievement.title}" on my quit-smoking journey with Nicara! 🏆`);
      alert('Achievement shared to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-3">
            <Link to="/">
              <Button variant="ghost" size="sm" className="p-2">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div className="flex items-center space-x-3">
              <Trophy className="w-8 h-8 text-yellow-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-800">Achievements</h1>
                <p className="text-sm text-gray-600">Your quit-smoking victories</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-8">
        {/* Progress Overview */}
        <Card className="border-0 shadow-lg bg-gradient-to-r from-yellow-500 to-yellow-600 text-white">
          <CardHeader>
            <CardTitle className="text-xl flex items-center space-x-2">
              <Trophy className="w-6 h-6" />
              <span>Achievement Progress</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/90">Badges Earned</span>
              <span className="text-2xl font-bold">{earnedCount}/{totalCount}</span>
            </div>
            <Progress value={completionPercentage} className="h-3 bg-white/20">
              <div 
                className="h-full bg-white rounded-full transition-all duration-500"
                style={{ width: `${completionPercentage}%` }}
              />
            </Progress>
            <p className="text-sm text-white/90">
              Keep going! {totalCount - earnedCount} more badges to unlock
            </p>
          </CardContent>
        </Card>

        {/* Social Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="border-0 shadow-md bg-white text-center">
            <CardContent className="p-4">
              <Users className="w-6 h-6 text-teal-500 mx-auto mb-2" />
              <h3 className="font-bold text-xl text-gray-800">{mockSocialStats.friendsQuit}</h3>
              <p className="text-sm text-gray-600">Friends Helped</p>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-md bg-white text-center">
            <CardContent className="p-4">
              <Heart className="w-6 h-6 text-coral-500 mx-auto mb-2" fill="currentColor" />
              <h3 className="font-bold text-xl text-gray-800">{mockSocialStats.encouragementsSent}</h3>
              <p className="text-sm text-gray-600">Encouragements</p>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-md bg-white text-center">
            <CardContent className="p-4">
              <Star className="w-6 h-6 text-yellow-600 mx-auto mb-2" fill="currentColor" />
              <h3 className="font-bold text-xl text-gray-800">{mockSocialStats.encouragementsReceived}</h3>
              <p className="text-sm text-gray-600">Received</p>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-md bg-white text-center">
            <CardContent className="p-4">
              <Award className="w-6 h-6 text-purple-500 mx-auto mb-2" />
              <h3 className="font-bold text-xl text-gray-800">#{mockSocialStats.communityRank}</h3>
              <p className="text-sm text-gray-600">Community Rank</p>
            </CardContent>
          </Card>
        </div>

        {/* Achievement Categories */}
        <div className="space-y-6">
          <div className="flex items-center space-x-2">
            <Shield className="w-5 h-5 text-teal-500" />
            <h2 className="text-lg font-semibold text-gray-800">Your Badges</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockAchievements.map((achievement) => (
              <Card
                key={achievement.id}
                className={`border-0 shadow-md transition-all duration-200 hover:shadow-lg ${
                  achievement.earned
                    ? `bg-gradient-to-br ${getBadgeColor(achievement.type)}`
                    : 'bg-white hover:bg-gray-50'
                }`}
              >
                <CardContent className="p-6 text-center">
                  {getBadgeIcon(achievement.type, achievement.earned)}
                  
                  <div className="space-y-2">
                    <h3 className={`font-bold text-lg ${
                      achievement.earned ? 'text-gray-800' : 'text-gray-500'
                    }`}>
                      {achievement.title}
                    </h3>
                    <p className={`text-sm ${
                      achievement.earned ? 'text-gray-600' : 'text-gray-400'
                    }`}>
                      {achievement.description}
                    </p>

                    {achievement.earned && (
                      <div className="space-y-3 mt-4">
                        <Badge 
                          variant="outline" 
                          className={`${
                            achievement.type === 'gold' ? 'border-yellow-600 text-yellow-600' :
                            achievement.type === 'silver' ? 'border-gray-500 text-gray-500' :
                            'border-orange-600 text-orange-600'
                          }`}
                        >
                          {achievement.type.charAt(0).toUpperCase() + achievement.type.slice(1)} Badge
                        </Badge>
                        <p className="text-xs text-gray-500">
                          Earned on {new Date(achievement.earnedDate).toLocaleDateString()}
                        </p>
                        <Button
                          onClick={() => handleShare(achievement)}
                          size="sm"
                          className="bg-coral-500 hover:bg-coral-600 text-white"
                        >
                          <Share2 className="w-3 h-3 mr-1" />
                          Share
                        </Button>
                      </div>
                    )}

                    {!achievement.earned && achievement.progress !== undefined && (
                      <div className="space-y-3 mt-4">
                        <div className="space-y-1">
                          <div className="flex justify-between text-xs text-gray-500">
                            <span>Progress</span>
                            <span>{achievement.progress}/{achievement.total}</span>
                          </div>
                          <Progress 
                            value={(achievement.progress / achievement.total) * 100} 
                            className="h-2"
                          />
                        </div>
                        <p className="text-xs text-gray-500">
                          {achievement.total - achievement.progress} more to go!
                        </p>
                      </div>
                    )}

                    {!achievement.earned && achievement.progress === undefined && (
                      <div className="mt-4">
                        <Badge variant="outline" className="border-gray-400 text-gray-400">
                          Locked
                        </Badge>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Motivational Message */}
        <Card className="border-0 shadow-md bg-gradient-to-r from-teal-100 to-coral-100">
          <CardContent className="p-6 text-center">
            <Star className="w-12 h-12 text-yellow-600 mx-auto mb-4" fill="currentColor" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              You're Making Amazing Progress!
            </h3>
            <p className="text-gray-600 mb-4">
              Every achievement is a step closer to a healthier, smoke-free life. 
              Keep up the fantastic work, {user.name}!
            </p>
            <Link to="/chat">
              <Button className="bg-teal-500 hover:bg-teal-600 text-white">
                Chat with {user.avatar === 'nick' ? 'Nick' : 'Nicky'}
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Achievements;