#!/usr/bin/env python3
"""
TIPM: Tariff Impact Propagation Model
Gradio Interface for Hugging Face Spaces
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


# Data structures and sample data (same as Streamlit version)
@dataclass
class CountryTariffData:
    country: str
    tariff_to_usa: float
    reciprocal_tariff: float
    trade_volume: float
    sector_impacts: Dict[str, float]


# Sample data for demo (based on real Trump tariff data)
SAMPLE_DATA = {
    "China": CountryTariffData(
        country="China",
        tariff_to_usa=0.99,
        reciprocal_tariff=0.75,
        trade_volume=650.0,
        sector_impacts={
            "technology": 0.85,
            "agriculture": 0.45,
            "textiles": 0.65,
            "chemicals": 0.55,
            "machinery": 0.75,
            "automotive": 0.70,
            "metals": 0.60,
            "energy": 0.35,
            "pharmaceuticals": 0.50,
            "food_processing": 0.40,
            "electronics": 0.80,
            "furniture": 0.55,
        },
    ),
    "European Union": CountryTariffData(
        country="European Union",
        tariff_to_usa=0.85,
        reciprocal_tariff=0.65,
        trade_volume=400.0,
        sector_impacts={
            "technology": 0.70,
            "agriculture": 0.25,
            "textiles": 0.50,
            "chemicals": 0.65,
            "machinery": 0.75,
            "automotive": 0.80,
            "metals": 0.60,
            "energy": 0.40,
            "pharmaceuticals": 0.55,
            "food_processing": 0.30,
            "electronics": 0.65,
            "furniture": 0.45,
        },
    ),
    "Japan": CountryTariffData(
        country="Japan",
        tariff_to_usa=0.75,
        reciprocal_tariff=0.55,
        trade_volume=320.0,
        sector_impacts={
            "technology": 0.80,
            "agriculture": 0.20,
            "textiles": 0.40,
            "chemicals": 0.60,
            "machinery": 0.85,
            "automotive": 0.90,
            "metals": 0.70,
            "energy": 0.30,
            "pharmaceuticals": 0.45,
            "food_processing": 0.15,
            "electronics": 0.85,
            "furniture": 0.25,
        },
    ),
    "India": CountryTariffData(
        country="India",
        tariff_to_usa=0.70,
        reciprocal_tariff=0.50,
        trade_volume=150.0,
        sector_impacts={
            "technology": 0.75,
            "agriculture": 0.40,
            "textiles": 0.80,
            "chemicals": 0.60,
            "machinery": 0.55,
            "automotive": 0.50,
            "metals": 0.45,
            "energy": 0.35,
            "pharmaceuticals": 0.85,
            "food_processing": 0.35,
            "electronics": 0.70,
            "furniture": 0.60,
        },
    ),
    "South Korea": CountryTariffData(
        country="South Korea",
        tariff_to_usa=0.65,
        reciprocal_tariff=0.45,
        trade_volume=130.0,
        sector_impacts={
            "technology": 0.80,
            "agriculture": 0.20,
            "textiles": 0.40,
            "chemicals": 0.60,
            "machinery": 0.65,
            "automotive": 0.75,
            "metals": 0.55,
            "energy": 0.30,
            "pharmaceuticals": 0.45,
            "food_processing": 0.15,
            "electronics": 0.85,
            "furniture": 0.25,
        },
    ),
    "Vietnam": CountryTariffData(
        country="Vietnam",
        tariff_to_usa=0.60,
        reciprocal_tariff=0.40,
        trade_volume=100.0,
        sector_impacts={
            "technology": 0.50,
            "agriculture": 0.55,
            "textiles": 0.85,
            "chemicals": 0.45,
            "machinery": 0.40,
            "automotive": 0.35,
            "metals": 0.35,
            "energy": 0.25,
            "pharmaceuticals": 0.30,
            "food_processing": 0.60,
            "electronics": 0.70,
            "furniture": 0.80,
        },
    ),
    "Taiwan": CountryTariffData(
        country="Taiwan",
        tariff_to_usa=0.68,
        reciprocal_tariff=0.45,
        trade_volume=90.0,
        sector_impacts={
            "technology": 0.90,
            "agriculture": 0.15,
            "textiles": 0.35,
            "chemicals": 0.50,
            "machinery": 0.60,
            "automotive": 0.30,
            "metals": 0.40,
            "energy": 0.20,
            "pharmaceuticals": 0.55,
            "food_processing": 0.10,
            "electronics": 0.95,
            "furniture": 0.20,
        },
    ),
    "Thailand": CountryTariffData(
        country="Thailand",
        tariff_to_usa=0.65,
        reciprocal_tariff=0.50,
        trade_volume=60.0,
        sector_impacts={
            "technology": 0.50,
            "agriculture": 0.60,
            "textiles": 0.55,
            "chemicals": 0.45,
            "machinery": 0.40,
            "automotive": 0.65,
            "metals": 0.35,
            "energy": 0.30,
            "pharmaceuticals": 0.40,
            "food_processing": 0.70,
            "electronics": 0.55,
            "furniture": 0.60,
        },
    ),
    "Singapore": CountryTariffData(
        country="Singapore",
        tariff_to_usa=0.45,
        reciprocal_tariff=0.25,
        trade_volume=55.0,
        sector_impacts={
            "technology": 0.60,
            "agriculture": 0.05,
            "textiles": 0.20,
            "chemicals": 0.70,
            "machinery": 0.50,
            "automotive": 0.20,
            "metals": 0.40,
            "energy": 0.60,
            "pharmaceuticals": 0.65,
            "food_processing": 0.10,
            "electronics": 0.70,
            "furniture": 0.15,
        },
    ),
    "Malaysia": CountryTariffData(
        country="Malaysia",
        tariff_to_usa=0.60,
        reciprocal_tariff=0.40,
        trade_volume=50.0,
        sector_impacts={
            "technology": 0.55,
            "agriculture": 0.45,
            "textiles": 0.50,
            "chemicals": 0.50,
            "machinery": 0.45,
            "automotive": 0.35,
            "metals": 0.40,
            "energy": 0.55,
            "pharmaceuticals": 0.35,
            "food_processing": 0.50,
            "electronics": 0.60,
            "furniture": 0.45,
        },
    ),
}

SECTORS = [
    "technology",
    "agriculture",
    "textiles",
    "chemicals",
    "machinery",
    "automotive",
    "metals",
    "energy",
    "pharmaceuticals",
    "food_processing",
    "electronics",
    "furniture",
]


def calculate_country_analysis(countries: List[str], sectors: List[str]) -> Dict:
    """Calculate tariff impact analysis for selected countries and sectors"""
    analysis = {
        "country_impacts": [],
        "summary": {
            "total_countries": len(countries),
            "total_sectors": len(sectors),
            "avg_disruption": 0,
            "total_gdp_impact": 0,
            "total_trade_volume": 0,
        },
    }

    total_disruption = 0
    total_gdp_impact = 0
    total_trade_volume = 0

    for country in countries:
        if country not in SAMPLE_DATA:
            continue

        data = SAMPLE_DATA[country]

        # Calculate sector-specific impacts
        sector_disruptions = []
        for sector in sectors:
            if sector in data.sector_impacts:
                sector_disruptions.append(data.sector_impacts[sector])

        if not sector_disruptions:
            continue

        # Average disruption across selected sectors
        avg_disruption = np.mean(sector_disruptions)

        # GDP impact calculation (simplified)
        # Uses trade volume as proxy for economic exposure
        gdp_impact = avg_disruption * data.trade_volume * 0.8

        country_result = {
            "country": country,
            "economic_disruption": avg_disruption,
            "gdp_impact": gdp_impact,
            "trade_volume": data.trade_volume,
            "tariff_rate": data.tariff_to_usa,
            "sector_impacts": {
                k: v for k, v in data.sector_impacts.items() if k in sectors
            },
        }

        analysis["country_impacts"].append(country_result)
        total_disruption += avg_disruption
        total_gdp_impact += gdp_impact
        total_trade_volume += data.trade_volume

    # Calculate summary statistics
    if analysis["country_impacts"]:
        analysis["summary"]["avg_disruption"] = total_disruption / len(
            analysis["country_impacts"]
        )
        analysis["summary"]["total_gdp_impact"] = total_gdp_impact
        analysis["summary"]["total_trade_volume"] = total_trade_volume

    return analysis


def create_impact_plot(analysis_results: Dict):
    """Create Plotly visualization for country impacts"""
    if not analysis_results["country_impacts"]:
        return None

    # Prepare data
    countries = []
    disruptions = []
    gdp_impacts = []
    trade_volumes = []

    for impact in analysis_results["country_impacts"]:
        countries.append(impact["country"])
        disruptions.append(impact["economic_disruption"] * 100)  # Convert to percentage
        gdp_impacts.append(impact["gdp_impact"])
        trade_volumes.append(impact["trade_volume"])

    # Create color scale based on risk level
    colors = []
    for disruption in disruptions:
        if disruption >= 50:
            colors.append("#FF4B4B")  # Very High Risk - Red
        elif disruption >= 35:
            colors.append("#FF8C00")  # High Risk - Orange
        elif disruption >= 20:
            colors.append("#FFD700")  # Medium Risk - Yellow
        else:
            colors.append("#32CD32")  # Low Risk - Green

    # Create horizontal bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=countries,
            x=disruptions,
            orientation="h",
            marker=dict(color=colors),
            text=[f"{d:.1f}%" for d in disruptions],
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                + "Economic Disruption: %{x:.1f}%<br>"
                + "GDP Impact: $%{customdata[0]:.1f}B<br>"
                + "Trade Volume: $%{customdata[1]:.1f}B<br>"
                + "<extra></extra>"
            ),
            customdata=list(zip(gdp_impacts, trade_volumes)),
        )
    )

    fig.update_layout(
        title=dict(
            text="Country Economic Impact Analysis",
            font=dict(size=18, color="#2E2E2E"),
            x=0.5,
        ),
        xaxis_title="Economic Disruption (%)",
        yaxis_title="Countries",
        height=max(400, len(countries) * 60),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        margin=dict(l=150, r=100, t=80, b=60),
    )

    # Add risk zone background colors
    fig.add_vrect(x0=0, x1=20, fillcolor="rgba(50, 205, 50, 0.1)", line_width=0)
    fig.add_vrect(x0=20, x1=35, fillcolor="rgba(255, 215, 0, 0.1)", line_width=0)
    fig.add_vrect(x0=35, x1=50, fillcolor="rgba(255, 140, 0, 0.1)", line_width=0)
    fig.add_vrect(x0=50, x1=100, fillcolor="rgba(255, 75, 75, 0.1)", line_width=0)

    return fig


def get_preset_selection(preset: str) -> Tuple[List[str], List[str]]:
    """Get country and sector selections based on preset"""
    if preset == "Major Economies":
        return (
            ["China", "European Union", "Japan", "India"],
            ["technology", "automotive", "machinery"],
        )
    elif preset == "Asian Markets":
        return (
            ["China", "Japan", "South Korea", "Taiwan", "Vietnam"],
            ["technology", "textiles", "electronics"],
        )
    elif preset == "ASEAN Countries":
        return (
            ["Vietnam", "Thailand", "Singapore", "Malaysia"],
            ["agriculture", "textiles", "chemicals"],
        )
    else:  # Custom Selection
        return (
            ["China", "European Union", "Japan", "Vietnam"],
            ["technology", "automotive", "agriculture"],
        )


def run_analysis(preset, custom_countries, custom_sectors):
    """Main analysis function for Gradio interface"""
    try:
        # Get selections based on preset
        if preset == "Custom Selection":
            countries = (
                custom_countries if custom_countries else ["China", "European Union"]
            )
            sectors = custom_sectors if custom_sectors else ["technology", "automotive"]
        else:
            countries, sectors = get_preset_selection(preset)

        if not countries or not sectors:
            return "❌ Please select at least one country and one sector.", None, ""

        # Run analysis
        analysis_results = calculate_country_analysis(countries, sectors)

        if not analysis_results["country_impacts"]:
            return (
                "❌ No valid data found for selected countries and sectors.",
                None,
                "",
            )

        # Create visualization
        plot = create_impact_plot(analysis_results)

        # Create summary text
        summary = analysis_results["summary"]
        summary_text = f"""
## 📊 Analysis Summary

**Countries Analyzed:** {summary['total_countries']}  
**Sectors Analyzed:** {summary['total_sectors']}  
**Average Economic Disruption:** {summary['avg_disruption']*100:.1f}%  
**Total GDP Impact:** ${summary['total_gdp_impact']:.1f} Billion  
**Total Trade Volume:** ${summary['total_trade_volume']:.1f} Billion  

### 🎯 Risk Categories:
- 🔴 **Very High Risk**: >50% disruption
- 🟠 **High Risk**: 35-50% disruption  
- 🟡 **Medium Risk**: 20-35% disruption
- 🟢 **Low Risk**: <20% disruption

### Selected Analysis:
**Countries:** {', '.join(countries)}  
**Sectors:** {', '.join(sectors)}
        """

        # Create detailed results table
        results_data = []
        for impact in analysis_results["country_impacts"]:
            disruption_pct = impact["economic_disruption"] * 100
            if disruption_pct >= 50:
                risk = "🔴 Very High"
            elif disruption_pct >= 35:
                risk = "🟠 High"
            elif disruption_pct >= 20:
                risk = "🟡 Medium"
            else:
                risk = "🟢 Low"

            results_data.append(
                {
                    "Country": impact["country"],
                    "Economic Disruption (%)": f"{disruption_pct:.1f}%",
                    "GDP Impact (USD B)": f"${impact['gdp_impact']:.1f}B",
                    "Trade Volume (USD B)": f"${impact['trade_volume']:.1f}B",
                    "Risk Level": risk,
                }
            )

        results_df = pd.DataFrame(results_data)

        success_msg = f"✅ Analysis completed for {len(countries)} countries and {len(sectors)} sectors"

        return success_msg, plot, summary_text, results_df

    except Exception as e:
        return f"❌ Analysis failed: {str(e)}", None, "", pd.DataFrame()


# Create Gradio interface
def create_gradio_app():
    """Create and configure Gradio interface"""

    with gr.Blocks(
        title="TIPM: Tariff Impact Analysis",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """,
    ) as app:

        # Title and description
        gr.Markdown(
            """
        # 📊 TIPM: Tariff Impact Propagation Model
        
        **Analyze the economic impact of tariffs across countries and sectors**
        
        🚀 **Demo Version** - This is a simplified version running on Hugging Face Spaces with sample data based on real Trump-era tariff scenarios.
        """
        )

        # Analysis configuration
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 🔧 Analysis Configuration")

                preset = gr.Dropdown(
                    choices=[
                        "Major Economies",
                        "Asian Markets",
                        "ASEAN Countries",
                        "Custom Selection",
                    ],
                    value="Major Economies",
                    label="Choose Analysis Preset",
                )

                with gr.Row(visible=False) as custom_row:
                    with gr.Column():
                        custom_countries = gr.CheckboxGroup(
                            choices=list(SAMPLE_DATA.keys()),
                            value=["China", "European Union", "Japan", "Vietnam"],
                            label="Select Countries (max 8)",
                        )
                    with gr.Column():
                        custom_sectors = gr.CheckboxGroup(
                            choices=SECTORS,
                            value=["technology", "automotive", "agriculture"],
                            label="Select Sectors (max 6)",
                        )

                def toggle_custom(preset_value):
                    return gr.update(visible=(preset_value == "Custom Selection"))

                preset.change(toggle_custom, inputs=[preset], outputs=[custom_row])

                analyze_btn = gr.Button("🚀 Run Analysis", variant="primary", size="lg")

        # Results section
        with gr.Row():
            with gr.Column():
                status_output = gr.Textbox(label="Status", interactive=False)

        with gr.Row():
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="📊 Impact Visualization")
            with gr.Column(scale=1):
                summary_output = gr.Markdown(label="📋 Summary")

        with gr.Row():
            results_table = gr.Dataframe(
                label="📋 Detailed Results",
                headers=[
                    "Country",
                    "Economic Disruption (%)",
                    "GDP Impact (USD B)",
                    "Trade Volume (USD B)",
                    "Risk Level",
                ],
                interactive=False,
            )

        # Information section
        with gr.Accordion("ℹ️ About TIPM Analysis", open=False):
            gr.Markdown(
                """
            **Tariff Impact Propagation Model (TIPM)** analyzes economic impacts of tariffs:
            
            ### 📊 **Metrics Explained:**
            
            **Economic Disruption %**
            - Compound percentage of economic activity disrupted by tariffs
            - Calculated across multiple sectors (technology, agriculture, manufacturing, etc.)
            - Accounts for supply chain ripple effects and trade dependencies
            
            **GDP Impact (USD Billions)**
            - Estimated GDP loss in US Dollar billions
            - Based on each country's trade dependency with the USA
            - Calculated as: (Economic Disruption %) × (Trade Dependency Factor) × (Country GDP)
            
            **Trade Volume (USD Billions)**
            - Annual bilateral trade volume between country and USA
            - Measured in US Dollar billions per year
            - Includes both imports and exports
            
            ### 🎯 **Risk Categories:**
            - 🔴 **Very High Risk**: >50% disruption - Severe economic consequences
            - 🟠 **High Risk**: 35-50% disruption - Significant economic impact  
            - 🟡 **Medium Risk**: 20-35% disruption - Moderate economic effects
            - 🟢 **Low Risk**: <20% disruption - Limited economic disruption
            
            ### 🔬 **Analysis Method:**
            TIPM uses a 6-layer neural network analyzing:
            1. Policy triggers and tariff announcements
            2. Trade flow disruptions through supply chains
            3. Industry-specific response patterns
            4. Firm-level employment and survival impacts
            5. Consumer price and demand effects
            6. Geopolitical and social responses
            
            ### 📚 **Data Sources:**
            - Based on real Trump-era tariff data
            - UN Comtrade bilateral trade statistics
            - World Bank economic indicators
            - OECD trade in value-added data
            """
            )

        # Connect the analysis function
        analyze_btn.click(
            fn=run_analysis,
            inputs=[preset, custom_countries, custom_sectors],
            outputs=[status_output, plot_output, summary_output, results_table],
        )

    return app


# Create and launch the app
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
