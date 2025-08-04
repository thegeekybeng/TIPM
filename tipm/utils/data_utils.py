"""
Data Engineering and Processing Utilities
========================================

Handles data ingestion, processing, and management for TIPM.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json


class DataLoader:
    """
    Data loading utilities for various TIPM data sources
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize data loader with configuration"""
        self.config = config or {}
        self.data_sources = {
            'trade': ['UN_COMTRADE', 'OECD_TiVA', 'WITS'],
            'policy': ['WTO', 'UNCTAD', 'USTR'],
            'economic': ['World_Bank', 'IMF', 'FRED'],
            'social': ['ACLED', 'GDELT', 'Twitter']
        }
    
    def load_trade_data(self, countries: List[str], years: List[int]) -> pd.DataFrame:
        """Load trade flow data for specified countries and years"""
        # Placeholder - would connect to actual data sources
        data = []
        
        for year in years:
            for origin in countries:
                for dest in countries:
                    if origin != dest:
                        # Generate synthetic trade data
                        trade_value = np.random.lognormal(15, 2)  # Log-normal distribution
                        data.append({
                            'year': year,
                            'origin_country': origin,
                            'destination_country': dest,
                            'hs_code': np.random.choice(['84', '85', '87', '27', '73']),
                            'trade_value': trade_value,
                            'transport_cost': np.random.uniform(0.02, 0.1),
                            'lead_time': np.random.randint(7, 45)
                        })
        
        return pd.DataFrame(data)
    
    def load_policy_data(self, date_range: tuple) -> pd.DataFrame:
        """Load tariff policy announcements"""
        start_date, end_date = date_range
        
        # Generate synthetic policy data
        policies = []
        current_date = start_date
        
        while current_date <= end_date:
            if np.random.random() < 0.1:  # 10% chance of policy per day
                policy = {
                    'policy_id': f'POL_{current_date.strftime("%Y%m%d")}_{np.random.randint(1000, 9999)}',
                    'effective_date': current_date,
                    'origin_country': np.random.choice(['US', 'CN', 'EU', 'JP']),
                    'destination_country': np.random.choice(['US', 'CN', 'EU', 'JP', 'GLOBAL']),
                    'hs_codes': [np.random.choice(['84', '85', '87', '27', '73'])],
                    'tariff_rate': np.random.uniform(0, 0.3),
                    'policy_text': self._generate_policy_text(),
                    'policy_type': np.random.choice(['tariff', 'quota', 'subsidy', 'sanction'])
                }
                policies.append(policy)
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(policies)
    
    def _generate_policy_text(self) -> str:
        """Generate synthetic policy announcement text"""
        templates = [
            "The United States Trade Representative announces a {rate}% tariff on imports of {product} from {country}, effective {date}.",
            "Emergency tariff measures implemented: {rate}% duty on {product} imports to protect domestic industry.",
            "Anti-dumping investigation concludes with {rate}% tariff on {country} {product} imports.",
            "Temporary suspension of {product} imports from {country} due to trade dispute.",
            "Bilateral agreement reduces tariffs on {product} by {rate}% over 12 months."
        ]
        
        template = np.random.choice(templates)
        return template.format(
            rate=np.random.randint(5, 35),
            product=np.random.choice(['electronics', 'automobiles', 'steel', 'textiles', 'chemicals']),
            country=np.random.choice(['China', 'Mexico', 'Germany', 'Japan', 'South Korea']),
            date=datetime.now().strftime('%B %d, %Y')
        )
    
    def load_economic_indicators(self, countries: List[str]) -> pd.DataFrame:
        """Load macroeconomic indicators"""
        indicators = []
        
        for country in countries:
            indicator = {
                'country': country,
                'gdp_growth': np.random.normal(2.5, 1.5),
                'inflation_rate': np.random.normal(2.0, 1.0),
                'unemployment_rate': np.random.normal(5.0, 2.0),
                'trade_balance': np.random.normal(0, 50000),
                'exchange_rate_volatility': np.random.uniform(0.05, 0.25),
                'political_stability': np.random.uniform(0.3, 1.0)
            }
            indicators.append(indicator)
        
        return pd.DataFrame(indicators)


class DataProcessor:
    """
    Data processing and transformation utilities
    """
    
    def __init__(self):
        """Initialize data processor"""
        self.cache = {}
    
    def process_trade_flows(self, trade_data: pd.DataFrame) -> pd.DataFrame:
        """Process and clean trade flow data"""
        processed = trade_data.copy()
        
        # Handle missing values
        processed['trade_value'] = processed['trade_value'].fillna(0)
        processed['transport_cost'] = processed['transport_cost'].fillna(0.05)
        processed['lead_time'] = processed['lead_time'].fillna(14)
        
        # Add derived features
        processed['trade_intensity'] = np.log1p(processed['trade_value'])
        processed['cost_ratio'] = processed['transport_cost'] / processed['trade_value']
        processed['time_cost'] = processed['lead_time'] * processed['transport_cost']
        
        # Standardize country codes
        processed['origin_country'] = processed['origin_country'].str.upper()
        processed['destination_country'] = processed['destination_country'].str.upper()
        
        return processed
    
    def aggregate_sector_data(self, trade_data: pd.DataFrame) -> pd.DataFrame:
        """Aggregate trade data by sector (HS code groups)"""
        # Map HS codes to sectors
        sector_mapping = {
            '01-05': 'agriculture',
            '25-27': 'mining',
            '28-38': 'chemicals',
            '39-40': 'plastics',
            '44-49': 'wood_paper',
            '50-63': 'textiles',
            '72-83': 'metals',
            '84-85': 'machinery_electronics',
            '86-89': 'transportation',
            '90-97': 'misc_manufacturing'
        }
        
        # Add sector column
        def map_hs_to_sector(hs_code):
            if not hs_code:
                return 'unknown'
            hs_num = int(hs_code[:2]) if hs_code[:2].isdigit() else 0
            
            for hs_range, sector in sector_mapping.items():
                start, end = map(int, hs_range.split('-'))
                if start <= hs_num <= end:
                    return sector
            return 'other'
        
        trade_data['sector'] = trade_data['hs_code'].apply(map_hs_to_sector)
        
        # Aggregate by sector
        sector_agg = trade_data.groupby(['origin_country', 'destination_country', 'sector']).agg({
            'trade_value': 'sum',
            'transport_cost': 'mean',
            'lead_time': 'mean'
        }).reset_index()
        
        return sector_agg
    
    def calculate_trade_dependencies(self, trade_data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate trade dependency metrics for each country"""
        dependencies = {}
        
        # Calculate total trade by country
        country_totals = {}
        for _, row in trade_data.iterrows():
            origin = row['origin_country']
            dest = row['destination_country']
            value = row['trade_value']
            
            if origin not in country_totals:
                country_totals[origin] = {'exports': 0, 'imports': 0}
            if dest not in country_totals:
                country_totals[dest] = {'exports': 0, 'imports': 0}
            
            country_totals[origin]['exports'] += value
            country_totals[dest]['imports'] += value
        
        # Calculate dependency ratios
        for country in country_totals:
            total_trade = country_totals[country]['exports'] + country_totals[country]['imports']
            
            dependencies[country] = {
                'export_dependency': country_totals[country]['exports'] / total_trade if total_trade > 0 else 0,
                'import_dependency': country_totals[country]['imports'] / total_trade if total_trade > 0 else 0,
                'trade_openness': total_trade / 1000000,  # Normalized trade openness
            }
        
        return dependencies
    
    def create_country_profiles(self, trade_data: pd.DataFrame, economic_data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Create comprehensive country profiles"""
        profiles = {}
        
        # Get unique countries
        countries = set(trade_data['origin_country'].unique()) | set(trade_data['destination_country'].unique())
        
        for country in countries:
            # Trade profile
            country_trade = trade_data[
                (trade_data['origin_country'] == country) | 
                (trade_data['destination_country'] == country)
            ]
            
            # Economic indicators
            econ_data = economic_data[economic_data['country'] == country]
            
            profile = {
                'trade_volume': country_trade['trade_value'].sum(),
                'num_partners': len(set(country_trade['origin_country'].unique()) | 
                                  set(country_trade['destination_country'].unique())) - 1,
                'top_exports': self._get_top_exports(country, trade_data),
                'top_imports': self._get_top_imports(country, trade_data),
                'economic_indicators': econ_data.to_dict('records')[0] if not econ_data.empty else {},
                'trade_complexity': self._calculate_trade_complexity(country, trade_data)
            }
            
            profiles[country] = profile
        
        return profiles
    
    def _get_top_exports(self, country: str, trade_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Get top export products for a country"""
        exports = trade_data[trade_data['origin_country'] == country]
        top_exports = exports.groupby('hs_code')['trade_value'].sum().nlargest(5)
        
        return [{'hs_code': code, 'value': value} for code, value in top_exports.items()]
    
    def _get_top_imports(self, country: str, trade_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Get top import products for a country"""
        imports = trade_data[trade_data['destination_country'] == country]
        top_imports = imports.groupby('hs_code')['trade_value'].sum().nlargest(5)
        
        return [{'hs_code': code, 'value': value} for code, value in top_imports.items()]
    
    def _calculate_trade_complexity(self, country: str, trade_data: pd.DataFrame) -> float:
        """Calculate trade complexity index for a country"""
        # Simplified complexity calculation
        country_exports = trade_data[trade_data['origin_country'] == country]
        unique_products = country_exports['hs_code'].nunique()
        unique_destinations = country_exports['destination_country'].nunique()
        
        # Complexity increases with product and destination diversity
        complexity = (unique_products * unique_destinations) / 100
        return min(complexity, 1.0)  # Normalize to 0-1
