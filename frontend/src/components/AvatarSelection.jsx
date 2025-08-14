import React, { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Heart, Shield } from "lucide-react";

const AvatarSelection = ({ onAvatarSelect }) => {
  const [selectedAvatar, setSelectedAvatar] = useState("nick");
  const [userName, setUserName] = useState("");

  const avatars = [
    {
      id: "nick",
      name: "Nick",
      description: "Your friendly male coach",
      image: "https://customer-assets.emergentagent.com/job_02ab1c2f-8459-42d4-8c93-e4e93beeb0d6/artifacts/cbd4bl6g_ChatGPT%20Image%20Aug%2014%2C%202025%2C%2008_54_47%20PM.png"
    },
    {
      id: "nicky",
      name: "Nicky",
      description: "Your supportive female coach",
      image: "https://customer-assets.emergentagent.com/job_02ab1c2f-8459-42d4-8c93-e4e93beeb0d6/artifacts/cbd4bl6g_ChatGPT%20Image%20Aug%2014%2C%202025%2C%2008_54_47%20PM.png"
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userName.trim() && selectedAvatar) {
      onAvatarSelect(selectedAvatar, userName.trim());
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-lg border-0 bg-white">
        <CardHeader className="text-center pb-8">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <Shield className="w-12 h-12 text-teal-500" />
              <Heart className="w-6 h-6 text-coral-500 absolute top-3 left-3" fill="currentColor" />
            </div>
            <h1 className="text-3xl font-bold text-gray-800 ml-3">NICARA</h1>
          </div>
          <CardTitle className="text-xl text-gray-700">
            Welcome to your quit-smoking journey!
          </CardTitle>
          <p className="text-gray-600 mt-2">
            Choose your AI coach and let's start this adventure together
          </p>
        </CardHeader>
        <CardContent className="space-y-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="name" className="text-base font-medium text-gray-700">
                What should we call you?
              </Label>
              <Input
                id="name"
                type="text"
                placeholder="Enter your name"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                className="mt-2 h-12 text-base border-gray-200 focus:border-teal-400 focus:ring-teal-400"
                required
              />
            </div>

            <div>
              <Label className="text-base font-medium text-gray-700 mb-4 block">
                Choose your AI coach
              </Label>
              <div className="grid md:grid-cols-2 gap-4">
                {avatars.map((avatar) => (
                  <div
                    key={avatar.id}
                    className={`relative cursor-pointer transition-all duration-200 ${
                      selectedAvatar === avatar.id
                        ? "transform scale-105"
                        : "hover:scale-102"
                    }`}
                    onClick={() => setSelectedAvatar(avatar.id)}
                  >
                    <Card
                      className={`border-2 transition-colors duration-200 ${
                        selectedAvatar === avatar.id
                          ? "border-teal-500 shadow-lg bg-teal-50"
                          : "border-gray-200 hover:border-teal-300 bg-white"
                      }`}
                    >
                      <CardContent className="p-6 text-center">
                        <div className="w-24 h-24 mx-auto mb-4 rounded-full overflow-hidden bg-teal-100">
                          <img
                            src={avatar.image}
                            alt={avatar.name}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <h3 className="text-xl font-bold text-gray-800 mb-2">
                          {avatar.name}
                        </h3>
                        <p className="text-gray-600 text-sm">
                          {avatar.description}
                        </p>
                        {selectedAvatar === avatar.id && (
                          <div className="absolute top-3 right-3">
                            <div className="w-6 h-6 bg-teal-500 rounded-full flex items-center justify-center">
                              <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              </svg>
                            </div>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </div>
                ))}
              </div>
            </div>

            <Button
              type="submit"
              className="w-full h-12 text-lg font-semibold bg-gradient-to-r from-coral-500 to-coral-600 hover:from-coral-600 hover:to-coral-700 text-white border-0 shadow-lg transition-all duration-200 hover:shadow-xl"
              disabled={!userName.trim()}
            >
              Start Your Journey
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default AvatarSelection;