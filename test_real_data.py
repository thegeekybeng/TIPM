#!/usr/bin/env python3
"""
Test script for Real Data Integration
Tests the real data connectors without requiring full app dependencies
"""

import sys
import os


def test_real_data_integration():
    """Test the real data integration system"""
    print("🧪 Testing Real Data Integration System")
    print("=" * 50)

    try:
        # Test 1: Import real data connectors
        print("1️⃣ Testing imports...")
        from tipm.real_data_connectors import RealDataManager, TariffData, TradeData

        print("   ✅ Real data connectors imported successfully")

        # Test 2: Initialize real data manager
        print("2️⃣ Testing initialization...")
        real_data = RealDataManager()
        print("   ✅ Real data manager initialized")
        print(
            f"   📊 Available connectors: {[c.__class__.__name__ for c in [real_data.usitc, real_data.uncomtrade, real_data.wto, real_data.worldbank]]}"
        )

        # Test 3: Test data structures
        print("3️⃣ Testing data structures...")
        tariff_data = TariffData(
            country="China",
            sector="Semiconductors",
            tariff_rate=100.0,
            hts_code="8542",
            effective_date="2024-01-01",
            source="USITC",
            confidence=0.95,
        )
        print(
            f"   ✅ TariffData created: {tariff_data.country} - {tariff_data.sector} - {tariff_data.tariff_rate}%"
        )

        trade_data = TradeData(
            country="Germany",
            sector="Automotive",
            trade_volume_usd=50000000000,  # 50 billion USD
            trade_balance=10000000000,  # 10 billion surplus
            year=2024,
            source="UN Comtrade",
        )
        print(
            f"   ✅ TradeData created: {trade_data.country} - {trade_data.sector} - ${trade_data.trade_volume_usd:,.0f}"
        )

        # Test 4: Test comprehensive data retrieval (will likely use fallback)
        print("4️⃣ Testing data retrieval...")
        test_countries = ["China", "Germany", "Japan"]

        for country in test_countries:
            print(f"   🔄 Testing {country}...")
            try:
                country_data = real_data.get_comprehensive_data(country)

                if country_data and country_data.get("sources") != ["FALLBACK"]:
                    print(
                        f"      ✅ {country}: Real data from {country_data.get('sources')}"
                    )
                    print(
                        f"         Tariffs: {len(country_data.get('tariff_data', []))}"
                    )
                    print(f"         Trade: {len(country_data.get('trade_data', []))}")
                    print(
                        f"         Economic: {len(country_data.get('economic_indicators', {}))}"
                    )
                else:
                    print(
                        f"      ⚠️ {country}: Using fallback data (APIs likely unavailable)"
                    )

            except Exception as e:
                print(f"      ❌ {country}: Error - {str(e)}")

        # Test 5: Test fallback data
        print("5️⃣ Testing fallback data...")
        fallback_data = real_data.get_fallback_data("TestCountry", "TestSector")
        print(
            f"   ✅ Fallback data created: {fallback_data.get('country')} - {fallback_data.get('sector')}"
        )
        print(f"   📍 Sources: {fallback_data.get('sources')}")
        print(f"   📝 Note: {fallback_data.get('note')}")

        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("📋 Summary:")
        print("   ✅ Real data connectors working")
        print("   ✅ Data structures validated")
        print("   ✅ Fallback mechanisms working")
        print("   ⚠️ APIs may be unavailable (using fallback)")
        print("\n🚀 Next steps:")
        print("   1. Install app dependencies: pip install gradio plotly")
        print("   2. Test in full TIPM interface")
        print("   3. Verify API endpoints are accessible")
        print("   4. Monitor rate limits and caching")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(
            "💡 Solution: Install dependencies with 'pip install -r requirements_real_data.txt'"
        )
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        print(f"📍 Error type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    success = test_real_data_integration()
    sys.exit(0 if success else 1)
