#!/usr/bin/env python3
"""
Basic functionality test for TIPM API
Tests core functions without external dependencies
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_basic_imports():
    """Test that basic modules can be imported"""
    try:
        print("🧪 Testing basic imports...")

        # Test working_analytics
        from working_analytics import (
            get_real_economic_analysis,
            get_real_mitigation_analysis,
        )

        print("✅ working_analytics imported successfully")

        # Test real_tariff_data_source
        from real_tariff_data_source import get_real_country_tariff

        print("✅ real_tariff_data_source imported successfully")

        # Test authoritative_tariff_parser
        from authoritative_tariff_parser import get_country_tariffs

        print("✅ authoritative_tariff_parser imported successfully")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_country_data():
    """Test basic country data retrieval"""
    try:
        print("\n🧪 Testing country data retrieval...")

        from real_tariff_data_source import get_real_country_tariff

        # Test China data
        china_data = get_real_country_tariff("China")
        if china_data and "average_tariff_rate" in china_data:
            print(f"✅ China tariff rate: {china_data['average_tariff_rate']}%")
        else:
            print("⚠️ China data incomplete")

        # Test Malaysia data
        malaysia_data = get_real_country_tariff("Malaysia")
        if malaysia_data and "average_tariff_rate" in malaysia_data:
            print(f"✅ Malaysia tariff rate: {malaysia_data['average_tariff_rate']}%")
        else:
            print("⚠️ Malaysia data incomplete")

        return True

    except Exception as e:
        print(f"❌ Country data test failed: {e}")
        return False


def test_tariff_parser():
    """Test tariff parser functionality"""
    try:
        print("\n🧪 Testing tariff parser...")

        from authoritative_tariff_parser import get_country_tariffs, get_all_countries

        # Test getting all countries
        countries = get_all_countries()
        print(f"✅ Total countries available: {len(countries)}")

        # Test getting country tariffs
        china_tariffs = get_country_tariffs("China")
        if china_tariffs:
            print(f"✅ China tariffs: {len(china_tariffs)} sectors")
        else:
            print("⚠️ China tariffs not available")

        return True

    except Exception as e:
        print(f"❌ Tariff parser test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting TIPM Basic Functionality Test\n")

    # Run tests
    test1 = test_basic_imports()
    test2 = test_country_data()
    test3 = test_tariff_parser()

    print(f"\n📊 Test Results:")
    print(f"✅ Basic imports: {'PASS' if test1 else 'FAIL'}")
    print(f"✅ Country data: {'PASS' if test2 else 'FAIL'}")
    print(f"✅ Tariff parser: {'PASS' if test3 else 'FAIL'}")

    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! Basic functionality is working.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
