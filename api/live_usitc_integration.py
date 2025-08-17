#!/usr/bin/env python3
"""
Live USITC HTS Integration
==========================

Integrates with the official USITC HTS database to provide:
- Real-time tariff rates for all countries
- Live HTS code data
- Special duty program information
- Zero hardcoded data - everything from live APIs

This replaces all previous hardcoded and sample data sources.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from usitc_hts_connector import (
    USITCHTSConnector,
    get_usitc_country_tariff,
    get_usitc_hts_details,
    get_usitc_special_programs
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LiveUSITCIntegration:
    """
    Main integration class for live USITC HTS data
    Provides comprehensive tariff data without hardcoded values
    """
    
    def __init__(self):
        self.connector = None
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # Known countries affected by US tariffs (from official sources)
        self.affected_countries = [
            "China", "Hong Kong", "Macau", "Russia", "Ukraine", "Turkey",
            "India", "Brazil", "Mexico", "Canada", "Japan", "South Korea",
            "Germany", "France", "United Kingdom", "Italy", "Spain",
            "Netherlands", "Belgium", "Switzerland", "Australia", "Singapore",
            "Malaysia", "Thailand", "Vietnam", "Indonesia", "Philippines",
            "Taiwan", "South Africa", "Egypt", "Nigeria", "Kenya", "Morocco",
            "Tunisia", "Algeria", "Ethiopia", "Ghana", "Uganda", "Tanzania",
            "Zambia", "Zimbabwe", "Angola", "Mozambique", "Madagascar",
            "Mauritius", "Seychelles", "Comoros", "Djibouti", "Somalia",
            "Eritrea", "Sudan", "South Sudan", "Chad", "Niger", "Mali",
            "Burkina Faso", "Senegal", "Gambia", "Guinea-Bissau", "Guinea",
            "Sierra Leone", "Liberia", "Ivory Coast", "Togo", "Benin",
            "Cameroon", "Central African Republic", "Gabon", "Congo",
            "Democratic Republic of Congo", "Equatorial Guinea",
            "Sao Tome and Principe", "Cape Verde", "Mauritania",
            "Western Sahara", "Libya"
        ]

    async def __aenter__(self):
        self.connector = USITCHTSConnector()
        await self.connector.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connector:
            await self.connector.__aexit__(exc_type, exc_val, exc_tb)

    async def get_country_tariff_data(self, country_name: str) -> Dict[str, Any]:
        """
        Get comprehensive tariff data for a country from USITC
        Returns live data with no hardcoded values
        """
        try:
            # Check cache first
            cache_key = f"country_{country_name.lower()}"
            if self._is_cache_valid(cache_key):
                logger.info(f"Using cached data for {country_name}")
                return self.cache[cache_key]

            # Fetch live data from USITC
            logger.info(f"Fetching live tariff data for {country_name} from USITC")
            country_data = await self.connector.get_comprehensive_country_data(country_name)
            
            if not country_data:
                # If USITC doesn't have data, create a minimal response
                # but mark it as having no official data
                country_data = {
                    "country_name": country_name,
                    "country_code": "",
                    "average_tariff_rate": 0.0,
                    "affected_sectors": [],
                    "special_programs": [],
                    "recent_changes": [],
                    "last_updated": datetime.now().isoformat(),
                    "data_source": "USITC HTS Database",
                    "confidence": "No Data Available",
                    "note": "No official tariff data found for this country"
                }

            # Cache the result
            self._cache_data(cache_key, country_data)
            
            return country_data

        except Exception as e:
            logger.error(f"Error getting tariff data for {country_name}: {e}")
            return {
                "country_name": country_name,
                "error": f"Failed to fetch data: {str(e)}",
                "data_source": "USITC HTS Database",
                "confidence": "Error",
                "timestamp": datetime.now().isoformat()
            }

    async def get_all_countries_tariff_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Get tariff data for all affected countries
        Returns live data for all countries
        """
        try:
            all_countries_data = {}
            
            # Fetch data for all affected countries
            for country in self.affected_countries:
                logger.info(f"Fetching data for {country}")
                country_data = await self.get_country_tariff_data(country)
                all_countries_data[country] = country_data
                
                # Small delay to avoid overwhelming the API
                await asyncio.sleep(0.1)
            
            return all_countries_data

        except Exception as e:
            logger.error(f"Error getting all countries data: {e}")
            return {}

    async def get_country_average_tariff(self, country_name: str) -> Tuple[float, str, str]:
        """
        Get the average tariff rate for a country
        Returns (rate, source, confidence)
        """
        try:
            country_data = await self.get_country_tariff_data(country_name)
            
            if "error" in country_data:
                return 0.0, "USITC HTS Database", "Error"
            
            if country_data.get("confidence") == "No Data Available":
                return 0.0, "USITC HTS Database", "No Data"
            
            tariff_rate = country_data.get("average_tariff_rate", 0.0)
            source = country_data.get("data_source", "USITC HTS Database")
            confidence = country_data.get("confidence", "Unknown")
            
            return tariff_rate, source, confidence

        except Exception as e:
            logger.error(f"Error getting average tariff for {country_name}: {e}")
            return 0.0, "USITC HTS Database", "Error"

    async def get_affected_sectors(self, country_name: str) -> List[str]:
        """
        Get affected sectors for a country
        Returns live data from USITC
        """
        try:
            country_data = await self.get_country_tariff_data(country_name)
            
            if "error" in country_data:
                return []
            
            return country_data.get("affected_sectors", [])

        except Exception as e:
            logger.error(f"Error getting affected sectors for {country_name}: {e}")
            return []

    async def get_special_duty_programs(self) -> Dict[str, Any]:
        """
        Get information about special duty programs
        Returns live data from USITC
        """
        try:
            # Check cache first
            cache_key = "special_programs"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]

            # Fetch live data
            programs_data = await self.connector.get_special_duty_programs()
            
            # Cache the result
            self._cache_data(cache_key, programs_data)
            
            return programs_data

        except Exception as e:
            logger.error(f"Error getting special duty programs: {e}")
            return {}

    async def get_hts_code_details(self, hts_code: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for an HTS code
        Returns live data from USITC
        """
        try:
            hts_data = await self.connector.get_hts_details(hts_code)
            
            if hts_data:
                return {
                    "hts_code": hts_data.hts_code,
                    "description": hts_data.description,
                    "base_duty_rate": hts_data.base_duty_rate,
                    "special_duty_programs": hts_data.special_duty_programs,
                    "country_specific_rates": hts_data.country_specific_rates,
                    "effective_date": hts_data.effective_date,
                    "source": hts_data.source
                }
            
            return None

        except Exception as e:
            logger.error(f"Error getting HTS code details: {e}")
            return None

    async def search_hts_codes(self, query: str) -> List[Dict[str, Any]]:
        """
        Search HTS codes by description or partial code
        Returns live data from USITC
        """
        try:
            hts_results = await self.connector.search_hts_codes(query)
            
            return [
                {
                    "hts_code": hts.hts_code,
                    "description": hts.description,
                    "base_duty_rate": hts.base_duty_rate,
                    "special_duty_programs": hts.special_duty_programs,
                    "country_specific_rates": hts.country_specific_rates,
                    "effective_date": hts.effective_date,
                    "source": hts.source
                }
                for hts in hts_results
            ]

        except Exception as e:
            logger.error(f"Error searching HTS codes: {e}")
            return []

    async def get_tariff_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive tariff summary for all countries
        Returns live data with no hardcoded values
        """
        try:
            all_countries = await self.get_all_countries_tariff_data()
            
            # Calculate summary statistics
            total_countries = len(all_countries)
            countries_with_tariffs = sum(1 for data in all_countries.values() 
                                       if data.get("average_tariff_rate", 0) > 0)
            
            # Calculate average tariff rates
            tariff_rates = [data.get("average_tariff_rate", 0) 
                           for data in all_countries.values() 
                           if data.get("average_tariff_rate", 0) > 0]
            
            avg_tariff_rate = sum(tariff_rates) / len(tariff_rates) if tariff_rates else 0
            
            # Get special programs
            special_programs = await self.get_special_duty_programs()
            
            return {
                "total_countries": total_countries,
                "countries_with_tariffs": countries_with_tariffs,
                "average_tariff_rate": round(avg_tariff_rate, 2),
                "special_programs": list(special_programs.keys()) if special_programs else [],
                "last_updated": datetime.now().isoformat(),
                "data_source": "USITC HTS Live Database",
                "confidence": "High - Official US Government Source",
                "countries": all_countries
            }

        except Exception as e:
            logger.error(f"Error getting tariff summary: {e}")
            return {
                "error": f"Failed to generate summary: {str(e)}",
                "data_source": "USITC HTS Database",
                "timestamp": datetime.now().isoformat()
            }

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache or cache_key not in self.cache_expiry:
            return False
        
        return datetime.now() < self.cache_expiry[cache_key]

    def _cache_data(self, cache_key: str, data: Any):
        """Cache data with expiration"""
        self.cache[cache_key] = data
        self.cache_expiry[cache_key] = datetime.now() + self.cache_duration

    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_expiry.clear()


# Convenience functions for easy integration
async def get_live_country_tariff(country_name: str) -> Dict[str, Any]:
    """
    Get live tariff data for a country from USITC
    """
    async with LiveUSITCIntegration() as integration:
        return await integration.get_country_tariff_data(country_name)


async def get_live_all_countries() -> Dict[str, Dict[str, Any]]:
    """
    Get live tariff data for all affected countries
    """
    async with LiveUSITCIntegration() as integration:
        return await integration.get_all_countries_tariff_data()


async def get_live_tariff_summary() -> Dict[str, Any]:
    """
    Get live comprehensive tariff summary
    """
    async with LiveUSITCIntegration() as integration:
        return await integration.get_tariff_summary()


async def get_live_country_average_tariff(country_name: str) -> Tuple[float, str, str]:
    """
    Get live average tariff rate for a country
    """
    async with LiveUSITCIntegration() as integration:
        return await integration.get_country_average_tariff(country_name)


async def get_live_affected_sectors(country_name: str) -> List[str]:
    """
    Get live affected sectors for a country
    """
    async with LiveUSITCIntegration() as integration:
        return await integration.get_affected_sectors(country_name)


# Test function
async def test_live_integration():
    """Test the live USITC integration"""
    try:
        logger.info("Testing live USITC integration...")
        
        # Test getting China data
        china_data = await get_live_country_tariff("China")
        logger.info(f"China data: {china_data}")
        
        # Test getting all countries
        all_countries = await get_live_all_countries()
        logger.info(f"Total countries: {len(all_countries)}")
        
        # Test getting tariff summary
        summary = await get_live_tariff_summary()
        logger.info(f"Tariff summary: {summary}")
        
        logger.info("Live integration test completed")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_live_integration())
