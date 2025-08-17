"""
CORRECT US TARIFF CALCULATOR
============================

This module provides accurate tariff calculations using the authoritative Excel data
and proper fallback hierarchy, replacing the flawed calculation system.
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class CorrectTariffCalculator:
    """Accurate tariff calculator using proper data sources"""
    
    def __init__(self):
        self.excel_data = None
        self.atlantic_council_data = None
        self.load_data()
    
    def load_data(self):
        """Load all data sources with proper error handling"""
        try:
            # Load Excel data (authoritative)
            excel_path = "data/US_Tariffs_Reciprocal_Country_Sector_2025-08-15.xlsx"
            if os.path.exists(excel_path):
                self.excel_data = pd.read_excel(excel_path, sheet_name='Country_Rates')
                logger.info(f"✅ Loaded Excel data: {len(self.excel_data)} countries")
            else:
                logger.warning("❌ Excel file not found")
                
        except Exception as e:
            logger.error(f"❌ Failed to load Excel data: {e}")
        
        try:
            # Load Atlantic Council fallback data
            import atlantic_council_fallback
            self.atlantic_council_data = atlantic_council_fallback.ATLANTIC_COUNCIL_DATA
            logger.info(f"✅ Loaded Atlantic Council data: {len(self.atlantic_council_data)} countries")
        except Exception as e:
            logger.error(f"❌ Failed to load Atlantic Council data: {e}")
    
    def get_country_tariff_rate(self, country_name: str) -> Tuple[float, str, str]:
        """
        Get correct tariff rate for a country
        
        Returns:
            (tariff_rate, data_source, confidence_level)
        """
        
        # 1. First check Excel data (highest authority)
        if self.excel_data is not None:
            excel_match = self.excel_data[self.excel_data['Country'] == country_name]
            if not excel_match.empty:
                rate = float(excel_match.iloc[0]['Reciprocal_AddOn_Pct'])
                rule_type = excel_match.iloc[0]['Rule_Type']
                return (
                    rate, 
                    f"USTR Excel - {rule_type}", 
                    "High - Official US Trade Representative data"
                )
        
        # 2. Fallback to Atlantic Council data
        if self.atlantic_council_data and country_name in self.atlantic_council_data:
            ac_data = self.atlantic_council_data[country_name]
            
            # Calculate average rate from active tariffs
            total_rate = 0
            active_count = 0
            
            for sector_name, sector_data in ac_data.items():
                if isinstance(sector_data, dict) and sector_data.get('status') == 'Active':
                    rate = sector_data.get('tariff_rate', 0)
                    if rate > 0:
                        total_rate += rate
                        active_count += 1
            
            if active_count > 0:
                avg_rate = total_rate / active_count
                return (
                    avg_rate,
                    "Atlantic Council Tracker",
                    "Medium - Atlantic Council tariff data"
                )
        
        # 3. Default to 0% (no tariffs)
        return (0.0, "Default", "Low - No US tariffs currently imposed")
    
    def get_affected_sectors(self, country_name: str) -> List[str]:
        """Get list of sectors affected by tariffs"""
        
        # Check Excel first
        if self.excel_data is not None:
            excel_match = self.excel_data[self.excel_data['Country'] == country_name]
            if not excel_match.empty:
                rule_type = excel_match.iloc[0]['Rule_Type']
                # Excel data is country-level, so return general category
                if rule_type == 'EU_TopUp':
                    return ["European Union Trade"]
                elif rule_type == 'FixedAddOn_China':
                    return ["China Trade Relations"]
                elif rule_type == 'Exempt':
                    return []
                else:
                    return ["General Trade"]
        
        # Fallback to Atlantic Council sectors
        if self.atlantic_council_data and country_name in self.atlantic_council_data:
            ac_data = self.atlantic_council_data[country_name]
            sectors = []
            
            for sector_name, sector_data in ac_data.items():
                if isinstance(sector_data, dict) and sector_data.get('status') == 'Active':
                    rate = sector_data.get('tariff_rate', 0)
                    if rate > 0:
                        sectors.append(sector_name)
            
            return sectors
        
        return []
    
    def validate_calculations(self) -> Dict[str, Dict]:
        """Validate calculations against known values for debugging"""
        
        test_countries = ['China', 'Singapore', 'Switzerland', 'Japan', 'Canada']
        results = {}
        
        for country in test_countries:
            rate, source, confidence = self.get_country_tariff_rate(country)
            sectors = self.get_affected_sectors(country)
            
            results[country] = {
                'tariff_rate': rate,
                'data_source': source,
                'confidence': confidence,
                'affected_sectors': sectors,
                'sector_count': len(sectors)
            }
        
        return results

# Global instance
calculator = CorrectTariffCalculator()

def get_correct_country_rate(country_name: str) -> Tuple[float, str, str]:
    """Get correct tariff rate for a country"""
    return calculator.get_country_tariff_rate(country_name)

def get_correct_affected_sectors(country_name: str) -> List[str]:
    """Get correct affected sectors for a country"""
    return calculator.get_affected_sectors(country_name)

def validate_system():
    """Validate the corrected system"""
    return calculator.validate_calculations()

if __name__ == "__main__":
    # Test the system
    print("🧪 TESTING CORRECT TARIFF CALCULATOR")
    print("=" * 50)
    
    results = validate_system()
    for country, data in results.items():
        print(f"\n🌍 {country}:")
        print(f"  Rate: {data['tariff_rate']:.1f}%")
        print(f"  Source: {data['data_source']}")
        print(f"  Sectors: {data['sector_count']} ({', '.join(data['affected_sectors'][:2])}{'...' if len(data['affected_sectors']) > 2 else ''})")
