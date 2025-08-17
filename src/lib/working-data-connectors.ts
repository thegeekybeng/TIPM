// File: src/lib/dataManager.ts

import { tryFetchWithProxies } from './utils/proxyFetch';

/** ----------- Interfaces ----------- **/

export interface USTRData {
  title: string;
  url: string;
  date: string;
  type: 'agreement' | 'policy' | 'report' | 'announcement';
  content: string;
  hasTariffInfo: boolean;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface WorldBankData {
  countryCode: string;
  countryName: string;
  indicator: string;
  value: number;
  year: number;
  unit: string;
  lastUpdated: string;
}

export interface AtlanticCouncilData {
  country: string;
  tariffRate: number;
  sectors: string[];
  effectiveDate: string;
  source: string;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  lastUpdated: string;
}

export interface WorkingDataSource {
  name: string;
  status: 'ACTIVE' | 'INACTIVE' | 'ERROR';
  lastCheck: string;
  dataQuality: 'HIGH' | 'MEDIUM' | 'LOW';
  coverage: number;
}

/** ----------- Connector Base ----------- **/

const evaluateDataQuality = (status: string) =>
  status === 'ACTIVE' ? 'HIGH' : 'LOW';

const getCurrentDate = () => new Date().toISOString().split('T')[0];

/** ----------- USTR Connector ----------- **/

export class USTRConnector {
  private baseUrl = 'https://ustr.gov';
  private lastCheck = '';
  private status: WorkingDataSource['status'] = 'INACTIVE';

  async checkStatus(): Promise<WorkingDataSource> {
    const url = `${this.baseUrl}/trade-agreements`;
    const response = await tryFetchWithProxies(url);
    this.status = response ? 'ACTIVE' : 'ERROR';
    this.lastCheck = new Date().toISOString();
    return {
      name: 'USTR (United States Trade Representative)',
      status: this.status,
      lastCheck: this.lastCheck,
      dataQuality: evaluateDataQuality(this.status),
      coverage: this.status === 'ACTIVE' ? 95 : 0,
    };
  }

  async getTradeAgreements(): Promise<USTRData[]> {
    const url = `${this.baseUrl}/trade-agreements`;
    const response = await tryFetchWithProxies(url);
    if (!response) return [];
    const html = await response.text();

    return html.includes('agreement') ? [{
      title: 'Trade Agreements Overview',
      url,
      date: getCurrentDate(),
      type: 'agreement',
      content: 'USTR trade agreements and policy info',
      hasTariffInfo: true,
      confidence: 'HIGH'
    }] : [];
  }

  async getTariffPolicy(): Promise<USTRData[]> {
    const url = `${this.baseUrl}/policy-agenda`;
    const response = await tryFetchWithProxies(url);
    if (!response) return [];
    const html = await response.text();
    return [{
      title: 'Trade Policy Agenda',
      url,
      date: getCurrentDate(),
      type: 'policy',
      content: 'USTR trade policy and tariff info',
      hasTariffInfo: html.includes('tariff'),
      confidence: 'HIGH'
    }];
  }
}

/** ----------- World Bank Connector ----------- **/

export class WorldBankConnector {
  private baseUrl = 'https://api.worldbank.org/v2';
  private lastCheck = '';
  private status: WorkingDataSource['status'] = 'INACTIVE';

  async checkStatus(): Promise<WorkingDataSource> {
    const url = `${this.baseUrl}/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1`;
    const response = await tryFetchWithProxies(url);
    this.status = response ? 'ACTIVE' : 'ERROR';
    this.lastCheck = new Date().toISOString();
    return {
      name: 'World Bank API',
      status: this.status,
      lastCheck: this.lastCheck,
      dataQuality: evaluateDataQuality(this.status),
      coverage: this.status === 'ACTIVE' ? 100 : 0,
    };
  }

  async getCountryList(): Promise<string[]> {
    const url = `${this.baseUrl}/country?format=json&per_page=300`;
    const response = await tryFetchWithProxies(url);
    if (!response) return [];
    const json = await response.json();
    return json[1]?.filter((c: any) => c.incomeLevel?.id !== 'INX').map((c: any) => c.id) || [];
  }

