'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Globe, 
  TrendingUp, 
  BarChart3, 
  Download, 
  Settings, 
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Users,
  Factory,
  ShoppingCart
} from 'lucide-react';

interface CountryData {
  name: string;
  tariff_rate: number;
  continent: string;
  global_groups: string[];
  emerging_market: boolean;
  gdp_billions: number;
  trade_volume_millions: number;
}

interface AnalysisResult {
  country_name: string;
  tariff_rate: number;
  overall_confidence: number;
  economic_impact: {
    trade_disruption_usd: number;
    price_increase_pct: number;
    employment_effect_jobs: number;
    gdp_impact_pct: number;
    industry_severity: string;
  };
  layer_confidences: Record<string, number>;
  timestamp: string;
}

const TIPMInterface: React.FC = () => {
  const [selectedCountry, setSelectedCountry] = useState<string>('');
  const [selectedProducts, setSelectedProducts] = useState<string[]>([]);
  const [customTariff, setCustomTariff] = useState<number | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sortMethod, setSortMethod] = useState<string>('tariff_rate');

  const productCategories = [
    'Agriculture & Food Products',
    'Automotive & Transportation',
    'Chemicals & Pharmaceuticals',
    'Electronics & Technology',
    'Energy & Petroleum',
    'Machinery & Industrial Equipment',
    'Metals & Mining Products',
    'Textiles & Apparel',
    'Wood & Paper Products',
    'Consumer Goods & Retail'
  ];

  const sortOptions = [
    { value: 'tariff_rate', label: 'By Tariff Rate', icon: TrendingUp },
    { value: 'continent', label: 'By Continent', icon: Globe },
    { value: 'gdp', label: 'By GDP', icon: DollarSign },
    { value: 'alphabetical', label: 'Alphabetical', icon: BarChart3 }
  ];

  const handleAnalysis = async () => {
    if (!selectedCountry) return;
    
    setIsLoading(true);
    
    try {
      // Simulate API call - replace with actual backend integration
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockResult: AnalysisResult = {
        country_name: selectedCountry,
        tariff_rate: customTariff || 25,
        overall_confidence: 87.5,
        economic_impact: {
          trade_disruption_usd: 1500000000,
          price_increase_pct: 7.5,
          employment_effect_jobs: 12500,
          gdp_impact_pct: 0.8,
          industry_severity: 'Medium'
        },
        layer_confidences: {
          'policy_trigger': 92,
          'trade_flow': 88,
          'industry_response': 85,
          'firm_impact': 82,
          'consumer_impact': 86,
          'geopolitical': 78
        },
        timestamp: new Date().toISOString()
      };
      
      setAnalysisResult(mockResult);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 85) return 'text-success-600 bg-success-50';
    if (confidence >= 75) return 'text-warning-600 bg-warning-50';
    return 'text-danger-600 bg-danger-50';
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 85) return <CheckCircle className="w-4 h-4" />;
    if (confidence >= 75) return <Clock className="w-4 h-4" />;
    return <AlertTriangle className="w-4 h-4" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            TIPM v1.5 - Tariff Impact Propagation Model
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Advanced AI system for predicting and analyzing the economic impact of tariffs 
            on global markets, supply chains, and populations
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Control Panel */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-1"
          >
            <div className="bg-white rounded-2xl shadow-soft p-6 sticky top-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-6 flex items-center gap-2">
                <Settings className="w-6 h-6 text-primary-600" />
                Analysis Parameters
              </h2>

              {/* Sort Method */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-3">
                  Sort Countries By
                </label>
                <div className="space-y-2">
                  {sortOptions.map((option) => {
                    const Icon = option.icon;
                    return (
                      <button
                        key={option.value}
                        onClick={() => setSortMethod(option.value)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg border transition-all ${
                          sortMethod === option.value
                            ? 'border-primary-500 bg-primary-50 text-primary-700'
                            : 'border-slate-200 hover:border-slate-300 text-slate-700'
                        }`}
                      >
                        <Icon className="w-5 h-5" />
                        {option.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Country Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-3">
                  Select Target Country
                </label>
                <select
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="">Choose a country...</option>
                  <option value="China">China</option>
                  <option value="European Union">European Union</option>
                  <option value="Japan">Japan</option>
                  <option value="South Korea">South Korea</option>
                  <option value="Mexico">Mexico</option>
                  <option value="Canada">Canada</option>
                </select>
              </div>

              {/* Product Categories */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-3">
                  Product Categories
                </label>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {productCategories.map((product) => (
                    <label key={product} className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedProducts.includes(product)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedProducts([...selectedProducts, product]);
                          } else {
                            setSelectedProducts(selectedProducts.filter(p => p !== product));
                          }
                        }}
                        className="w-4 h-4 text-primary-600 border-slate-300 rounded focus:ring-primary-500"
                      />
                      <span className="text-sm text-slate-700">{product}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Custom Tariff Rate */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-3">
                  Custom Tariff Rate (Optional)
                </label>
                <input
                  type="number"
                  placeholder="Enter percentage (e.g., 25)"
                  value={customTariff || ''}
                  onChange={(e) => setCustomTariff(e.target.value ? Number(e.target.value) : null)}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  min="0"
                  max="200"
                />
                <p className="text-xs text-slate-500 mt-1">
                  Override default rate for scenario testing
                </p>
              </div>

              {/* Run Analysis Button */}
              <button
                onClick={handleAnalysis}
                disabled={!selectedCountry || isLoading}
                className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-slate-300 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Running Analysis...
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-5 h-5" />
                    Run TIPM Analysis
                  </>
                )}
              </button>
            </div>
          </motion.div>

          {/* Results Panel */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-2"
          >
            {!analysisResult ? (
              <div className="bg-white rounded-2xl shadow-soft p-12 text-center">
                <Globe className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-slate-600 mb-2">
                  Ready for Analysis
                </h3>
                <p className="text-slate-500">
                  Select a country and product categories, then run the analysis to see results
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Summary Card */}
                <div className="bg-white rounded-2xl shadow-soft p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-semibold text-slate-900">
                      Analysis Results for {analysisResult.country_name}
                    </h2>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-slate-500">Overall Confidence:</span>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getConfidenceColor(analysisResult.overall_confidence)}`}>
                        {analysisResult.overall_confidence.toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <DollarSign className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">Trade Disruption</span>
                      </div>
                      <p className="text-2xl font-bold text-slate-900">
                        ${(analysisResult.economic_impact.trade_disruption_usd / 1000000000).toFixed(2)}B
                      </p>
                    </div>

                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <ShoppingCart className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">Price Increase</span>
                      </div>
                      <p className="text-2xl font-bold text-slate-900">
                        {analysisResult.economic_impact.price_increase_pct.toFixed(1)}%
                      </p>
                    </div>

                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Users className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">Jobs Affected</span>
                      </div>
                      <p className="text-2xl font-bold text-slate-900">
                        {analysisResult.economic_impact.employment_effect_jobs.toLocaleString()}
                      </p>
                    </div>

                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Factory className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">Industry Severity</span>
                      </div>
                      <p className="text-2xl font-bold text-slate-900">
                        {analysisResult.economic_impact.industry_severity}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-slate-500">
                    <span>Analysis completed at {new Date(analysisResult.timestamp).toLocaleString()}</span>
                    <button className="flex items-center gap-2 text-primary-600 hover:text-primary-700">
                      <Download className="w-4 h-4" />
                      Export Results
                    </button>
                  </div>
                </div>

                {/* Layer Confidence */}
                <div className="bg-white rounded-2xl shadow-soft p-6">
                  <h3 className="text-xl font-semibold text-slate-900 mb-4">
                    AI Layer Confidence Scores
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(analysisResult.layer_confidences).map(([layer, confidence]) => (
                      <div key={layer} className="bg-slate-50 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-slate-700 capitalize">
                            {layer.replace('_', ' ')}
                          </span>
                          {getConfidenceIcon(confidence)}
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-300 ${
                              confidence >= 85 ? 'bg-success-500' : 
                              confidence >= 75 ? 'bg-warning-500' : 'bg-danger-500'
                            }`}
                            style={{ width: `${confidence}%` }}
                          />
                        </div>
                        <span className={`text-sm font-semibold ${getConfidenceColor(confidence)}`}>
                          {confidence.toFixed(1)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default TIPMInterface;
