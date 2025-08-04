#!/usr/bin/env python3
"""
TIPM Quick Start Example
========================

This script demonstrates basic TIPM usage for analyzing tariff impacts.
Run this script to see the TIPM model in action.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tipm.core import TIPMModel, TariffShock
from tipm.config import TIPMConfig
from tipm.utils.data_utils import DataLoader


def main():
    """Run TIPM quick start example"""

    print("🚀 TIPM Quick Start Example")
    print("=" * 50)

    # 1. Initialize model
    print("\n1. Initializing TIPM model...")
    config = TIPMConfig()
    model = TIPMModel(config)
    print(f"   ✅ Model initialized (version {config.model_version})")

    # 2. Train model (using synthetic data)
    print("\n2. Training model with synthetic data...")
    # Create minimal synthetic training data for demo
    import pandas as pd

    synthetic_data = {
        "tariff_shocks": pd.DataFrame(
            {
                "policy_text": ["Demo tariff policy"],
                "effective_date": ["2024-01-01"],
                "hs_codes": ["8517"],
                "tariff_rates": [0.15],
                "countries": ["CN,US"],
            }
        ),
        "trade_flows": pd.DataFrame(
            {
                "hs_code": ["8517"],
                "origin_country": ["CN"],
                "destination_country": ["US"],
                "trade_value": [1000000],
                "year": [2023],
                "transport_cost": [50000],
                "lead_time": [30],
            }
        ),
        "industry_responses": pd.DataFrame(
            {"industry_code": ["electronics"], "response_metric": [0.1]}
        ),
        "firm_responses": pd.DataFrame(
            {"firm_id": ["demo_firm"], "response_metric": [0.1]}
        ),
        "consumer_impacts": pd.DataFrame(
            {"product_category": ["electronics"], "price_change": [0.05]}
        ),
        "geopolitical_events": pd.DataFrame(
            {"event_text": ["Demo geopolitical response"], "sentiment": [0.0]}
        ),
    }
    model.fit(synthetic_data)
    print(f"   ✅ Model trained with synthetic data")

    # 3. Create tariff shock scenario
    print("\n3. Creating tariff shock scenario...")
    shock = TariffShock(
        tariff_id="QUICKSTART_DEMO",
        hs_codes=["8517", "8525"],  # Electronics
        rate_change=0.20,  # 20% tariff
        origin_country="CN",
        destination_country="US",
        effective_date="2024-08-01",
        policy_text="Quick start demo: 20% tariff on Chinese electronics",
    )
    print(
        f"   📊 Scenario: {shock.rate_change*100}% tariff {shock.origin_country}→{shock.destination_country}"
    )
    print(f"   📱 Products: {', '.join(shock.hs_codes)}")

    # 4. Run prediction
    print("\n4. Running tariff impact prediction...")
    prediction = model.predict(shock)
    print(f"   ✅ Prediction completed")

    # 5. Display results
    print("\n5. RESULTS SUMMARY")
    print("-" * 30)

    print(
        f"\n📈 Overall Confidence: {prediction.confidence_scores.get('overall_confidence', 0):.1%}"
    )

    print(f"\n🔍 Layer Confidence Scores:")
    for layer, confidence in prediction.confidence_scores.items():
        if layer != "overall_confidence":
            status = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.6 else "🔴"
            layer_name = layer.replace("_confidence", "").title()
            print(f"   {status} {layer_name}: {confidence:.1%}")

    # 6. Key insights
    print(f"\n💡 KEY INSIGHTS:")
    print(f"   • Trade routes affected: Multiple US-China electronics routes")
    print(f"   • Industry impact: Electronics sector disruption expected")
    print(f"   • Consumer impact: Price increases in electronics products")
    print(f"   • Policy response: Monitoring and potential counter-measures")

    # 7. Next steps
    print(f"\n🎯 NEXT STEPS:")
    print(f"   • Explore the Jupyter notebook: notebooks/tipm_demo.ipynb")
    print(f"   • Try the CLI tool: python -m tipm.cli --help")
    print(f"   • Run with real data sources")
    print(f"   • Customize configuration for your use case")

    print(f"\n✨ TIPM Quick Start completed successfully!")

    return prediction


if __name__ == "__main__":
    try:
        prediction = main()
        print(
            f"\n🎉 Demo completed! Check out the full results in the prediction object."
        )

    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print(
            f"   Make sure you've installed dependencies: pip install -r requirements.txt"
        )
        sys.exit(1)
