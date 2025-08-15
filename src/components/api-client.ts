// TIPM API Client - Connects React frontend to FastAPI backend
// Base URL for the FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// API Response types
export interface CountryInfo {
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

export interface AnalysisResult {
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

export interface SectorAnalysis {
  sector: string;
  tariff_rate: number;
  trade_volume: number;
  impact: string;
}

export interface SectorAnalysisResponse {
  total_impact: number;
  sectors: SectorAnalysis[];
}

// API Client class
class TIPMApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // Health check
  async healthCheck(): Promise<{ status: string; real_data_available: boolean }> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  // Get available countries
  async getAvailableCountries(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/api/countries`);
    if (!response.ok) {
      throw new Error(`Failed to get countries: ${response.statusText}`);
    }
    return response.json();
  }

  // Get all countries from dataset
  async getAllCountries(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/api/dataset/countries`);
    if (!response.ok) {
      throw new Error(`Failed to fetch countries: ${response.statusText}`);
    }
    const data = await response.json();
    return data.countries || [];
  }

  // Get country information
  async getCountryInfo(countryName: string): Promise<CountryInfo> {
    const response = await fetch(`${this.baseUrl}/api/countries/${encodeURIComponent(countryName)}`);
    if (!response.ok) {
      throw new Error(`Failed to get country info: ${response.statusText}`);
    }
    return response.json();
  }

  // Analyze country tariff impact
  async analyzeCountry(countryName: string, customTariffRate?: number | null): Promise<AnalysisResult> {
    const response = await fetch(`${this.baseUrl}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        country_name: countryName,
        custom_tariff_rate: customTariffRate,
      }),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }
    return response.json();
  }

  // Get sector analysis
  async getSectorAnalysis(countryName: string, tariffRate: number = 25.0): Promise<SectorAnalysisResponse> {
    const response = await fetch(
      `${this.baseUrl}/api/sectors/${encodeURIComponent(countryName)}?tariff_rate=${tariffRate}`
    );
    if (!response.ok) {
      throw new Error(`Sector analysis failed: ${response.statusText}`);
    }
    return response.json();
  }

  // Get available sectors
  async getAvailableSectors(): Promise<{ sectors: string[] }> {
    const response = await fetch(`${this.baseUrl}/api/sectors`);
    if (!response.ok) {
      throw new Error(`Failed to get sectors: ${response.statusText}`);
    }
    return response.json();
  }

  // Test API connectivity
  async testConnectivity(): Promise<{ success: boolean; message: string }> {
    try {
      const health = await this.healthCheck();
      return {
        success: true,
        message: `API connected successfully. Real data available: ${health.real_data_available}`,
      };
    } catch (error) {
      return {
        success: false,
        message: `API connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  }
}

// Export singleton instance
export const apiClient = new TIPMApiClient();

// Types are defined in the components that use them
