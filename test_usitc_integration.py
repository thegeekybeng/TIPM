#!/usr/bin/env python3
"""
Test USITC HTS Integration
==========================

Tests the live USITC HTS integration to ensure it's working correctly.
"""

import asyncio
import sys
import os

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

async def test_usitc_connector():
    """Test the USITC HTS connector"""
    try:
        print("🧪 Testing USITC HTS Connector...")
        
        from usitc_hts_connector import USITCHTSConnector
        
        async with USITCHTSConnector() as connector:
            print("✅ USITC connector initialized successfully")
            
            # Test country data
            print("\n🌍 Testing country data retrieval...")
            china_data = await connector.get_comprehensive_country_data("China")
            print(f"China data: {china_data}")
            
            # Test HTS search
            print("\n🔍 Testing HTS code search...")
            hts_results = await connector.search_hts_codes("laptop")
            print(f"HTS search results: {len(hts_results)}")
            
            # Test special programs
            print("\n📋 Testing special duty programs...")
            special_programs = await connector.get_special_duty_programs()
            print(f"Special programs: {special_programs}")
            
        print("\n✅ USITC connector test completed successfully")
        
    except Exception as e:
        print(f"❌ USITC connector test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_live_integration():
    """Test the live USITC integration"""
    try:
        print("\n🧪 Testing Live USITC Integration...")
        
        from live_usitc_integration import (
            get_live_country_tariff,
            get_live_all_countries,
            get_live_tariff_summary
        )
        
        # Test getting China data
        print("\n🇨🇳 Testing China tariff data...")
        china_data = await get_live_country_tariff("China")
        print(f"China tariff data: {china_data}")
        
        # Test getting all countries
        print("\n🌍 Testing all countries data...")
        all_countries = await get_live_all_countries()
        print(f"Total countries: {len(all_countries)}")
        
        # Test getting tariff summary
        print("\n📊 Testing tariff summary...")
        summary = await get_live_tariff_summary()
        print(f"Tariff summary: {summary}")
        
        print("\n✅ Live integration test completed successfully")
        
    except Exception as e:
        print(f"❌ Live integration test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🚀 Starting USITC HTS Integration Tests...")
    print("=" * 50)
    
    # Test the connector
    await test_usitc_connector()
    
    # Test the live integration
    await test_live_integration()
    
    print("\n" + "=" * 50)
    print("🏁 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
