"""
Command Line Interface for TIPM
"""

import click
import pandas as pd
from datetime import datetime
import json

from tipm.core import TIPMModel, TariffShock
from tipm.config import TIPMConfig
from tipm.utils.data_utils import DataLoader


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Tariff Impact Propagation Model (TIPM) CLI"""
    pass


@main.command()
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="Path to configuration file"
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="model_output.json",
    help="Output file path",
)
@click.option(
    "--tariff-rate", type=float, required=True, help="Tariff rate (e.g., 0.25 for 25%)"
)
@click.option(
    "--origin", type=str, required=True, help="Origin country code (e.g., CN)"
)
@click.option(
    "--destination", type=str, required=True, help="Destination country code (e.g., US)"
)
@click.option("--hs-codes", type=str, help="Comma-separated HS codes (e.g., 8517,8525)")
@click.option("--policy-text", type=str, help="Policy announcement text")
def predict(config, output, tariff_rate, origin, destination, hs_codes, policy_text):
    """Run tariff impact prediction"""

    # Load configuration
    if config:
        with open(config, "r") as f:
            config_dict = json.load(f)
        tipm_config = TIPMConfig(**config_dict)
    else:
        tipm_config = TIPMConfig()

    # Initialize model
    click.echo("Initializing TIPM model...")
    model = TIPMModel(tipm_config)

    # Train model with synthetic data
    click.echo("Training model...")
    import pandas as pd

    synthetic_data = {
        "tariff_shocks": pd.DataFrame(
            {
                "policy_text": ["Demo CLI policy"],
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

    # Create tariff shock
    shock = TariffShock(
        tariff_id=f"{origin}_{destination}_{datetime.now().strftime('%Y%m%d')}",
        hs_codes=hs_codes.split(",") if hs_codes else ["85"],
        rate_change=tariff_rate,
        origin_country=origin,
        destination_country=destination,
        effective_date=datetime.now().strftime("%Y-%m-%d"),
        policy_text=policy_text
        or f"Tariff of {tariff_rate*100}% imposed on imports from {origin} to {destination}",
    )

    # Make prediction
    click.echo("Running prediction...")
    prediction = model.predict(shock)

    # Format output
    result = {
        "tariff_shock": {
            "id": shock.tariff_id,
            "rate": shock.rate_change,
            "origin": shock.origin_country,
            "destination": shock.destination_country,
            "hs_codes": shock.hs_codes,
        },
        "predictions": {
            "trade_flow_impact": str(prediction.trade_flow_impact),
            "industry_response": str(prediction.industry_response),
            "firm_impact": str(prediction.firm_impact),
            "consumer_impact": str(prediction.consumer_impact),
            "geopolitical_impact": str(prediction.geopolitical_impact),
        },
        "confidence_scores": prediction.confidence_scores,
        "timestamp": datetime.now().isoformat(),
    }

    # Save output
    with open(output, "w") as f:
        json.dump(result, f, indent=2)

    click.echo(f"Prediction completed. Results saved to {output}")
    click.echo(
        f"Overall confidence: {prediction.confidence_scores.get('overall_confidence', 'N/A')}"
    )


@main.command()
@click.option(
    "--countries",
    type=str,
    default="US,CN,DE,JP,SG",
    help="Comma-separated country codes",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="sample_data.csv",
    help="Output file path",
)
@click.option(
    "--years", type=str, default="2020,2021,2022,2023", help="Comma-separated years"
)
def generate_data(countries, output, years):
    """Generate sample trade data for testing"""

    click.echo("Generating sample trade data...")

    # Parse inputs
    country_list = countries.split(",")
    year_list = [int(y) for y in years.split(",")]

    # Generate data
    loader = DataLoader()
    trade_data = loader.load_trade_data(country_list, year_list)

    # Save data
    trade_data.to_csv(output, index=False)

    click.echo(f"Sample data generated: {len(trade_data)} records saved to {output}")


@main.command()
@click.option(
    "--data", type=click.Path(exists=True), required=True, help="Path to trade data CSV"
)
def analyze_network(data):
    """Analyze trade network structure"""

    click.echo("Loading trade data...")
    trade_data = pd.read_csv(data)

    # Basic network analysis
    countries = set(trade_data["origin_country"].unique()) | set(
        trade_data["destination_country"].unique()
    )
    total_trade = trade_data["trade_value"].sum()

    click.echo(f"Trade Network Analysis:")
    click.echo(f"  Countries: {len(countries)}")
    click.echo(f"  Trade routes: {len(trade_data)}")
    click.echo(f"  Total trade value: ${total_trade:,.0f}")

    # Top trading countries
    country_totals = {}
    for _, row in trade_data.iterrows():
        origin = row["origin_country"]
        dest = row["destination_country"]
        value = row["trade_value"]

        country_totals[origin] = country_totals.get(origin, 0) + value
        country_totals[dest] = country_totals.get(dest, 0) + value

    top_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)[:5]

    click.echo("\nTop 5 Trading Countries:")
    for country, total in top_countries:
        click.echo(f"  {country}: ${total:,.0f}")


@main.command()
@click.option(
    "--input",
    type=click.Path(exists=True),
    required=True,
    help="Input prediction JSON file",
)
def visualize(input):
    """Create visualizations from prediction results"""

    click.echo("Loading prediction results...")
    with open(input, "r") as f:
        results = json.load(f)

    click.echo("Creating visualizations...")

    # Display confidence scores
    if "confidence_scores" in results:
        click.echo("\nModel Confidence Scores:")
        for layer, score in results["confidence_scores"].items():
            click.echo(f"  {layer}: {score:.2f}")

    click.echo("\nVisualization files would be generated here")
    click.echo("(Requires matplotlib/plotly installation)")


if __name__ == "__main__":
    main()
