/**
 * Working Tariff Impact Model for TIPM
 * Integrates USTR, World Bank, and Atlantic Council data sources
 */

import { 
  workingDataManager, 
  WorldBankData, 
  AtlanticCouncilData, 
  USTRData 
} from '../lib/working-data-connectors';

export interface CountryTariffProfile {
  countryCode: string;
  countryName: string;
  gdpData: WorldBankData[];
  tradeData: WorldBankData[];
  tariffData: AtlanticCouncilData | null;
  ustrInfo: USTRData[];
  
  // Calculated metrics
  currentGDP: number;
  gdpGrowth: number;
  tradeIntensity: number;
  tradeVolume: number;
  tariffRate: number;
  tariffImpact: 'HIGH' | 'MEDIUM' | 'LOW';
  
  // Data quality indicators
  dataConfidence: 'HIGH' | 'MEDIUM' | 'LOW';
  lastUpdated: string;
  dataSources: string[];
}

export interface TariffImpactAnalysis {
  country: CountryTariffProfile;
  
  // Economic impact calculations
  economicImpact: {
    gdpImpact: number; // Percentage change in GDP
    tradeImpact: number; // Percentage change in trade
    employmentImpact: number; // Estimated job impact
    consumerPriceImpact: number; // Price increase estimate
  };
  
  // Sector analysis
  sectorImpact: {
    primary: number;
    secondary: number;
    tertiary: number;
    technology: number;
  };
  
  // Risk assessment
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  riskFactors: string[];
  
  // Recommendations
  recommendations: string[];
}

export interface GlobalTariffOverview {
  totalCountries: number;
  countriesWithData: number;
  averageTariffRate: number;
  highImpactCountries: string[];
  mediumImpactCountries: string[];
  lowImpactCountries: string[];
  
  // Data quality summary
  dataQuality: {
    high: number;
    medium: number;
    low: number;
  };
  
  // Economic summary
  totalGDPImpact: number;
  totalTradeImpact: number;
}

export class WorkingTariffModel {
  private dataManager = workingDataManager;
  private countryProfiles: Map<string, CountryTariffProfile> = new Map();
  private lastAnalysis: string = '';

  async initialize(): Promise<void> {
    console.log('🚀 Initializing Working Tariff Model...');
    await this.dataManager.initialize();
    console.log('✅ Working Tariff Model initialized');
  }

  // Add method to expose data manager
  getDataManager() {
    return this.dataManager;
  }

  async getCountryProfile(countryCode: string): Promise<CountryTariffProfile | null> {
    try {
      // Check if we have cached data
      if (this.countryProfiles.has(countryCode)) {
        const cached = this.countryProfiles.get(countryCode)!;
        const cacheAge = Date.now() - new Date(cached.lastUpdated).getTime();
        
        // Use cache if less than 1 hour old
        if (cacheAge < 60 * 60 * 1000) {
          return cached;
        }
      }

      // Fetch fresh data
      const rawData = await this.dataManager.getCountryData(countryCode);
      
      if (!rawData.gdp.length && !rawData.trade.length) {
        return null; // No data available
      }

      // Calculate metrics
      const currentGDP = this.calculateCurrentGDP(rawData.gdp);
      const gdpGrowth = this.calculateGDPGrowth(rawData.gdp);
      const tradeIntensity = this.calculateTradeIntensity(rawData.trade);
      const tradeVolume = this.calculateTradeVolume(rawData.trade, currentGDP);
      const tariffRate = rawData.tariffs?.tariffRate || 0;
      const tariffImpact = this.calculateTariffImpact(tariffRate, tradeIntensity);
      
      // Determine data confidence
      const dataConfidence = this.assessDataConfidence(rawData);
      
      // Get data sources
      const dataSources = this.getDataSources(rawData);
      
      const profile: CountryTariffProfile = {
        countryCode,
        countryName: rawData.gdp[0]?.countryName || countryCode,
        gdpData: rawData.gdp,
        tradeData: rawData.trade,
        tariffData: rawData.tariffs,
        ustrInfo: rawData.ustrInfo,
        currentGDP,
        gdpGrowth,
        tradeIntensity,
        tradeVolume,
        tariffRate,
        tariffImpact,
        dataConfidence,
        lastUpdated: new Date().toISOString(),
        dataSources
      };

      // Cache the profile
      this.countryProfiles.set(countryCode, profile);
      
      return profile;
    } catch (error) {
      console.error(`Error getting country profile for ${countryCode}:`, error);
      return null;
    }
  }

  async analyzeCountry(countryCode: string): Promise<TariffImpactAnalysis | null> {
    try {
      const profile = await this.getCountryProfile(countryCode);
      
      if (!profile) {
        return null;
      }

      // Calculate economic impact
      const economicImpact = this.calculateEconomicImpact(profile);
      
      // Calculate sector impact
      const sectorImpact = this.calculateSectorImpact(profile);
      
      // Assess risk
      const riskLevel = this.assessRiskLevel(profile);
      const riskFactors = this.identifyRiskFactors(profile);
      
      // Generate recommendations
      const recommendations = this.generateRecommendations(profile, economicImpact);

      const analysis: TariffImpactAnalysis = {
        country: profile,
        economicImpact,
        sectorImpact,
        riskLevel,
        riskFactors,
        recommendations
      };

      this.lastAnalysis = new Date().toISOString();
      return analysis;
    } catch (error) {
      console.error(`Error analyzing country ${countryCode}:`, error);
      return null;
    }
  }

