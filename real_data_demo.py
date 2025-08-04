#!/usr/bin/env python3
"""
Real Data TIPM Demo
===================

Demonstrates TIPM using real-world datasets from authoritative sources:
- UN Comtrade (trade flows)
- WITS (tariff rates)
- World Bank (economic indicators)
- GDELT (news sentiment)
- ACLED (political events)

Usage:
    python real_data_demo.py --scenario us_china_tech
    python real_data_demo.py --scenario eu_us_auto --years 2022,2023
    python real_data_demo.py --scenario all --force-refresh
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

# Add the tipm package to the path
sys.path.append(str(Path(__file__).parent))

from tipm.real_data_core import RealDataTIPMModel, RealDataConfig, TariffShock
from tipm.config.settings import TIPMConfig


def main():
    parser = argparse.ArgumentParser(description="TIPM Real Data Integration Demo")
    parser.add_argument(
        "--scenario",
        choices=["us_china_tech", "eu_us_auto", "global_steel", "all"],
        default="us_china_tech",
        help="Trade scenario to analyze",
    )
    parser.add_argument(
        "--years", default="2022,2023,2024", help="Comma-separated years to analyze"
    )
    parser.add_argument(
        "--force-refresh", action="store_true", help="Force refresh of cached data"
    )
    parser.add_argument(
        "--output", default="real_data_results.json", help="Output file for results"
    )
    parser.add_argument(
        "--data-quality-threshold",
        type=float,
        default=0.3,
        help="Minimum data quality threshold",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        import logging

        logging.basicConfig(level=logging.INFO)
        print("🔍 Verbose mode enabled")

    # Parse years
    years = [int(y.strip()) for y in args.years.split(",")]

    print(f"🌍 TIPM Real Data Integration Demo")
    print(f"📅 Analyzing years: {years}")
    print(f"🎯 Scenario: {args.scenario}")
    print(f"🔄 Force refresh: {args.force_refresh}")
    print("=" * 60)

    # Define scenarios
    scenarios = {
        "us_china_tech": {
            "name": "US-China Technology Trade",
            "countries": ["840", "156"],  # US, China
            "hs_codes": ["8517", "8471", "8542"],  # Telecom, computers, semiconductors
            "description": "Analyzing tariff impacts on US-China technology trade",
        },
        "eu_us_auto": {
            "name": "EU-US Automotive Trade",
            "countries": ["276", "840"],  # Germany, US
            "hs_codes": ["8703", "8708"],  # Cars, auto parts
            "description": "Analyzing tariff impacts on EU-US automotive sector",
        },
        "global_steel": {
            "name": "Global Steel Trade",
            "countries": ["840", "156", "276", "392"],  # US, China, Germany, Japan
            "hs_codes": ["7208", "7210"],  # Steel products
            "description": "Analyzing global steel tariff impacts",
        },
    }

    if args.scenario == "all":
        selected_scenarios = list(scenarios.values())
    else:
        selected_scenarios = [scenarios[args.scenario]]

    # Configure real data integration
    real_data_config = RealDataConfig(
        data_cache_dir="real_data_cache",
        max_cache_age_hours=24 if not args.force_refresh else 0,
        fallback_to_synthetic=True,
        min_data_points=10,
        primary_trade_source="comtrade",
        primary_economic_source="worldbank",
        primary_sentiment_source="gdelt",
        min_trade_coverage=0.7,
        min_temporal_coverage=0.8,
        max_missing_data_ratio=0.3,
    )

    # Initialize enhanced TIPM model
    print("🚀 Initializing TIPM with real data connectors...")
    model = RealDataTIPMModel(real_data_config=real_data_config)

    all_results = {}

    for scenario in selected_scenarios:
        print(f"\n📊 Processing: {scenario['name']}")
        print(f"📝 {scenario['description']}")
        print(f"🌍 Countries: {scenario['countries']}")
        print(f"📦 Products: {scenario['hs_codes']}")

        try:
            # Train model with real data
            print("🔧 Training model with real datasets...")
            model.fit_with_real_data(
                countries=scenario["countries"],
                hs_codes=scenario["hs_codes"],
                years=years,
                force_refresh=args.force_refresh,
            )

            # Get data provenance information
            provenance = model.get_data_provenance()
            print(f"📈 Data Quality Overview:")
            for dataset, quality in provenance["data_quality_metrics"].items():
                score = quality["quality_score"]
                count = quality["record_count"]
                emoji = "✅" if score > 0.7 else "⚠️" if score > 0.3 else "❌"
                print(f"  {emoji} {dataset}: {score:.2f} quality, {count} records")
                if quality["issues"]:
                    for issue in quality["issues"]:
                        print(f"    - {issue}")

            # Create tariff shock scenario
            tariff_shock = TariffShock(
                tariff_id=f"demo_{scenario['name'].lower().replace(' ', '_').replace('-', '_')}",
                policy_text=f"20% tariff on imports from {scenario['countries'][1] if len(scenario['countries']) > 1 else 'trading partners'}",
                effective_date="2024-01-01",
                hs_codes=scenario["hs_codes"],
                rate_change=0.20,  # 20% tariff increase
                origin_country=(
                    scenario["countries"][1]
                    if len(scenario["countries"]) > 1
                    else scenario["countries"][0]
                ),
                destination_country=scenario["countries"][0],
            )

            # Make prediction
            print("🔮 Generating predictions...")
            prediction = model.predict(tariff_shock)

            # Store results
            scenario_results = {
                "scenario": scenario,
                "tariff_shock": {
                    "tariff_id": tariff_shock.tariff_id,
                    "policy_text": tariff_shock.policy_text,
                    "effective_date": tariff_shock.effective_date,
                    "hs_codes": tariff_shock.hs_codes,
                    "rate_change": tariff_shock.rate_change,
                    "origin_country": tariff_shock.origin_country,
                    "destination_country": tariff_shock.destination_country,
                },
                "prediction": {
                    "trade_flow_impact": prediction.trade_flow_impact,
                    "industry_response": prediction.industry_response,
                    "firm_impact": prediction.firm_impact,
                    "consumer_impact": prediction.consumer_impact,
                    "geopolitical_impact": prediction.geopolitical_impact,
                    "confidence_scores": prediction.confidence_scores,
                    "timestamp": datetime.now().isoformat(),
                },
                "data_provenance": provenance,
                "processing_time": datetime.now().isoformat(),
            }

            all_results[
                args.scenario if args.scenario != "all" else scenario["name"]
            ] = scenario_results

            # Display results
            print(f"\n📊 PREDICTION RESULTS")

            # Calculate overall confidence from individual confidence scores
            overall_confidence = sum(prediction.confidence_scores.values()) / len(
                prediction.confidence_scores
            )

            # Extract numeric values from prediction dictionaries
            trade_impact = (
                prediction.trade_flow_impact.get("impact_magnitude", 0.0)
                if isinstance(prediction.trade_flow_impact, dict)
                else 0.0
            )
            industry_impact = (
                prediction.industry_response.get("impact_magnitude", 0.0)
                if isinstance(prediction.industry_response, dict)
                else 0.0
            )
            firm_impact = (
                prediction.firm_impact.get("impact_magnitude", 0.0)
                if isinstance(prediction.firm_impact, dict)
                else 0.0
            )
            consumer_impact = (
                prediction.consumer_impact.get("impact_magnitude", 0.0)
                if isinstance(prediction.consumer_impact, dict)
                else 0.0
            )
            geo_impact = (
                prediction.geopolitical_impact.get("impact_magnitude", 0.0)
                if isinstance(prediction.geopolitical_impact, dict)
                else 0.0
            )

            print(f"🎯 Overall Confidence: {overall_confidence:.1%}")
            print(f"📈 Trade Flow Impact: {trade_impact:.2%}")
            print(f"🏭 Industry Response: {industry_impact:.2%}")
            print(f"👥 Employment Impact: {firm_impact:.2%}")
            print(f"💰 Consumer Price Impact: {consumer_impact:.2%}")
            print(f"🌐 Geopolitical Response: {geo_impact:.2%}")

        except Exception as e:
            error_result = {
                "scenario": scenario,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
            all_results[f"{scenario['name']}_ERROR"] = error_result
            print(f"❌ Error processing {scenario['name']}: {e}")
            if args.verbose:
                import traceback

                traceback.print_exc()

    # Save results
    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {args.output}")

    # Summary statistics
    successful_scenarios = [k for k, v in all_results.items() if "error" not in v]
    error_scenarios = [k for k, v in all_results.items() if "error" in v]

    print(f"\n📊 EXECUTION SUMMARY")
    print(f"✅ Successful scenarios: {len(successful_scenarios)}")
    print(f"❌ Failed scenarios: {len(error_scenarios)}")

    if successful_scenarios:
        print(f"\n🎯 AVERAGE PREDICTIONS:")

        # Extract numeric impacts from successful scenarios
        confidence_scores = []
        trade_impacts = []
        consumer_impacts = []

        for scenario_name in successful_scenarios:
            result = all_results[scenario_name]
            prediction = result["prediction"]

            # Calculate overall confidence from confidence scores
            conf_scores = prediction["confidence_scores"]
            overall_conf = (
                sum(conf_scores.values()) / len(conf_scores) if conf_scores else 0.77
            )
            confidence_scores.append(overall_conf)

            # Extract trade and consumer impacts
            trade_impact = (
                prediction["trade_flow_impact"].get("impact_magnitude", 0.0)
                if isinstance(prediction["trade_flow_impact"], dict)
                else 0.0
            )
            consumer_impact = (
                prediction["consumer_impact"].get("impact_magnitude", 0.0)
                if isinstance(prediction["consumer_impact"], dict)
                else 0.0
            )

            trade_impacts.append(trade_impact)
            consumer_impacts.append(consumer_impact)

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        )
        avg_trade_impact = (
            sum(trade_impacts) / len(trade_impacts) if trade_impacts else 0
        )
        avg_consumer_impact = (
            sum(consumer_impacts) / len(consumer_impacts) if consumer_impacts else 0
        )

        print(f"📈 Average Confidence: {avg_confidence:.1%}")
        print(f"📊 Average Trade Impact: {avg_trade_impact:.2%}")
        print(f"💰 Average Consumer Impact: {avg_consumer_impact:.2%}")

    if error_scenarios:
        print(f"\n⚠️  FAILED SCENARIOS:")
        for scenario in error_scenarios:
            print(f"  - {scenario}: {all_results[scenario]['error']}")

    print(f"\n🎉 TIPM Real Data Demo Complete!")
    print(f"📁 Detailed results available in: {args.output}")


if __name__ == "__main__":
    main()
