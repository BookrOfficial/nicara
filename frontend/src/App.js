import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import { mockUser } from "./data/mockData";

// Import components
import AvatarSelection from "./components/AvatarSelection";
import Dashboard from "./components/Dashboard";
import ChatCoach from "./components/ChatCoach";
import Achievements from "./components/Achievements";
import CravingHelp from "./components/CravingHelp";

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading user data
    const timer = setTimeout(() => {
      const savedUser = localStorage.getItem('nicara_user');
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      }
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleAvatarSelection = (selectedAvatar, userName) => {
    const userData = {
      ...mockUser,
      name: userName,
      avatar: selectedAvatar
    };
    setUser(userData);
    localStorage.setItem('nicara_user', JSON.stringify(userData));
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r from-teal-400 to-teal-600 animate-pulse"></div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">NICARA</h1>
          <p className="text-gray-600">Loading your quit-smoking journey...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50">
        <AvatarSelection onAvatarSelect={handleAvatarSelection} />
        <Toaster />
      </div>
    );
  }

  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard user={user} />} />
          <Route path="/chat" element={<ChatCoach user={user} />} />
          <Route path="/achievements" element={<Achievements user={user} />} />
          <Route path="/craving-help" element={<CravingHelp user={user} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;