  async getGlobalOverview(): Promise<GlobalTariffOverview> {
    try {
      const countries = await this.dataManager.getAvailableCountries();
      const activeSources = await this.dataManager.getActiveSources();
      
      let totalCountries = countries.length;
      let countriesWithData = 0;
      let totalTariffRate = 0;
      let totalGDPImpact = 0;
      let totalTradeImpact = 0;
      
      const highImpactCountries: string[] = [];
      const mediumImpactCountries: string[] = [];
      const lowImpactCountries: string[] = [];
      
      const dataQualityCounts = { high: 0, medium: 0, low: 0 };

      // Sample analysis of major countries (for performance)
      const majorCountries = ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'CAN', 'BRA', 'IND'];
      
      for (const countryCode of majorCountries) {
        const profile = await this.getCountryProfile(countryCode);
        
        if (profile) {
          countriesWithData++;
          totalTariffRate += profile.tariffRate;
          
          // Categorize by impact
          if (profile.tariffImpact === 'HIGH') {
            highImpactCountries.push(profile.countryName);
          } else if (profile.tariffImpact === 'MEDIUM') {
            mediumImpactCountries.push(profile.countryName);
          } else {
            lowImpactCountries.push(profile.countryName);
          }
          
          // Count data quality
          if (profile.dataConfidence === 'HIGH') dataQualityCounts.high++;
          else if (profile.dataConfidence === 'MEDIUM') dataQualityCounts.medium++;
          else dataQualityCounts.low++;
          
          // Calculate impacts
          const analysis = await this.analyzeCountry(countryCode);
          if (analysis) {
            totalGDPImpact += analysis.economicImpact.gdpImpact;
            totalTradeImpact += analysis.economicImpact.tradeImpact;
          }
        }
      }

      const averageTariffRate = totalTariffRate / Math.max(countriesWithData, 1);

      return {
        totalCountries,
        countriesWithData,
        averageTariffRate,
        highImpactCountries,
        mediumImpactCountries,
        lowImpactCountries,
        dataQuality: dataQualityCounts,
        totalGDPImpact,
        totalTradeImpact
      };
    } catch (error) {
      console.error('Error getting global overview:', error);
      return {
        totalCountries: 0,
        countriesWithData: 0,
        averageTariffRate: 0,
        highImpactCountries: [],
        mediumImpactCountries: [],
        lowImpactCountries: [],
        dataQuality: { high: 0, medium: 0, low: 0 },
        totalGDPImpact: 0,
        totalTradeImpact: 0
      };
    }
  }

  // Private helper methods
  private calculateCurrentGDP(gdpData: WorldBankData[]): number {
    if (!gdpData.length) return 0;
    
    // Get the most recent year with data
    const sortedData = gdpData
      .filter(item => item.value > 0)
      .sort((a, b) => b.year - a.year);
    
    return sortedData[0]?.value || 0;
  }

  private calculateGDPGrowth(gdpData: WorldBankData[]): number {
    if (gdpData.length < 2) return 0;
    
    const sortedData = gdpData
      .filter(item => item.value > 0)
      .sort((a, b) => b.year - a.year);
    
    if (sortedData.length < 2) return 0;
    
    const current = sortedData[0].value;
    const previous = sortedData[1].value;
    
    if (previous === 0) return 0;
    
    return ((current - previous) / previous) * 100;
  }

  private calculateTradeIntensity(tradeData: WorldBankData[]): number {
    if (!tradeData.length) return 0;
    
    // Average trade intensity over available years
    const validValues = tradeData
      .filter(item => item.value > 0)
      .map(item => item.value);
    
    if (!validValues.length) return 0;
    
    return validValues.reduce((sum, val) => sum + val, 0) / validValues.length;
  }

  private calculateTradeVolume(tradeData: WorldBankData[], currentGDP: number): number {
    if (!tradeData.length) return 0;

    // Calculate total trade volume as a percentage of GDP
    const totalTradeValue = tradeData.reduce((sum, item) => sum + item.value, 0);
    if (currentGDP === 0) return 0;
    return (totalTradeValue / currentGDP) * 100;
  }

  private calculateTariffImpact(tariffRate: number, tradeIntensity: number): 'HIGH' | 'MEDIUM' | 'LOW' {
    if (tariffRate >= 20 || tradeIntensity >= 50) return 'HIGH';
    if (tariffRate >= 10 || tradeIntensity >= 25) return 'MEDIUM';
    return 'LOW';
  }

  private assessDataConfidence(data: any): 'HIGH' | 'MEDIUM' | 'LOW' {
    let score = 0;
    
    if (data.gdp.length > 0) score += 2;
    if (data.trade.length > 0) score += 2;
    if (data.tariffs) score += 1;
    if (data.ustrInfo.length > 0) score += 1;
    
    if (score >= 5) return 'HIGH';
    if (score >= 3) return 'MEDIUM';
    return 'LOW';
  }

  private getDataSources(data: any): string[] {
    const sources: string[] = [];
    
    if (data.gdp.length > 0) sources.push('World Bank');
    if (data.trade.length > 0) sources.push('World Bank');
    if (data.tariffs) sources.push('Atlantic Council');
    if (data.ustrInfo.length > 0) sources.push('USTR');
    
    return sources;
  }

  private calculateEconomicImpact(profile: CountryTariffProfile) {
    const { tariffRate, tradeIntensity, currentGDP } = profile;
    
    // Simplified economic impact calculations
    // In production, these would use more sophisticated economic models
    
    const gdpImpact = -(tariffRate * tradeIntensity * 0.01); // Negative impact
    const tradeImpact = -(tariffRate * 0.5); // Trade reduction
    const employmentImpact = gdpImpact * 0.3; // Employment follows GDP
    const consumerPriceImpact = tariffRate * 0.3; // Price increase
    
    return {
      gdpImpact: Math.max(gdpImpact, -50), // Cap at -50%
      tradeImpact: Math.max(tradeImpact, -30), // Cap at -30%
      employmentImpact: Math.max(employmentImpact, -15), // Cap at -15%
      consumerPriceImpact: Math.min(consumerPriceImpact, 20) // Cap at 20%
    };
  }

  private calculateSectorImpact(profile: CountryTariffProfile) {
    const { tariffRate, tariffData } = profile;
    
    // Base sector impacts based on tariff rate
    const baseImpact = tariffRate * 0.01;
    
    return {
      primary: baseImpact * 0.8, // Agriculture, mining
      secondary: baseImpact * 1.2, // Manufacturing
      tertiary: baseImpact * 0.6, // Services
      technology: baseImpact * 1.5 // High-tech sectors
    };
  }

  private assessRiskLevel(profile: CountryTariffProfile): 'LOW' | 'MEDIUM' | 'HIGH' {
    const { tariffRate, tradeIntensity, dataConfidence } = profile;
    
    let riskScore = 0;
    
    if (tariffRate >= 25) riskScore += 3;
    else if (tariffRate >= 15) riskScore += 2;
    else if (tariffRate >= 5) riskScore += 1;
    
    if (tradeIntensity >= 50) riskScore += 3;
    else if (tradeIntensity >= 25) riskScore += 2;
    else if (tradeIntensity >= 10) riskScore += 1;
    
    if (dataConfidence === 'LOW') riskScore += 2;
    else if (dataConfidence === 'MEDIUM') riskScore += 1;
    
    if (riskScore >= 6) return 'HIGH';
    if (riskScore >= 3) return 'MEDIUM';
    return 'LOW';
  }

  private identifyRiskFactors(profile: CountryTariffProfile): string[] {
    const factors: string[] = [];
    const { tariffRate, tradeIntensity, dataConfidence } = profile;
    
    if (tariffRate >= 25) factors.push('Very high tariff rates');
    if (tariffRate >= 15) factors.push('High tariff rates');
    if (tradeIntensity >= 50) factors.push('High trade dependency');
    if (tradeIntensity >= 25) factors.push('Moderate trade dependency');
    if (dataConfidence === 'LOW') factors.push('Low data confidence');
    if (dataConfidence === 'MEDIUM') factors.push('Medium data confidence');
    
    return factors;
  }

  private generateRecommendations(profile: CountryTariffProfile, economicImpact: any): string[] {
    const recommendations: string[] = [];
    const { tariffRate, tradeIntensity } = profile;
    
    if (tariffRate >= 20) {
      recommendations.push('Consider diversifying trade partners to reduce tariff exposure');
      recommendations.push('Evaluate supply chain alternatives in lower-tariff regions');
    }
    
    if (tradeIntensity >= 40) {
      recommendations.push('High trade dependency increases vulnerability to tariff changes');
      recommendations.push('Consider domestic production alternatives for critical goods');
    }
    
    if (economicImpact.gdpImpact < -10) {
      recommendations.push('Significant GDP impact expected - monitor economic indicators closely');
      recommendations.push('Consider policy responses to mitigate economic damage');
    }
    
    if (economicImpact.employmentImpact < -5) {
      recommendations.push('Employment impact expected - prepare workforce transition programs');
      recommendations.push('Monitor sector-specific employment trends');
    }
    
    if (recommendations.length === 0) {
      recommendations.push('Current tariff levels appear manageable for this economy');
      recommendations.push('Continue monitoring for policy changes');
    }
    
    return recommendations;
  }

  getLastAnalysis(): string {
    return this.lastAnalysis;
  }

  getDataQuality(): 'HIGH' | 'MEDIUM' | 'LOW' {
    return this.dataManager.getDataQuality();
  }

  async refreshData(): Promise<void> {
    console.log('🔄 Refreshing tariff model data...');
    this.countryProfiles.clear();
    await this.dataManager.initialize();
    console.log('✅ Tariff model data refreshed');
  }
}

// Export singleton instance
export const workingTariffModel = new WorkingTariffModel();
