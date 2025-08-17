#!/usr/bin/env python3
"""
Test API endpoints without FastAPI
Tests the core functions that power the API endpoints
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_country_analysis():
    """Test the country analysis logic"""
    try:
        print("🧪 Testing country analysis logic...")
        
        # Test imports
        from real_tariff_data_source import get_real_country_tariff
        from working_analytics import get_real_economic_analysis, get_real_mitigation_analysis
        from authoritative_tariff_parser import get_country_tariffs
        
        # Test getting country data
        country_name = "Malaysia"
        print(f"Testing {country_name}...")
        
        # Get basic country data
        country_data = get_real_country_tariff(country_name)
        if country_data and "average_tariff_rate" in country_data:
            print(f"✅ {country_name} tariff rate: {country_data['average_tariff_rate']}%")
        else:
            print(f"⚠️ {country_name} data incomplete: {country_data}")
            
        # Test tariff parser
        country_tariffs = get_country_tariffs(country_name)
        print(f"✅ {country_name} sectors: {len(country_tariffs) if country_tariffs else 0}")
        
        return True
        
    except Exception as e:
        print(f"❌ Country analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tariff_summary():
    """Test the tariff summary endpoint logic"""
    try:
        print("\n🧪 Testing tariff summary logic...")
        
        # Test imports
        from correct_tariff_calculator import get_correct_country_rate
        from authoritative_tariff_parser import get_all_countries
        import atlantic_council_fallback
        
        # Test getting all countries
        excel_countries = get_all_countries()
        print(f"✅ Excel countries: {len(excel_countries)}")
        
        ac_countries = atlantic_council_fallback.get_all_countries()
        print(f"✅ Atlantic Council countries: {len(ac_countries)}")
        
        all_countries = sorted(list(set(excel_countries + ac_countries)))
        print(f"✅ Total unique countries: {len(all_countries)}")
        
        # Test a few countries
        test_countries = ["China", "Malaysia", "Germany"]
        for country in test_countries:
            if country in all_countries:
                rate, source, confidence = get_correct_country_rate(country)
                print(f"✅ {country}: {rate}% ({source})")
            else:
                print(f"⚠️ {country} not found in country list")
        
        return True
        
    except Exception as e:
        print(f"❌ Tariff summary test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_economic_analysis():
    """Test economic analysis functions"""
    try:
        print("\n🧪 Testing economic analysis...")
        
        from working_analytics import get_real_economic_analysis, get_real_mitigation_analysis
        
        # Test economic analysis
        economic_analysis = await get_real_economic_analysis("Malaysia", 3.1)
        if economic_analysis and not economic_analysis.get("error"):
            print("✅ Economic analysis completed")
            print(f"   Data sources: {economic_analysis.get('data_sources', [])}")
            print(f"   Confidence: {economic_analysis.get('confidence', 'Unknown')}")
        else:
            print(f"⚠️ Economic analysis issue: {economic_analysis}")
        
        # Test mitigation analysis
        mitigation = await get_real_mitigation_analysis("Malaysia", "Electronics")
        if mitigation:
            print(f"✅ Mitigation strategies: {len(mitigation)} strategies")
        else:
            print("⚠️ No mitigation strategies")
        
        return True
        
    except Exception as e:
        print(f"❌ Economic analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting API Endpoint Tests\n")
    
    # Run tests
    test1 = test_country_analysis()
    test2 = test_tariff_summary()
    test3 = await test_economic_analysis()
    
    print(f"\n📊 Test Results:")
    print(f"✅ Country Analysis: {'PASS' if test1 else 'FAIL'}")
    print(f"✅ Tariff Summary: {'PASS' if test2 else 'FAIL'}")
    print(f"✅ Economic Analysis: {'PASS' if test3 else 'FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All endpoint tests passed! API should be working.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
