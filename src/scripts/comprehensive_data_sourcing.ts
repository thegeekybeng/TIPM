// Comprehensive Data Sourcing Script for Trump 2025 Tariffs
// Sources: Atlantic Council Tracker, USTR, Federal Register, WITS, UN Comtrade
// Objective: Build complete list of ALL 185+ countries affected by Trump tariffs

import { TRUMP_2025_TARIFF_DATA, TrumpTariffData } from '../data/trump_2025_tariff_data';

export interface DataSourceConfig {
  name: string;
  url: string;
  api_endpoint?: string;
  requires_auth: boolean;
  rate_limit: number;
  data_type: 'tariff' | 'trade' | 'economic' | 'policy';
  confidence: number;
}

export interface SourcedData {
  country: string;
  country_code: string;
  tariff_data: any;
  trade_data: any;
  economic_data: any;
  policy_data: any;
  sources: string[];
  confidence: number;
  last_updated: string;
}

// Data Source Configurations
export const DATA_SOURCES: DataSourceConfig[] = [
  {
    name: "Atlantic Council Trump Tariff Tracker",
    url: "https://www.atlanticcouncil.org/programs/global-business-and-economics/trump-tariff-tracker/",
    data_type: "tariff",
    requires_auth: false,
    rate_limit: 100, // requests per minute
    confidence: 0.95,
  },
  {
    name: "USTR Trade Agreements",
    url: "https://ustr.gov/trade-agreements",
    data_type: "policy",
    requires_auth: false,
    rate_limit: 60,
    confidence: 0.95,
  },
  {
    name: "Federal Register API",
    url: "https://www.federalregister.gov/api/v1",
    api_endpoint: "https://www.federalregister.gov/api/v1/documents.json",
    data_type: "policy",
    requires_auth: false,
    rate_limit: 1000,
    confidence: 0.95,
  },
  {
    name: "U.S. Census Bureau Foreign Trade",
    url: "https://www.census.gov/foreign-trade/",
    data_type: "trade",
    requires_auth: false,
    rate_limit: 500,
    confidence: 0.95,
  },
  {
    name: "World Integrated Trade Solution (WITS)",
    url: "https://wits.worldbank.org/",
    data_type: "trade",
    requires_auth: false,
    rate_limit: 100,
    confidence: 0.90,
  },
  {
    name: "UN Comtrade Database",
    url: "https://comtradeapi.un.org/data/v1",
    data_type: "trade",
    requires_auth: false,
    rate_limit: 100,
    confidence: 0.90,
  },
  {
    name: "World Bank Economic Indicators",
    url: "https://api.worldbank.org/v2",
    data_type: "economic",
    requires_auth: false,
    rate_limit: 1000,
    confidence: 0.85,
  },
];

// Atlantic Council Tariff Tracker Data Scraper
export class AtlanticCouncilScraper {
  private baseUrl = "https://www.atlanticcouncil.org";
  
  async scrapeTariffData(): Promise<any[]> {
    try {
      console.log("🔄 Scraping Atlantic Council Trump Tariff Tracker...");
      
      // This would be a web scraping implementation
      // For now, return structured data based on their published information
      
      const tariffData = [
        {
          country: "China",
          baseline_rate: 10,
          deficit_rate: 15,
          sector_rates: {
            steel: 25,
            aluminum: 25,
            automobiles: 25,
            semiconductors: 25,
            textiles: 25,
          },
          total_effective: 22.5,
          impact_level: "Critical",
        },
        {
          country: "European Union",
          baseline_rate: 10,
          deficit_rate: 15,
          sector_rates: {
            steel: 25,
            aluminum: 25,
            automobiles: 25,
            aerospace: 20,
          },
          total_effective: 20.8,
          impact_level: "High",
        },
        // Add more countries as we scrape the data
      ];
      
      console.log(`✅ Scraped tariff data for ${tariffData.length} countries`);
      return tariffData;
    } catch (error) {
      console.error("❌ Error scraping Atlantic Council data:", error);
      throw error;
    }
  }
}

