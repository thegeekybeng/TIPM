#!/usr/bin/env python3
"""
Test the new standardized economic impact calculation
This verifies that Singapore with 10% tariff shows realistic ~15-20% impact instead of 55%
"""

# Import required functions
import sys
import os

sys.path.append(".")
from app_gradio import calculate_standardized_economic_impact, SAMPLE_DATA

# NEW STANDARDIZED FORMULA DESIGN:
"""
Core Problem Identified:
- Singapore: 10% tariff showing 55% economic impact due to pre-set sector_impacts (technology: 85%, financial_services: 95%)
- Root cause: System uses unrealistic base disruption values independent of tariff rates

Standardized Solution:
Economic Impact = Base Sector Vulnerability * Tariff Impact Multiplier * Country Factors

Where:
- Base Sector Vulnerability: Realistic 5-20% baseline per sector (technology: 15%, financial: 8%)
- Tariff Impact Multiplier: 1 + (tariff_rate * sector_sensitivity * 2.5 supply chain amplification)
- Country Factors: Trade volume normalization and caps

Expected Results:
- Singapore (10%): ~15-20% total economic impact
- China (67%): ~50-65% total economic impact
- Proportional scaling across all countries and sectors
"""


def test_standardized_calculation():
    """Test the new standardized formula with key countries"""

    print("🧪 TESTING NEW STANDARDIZED ECONOMIC IMPACT CALCULATION")
    print("=" * 70)

    # Test cases: (country, expected_range_description)
    test_countries = [
        ("Singapore", "~15-20% (10% tariff)"),
        ("China", "~50-65% (67% tariff)"),
        ("Germany", "~25-35% (39% tariff)"),
        ("United Kingdom", "~15-20% (10% tariff)"),
        ("Vietnam", "~60-75% (90% tariff)"),
    ]

    # Key sectors to test
    test_sectors = ["technology", "financial_services", "electronics", "agriculture"]

    for country, expected in test_countries:
        if country not in SAMPLE_DATA:
            continue

        data = SAMPLE_DATA[country]
        tariff_rate = data.tariff_to_usa
        trade_volume = data.trade_volume

        print(f"\n🌍 {country.upper()}")
        print(f"   Tariff Rate: {tariff_rate:.0%}")
        print(f"   Expected Range: {expected}")
        print(f"   Trade Volume: ${trade_volume}B")
        print("   Sector Impacts:")

        sector_impacts = []
        for sector in test_sectors:
            impact = calculate_standardized_economic_impact(
                tariff_rate=tariff_rate, sector=sector, trade_volume=trade_volume
            )
            sector_impacts.append(impact)
            print(f"     {sector}: {impact:.1%}")

        # Calculate average impact
        avg_impact = sum(sector_impacts) / len(sector_impacts)
        print(f"   📊 AVERAGE ECONOMIC IMPACT: {avg_impact:.1%}")

        # Verify if it's realistic
        if (
            country == "Singapore" and avg_impact < 0.25
        ):  # Should be under 25% for 10% tariff
            print("   ✅ REALISTIC - Much better than previous 55%!")
        elif (
            country == "China" and avg_impact > 0.40
        ):  # Should be over 40% for 67% tariff
            print("   ✅ REALISTIC - Proportional to high tariff rate")
        else:
            print(
                f"   ⚠️  Review needed - Check if {avg_impact:.1%} is proportional to {tariff_rate:.0%} tariff"
            )

    print("\n" + "=" * 70)
    print("✅ STANDARDIZED FORMULA TEST COMPLETE")
    print(
        "🎯 Key Success Metric: Singapore should show ~15-20% instead of previous 55%"
    )


if __name__ == "__main__":
    test_standardized_calculation()
