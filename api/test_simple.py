#!/usr/bin/env python3
"""
Simple test without external dependencies
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functions():
    """Test basic functions that don't require external deps"""
    try:
        print("🧪 Testing basic functions...")
        
        # Test real tariff data source
        from real_tariff_data_source import get_real_country_tariff
        
        countries = ["China", "Malaysia", "Germany"]
        for country in countries:
            data = get_real_country_tariff(country)
            print(f"✅ {country}: {data.get('average_tariff_rate', 'N/A')}%")
        
        # Test Atlantic Council data
        import atlantic_council_fallback
        ac_countries = atlantic_council_fallback.get_all_countries()
        print(f"✅ Atlantic Council countries: {len(ac_countries)}")
        
        # Test correct tariff calculator
        from correct_tariff_calculator import get_correct_country_rate
        for country in ["China", "Malaysia"]:
            rate, source, confidence = get_correct_country_rate(country)
            print(f"✅ {country}: {rate}% from {source}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analysis_without_external_deps():
    """Test analysis functions that use fallbacks"""
    try:
        print("\n🧪 Testing analysis with fallbacks...")
        
        # Test country info functions
        from main import get_continent, get_global_groups, is_emerging_market
        
        test_country = "Malaysia"
        continent = get_continent(test_country)
        groups = get_global_groups(test_country)
        emerging = is_emerging_market(test_country)
        
        print(f"✅ {test_country}: {continent}, Groups: {groups}, Emerging: {emerging}")
        
        # Test GDP and trade functions
        import asyncio
        from main import get_country_gdp, get_country_trade_volume
        
        async def test_async():
            gdp = await get_country_gdp(test_country)
            trade = await get_country_trade_volume(test_country)
            print(f"✅ {test_country}: GDP ${gdp}B, Trade ${trade}M")
            return True
        
        result = asyncio.run(test_async())
        return result
        
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Simple Tests\n")
    
    test1 = test_basic_functions()
    test2 = test_analysis_without_external_deps()
    
    print(f"\n📊 Test Results:")
    print(f"✅ Basic Functions: {'PASS' if test1 else 'FAIL'}")
    print(f"✅ Analysis Functions: {'PASS' if test2 else 'FAIL'}")
    
    if all([test1, test2]):
        print("\n🎉 Core functionality is working! API should be functional.")
    else:
        print("\n⚠️ Some tests failed.")