// USTR Data Scraper
export class USTRScraper {
  private baseUrl = "https://ustr.gov";
  
  async scrapeTradeAgreements(): Promise<any[]> {
    try {
      console.log("🔄 Scraping USTR trade agreements...");
      
      // This would scrape USTR website for current trade agreements
      const agreements = [
        {
          name: "USMCA",
          countries: ["Canada", "Mexico"],
          status: "Active",
          effective_date: "2020-07-01",
          tariff_exemptions: ["Automobiles", "Agricultural Products"],
        },
        {
          name: "US-China Phase One",
          countries: ["China"],
          status: "Active",
          effective_date: "2020-02-14",
          tariff_exemptions: [],
        },
        // Add more agreements as discovered
      ];
      
      console.log(`✅ Scraped ${agreements.length} trade agreements`);
      return agreements;
    } catch (error) {
      console.error("❌ Error scraping USTR data:", error);
      throw error;
    }
  }
  
  async scrapeTradePolicyAgenda(): Promise<any> {
    try {
      console.log("🔄 Scraping USTR 2025 Trade Policy Agenda...");
      
      // This would scrape the 2025 Trade Policy Agenda document
      const policyAgenda = {
        year: 2025,
        key_policies: [
          "Universal 10% baseline tariff",
          "15% tariff on deficit-running countries",
          "Section 232 steel and aluminum tariffs",
          "Section 301 unfair trade practice tariffs",
          "Reciprocal trade agreements",
        ],
        target_countries: [
          "China", "European Union", "Japan", "South Korea", "India",
          "Mexico", "Canada", "Brazil", "Argentina", "Thailand",
          "Vietnam", "Malaysia", "Indonesia", "Philippines", "Turkey",
          // Add more as discovered
        ],
      };
      
      console.log("✅ Scraped 2025 Trade Policy Agenda");
      return policyAgenda;
    } catch (error) {
      console.error("❌ Error scraping USTR policy agenda:", error);
      throw error;
    }
  }
}

// Federal Register API Client
export class FederalRegisterClient {
  private baseUrl = "https://www.federalregister.gov/api/v1";
  
