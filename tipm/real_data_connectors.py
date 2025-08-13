"""
Real Data Connectors for TIPM
Connects to authoritative sources for tariff and trade data
"""

import requests
import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class TariffData:
    """Real tariff data from authoritative sources"""
    country: str
    sector: str
    tariff_rate: float
    hts_code: str
    effective_date: str
    source: str
    confidence: float

@dataclass
class TradeData:
    """Real trade data from authoritative sources"""
    country: str
    sector: str
    trade_volume_usd: float
    trade_balance: float
    year: int
    source: str

class USITCConnector:
    """Connects to U.S. International Trade Commission API"""
    
    BASE_URL = "https://data.usitc.gov/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TIPM-Research/1.0'
        })
    
    def get_tariff_rates(self, country: str, sector: str = None) -> List[TariffData]:
        """Get real tariff rates from USITC"""
        try:
            # USITC Tariff Database API endpoint
            url = f"{self.BASE_URL}/tariff_rates"
            params = {
                'country': country,
                'sector': sector,
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            tariff_data = []
            
            for item in data.get('results', []):
                tariff_data.append(TariffData(
                    country=item.get('country', country),
                    sector=item.get('sector', sector or 'General'),
                    tariff_rate=float(item.get('tariff_rate', 0)),
                    hts_code=item.get('hts_code', ''),
                    effective_date=item.get('effective_date', ''),
                    source='USITC',
                    confidence=0.95
                ))
            
            logger.info(f"Retrieved {len(tariff_data)} tariff records from USITC for {country}")
            return tariff_data
            
        except Exception as e:
            logger.error(f"USITC API error for {country}: {e}")
            return []

class UNComtradeConnector:
    """Connects to UN Comtrade Database"""
    
    BASE_URL = "https://comtradeapi.un.org/data/v1"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TIPM-Research/1.0'
        })
    
    def get_trade_data(self, country: str, sector: str = None, year: int = 2023) -> List[TradeData]:
        """Get real trade data from UN Comtrade"""
        try:
            # UN Comtrade API endpoint
            url = f"{self.BASE_URL}/get"
            params = {
                'r': self._get_country_code(country),
                'p': 840,  # USA
                'cc': self._get_sector_code(sector) if sector else 'TOTAL',
                'freq': 'A',
                'fmt': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            trade_data = []
            
            for item in data.get('dataset', []):
                trade_data.append(TradeData(
                    country=country,
                    sector=sector or 'Total',
                    trade_volume_usd=float(item.get('TradeValue', 0)),
                    trade_balance=float(item.get('NetWeight', 0)),
                    year=year,
                    source='UN Comtrade'
                ))
            
            logger.info(f"Retrieved {len(trade_data)} trade records from UN Comtrade for {country}")
            return trade_data
            
        except Exception as e:
            logger.error(f"UN Comtrade API error for {country}: {e}")
            return []
    
    def _get_country_code(self, country: str) -> str:
        """Convert country name to UN Comtrade country code"""
        country_codes = {
            'China': '156', 'Germany': '276', 'Japan': '392',
            'Canada': '124', 'Mexico': '484', 'United Kingdom': '826',
            'France': '250', 'Italy': '380', 'South Korea': '410',
            'India': '356', 'Brazil': '076', 'Australia': '036'
        }
        return country_codes.get(country, '000')
    
    def _get_sector_code(self, sector: str) -> str:
        """Convert sector name to UN Comtrade sector code"""
        sector_codes = {
            'Semiconductors': '8542', 'Steel': '72', 'Automotive': '87',
            'Textiles': '50-63', 'Electronics': '85', 'Machinery': '84'
        }
        return sector_codes.get(sector, 'TOTAL')

class WTOConnector:
    """Connects to World Trade Organization Tariff Database"""
    
    BASE_URL = "https://tariffdata.wto.org/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TIPM-Research/1.0'
        })
    
    def get_global_tariffs(self, country: str) -> List[TariffData]:
        """Get global tariff schedules from WTO"""
        try:
            url = f"{self.BASE_URL}/tariffs"
            params = {
                'reporter': country,
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            tariff_data = []
            
            for item in data.get('tariffs', []):
                tariff_data.append(TariffData(
                    country=country,
                    sector=item.get('sector', 'General'),
                    tariff_rate=float(item.get('rate', 0)),
                    hts_code=item.get('code', ''),
                    effective_date=item.get('date', ''),
                    source='WTO',
                    confidence=0.90
                ))
            
            logger.info(f"Retrieved {len(tariff_data)} tariff records from WTO for {country}")
            return tariff_data
            
        except Exception as e:
            logger.error(f"WTO API error for {country}: {e}")
            return []

class WorldBankConnector:
    """Connects to World Bank Economic Indicators"""
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TIPM-Research/1.0'
        })
    
    def get_economic_indicators(self, country: str) -> Dict[str, Any]:
        """Get economic indicators from World Bank"""
        try:
            indicators = {
                'GDP': 'NY.GDP.MKTP.CD',  # GDP (current US$)
                'Trade': 'NE.TRD.GNFS.ZS',  # Trade (% of GDP)
                'Exports': 'NE.EXP.GNFS.CD',  # Exports of goods and services (current US$)
                'Imports': 'NE.IMP.GNFS.CD'   # Imports of goods and services (current US$)
            }
            
            data = {}
            for name, code in indicators.items():
                url = f"{self.BASE_URL}/country/{self._get_country_code(country)}/indicator/{code}"
                params = {'format': 'json', 'per_page': 1}
                
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                if len(result) > 1 and result[1]:
                    data[name] = result[1][0].get('value', 0)
                else:
                    data[name] = 0
                
                time.sleep(0.1)  # Rate limiting
            
            logger.info(f"Retrieved economic indicators from World Bank for {country}")
            return data
            
        except Exception as e:
            logger.error(f"World Bank API error for {country}: {e}")
            return {}
    
    def _get_country_code(self, country: str) -> str:
        """Convert country name to World Bank country code"""
        country_codes = {
            'China': 'CHN', 'Germany': 'DEU', 'Japan': 'JPN',
            'Canada': 'CAN', 'Mexico': 'MEX', 'United Kingdom': 'GBR',
            'France': 'FRA', 'Italy': 'ITA', 'South Korea': 'KOR',
            'India': 'IND', 'Brazil': 'BRA', 'Australia': 'AUS'
        }
        return country_codes.get(country, 'USA')