  private async fetchData(country: string, indicator: string, years = 5): Promise<WorldBankData[]> {
    const url = `${this.baseUrl}/country/${country}/indicator/${indicator}?format=json&per_page=${years}`;
    const response = await tryFetchWithProxies(url);
    if (!response) return [];
    const json = await response.json();

    return (json[1] || []).map((d: any) => ({
      countryCode: d.country.id,
      countryName: d.country.value,
      indicator: d.indicator.value,
      value: d.value || 0,
      year: parseInt(d.date),
      unit: d.unit || 'USD',
      lastUpdated: json[0]?.lastupdated || getCurrentDate()
    }));
  }

  getGDPData(country: string) {
    return this.fetchData(country, 'NY.GDP.MKTP.CD');
  }

  getTradeData(country: string) {
    return this.fetchData(country, 'TM.VAL.MRCH.CD.WT.ZS');
  }
}

/** ----------- Atlantic Council Connector ----------- **/

export class AtlanticCouncilConnector {
  private baseUrl = 'https://www.atlanticcouncil.org';
  private lastCheck = '';
  private status: WorkingDataSource['status'] = 'INACTIVE';

  async checkStatus(): Promise<WorkingDataSource> {
    const url = `${this.baseUrl}/programs/global-business-and-economics/trump-tariff-tracker/`;
    const response = await tryFetchWithProxies(url);
    this.status = response ? 'ACTIVE' : 'ERROR';
    this.lastCheck = new Date().toISOString();
    return {
      name: 'Atlantic Council Trump Tariff Tracker',
      status: this.status,
      lastCheck: this.lastCheck,
      dataQuality: this.status === 'ACTIVE' ? 'MEDIUM' : 'LOW',
      coverage: this.status === 'ACTIVE' ? 80 : 0,
    };
  }

  async getTariffTrackerData(): Promise<AtlanticCouncilData[]> {
    const url = `${this.baseUrl}/programs/global-business-and-economics/trump-tariff-tracker/`;
    const response = await tryFetchWithProxies(url);
    if (!response) return [];
    const html = await response.text();
    if (html.includes('tariff')) {
      console.log('Atlantic Council tariff page fetched, parsing TBD');
    }
    return []; // Placeholder
  }

  async getCountryTariffData(country: string): Promise<AtlanticCouncilData | null> {
    const list = await this.getTariffTrackerData();
    return list.find(d => d.country.toLowerCase() === country.toLowerCase()) || null;
  }
}

/** ----------- Data Aggregator ----------- **/

export class WorkingDataManager {
  private ustr = new USTRConnector();
  private wb = new WorldBankConnector();
  private ac = new AtlanticCouncilConnector();
  private lastUpdate = '';
  private sources: WorkingDataSource[] = [];

  async initialize() {
    this.sources = await Promise.all([
      this.ustr.checkStatus(),
      this.wb.checkStatus(),
      this.ac.checkStatus(),
    ]);
    this.lastUpdate = new Date().toISOString();
  }

  getDataSources() {
    return this.sources;
  }

  getActiveSources() {
    return this.sources.filter(s => s.status === 'ACTIVE');
  }

  getLastUpdate() {
    return this.lastUpdate;
  }

  getDataQuality(): 'HIGH' | 'MEDIUM' | 'LOW' {
    const active = this.getActiveSources();
    const score = active.reduce((sum, src) =>
      sum + { HIGH: 3, MEDIUM: 2, LOW: 1 }[src.dataQuality], 0) / active.length;

    return score >= 2.5 ? 'HIGH' : score >= 1.5 ? 'MEDIUM' : 'LOW';
  }

  async getCountryData(country: string) {
    try {
      const [gdp, trade, tariffs, ustrInfo] = await Promise.all([
        this.wb.getGDPData(country),
        this.wb.getTradeData(country),
        this.ac.getCountryTariffData(country),
        this.ustr.getTradeAgreements(),
      ]);
      return { gdp, trade, tariffs, ustrInfo };
    } catch (e) {
      console.error(`[❌] Failed to load data for ${country}`, e);
      return { gdp: [], trade: [], tariffs: null, ustrInfo: [] };
    }
  }

  getAvailableCountries() {
    return this.wb.getCountryList();
  }
}

export const workingDataManager = new WorkingDataManager();