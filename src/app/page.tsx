"use client";

import React, { useState } from "react";
import TIPMInterface from "../components/TIPMInterface";
import { EnhancedDashboard } from "../components/EnhancedDashboard";

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"original" | "enhanced">(
    "enhanced"
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab("enhanced")}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                activeTab === "enhanced"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              🚀 TIPM v3.0
            </button>
            <button
              onClick={() => setActiveTab("original")}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                activeTab === "original"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              📊 TIPM 2.0
            </button>
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <main>
        <div className="p-4">
          {activeTab === "enhanced" ? (
            <div className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h2 className="text-lg font-semibold text-blue-900">🚀 TIPM v3.0 - Enhanced Dashboard</h2>
                <p className="text-blue-700 mt-2">Advanced analytics and visualizations</p>
              </div>
              <EnhancedDashboard />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h2 className="text-lg font-semibold text-green-900">📊 TIPM 2.0 - Interface</h2>
                <p className="text-green-700 mt-2">Core tariff analysis functionality</p>
              </div>
              <TIPMInterface />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="text-sm">
              TIPM v3.0 - The AI-Powered Impact Analysis Tool
            </p>
            <p className="text-xs mt-2 text-gray-500">
              Advanced US tariff impact analysis using authoritative government
              data
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
