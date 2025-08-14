import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import {
  ArrowLeft,
  Heart,
  Shield,
  Wind,
  Phone,
  Zap,
  Clock,
  CheckCircle,
  RefreshCw,
  MessageCircle
} from "lucide-react";
import { mockCravingTips, mockQuotes } from "../data/mockData";

const CravingHelp = ({ user }) => {
  const [selectedTip, setSelectedTip] = useState(null);
  const [timer, setTimer] = useState(0);
  const [isTimerActive, setIsTimerActive] = useState(false);
  const [currentQuote, setCurrentQuote] = useState(0);

  // Timer for craving exercises
  useEffect(() => {
    let interval = null;
    if (isTimerActive && timer > 0) {
      interval = setInterval(() => {
        setTimer(timer => timer - 1);
      }, 1000);
    } else if (timer === 0 && isTimerActive) {
      setIsTimerActive(false);
      // Show completion message
      alert("Great job! You've successfully worked through this craving exercise. 🎉");
    }
    return () => clearInterval(interval);
  }, [isTimerActive, timer]);

  const startExercise = (tip) => {
    setSelectedTip(tip);
    const duration = parseInt(tip.duration) * 60; // Convert minutes to seconds
    setTimer(duration);
    setIsTimerActive(true);
  };

  const stopExercise = () => {
    setIsTimerActive(false);
    setTimer(0);
    setSelectedTip(null);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'breathing':
        return <Wind className="w-5 h-5" />;
      case 'distraction':
        return <RefreshCw className="w-5 h-5" />;
      case 'social':
        return <Phone className="w-5 h-5" />;
      case 'physical':
        return <Zap className="w-5 h-5" />;
      default:
        return <Heart className="w-5 h-5" />;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'breathing':
        return 'from-blue-100 to-blue-50 text-blue-600';
      case 'distraction':
        return 'from-purple-100 to-purple-50 text-purple-600';
      case 'social':
        return 'from-green-100 to-green-50 text-green-600';
      case 'physical':
        return 'from-orange-100 to-orange-50 text-orange-600';
      default:
        return 'from-teal-100 to-teal-50 text-teal-600';
    }
  };

  const nextQuote = () => {
    setCurrentQuote((prev) => (prev + 1) % mockQuotes.length);
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
              <div className="relative">
                <Shield className="w-8 h-8 text-coral-500" />
                <Heart className="w-4 h-4 text-white absolute top-2 left-2" fill="currentColor" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">Craving Help</h1>
                <p className="text-sm text-gray-600">Immediate support when you need it</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-8">
        {/* Emergency Support */}
        <Card className="border-0 shadow-lg bg-gradient-to-r from-coral-500 to-coral-600 text-white">
          <CardHeader>
            <CardTitle className="text-xl flex items-center space-x-2">
              <Heart className="w-6 h-6" fill="currentColor" />
              <span>Having a Strong Craving?</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-white/90">
              Remember: Cravings are temporary and will pass. You're stronger than this moment.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link to="/chat">
                <Button className="bg-white text-coral-600 hover:bg-gray-100">
                  <MessageCircle className="w-4 h-4 mr-2" />
                  Talk to {user.avatar === 'nick' ? 'Nick' : 'Nicky'}
                </Button>
              </Link>
              <Button 
                onClick={() => startExercise(mockCravingTips[0])}
                className="bg-white/20 text-white hover:bg-white/30 border border-white/30"
              >
                <Wind className="w-4 h-4 mr-2" />
                Quick Breathing Exercise
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Active Exercise Timer */}
        {isTimerActive && selectedTip && (
          <Card className="border-0 shadow-lg bg-gradient-to-r from-teal-500 to-teal-600 text-white">
            <CardContent className="p-6 text-center">
              <div className="space-y-4">
                <div className="flex items-center justify-center space-x-2">
                  {getCategoryIcon(selectedTip.category)}
                  <h3 className="text-xl font-semibold">{selectedTip.title}</h3>
                </div>
                <div className="text-4xl font-bold">
                  {formatTime(timer)}
                </div>
                <p className="text-white/90">{selectedTip.description}</p>
                <div className="flex justify-center space-x-3">
                  <Button
                    onClick={stopExercise}
                    className="bg-white text-teal-600 hover:bg-gray-100"
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Complete
                  </Button>
                  <Button
                    onClick={stopExercise}
                    variant="outline"
                    className="border-white text-white hover:bg-white/10"
                  >
                    Stop
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Relief Techniques */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
            <Zap className="w-5 h-5 text-yellow-600" />
            <span>Quick Relief Techniques</span>
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockCravingTips.map((tip) => (
              <Card
                key={tip.id}
                className={`border-0 shadow-md hover:shadow-lg transition-all duration-200 cursor-pointer bg-gradient-to-br ${getCategoryColor(tip.category)}`}
                onClick={() => !isTimerActive ? startExercise(tip) : null}
              >
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className={`p-3 rounded-full bg-white/50`}>
                      {getCategoryIcon(tip.category)}
                    </div>
                    <div className="flex-1 space-y-2">
                      <h3 className="font-semibold text-gray-800">{tip.title}</h3>
                      <p className="text-sm text-gray-700">{tip.description}</p>
                      <div className="flex items-center justify-between">
                        <Badge variant="outline" className="border-current text-current bg-white/30">
                          <Clock className="w-3 h-3 mr-1" />
                          {tip.duration}
                        </Badge>
                        <Button
                          size="sm"
                          disabled={isTimerActive}
                          className="bg-white/80 text-gray-800 hover:bg-white"
                        >
                          Start
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Motivational Quote */}
        <Card className="border-0 shadow-md bg-gradient-to-r from-yellow-100 to-yellow-50">
          <CardContent className="p-6 text-center">
            <div className="space-y-4">
              <div className="text-4xl">💪</div>
              <blockquote className="text-lg font-medium text-gray-800 italic">
                "{mockQuotes[currentQuote]}"
              </blockquote>
              <Button
                onClick={nextQuote}
                variant="outline"
                size="sm"
                className="border-yellow-600 text-yellow-600 hover:bg-yellow-50"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                New Quote
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Success Reminders */}
        <Card className="border-0 shadow-md bg-white">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span>Remember Your Progress</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{user.streak}</div>
                <p className="text-sm text-green-700">Days Smoke-Free</p>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">90</div>
                <p className="text-sm text-blue-700">Cigarettes Avoided</p>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">$45.00</div>
                <p className="text-sm text-yellow-700">Money Saved</p>
              </div>
            </div>
            <p className="text-center text-gray-600 text-sm">
              You've already overcome so many cravings. You can do this one too! 🌟
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CravingHelp;