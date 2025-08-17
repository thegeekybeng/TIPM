"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Factory,
  ShoppingCart,
  MapPin,
  Building2,
  Globe,
  BarChart3,
  Download,
  Settings,
  AlertTriangle,
  CheckCircle,
  Clock,
  Database,
  RefreshCw,
  Info,
  Target,
  Shield,
  TrendingUpIcon,
} from "lucide-react";
import {
  apiClient,
  CountryInfo,
  AnalysisResult,
  SectorAnalysisResponse,
} from "./api-client";

const TIPMInterface: React.FC = () => {
  const [selectedCountry, setSelectedCountry] = useState<string>("");
  const [customTariff, setCustomTariff] = useState<number | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(
    null
  );
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [apiStatus, setApiStatus] = useState<string>(
    "🔄 Initializing API connection..."
  );
  const [availableCountries, setAvailableCountries] = useState<string[]>([]);
  const [showCustomTariff, setShowCustomTariff] = useState<boolean>(false);

  // Enhanced sorting functionality
  const [sortMethod, setSortMethod] = useState<string>("tariff_rate");
  const [sortDirection, setSortDirection] = useState<string>("desc");

  // Initialize API connection on component mount
  useEffect(() => {
    initializeAPI();
  }, []);

  const initializeAPI = async () => {
    try {
      setApiStatus("🔄 Testing API connectivity...");

      // Test the API connectivity
      const connectivityTest = await apiClient.testConnectivity();

      if (connectivityTest.success) {
        setApiStatus(connectivityTest.message);

        // Get available countries from API
        const countries = await getAvailableCountries();
        setAvailableCountries(countries);
      } else {
        setApiStatus("⚠️ API available but connection failed");
      }
    } catch (error) {
      console.error("API initialization error:", error);
      setApiStatus("❌ API not working - check backend connection");
    }
  };

  const getAvailableCountries = async (): Promise<string[]> => {
    try {
      // Get countries from API
      return await apiClient.getAvailableCountries();
    } catch (error) {
      console.error("Error getting available countries:", error);
      // Fallback to comprehensive list
      return [
        "China",
        "European Union",
        "Japan",
        "South Korea",
        "India",
        "Mexico",
        "Canada",
        "Germany",
        "France",
        "Italy",
        "Spain",
        "Netherlands",
        "Belgium",
        "Sweden",
        "Thailand",
        "Vietnam",
        "Malaysia",
        "Singapore",
        "Indonesia",
        "Philippines",
        "Brazil",
        "Argentina",
        "Chile",
        "Peru",
        "Colombia",
        "Venezuela",
        "South Africa",
        "Nigeria",
        "Kenya",
        "Ethiopia",
        "Ghana",
        "Uganda",
        "Saudi Arabia",
        "UAE",
        "Israel",
        "Turkey",
        "Iran",
        "Qatar",
        "Australia",
        "New Zealand",
        "Fiji",
        "Papua New Guinea",
      ];
    }
  };

  // Helper functions for country classification
  const getContinent = (countryName: string): string => {
    const continentMap: Record<string, string> = {
      China: "Asia",
      Japan: "Asia",
      "South Korea": "Asia",
      India: "Asia",
      Thailand: "Asia",
      Vietnam: "Asia",
      Malaysia: "Asia",
      Singapore: "Asia",
      Indonesia: "Asia",
      Philippines: "Asia",
      "European Union": "Europe",
      Germany: "Europe",
      France: "Europe",
      Italy: "Europe",
      Spain: "Europe",
      Netherlands: "Europe",
      Belgium: "Europe",
      Sweden: "Europe",
      Mexico: "Americas",
      Canada: "Americas",
      Brazil: "Americas",
      Argentina: "Americas",
      Chile: "Americas",
      Peru: "Americas",
      Colombia: "Americas",
      Venezuela: "Americas",
      "South Africa": "Africa",
      Nigeria: "Africa",
      Kenya: "Africa",
      Ethiopia: "Africa",
      Ghana: "Africa",
      Uganda: "Africa",
      "Saudi Arabia": "Middle East",
      UAE: "Middle East",
      Israel: "Middle East",
      Turkey: "Middle East",
      Iran: "Middle East",
      Qatar: "Middle East",
      Australia: "Oceania",
      "New Zealand": "Oceania",
      Fiji: "Oceania",
      "Papua New Guinea": "Oceania",
    };
    return continentMap[countryName] || "Unknown";
  };

  const getGlobalGroups = (countryName: string): string[] => {
    const groups: Record<string, string[]> = {
      China: ["G20", "BRICS"],
      Japan: ["G7", "G20"],
      Germany: ["G7", "G20", "EU"],
      France: ["G7", "G20", "EU"],
      Italy: ["G7", "G20", "EU"],
      Canada: ["G7", "G20"],
      India: ["G20", "BRICS"],
      Brazil: ["G20", "BRICS"],
      "South Africa": ["G20", "BRICS"],
      "European Union": ["G7"],
      "South Korea": ["G20"],
      Australia: ["G20"],
      Mexico: ["G20"],
      Argentina: ["G20"],
      Turkey: ["G20"],
      "Saudi Arabia": ["G20"],
      Indonesia: ["G20"],
    };
    return groups[countryName] || [];
  };

  const isEmergingMarket = (countryName: string): boolean => {
    const emergingMarkets = [
      "China",
      "India",
      "Brazil",
      "Russia",
      "South Africa",
      "Mexico",
      "Indonesia",
      "Turkey",
      "Thailand",
      "Malaysia",
      "Philippines",
      "Vietnam",
      "Egypt",
      "Nigeria",
      "Kenya",
      "Ethiopia",
      "Ghana",
      "Uganda",
      "Colombia",
      "Peru",
      "Chile",
      "Argentina",
      "Venezuela",
    ];
    return emergingMarkets.includes(countryName);
  };

  // Get countries for selected category
  const getCountriesForCategory = (category: string): string[] => {
    if (category === "all") {
      return availableCountries;
    }

    // Filter countries by continent/category
    const categoryMap: Record<string, string[]> = {
      "Asian Nations": availableCountries.filter(
        (c) => getContinent(c) === "Asia"
      ),
      "European Nations": availableCountries.filter(
        (c) => getContinent(c) === "Europe"
      ),
      Americas: availableCountries.filter(
        (c) => getContinent(c) === "Americas"
      ),
      "African Nations": availableCountries.filter(
        (c) => getContinent(c) === "Africa"
      ),
      "Middle East": availableCountries.filter(
        (c) => getContinent(c) === "Middle East"
      ),
      Oceania: availableCountries.filter((c) => getContinent(c) === "Oceania"),
    };

    return categoryMap[category] || availableCountries;
  };

  // Sort countries based on selected method and direction
  const getSortedCountries = async (category: string) => {
    let countries = getCountriesForCategory(category);

    if (sortMethod === "alphabetical") {
      return countries.sort((a, b) =>
        sortDirection === "desc" ? b.localeCompare(a) : a.localeCompare(b)
      );
    }

    // For other sort methods, we need to get real data
    const countriesWithData = await Promise.all(
      countries.map(async (country) => {
        try {
          const data = await apiClient.getCountryInfo(country);
          return { name: country, data };
        } catch (error) {
          console.error(`Error getting data for ${country}:`, error);
          return { name: country, data: null };
        }
      })
    );

    // Filter out countries without data
    const validCountries = countriesWithData.filter(
      (item) => item.data !== null
    );

    return validCountries.sort((a, b) => {
      if (!a.data || !b.data) return 0;

      let comparison = 0;
      switch (sortMethod) {
        case "tariff_rate":
          comparison = a.data.tariff_rate - b.data.tariff_rate;
          break;
        case "gdp":
          comparison = b.data.gdp_billions - a.data.gdp_billions;
          break;
        case "continent":
          comparison = a.data.continent.localeCompare(b.data.continent);
          break;
        default:
          comparison = 0;
      }

      return sortDirection === "desc" ? comparison : -comparison;
    });
  };

  // Toggle sort direction
  const toggleSortDirection = () => {
    setSortDirection(sortDirection === "desc" ? "asc" : "desc");
  };

  // Format GDP for display
  const formatGDP = (gdp: number): string => {
    if (gdp >= 1e12) return `$${(gdp / 1e12).toFixed(1)}T`;
    if (gdp >= 1e9) return `$${(gdp / 1e9).toFixed(1)}B`;
    if (gdp >= 1e6) return `$${(gdp / 1e6).toFixed(1)}M`;
    return `$${gdp.toLocaleString()}`;
  };

  // Enhanced analysis function using API
  const analyzeCountry = async (
    countryName: string,
    customTariffRate: number | null = null
  ) => {
    setIsLoading(true);
    try {
      const result = await apiClient.analyzeCountry(
        countryName,
        customTariffRate
      );
      setAnalysisResult(result);
    } catch (error) {
      console.error("Analysis error:", error);
      setAnalysisResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Refresh API connection
  const refreshAPI = async () => {
    setApiStatus("🔄 Refreshing API connection...");
    await initializeAPI();
  };

  // Get sorted countries for display
  const [sortedCountries, setSortedCountries] = useState<string[]>([]);

  useEffect(() => {
    const loadSortedCountries = async () => {
      const sorted = await getSortedCountries(selectedCategory);
      setSortedCountries(
        sorted.map((item) => (typeof item === "string" ? item : item.name))
      );
    };

    if (availableCountries.length > 0) {
      loadSortedCountries();
    }
  }, [selectedCategory, sortMethod, sortDirection, availableCountries]);

  // Country categories for filtering
  const COUNTRY_CATEGORIES = {
    all: "All Countries",
    "Asian Nations": "Asian Nations",
    "European Nations": "European Nations",
    Americas: "Americas",
    "African Nations": "African Nations",
    "Middle East": "Middle East",
    Oceania: "Oceania",
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🌐 TIPM - Tariff Impact Propagation Model
              </h1>
              <p className="mt-2 text-gray-600">
                Real US-imposed tariff analysis with economic insights
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">{apiStatus}</div>
              <button
                onClick={refreshAPI}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="Refresh API connection"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* API Status */}
        <div className="mb-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <Database className="w-6 h-6 text-blue-600" />
            <div>
              <h3 className="text-lg font-semibold text-blue-900">
                API Connection Status
              </h3>
              <p className="text-blue-700">{apiStatus}</p>
              <div className="mt-2 text-sm text-blue-600">
                <strong>Backend:</strong> FastAPI with real US tariff data
              </div>
            </div>
          </div>
        </div>

        {/* Main Interface */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - Country Selection */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                🎯 Country Selection
              </h2>

              {/* Category Filter */}
              <div className="mb-4">
                <label
                  htmlFor="category-filter"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Filter by Region
                </label>
                <select
                  id="category-filter"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {Object.entries(COUNTRY_CATEGORIES).map(([key, label]) => (
                    <option key={key} value={key}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Sorting Controls */}
              <div className="mb-4">
                <label
                  htmlFor="sort-method"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Sort by
                </label>
                <div className="flex space-x-2">
                  <select
                    id="sort-method"
                    value={sortMethod}
                    onChange={(e) => setSortMethod(e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="tariff_rate">Tariff Rate</option>
                    <option value="gdp">GDP</option>
                    <option value="continent">Continent</option>
                    <option value="alphabetical">Alphabetical</option>
                  </select>
                  <button
                    onClick={toggleSortDirection}
                    className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                    title="Toggle sort direction"
                  >
                    {sortDirection === "desc" ? "↓" : "↑"}
                  </button>
                </div>
              </div>

              {/* Country List */}
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {sortedCountries.map((country) => (
                  <button
                    key={country}
                    onClick={() => setSelectedCountry(country)}
                    className={`w-full text-left p-3 rounded-lg border transition-all ${
                      selectedCountry === country
                        ? "border-blue-500 bg-blue-50 text-blue-900"
                        : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                    }`}
                  >
                    <div className="font-medium">{country}</div>
                    <div className="text-sm text-gray-500">
                      {getContinent(country)}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right Panel - Analysis */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                📊 Tariff Impact Analysis
              </h2>

              {selectedCountry ? (
                <div className="space-y-6">
                  {/* Country Info */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {selectedCountry}
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Continent:</span>
                        <div className="font-medium">
                          {getContinent(selectedCountry)}
                        </div>
                      </div>
                      <div>
                        <span className="text-gray-500">Global Groups:</span>
                        <div className="font-medium">
                          {getGlobalGroups(selectedCountry).join(", ") ||
                            "None"}
                        </div>
                      </div>
                      <div>
                        <span className="text-gray-500">Market Type:</span>
                        <div className="font-medium">
                          {isEmergingMarket(selectedCountry)
                            ? "Emerging"
                            : "Developed"}
                        </div>
                      </div>
                      <div>
                        <span className="text-gray-500">Data Status:</span>
                        <div className="font-medium text-green-600">
                          API Connected
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Analysis Controls */}
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h4 className="text-lg font-semibold text-gray-900">
                        Analysis Options
                      </h4>
                      <button
                        onClick={() => setShowCustomTariff(!showCustomTariff)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        {showCustomTariff
                          ? "Hide Custom Rate"
                          : "Add Custom Rate"}
                      </button>
                    </div>

                    {showCustomTariff && (
                      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <label
                          htmlFor="custom-tariff-input"
                          className="block text-sm font-medium text-yellow-800 mb-2"
                        >
                          Custom Tariff Rate (%) - Optional
                        </label>
                        <div className="flex space-x-2">
                          <input
                            id="custom-tariff-input"
                            type="number"
                            value={customTariff || ""}
                            onChange={(e) =>
                              setCustomTariff(
                                e.target.value ? Number(e.target.value) : null
                              )
                            }
                            className="flex-1 px-3 py-2 border border-yellow-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                            min="0"
                            max="100"
                            step="0.1"
                            placeholder="Enter custom tariff rate"
                          />
                          <button
                            onClick={() => setCustomTariff(null)}
                            className="px-3 py-2 text-yellow-700 border border-yellow-300 rounded-md hover:bg-yellow-100 transition-colors"
                          >
                            Clear
                          </button>
                        </div>
                        <p className="text-xs text-yellow-600 mt-1">
                          Leave empty to use actual US-imposed tariff rates
                        </p>
                      </div>
                    )}

                    <button
                      onClick={() =>
                        analyzeCountry(selectedCountry, customTariff)
                      }
                      disabled={isLoading}
                      className="w-full px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors font-medium"
                    >
                      {isLoading
                        ? "Analyzing..."
                        : "Analyze with Real Tariff Data"}
                    </button>
                  </div>

                  {/* Analysis Results */}
                  {analysisResult && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-6"
                    >
                      {/* Economic Impact Summary */}
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
                          <TrendingUpIcon className="w-5 h-5 mr-2" />
                          Economic Impact Analysis
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">
                              $
                              {(
                                analysisResult.economic_impact
                                  .trade_disruption_usd / 1000000
                              ).toFixed(1)}
                              M
                            </div>
                            <div className="text-sm text-blue-700">
                              Trade Disruption
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">
                              {analysisResult.economic_impact.price_increase_pct.toFixed(
                                1
                              )}
                              %
                            </div>
                            <div className="text-sm text-blue-700">
                              Price Increase
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">
                              {analysisResult.economic_impact.employment_effect_jobs.toLocaleString()}
                            </div>
                            <div className="text-sm text-blue-700">
                              Jobs Affected
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">
                              {analysisResult.economic_impact.gdp_impact_pct.toFixed(
                                2
                              )}
                              %
                            </div>
                            <div className="text-sm text-blue-700">
                              GDP Impact
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Sector Analysis */}
                      {analysisResult.sector_analysis &&
                        analysisResult.sector_analysis.length > 0 && (
                          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                            <h4 className="text-lg font-semibold text-green-900 mb-3 flex items-center">
                              <Target className="w-5 h-5 mr-2" />
                              Sector-Specific Analysis
                            </h4>
                            <div className="space-y-3">
                              {analysisResult.sector_analysis.map(
                                (sector, index) => (
                                  <div
                                    key={index}
                                    className="bg-white rounded-lg p-3 border border-green-200"
                                  >
                                    <div className="flex items-center justify-between mb-2">
                                      <span className="font-medium text-green-900">
                                        {sector.sector}
                                      </span>
                                      <span
                                        className={`px-2 py-1 rounded-full text-xs font-medium ${
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
                                    <div className="text-sm text-green-700">
                                      <span className="font-medium">
                                        Tariff Rate:
                                      </span>{" "}
                                      {Math.round(sector.tariff_rate)}% |
                                      <span className="font-medium ml-2">
                                        Source:
                                      </span>{" "}
                                      {sector.source}
                                    </div>
                                    <div className="text-xs text-green-600 mt-1">
                                      {sector.notes}
                                    </div>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}

                      {/* Economic Insights */}
                      {analysisResult.economic_insights &&
                        analysisResult.economic_insights.length > 0 && (
                          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                            <h4 className="text-lg font-semibold text-purple-900 mb-3 flex items-center">
                              <Info className="w-5 h-5 mr-2" />
                              Economic Insights & Considerations
                            </h4>
                            <ul className="space-y-2">
                              {analysisResult.economic_insights.map(
                                (insight, index) => (
                                  <li key={index} className="flex items-start">
                                    <span className="text-purple-500 mr-2">
                                      •
                                    </span>
                                    <span className="text-sm text-purple-800">
                                      {insight}
                                    </span>
                                  </li>
                                )
                              )}
                            </ul>
                          </div>
                        )}

                      {/* Mitigation Strategies */}
                      {analysisResult.mitigation_strategies &&
                        analysisResult.mitigation_strategies.length > 0 && (
                          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                            <h4 className="text-lg font-semibold text-orange-900 mb-3 flex items-center">
                              <Shield className="w-5 h-5 mr-2" />
                              Potential Mitigation Strategies
                            </h4>
                            <ul className="space-y-2">
                              {analysisResult.mitigation_strategies.map(
                                (strategy, index) => (
                                  <li key={index} className="flex items-start">
                                    <span className="text-orange-500 mr-2">
                                      •
                                    </span>
                                    <span className="text-sm text-orange-800">
                                      {strategy}
                                    </span>
                                  </li>
                                )
                              )}
                            </ul>
                          </div>
                        )}

                      {/* Data Sources */}
                      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">
                          Data Sources & Confidence
                        </h4>
                        <div className="flex items-center space-x-2 text-sm text-gray-700">
                          <CheckCircle className="w-4 h-4" />
                          <span>
                            Sources: {analysisResult.data_sources.join(", ")}
                          </span>
                          <span>•</span>
                          <span>
                            Confidence:{" "}
                            {analysisResult.overall_confidence * 100}%
                          </span>
                          <span>•</span>
                          <span>
                            Last Updated:{" "}
                            {new Date(
                              analysisResult.timestamp
                            ).toLocaleString()}
                          </span>
                        </div>
                        {analysisResult.custom_tariff_rate && (
                          <div className="mt-2 text-sm text-blue-600">
                            <Info className="w-4 h-4 inline mr-1" />
                            Analysis includes custom tariff rate of{" "}
                            {Math.round(analysisResult.custom_tariff_rate)}%
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <Globe className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                  <p>Select a country to begin analysis</p>
                  <p className="text-sm mt-2">
                    Analysis will use real US-imposed tariff rates with economic
                    insights
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TIPMInterface;
