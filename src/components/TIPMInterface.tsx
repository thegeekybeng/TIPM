"use client";

import React, { useState, useEffect } from "react";
import { apiClient } from "./api-client";

interface CountryInfo {
  name: string;
  tariff_rate: number;
  continent: string;
  global_groups: string[];
  emerging_market: boolean;
  gdp_billions: number;
  trade_volume_millions: number;
  data_confidence: string;
  data_sources: string[];
  last_updated: string;
  affected_sectors: string[];
}

interface AnalysisResult {
  country_name: string;
  actual_tariff_rate: number;
  custom_tariff_rate: number | null;
  overall_confidence: number;
  economic_impact: {
    trade_disruption_usd: number;
    price_increase_pct: number;
    employment_effect_jobs: number;
    gdp_impact_pct: number;
    industry_severity: string;
  };
  sector_analysis: Array<{
    sector: string;
    tariff_rate: number;
    impact_level: string;
    source: string;
    trade_volume: number;
    notes: string;
  }>;
  economic_insights: string[];
  mitigation_strategies: string[];
  timestamp: string;
  data_sources: string[];
}

const TIPMInterface: React.FC = () => {
  const [selectedCountry, setSelectedCountry] = useState<string>("");
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(
    null
  );
  const [availableCountries, setAvailableCountries] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<string>("Checking...");

  useEffect(() => {
    initializeSystem();
  }, []);

  const initializeSystem = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log("🚀 Initializing TIPM System...");

      // Test API connectivity
      const connectivityTest = await apiClient.testConnectivity();
      setApiStatus(connectivityTest.success ? "Connected" : "Failed");

      if (!connectivityTest.success) {
        throw new Error(connectivityTest.message);
      }

      // Get available countries
      const countries = await apiClient.getAvailableCountries();
      setAvailableCountries(countries);

      console.log("✅ TIPM System initialized successfully");
      console.log(`📊 Available countries: ${countries.length}`);
    } catch (error) {
      console.error("❌ Failed to initialize TIPM System:", error);
      setError(error instanceof Error ? error.message : "Unknown error");
      setApiStatus("Failed");
    } finally {
      setIsLoading(false);
    }
  };

  const analyzeCountry = async (
    countryName: string,
    customTariffRate?: number
  ) => {
    try {
      setIsLoading(true);
      setError(null);

      console.log(`🔍 Analyzing country: ${countryName}`);

      const result = await apiClient.analyzeCountry(
        countryName,
        customTariffRate
      );
      setAnalysisResult(result);

      console.log("✅ Analysis completed successfully");
    } catch (error) {
      console.error("❌ Analysis failed:", error);
      setError(error instanceof Error ? error.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCountrySelect = (countryName: string) => {
    setSelectedCountry(countryName);
    if (countryName) {
      analyzeCountry(countryName);
    }
  };

  const handleCustomTariffAnalysis = () => {
    if (selectedCountry) {
      const customRate = prompt(
        `Enter custom tariff rate for ${selectedCountry} (0-100%):`
      );
      if (customRate) {
        const rate = parseFloat(customRate);
        if (!isNaN(rate) && rate >= 0 && rate <= 100) {
          analyzeCountry(selectedCountry, rate);
        } else {
          alert("Please enter a valid tariff rate between 0 and 100");
        }
      }
    }
  };

  if (isLoading && !availableCountries.length) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Initializing TIPM System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚀 TIPM - Tariff Impact Propagation Model
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Economic Analysis & Insights
          </p>
          <div className="mt-4">
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                apiStatus === "Connected"
                  ? "bg-green-100 text-green-800"
                  : apiStatus === "Failed"
                    ? "bg-red-100 text-red-800"
                    : "bg-yellow-100 text-yellow-800"
              }`}
            >
              API Status: {apiStatus}
            </span>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Country Selection */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                🌍 Select Country
              </h2>

              <div className="space-y-4">
                <select
                  value={selectedCountry}
                  onChange={(e) => handleCountrySelect(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  aria-label="Select a country for tariff analysis"
                >
                  <option value="">Choose a country...</option>
                  {availableCountries.map((country) => (
                    <option key={country} value={country}>
                      {country}
                    </option>
                  ))}
                </select>

                {selectedCountry && (
                  <button
                    onClick={handleCustomTariffAnalysis}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                  >
                    🔧 Custom Tariff Analysis
                  </button>
                )}
              </div>

              <div className="mt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  📊 Available Countries
                </h3>
                <p className="text-sm text-gray-600">
                  Total: {availableCountries.length} countries
                </p>
                <div className="mt-2 text-xs text-gray-500">
                  {availableCountries.slice(0, 5).join(", ")}
                  {availableCountries.length > 5 && "..."}
                </div>
              </div>
            </div>
          </div>

          {/* Analysis Results */}
          <div className="lg:col-span-2">
            {analysisResult ? (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  📈 Analysis Results: {analysisResult.country_name}
                </h2>

                {/* Tariff Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-medium text-blue-900 mb-2">
                      Actual Tariff Rate
                    </h3>
                    <p className="text-2xl font-bold text-blue-600">
                      {analysisResult.actual_tariff_rate}%
                    </p>
                  </div>

                  {analysisResult.custom_tariff_rate && (
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h3 className="font-medium text-green-900 mb-2">
                        Custom Tariff Rate
                      </h3>
                      <p className="text-2xl font-bold text-green-600">
                        {analysisResult.custom_tariff_rate}%
                      </p>
                    </div>
                  )}
                </div>

                {/* Economic Impact */}
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    💰 Economic Impact
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <span className="text-sm text-gray-600">
                        Trade Disruption:
                      </span>
                      <p className="font-medium">
                        $
                        {(
                          analysisResult.economic_impact.trade_disruption_usd /
                          1000000
                        ).toFixed(1)}
                        M
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <span className="text-sm text-gray-600">
                        Price Increase:
                      </span>
                      <p className="font-medium">
                        {analysisResult.economic_impact.price_increase_pct.toFixed(
                          1
                        )}
                        %
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <span className="text-sm text-gray-600">
                        Employment Impact:
                      </span>
                      <p className="font-medium">
                        {analysisResult.economic_impact.employment_effect_jobs.toLocaleString()}{" "}
                        jobs
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <span className="text-sm text-gray-600">GDP Impact:</span>
                      <p className="font-medium">
                        {analysisResult.economic_impact.gdp_impact_pct.toFixed(
                          2
                        )}
                        %
                      </p>
                    </div>
                  </div>
                </div>

                {/* Sector Analysis */}
                {analysisResult.sector_analysis.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-3">
                      🏭 Sector Analysis
                    </h3>
                    <div className="space-y-2">
                      {analysisResult.sector_analysis.map((sector, index) => (
                        <div
                          key={index}
                          className="flex justify-between items-center bg-gray-50 p-3 rounded"
                        >
                          <span className="font-medium">{sector.sector}</span>
                          <span
                            className={`px-2 py-1 rounded text-xs font-medium ${
                              sector.impact_level === "Critical"
                                ? "bg-red-100 text-red-800"
                                : sector.impact_level === "High"
                                  ? "bg-orange-100 text-orange-800"
                                  : sector.impact_level === "Medium"
                                    ? "bg-yellow-100 text-yellow-800"
                                    : "bg-green-100 text-green-800"
                            }`}
                          >
                            {sector.impact_level}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Economic Insights */}
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    💡 Economic Insights
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.economic_insights.map((insight, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-blue-500 mr-2">•</span>
                        <span className="text-gray-700">{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Mitigation Strategies */}
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    🛡️ Mitigation Strategies
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.mitigation_strategies.map(
                      (strategy, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-green-500 mr-2">•</span>
                          <span className="text-gray-700">{strategy}</span>
                        </li>
                      )
                    )}
                  </ul>
                </div>

                {/* Data Sources */}
                <div className="text-sm text-gray-500">
                  <p>
                    <strong>Data Sources:</strong>{" "}
                    {analysisResult.data_sources.join(", ")}
                  </p>
                  <p>
                    <strong>Analysis Time:</strong>{" "}
                    {new Date(analysisResult.timestamp).toLocaleString()}
                  </p>
                  <p>
                    <strong>Confidence:</strong>{" "}
                    {(analysisResult.overall_confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-gray-400 text-6xl mb-4">🌍</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Select a country to begin analysis
                </h3>
                <p className="text-gray-600">
                  Choose a country from the dropdown to analyze tariff impact
                  and economic effects
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-sm text-gray-500">
          <p>
            Powered by US Government Official Tariff Data • Real-time Economic
            Analysis
          </p>
        </div>
      </div>
    </div>
  );
};

export default TIPMInterface;