class RealDataManager:
    """Manages all real data connectors"""
    
    def __init__(self):
        self.usitc = USITCConnector()
        self.uncomtrade = UNComtradeConnector()
        self.wto = WTOConnector()
        self.worldbank = WorldBankConnector()
        
        # Cache for API responses
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def get_comprehensive_data(self, country: str, sector: str = None) -> Dict[str, Any]:
        """Get comprehensive data from all sources"""
        cache_key = f"{country}_{sector}"
        
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_ttl:
                return cached_data['data']
        
        try:
            # Collect data from all sources
            tariff_data = self.usitc.get_tariff_rates(country, sector)
            trade_data = self.uncomtrade.get_trade_data(country, sector)
            wto_tariffs = self.wto.get_global_tariffs(country)
            economic_data = self.worldbank.get_economic_indicators(country)
            
            # Combine and validate data
            comprehensive_data = {
                'country': country,
                'sector': sector,
                'tariff_data': tariff_data,
                'trade_data': trade_data,
                'wto_tariffs': wto_tariffs,
                'economic_indicators': economic_data,
                'timestamp': time.time(),
                'sources': ['USITC', 'UN Comtrade', 'WTO', 'World Bank']
            }
            
            # Cache the result
            self.cache[cache_key] = {
                'data': comprehensive_data,
                'timestamp': time.time()
            }
            
            logger.info(f"Retrieved comprehensive data for {country} from {len(comprehensive_data['sources'])} sources")
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error getting comprehensive data for {country}: {e}")
            return {}
    
    def get_fallback_data(self, country: str, sector: str = None) -> Dict[str, Any]:
        """Get fallback data when APIs are unavailable"""
        logger.warning(f"Using fallback data for {country} - APIs may be unavailable")
        
        # Return realistic but clearly marked fallback data
        return {
            'country': country,
            'sector': sector,
            'tariff_data': [],
            'trade_data': [],
            'wto_tariffs': [],
            'economic_indicators': {},
            'timestamp': time.time(),
            'sources': ['FALLBACK'],
            'note': 'This is fallback data. Real-time data unavailable.'
        }