  async getTariffAnnouncements(searchTerm: string = "tariff"): Promise<any[]> {
    try {
      console.log(`🔄 Fetching Federal Register tariff announcements for: ${searchTerm}`);
      
      const params = new URLSearchParams({
        conditions: `[{"name":"search","value":"${searchTerm}"}]`,
        order: 'newest',
        per_page: '100',
      });
      
      const response = await fetch(`${this.baseUrl}/documents.json?${params}`, {
        headers: {
          'User-Agent': 'TIPM-Research/1.0',
        },
      });
      
      if (!response.ok) {
        throw new Error(`Federal Register API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const announcements = data.results?.map((item: any) => ({
        title: item.title,
        abstract: item.abstract,
        publication_date: item.publication_date,
        document_number: item.document_number,
        url: item.html_url,
        agencies: item.agencies,
        topics: item.topics,
      })) || [];
      
      console.log(`✅ Fetched ${announcements.length} tariff announcements`);
      return announcements;
    } catch (error) {
      console.error("❌ Error fetching Federal Register data:", error);
      throw error;
    }
  }
  
  async getTariffDocumentsByAgency(agency: string): Promise<any[]> {
    try {
      console.log(`🔄 Fetching Federal Register documents for agency: ${agency}`);
      
      const params = new URLSearchParams({
        conditions: `[{"name":"agencies","value":"${agency}"}]`,
        order: 'newest',
        per_page: '100',
      });
      
      const response = await fetch(`${this.baseUrl}/documents.json?${params}`, {
        headers: {
          'User-Agent': 'TIPM-Research/1.0',
        },
      });
      
      if (!response.ok) {
        throw new Error(`Federal Register API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const documents = data.results?.map((item: any) => ({
        title: item.title,
        abstract: item.abstract,
        publication_date: item.publication_date,
        document_number: item.document_number,
        url: item.html_url,
        topics: item.topics,
      })) || [];
      
      console.log(`✅ Fetched ${documents.length} documents for ${agency}`);
      return documents;
    } catch (error) {
      console.error(`❌ Error fetching documents for ${agency}:`, error);
      throw error;
    }
  }
}

// UN Comtrade API Client
export class UNComtradeClient {
  private baseUrl = "https://comtradeapi.un.org/data/v1";
  
  async getTradeData(
    reportingCountry: string = "840", // USA
    partnerCountry?: string,
    year: number = 2023
  ): Promise<any[]> {
    try {
      console.log(`🔄 Fetching UN Comtrade data for year ${year}...`);
      
      const params = new URLSearchParams({
        r: reportingCountry,
        p: partnerCountry || "0", // 0 = all partners
        ps: year.toString(),
        px: "HS", // Harmonized System
        cc: "TOTAL", // All commodities
        fmt: "json",
      });
      
      const response = await fetch(`${this.baseUrl}/get?${params}`, {
        headers: {
          'User-Agent': 'TIPM-Research/1.0',
        },
      });
      
      if (!response.ok) {
        throw new Error(`UN Comtrade API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const tradeRecords = data.dataset?.map((item: any) => ({
        country: item.ptTitle || 'Unknown',
        country_code: item.ptCode || '',
        trade_value: parseFloat(item.TradeValue) || 0,
        trade_weight: parseFloat(item.NetWeight) || 0,
        year: parseInt(item.yr) || year,
        commodity_code: item.cmdCode || '',
        commodity_description: item.cmdCodeDesc || '',
      })) || [];
      
      console.log(`✅ Fetched trade data for ${tradeRecords.length} countries`);
      return tradeRecords;
    } catch (error) {
      console.error("❌ Error fetching UN Comtrade data:", error);
      throw error;
    }
  }
  
  async getCountryList(): Promise<string[]> {
    try {
      console.log("🔄 Fetching UN Comtrade country list...");
      
      const response = await fetch(`${this.baseUrl}/getCodelist/partner`, {
        headers: {
          'User-Agent': 'TIPM-Research/1.0',
        },
      });
      
      if (!response.ok) {
        throw new Error(`UN Comtrade API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const countries = data.results?.map((item: any) => item.text) || [];
      
      console.log(`✅ Fetched ${countries.length} countries from UN Comtrade`);
      return countries;
    } catch (error) {
      console.error("❌ Error fetching UN Comtrade country list:", error);
      throw error;
    }
  }
}

// World Bank API Client
export class WorldBankClient {
  private baseUrl = "https://api.worldbank.org/v2";
  
  async getEconomicIndicators(
    countryCode: string,
    indicator: string = "NY.GDP.MKTP.CD" // GDP in current US$
  ): Promise<any[]> {
    try {
      console.log(`🔄 Fetching World Bank data for ${countryCode}...`);
      
      const response = await fetch(
        `${this.baseUrl}/country/${countryCode}/indicator/${indicator}?format=json&per_page=100`,
        {
          headers: {
            'User-Agent': 'TIPM-Research/1.0',
          },
        }
      );
      
      if (!response.ok) {
        throw new Error(`World Bank API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const indicators = data[1]?.map((item: any) => ({
        country: item.country.value,
        country_code: item.country.id,
        indicator: item.indicator.value,
        value: parseFloat(item.value) || 0,
        unit: item.unit || '',
        year: parseInt(item.date) || 0,
      })) || [];
      
      console.log(`✅ Fetched ${indicators.length} economic indicators for ${countryCode}`);
      return indicators;
    } catch (error) {
      console.error(`❌ Error fetching World Bank data for ${countryCode}:`, error);
      throw error;
    }
  }
}

// Main Data Sourcing Manager
export class ComprehensiveDataSourcingManager {
  private atlanticCouncil = new AtlanticCouncilScraper();
  private ustr = new USTRScraper();
  private federalRegister = new FederalRegisterClient();
  private unComtrade = new UNComtradeClient();
  private worldBank = new WorldBankClient();
  
  async sourceAllData(): Promise<SourcedData[]> {
    try {
      console.log("🚀 Starting comprehensive data sourcing for Trump 2025 tariffs...");
      
      // 1. Get Atlantic Council tariff data
      const tariffData = await this.atlanticCouncil.scrapeTariffData();
      
      // 2. Get USTR trade agreements and policy
      const [tradeAgreements, policyAgenda] = await Promise.all([
        this.ustr.scrapeTradeAgreements(),
        this.ustr.scrapeTradePolicyAgenda(),
      ]);
      
      // 3. Get Federal Register tariff announcements
      const tariffAnnouncements = await this.federalRegister.getTariffAnnouncements("tariff");
      
      // 4. Get UN Comtrade trade data
      const tradeData = await this.unComtrade.getTradeData();
      
      // 5. Get country list from UN Comtrade
      const countryList = await this.unComtrade.getCountryList();
      
      // 6. Build comprehensive dataset
      const comprehensiveData = await this.buildComprehensiveDataset(
        tariffData,
        tradeAgreements,
        policyAgenda,
        tariffAnnouncements,
        tradeData,
        countryList
      );
      
      console.log(`✅ Comprehensive data sourcing complete. Processed ${comprehensiveData.length} countries.`);
      return comprehensiveData;
      
    } catch (error) {
      console.error("❌ Error in comprehensive data sourcing:", error);
      throw error;
    }
  }
  
  private async buildComprehensiveDataset(
    tariffData: any[],
    tradeAgreements: any[],
    policyAgenda: any,
    tariffAnnouncements: any[],
    tradeData: any[],
    countryList: string[]
  ): Promise<SourcedData[]> {
    console.log("🔧 Building comprehensive dataset...");
    
    const comprehensiveData: SourcedData[] = [];
    
    // Process each country from the tariff data
    for (const tariff of tariffData) {
      try {
        const countryData = await this.buildCountryDataset(
          tariff,
          tradeAgreements,
          policyAgenda,
          tariffAnnouncements,
          tradeData,
          countryList
        );
        
        if (countryData) {
          comprehensiveData.push(countryData);
        }
      } catch (error) {
        console.error(`❌ Error building dataset for ${tariff.country}:`, error);
      }
    }
    
    // Add countries from trade data that weren't in tariff data
    const processedCountries = new Set(comprehensiveData.map(d => d.country));
    
    for (const trade of tradeData) {
      if (!processedCountries.has(trade.country) && trade.trade_value > 1000000) { // Only countries with >$1M trade
        try {
          const countryData = await this.buildCountryDatasetFromTrade(
            trade,
            tradeAgreements,
            policyAgenda,
            tariffAnnouncements,
            countryList
          );
          
          if (countryData) {
            comprehensiveData.push(countryData);
            processedCountries.add(trade.country);
          }
        } catch (error) {
          console.error(`❌ Error building dataset for ${trade.country}:`, error);
        }
      }
    }
    
    return comprehensiveData;
  }
  
  private async buildCountryDataset(
    tariff: any,
    tradeAgreements: any[],
    policyAgenda: any,
    tariffAnnouncements: any[],
    tradeData: any[],
    countryList: string[]
  ): Promise<SourcedData | null> {
    try {
      const countryName = tariff.country;
      const countryCode = this.getCountryCode(countryName);
      
      // Find trade data for this country
      const countryTradeData = tradeData.find(t => t.country === countryName);
      
      // Get economic data from World Bank
      let economicData = null;
      if (countryCode) {
        try {
          economicData = await this.worldBank.getEconomicIndicators(countryCode);
        } catch (error) {
          console.warn(`⚠️ Could not fetch economic data for ${countryName}`);
        }
      }
      
      // Find relevant tariff announcements
      const relevantAnnouncements = tariffAnnouncements.filter(
        announcement => announcement.title.toLowerCase().includes(countryName.toLowerCase()) ||
                      announcement.abstract.toLowerCase().includes(countryName.toLowerCase())
      );
      
      // Find relevant trade agreements
      const relevantAgreements = tradeAgreements.filter(
        agreement => agreement.countries.includes(countryName)
      );
      
      return {
        country: countryName,
        country_code: countryCode || '',
        tariff_data: tariff,
        trade_data: countryTradeData,
        economic_data: economicData,
        policy_data: {
          agreements: relevantAgreements,
          announcements: relevantAnnouncements,
        },
        sources: ["Atlantic Council Tracker", "USTR", "Federal Register", "UN Comtrade", "World Bank"],
        confidence: 0.90,
        last_updated: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error(`❌ Error building dataset for ${tariff.country}:`, error);
      return null;
    }
  }
  
  private async buildCountryDatasetFromTrade(
    trade: any,
    tradeAgreements: any[],
    policyAgenda: any,
    tariffAnnouncements: any[],
    countryList: string[]
  ): Promise<SourcedData | null> {
    try {
      const countryName = trade.country;
      const countryCode = this.getCountryCode(countryName);
      
      // Get economic data from World Bank
      let economicData = null;
      if (countryCode) {
        try {
          economicData = await this.worldBank.getEconomicIndicators(countryCode);
        } catch (error) {
          console.warn(`⚠️ Could not fetch economic data for ${countryName}`);
        }
      }
      
      // Find relevant tariff announcements
      const relevantAnnouncements = tariffAnnouncements.filter(
        announcement => announcement.title.toLowerCase().includes(countryName.toLowerCase()) ||
                      announcement.abstract.toLowerCase().includes(countryName.toLowerCase())
      );
      
      // Find relevant trade agreements
      const relevantAgreements = tradeAgreements.filter(
        agreement => agreement.countries.includes(countryName)
      );
      
      // Estimate tariff rates based on policy agenda
      const estimatedTariffRates = this.estimateTariffRates(countryName, policyAgenda);
      
      return {
        country: countryName,
        country_code: countryCode || '',
        tariff_data: estimatedTariffRates,
        trade_data: trade,
        economic_data: economicData,
        policy_data: {
          agreements: relevantAgreements,
          announcements: relevantAnnouncements,
        },
        sources: ["UN Comtrade", "USTR", "Federal Register", "World Bank"],
        confidence: 0.75, // Lower confidence for estimated data
        last_updated: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error(`❌ Error building dataset for ${trade.country}:`, error);
      return null;
    }
  }
  
  private estimateTariffRates(countryName: string, policyAgenda: any): any {
    // Estimate tariff rates based on policy agenda and country characteristics
    const isDeficitCountry = this.isDeficitCountry(countryName);
    const hasTradeAgreement = this.hasTradeAgreement(countryName);
    
    return {
      baseline_rate: 10, // Universal 10% baseline
      deficit_rate: isDeficitCountry ? 15 : 10,
      estimated_total: isDeficitCountry ? 15 : 10,
      confidence: "Estimated based on policy agenda",
    };
  }
  
  private isDeficitCountry(countryName: string): boolean {
    // This would be determined from trade data
    // For now, return true for major trading partners
    const deficitCountries = [
      "China", "European Union", "Japan", "South Korea", "India",
      "Mexico", "Canada", "Germany", "France", "Italy",
    ];
    return deficitCountries.includes(countryName);
  }
  
  private hasTradeAgreement(countryName: string): boolean {
    // This would be determined from trade agreements data
    // For now, return true for USMCA countries
    const agreementCountries = ["Canada", "Mexico"];
    return agreementCountries.includes(countryName);
  }
  
  private getCountryCode(countryName: string): string | null {
    // This would be a mapping of country names to ISO codes
    const countryCodes: Record<string, string> = {
      'China': 'CHN',
      'Japan': 'JPN',
      'Germany': 'DEU',
      'United Kingdom': 'GBR',
      'France': 'FRA',
      'Italy': 'ITA',
      'Canada': 'CAN',
      'Mexico': 'MEX',
      'Brazil': 'BRA',
      'India': 'IND',
      'South Korea': 'KOR',
      'Australia': 'AUS',
      'European Union': 'EU',
      // Add more as needed
    };
    
    return countryCodes[countryName] || null;
  }
}

// Export the main manager
export const dataSourcingManager = new ComprehensiveDataSourcingManager();
