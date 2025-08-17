"use client";

import React, { useState, useEffect } from "react";
import {
  workingTariffModel,
  CountryTariffProfile,
  TariffImpactAnalysis,
  GlobalTariffOverview,
} from "../models/working-tariff-model";
import {
  workingDataManager,
  WorkingDataSource,
} from "../lib/working-data-connectors";

interface CountryData {
  name: string;
  code: string;
  continent: string;
  tariff_rate: number;
  gdp_usd: number;
  trade_volume: number;
  data_confidence: "HIGH" | "MEDIUM" | "LOW";
  data_sources: string[];
  last_updated: string;
}

interface AnalysisResult {
  country: string;
  tariff_impact: "HIGH" | "MEDIUM" | "LOW";
  economic_impact: {
    gdp_impact: number;
    trade_impact: number;
    employment_impact: number;
    consumer_price_impact: number;
  };
  sector_analysis: {
    primary: number;
    secondary: number;
    tertiary: number;
    technology: number;
  };
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  risk_factors: string[];
  recommendations: string[];
  data_sources: string[];
  trade_volume?: number; // Added trade_volume to the interface
}

const TIPMInterface: React.FC = () => {
  const [selectedCountry, setSelectedCountry] = useState<string>("");
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(
    null
  );
  const [availableCountries, setAvailableCountries] = useState<string[]>([]);
  const [dataSources, setDataSources] = useState<WorkingDataSource[]>([]);
  const [globalOverview, setGlobalOverview] =
    useState<GlobalTariffOverview | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dataQuality, setDataQuality] = useState<"HIGH" | "MEDIUM" | "LOW">(
    "LOW"
  );

  useEffect(() => {
    initializeSystem();
  }, []);

  const initializeSystem = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log("🚀 Initializing TIPM System...");

      // Initialize the tariff model
      await workingTariffModel.initialize();

      // Get available countries
      const countries = await workingTariffModel
        .getDataManager()
        .getAvailableCountries();
      setAvailableCountries(countries);

      // Get data sources status
      const sources = await workingTariffModel
        .getDataManager()
        .getDataSources();
      setDataSources(sources);

      // Get global overview
      const overview = await workingTariffModel.getGlobalOverview();
      setGlobalOverview(overview);

      // Get overall data quality
      const quality = workingTariffModel.getDataQuality();
      setDataQuality(quality);

      console.log("✅ TIPM System initialized successfully");
      console.log(`📊 Available countries: ${countries.length}`);
      console.log(`🔗 Active data sources: ${sources.filter((s: WorkingDataSource) => s.status === 'ACTIVE').length}/${sources.length}`);
      
      // Debug: Log first few countries to verify data
      console.log('🔍 Sample countries:', countries.slice(0, 10));
      console.log('🔍 Data sources:', sources.map(s => `${s.name}: ${s.status}`));
    } catch (err) {
      console.error("❌ Error initializing TIPM System:", err);
      setError(
        "Failed to initialize system. Please check your connection and try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const analyzeCountry = async (countryCode: string) => {
    try {
      setIsLoading(true);
      setError(null);

      console.log(`🔍 Analyzing country: ${countryCode}`);

      const analysis = await workingTariffModel.analyzeCountry(countryCode);

      if (!analysis) {
        setError(`No data available for ${countryCode}`);
        return;
      }

      // Convert to our interface format
      const result: AnalysisResult = {
        country: analysis.country.countryName,
        tariff_impact: analysis.country.tariffImpact,
        economic_impact: {
          gdp_impact: analysis.economicImpact.gdpImpact,
          trade_impact: analysis.economicImpact.tradeImpact,
          employment_impact: analysis.economicImpact.employmentImpact,
          consumer_price_impact: analysis.economicImpact.consumerPriceImpact,
        },
        sector_analysis: analysis.sectorImpact,
        risk_level: analysis.riskLevel,
        risk_factors: analysis.riskFactors,
        recommendations: analysis.recommendations,
        data_sources: analysis.country.dataSources,
        trade_volume: analysis.country.tradeVolume, // Assign trade_volume
      };

      setAnalysisResult(result);
      console.log("✅ Analysis completed successfully");
    } catch (err) {
      console.error("❌ Error analyzing country:", err);
      setError("Failed to analyze country. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCountrySelect = (countryCode: string) => {
    setSelectedCountry(countryCode);
    if (countryCode) {
      analyzeCountry(countryCode);
    }
  };

  const refreshData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log("🔄 Refreshing data...");
      await workingTariffModel.refreshData();

      // Re-initialize system
      await initializeSystem();

      console.log("✅ Data refreshed successfully");
    } catch (err) {
      console.error("❌ Error refreshing data:", err);
      setError("Failed to refresh data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getDataQualityColor = (quality: "HIGH" | "MEDIUM" | "LOW") => {
    switch (quality) {
      case "HIGH":
        return "text-green-600 bg-green-100";
      case "MEDIUM":
        return "text-yellow-600 bg-yellow-100";
      case "LOW":
        return "text-red-600 bg-red-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const getImpactColor = (impact: "HIGH" | "MEDIUM" | "LOW") => {
    switch (impact) {
      case "HIGH":
        return "text-red-600 bg-red-100";
      case "MEDIUM":
        return "text-yellow-600 bg-yellow-100";
      case "LOW":
        return "text-green-600 bg-green-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
    if (num >= 1e3) return `${(num / 1e3).toFixed(2)}K`;
    return num.toFixed(2);
  };

  const formatPercentage = (num: number) => {
    return `${num.toFixed(2)}%`;
  };

  if (isLoading && !analysisResult) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">
            Initializing TIPM System...
          </p>
          <p className="text-sm text-gray-500">Connecting to data sources...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">TIPM v2.0</h1>
              <p className="text-gray-600">
                Trump 2025 Tariff Impact Propagation Model
              </p>
              <p className="text-sm text-gray-500">
                Using reliable data sources: USTR, World Bank, Atlantic Council
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div
                className={`px-3 py-1 rounded-full text-sm font-medium ${getDataQualityColor(dataQuality)}`}
              >
                Data Quality: {dataQuality}
              </div>
              <button
                onClick={refreshData}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? "Refreshing..." : "Refresh Data"}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Data Sources Status */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Data Sources Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {dataSources.map((source, index) => (
              <div
                key={index}
                className="bg-white p-4 rounded-lg shadow-sm border"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{source.name}</h3>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      source.status === "ACTIVE"
                        ? "text-green-600 bg-green-100"
                        : "text-red-600 bg-red-100"
                    }`}
                  >
                    {source.status}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <p>
                    Quality:{" "}
                    <span
                      className={`font-medium ${getDataQualityColor(source.dataQuality)}`}
                    >
                      {source.dataQuality}
                    </span>
                  </p>
                  <p>Coverage: {source.coverage}%</p>
                  <p>
                    Last Check:{" "}
                    {new Date(source.lastCheck).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Global Overview */}
        {globalOverview && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Global Tariff Overview
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="text-sm font-medium text-gray-500">
                  Total Countries
                </h3>
                <p className="text-2xl font-bold text-gray-900">
                  {globalOverview.totalCountries}
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="text-sm font-medium text-gray-500">
                  Countries with Data
                </h3>
                <p className="text-2xl font-bold text-gray-900">
                  {globalOverview.countriesWithData}
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="text-sm font-medium text-gray-500">
                  Average Tariff Rate
                </h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatPercentage(globalOverview.averageTariffRate)}
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <h3 className="text-sm font-medium text-gray-500">
                  Data Quality
                </h3>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">High:</span>
                    <span className="font-medium text-green-600">
                      {globalOverview.dataQuality.high}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Medium:</span>
                    <span className="font-medium text-yellow-600">
                      {globalOverview.dataQuality.medium}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Low:</span>
                    <span className="font-medium text-red-600">
                      {globalOverview.dataQuality.low}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Country Selection */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Country Analysis
          </h2>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <label
              htmlFor="country-select"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Select a Country
            </label>
            <select
              id="country-select"
              value={selectedCountry}
              onChange={(e) => handleCountrySelect(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Choose a country...</option>
              {availableCountries.map((countryCode) => (
                <option key={countryCode} value={countryCode}>
                  {countryCode}
                </option>
              ))}
            </select>
            <p className="text-sm text-gray-500 mt-2">
              {availableCountries.length} countries available from World Bank database.
            </p>
          </div>
        </div>

        {/* Analysis Results */}
        {isLoading && selectedCountry && (
          <div className="mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">
                  Analyzing {selectedCountry}...
                </p>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="mb-8">
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
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
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {analysisResult && (
          <div className="space-y-6">
            {/* Country Summary */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Analysis Results for {analysisResult.country}
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">
                    Tariff Impact
                  </h4>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${getImpactColor(analysisResult.tariff_impact)}`}
                  >
                    {analysisResult.tariff_impact}
                  </span>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Risk Level</h4>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${getImpactColor(analysisResult.risk_level)}`}
                  >
                    {analysisResult.risk_level}
                  </span>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700 mb-2">
                    Trade Volume
                  </h4>
                  <span className="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    {analysisResult.trade_volume ? formatPercentage(analysisResult.trade_volume) : 'N/A'}
                  </span>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700 mb-2">
                    Data Sources
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {analysisResult.data_sources.map((source, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                      >
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Economic Impact */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                Economic Impact Analysis
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    GDP Impact
                  </h5>
                  <p
                    className={`text-2xl font-bold ${analysisResult.economic_impact.gdp_impact < 0 ? "text-red-600" : "text-green-600"}`}
                  >
                    {formatPercentage(
                      analysisResult.economic_impact.gdp_impact
                    )}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Trade Impact
                  </h5>
                  <p
                    className={`text-2xl font-bold ${analysisResult.economic_impact.trade_impact < 0 ? "text-red-600" : "text-green-600"}`}
                  >
                    {formatPercentage(
                      analysisResult.economic_impact.trade_impact
                    )}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Employment Impact
                  </h5>
                  <p
                    className={`text-2xl font-bold ${analysisResult.economic_impact.employment_impact < 0 ? "text-red-600" : "text-green-600"}`}
                  >
                    {formatPercentage(
                      analysisResult.economic_impact.employment_impact
                    )}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Consumer Price Impact
                  </h5>
                  <p className="text-2xl font-bold text-red-600">
                    +
                    {formatPercentage(
                      analysisResult.economic_impact.consumer_price_impact
                    )}
                  </p>
                </div>
              </div>
            </div>

            {/* Sector Analysis */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                Sector Impact Analysis
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Primary Sector
                  </h5>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPercentage(analysisResult.sector_analysis.primary)}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Secondary Sector
                  </h5>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPercentage(analysisResult.sector_analysis.secondary)}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Tertiary Sector
                  </h5>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPercentage(analysisResult.sector_analysis.tertiary)}
                  </p>
                </div>
                <div>
                  <h5 className="text-sm font-medium text-gray-500">
                    Technology Sector
                  </h5>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPercentage(
                      analysisResult.sector_analysis.technology
                    )}
                  </p>
                </div>
              </div>
            </div>

            {/* Risk Factors */}
            {analysisResult.risk_factors.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  Risk Factors
                </h4>
                <div className="space-y-2">
                  {analysisResult.risk_factors.map((factor, index) => (
                    <div key={index} className="flex items-center">
                      <svg
                        className="h-5 w-5 text-red-500 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="text-gray-700">{factor}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {analysisResult.recommendations.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  Recommendations
                </h4>
                <div className="space-y-3">
                  {analysisResult.recommendations.map(
                    (recommendation, index) => (
                      <div key={index} className="flex items-start">
                        <svg
                          className="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fillRule="evenodd"
                            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                            clipRule="evenodd"
                          />
                        </svg>
                        <span className="text-gray-700">{recommendation}</span>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TIPMInterface;
