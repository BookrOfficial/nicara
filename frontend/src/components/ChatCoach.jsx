import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import {
  ArrowLeft,
  Send,
  Heart,
  Shield,
  MessageCircle,
  Lightbulb
} from "lucide-react";
import { mockChatMessages } from "../data/mockData";

const ChatCoach = ({ user }) => {
  const [messages, setMessages] = useState(mockChatMessages);
  const [newMessage, setNewMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    // Add user message
    const userMessage = {
      id: `msg_${Date.now()}`,
      sender: "user",
      message: newMessage.trim(),
      timestamp: new Date().toISOString(),
      type: "message"
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessage("");
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponses = [
        "I'm here to support you! Remember, every craving you overcome makes you stronger. 💪",
        "That's a great question! Cravings are temporary, but your commitment to quit is permanent. Try taking 5 deep breaths.",
        "You're doing amazing! Each day smoke-free is a victory. What's one thing you're grateful for today?",
        "I understand this can be challenging. Let's try a quick mindfulness exercise - focus on 3 things you can see right now.",
        "Your progress is inspiring! Remember, setbacks are just setups for comebacks. Keep going! 🌟"
      ];

      const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];

      const aiMessage = {
        id: `msg_${Date.now()}_ai`,
        sender: user.avatar,
        message: randomResponse,
        timestamp: new Date().toISOString(),
        type: "advice"
      };

      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const quickActions = [
    { text: "I'm having a craving", action: "craving" },
    { text: "How am I doing?", action: "progress" },
    { text: "Need motivation", action: "motivation" },
    { text: "Share a tip", action: "tip" }
  ];

  const handleQuickAction = (action) => {
    const actionMessages = {
      craving: "I'm having a craving right now. Can you help?",
      progress: "Can you tell me how I'm doing with my quit journey?",
      motivation: "I could use some motivation today.",
      tip: "Can you share a helpful tip for staying smoke-free?"
    };

    setNewMessage(actionMessages[action]);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-3">
            <Link to="/">
              <Button variant="ghost" size="sm" className="p-2">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center">
                <div className="relative">
                  <Shield className="w-6 h-6 text-teal-500" />
                  <Heart className="w-3 h-3 text-coral-500 absolute top-1.5 left-1.5" fill="currentColor" />
                </div>
              </div>
              <div>
                <h1 className="font-semibold text-gray-800">
                  {user.avatar === 'nick' ? 'Nick' : 'Nicky'}
                </h1>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">Online</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 max-w-2xl mx-auto w-full px-4 py-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-xs lg:max-w-md ${message.sender === 'user' ? 'order-2' : 'order-1'}`}>
              {message.sender !== 'user' && (
                <div className="flex items-center space-x-2 mb-1">
                  <div className="w-6 h-6 rounded-full bg-teal-100 flex items-center justify-center">
                    <Shield className="w-4 h-4 text-teal-500" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">
                    {message.sender === 'nick' ? 'Nick' : 'Nicky'}
                  </span>
                </div>
              )}
              <Card className={`${
                message.sender === 'user'
                  ? 'bg-teal-500 text-white border-0'
                  : 'bg-white border-gray-200'
              }`}>
                <CardContent className="p-3">
                  <p className={`text-sm ${message.sender === 'user' ? 'text-white' : 'text-gray-800'}`}>
                    {message.message}
                  </p>
                  {message.type === 'advice' && message.sender !== 'user' && (
                    <Badge variant="outline" className="mt-2 text-xs border-teal-200 text-teal-600">
                      <Lightbulb className="w-3 h-3 mr-1" />
                      Tip
                    </Badge>
                  )}
                </CardContent>
              </Card>
              <p className="text-xs text-gray-500 mt-1 px-3">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md">
              <div className="flex items-center space-x-2 mb-1">
                <div className="w-6 h-6 rounded-full bg-teal-100 flex items-center justify-center">
                  <Shield className="w-4 h-4 text-teal-500" />
                </div>
                <span className="text-sm font-medium text-gray-700">
                  {user.avatar === 'nick' ? 'Nick' : 'Nicky'}
                </span>
              </div>
              <Card className="bg-white border-gray-200">
                <CardContent className="p-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="max-w-2xl mx-auto w-full px-4 pb-4">
        <div className="flex flex-wrap gap-2 mb-4">
          {quickActions.map((action, index) => (
            <Button
              key={index}
              variant="outline"
              size="sm"
              onClick={() => handleQuickAction(action.action)}
              className="text-xs bg-white hover:bg-teal-50 border-teal-200 text-teal-600"
            >
              {action.text}
            </Button>
          ))}
        </div>
      </div>

      {/* Message Input */}
      <div className="bg-white border-t">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <Input
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder={`Message ${user.avatar === 'nick' ? 'Nick' : 'Nicky'}...`}
              className="flex-1 border-gray-200 focus:border-teal-400 focus:ring-teal-400"
            />
            <Button
              type="submit"
              disabled={!newMessage.trim() || isTyping}
              className="bg-teal-500 hover:bg-teal-600 text-white"
            >
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatCoach;