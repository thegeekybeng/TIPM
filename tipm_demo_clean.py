#!/usr/bin/env python3
"""
TIPM Clean Demo - Simple and Effective
Shows clear country impact analysis without clutter
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List
import os
import sys

# Add the TIPM module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tipm.enhanced_config import EnhancedTariffDataManager

    ENHANCED_AVAILABLE = True
except ImportError as e:
    st.error(f"Enhanced TIPM modules not available: {e}")
    ENHANCED_AVAILABLE = False

st.set_page_config(page_title="TIPM Analysis", page_icon="📊", layout="wide")


def create_impact_visualization(analysis_results: Dict):
    """Create clean, meaningful visualizations"""

    if (
        "country_impacts" not in analysis_results
        or not analysis_results["country_impacts"]
    ):
        st.error("No country impact data available.")
        return

    # Extract data cleanly
    country_data = []
    for country, data in analysis_results["country_impacts"].items():
        if isinstance(data, dict) and "average_impact" in data:
            impact = data["average_impact"]

            # Risk categories
            if impact > 0.5:
                risk_category = "Very High Risk"
                color = "#FF0000"
            elif impact > 0.35:
                risk_category = "High Risk"
                color = "#FF8C00"
            elif impact > 0.2:
                risk_category = "Medium Risk"
                color = "#FFD700"
            elif impact > 0.1:
                risk_category = "Low Risk"
                color = "#90EE90"
            else:
                risk_category = "Very Low Risk"
                color = "#008000"

            country_data.append(
                {
                    "Country": country,
                    "Impact": impact,
                    "Impact_Percent": f"{impact:.1%}",
                    "Risk_Category": risk_category,
                    "Color": color,
                    "GDP_Loss": data.get("estimated_gdp_loss", 0),
                    "Trade_Volume": data.get("trade_volume", 0),
                }
            )

    if not country_data:
        st.error("No valid country data found")
        return

    df = pd.DataFrame(country_data).sort_values("Impact", ascending=False)

    # Main visualization
    st.subheader("📊 Country Impact Analysis")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Create horizontal bar chart
        fig = go.Figure()

        for _, row in df.iterrows():
            fig.add_trace(
                go.Bar(
                    y=[row["Country"]],
                    x=[row["Impact"]],
                    orientation="h",
                    marker_color=row["Color"],
                    text=row["Impact_Percent"],
                    textposition="auto",
                    name=row["Country"],
                    showlegend=False,
                )
            )

        # Add threshold lines
        fig.add_vline(x=0.5, line_dash="dash", line_color="red", line_width=2)
        fig.add_vline(x=0.35, line_dash="dash", line_color="orange", line_width=1)
        fig.add_vline(x=0.2, line_dash="dash", line_color="gold", line_width=1)

        fig.update_layout(
            title="Tariff Impact by Country",
            xaxis_title="Impact Level",
            yaxis_title="Countries",
            height=400,
            xaxis=dict(tickformat=".1%"),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Risk summary
        st.markdown("**Risk Summary**")

        very_high = len(df[df["Risk_Category"] == "Very High Risk"])
        high = len(df[df["Risk_Category"] == "High Risk"])
        medium = len(df[df["Risk_Category"] == "Medium Risk"])
        low_total = len(df[df["Risk_Category"].isin(["Low Risk", "Very Low Risk"])])

        st.metric("Very High Risk", very_high, help=">50% impact")
        st.metric("High Risk", high, help="35-50% impact")
        st.metric("Medium Risk", medium, help="20-35% impact")
        st.metric("Low Risk", low_total, help="<20% impact")

    # Data table
    st.subheader("📋 Detailed Results")

    # Create properly labeled dataframe with clear units
    display_df = df[
        ["Country", "Impact_Percent", "Risk_Category", "GDP_Loss", "Trade_Volume"]
    ].copy()
    display_df.columns = [
        "Country",
        "Economic Disruption %",
        "Risk Category",
        "GDP Impact (USD Billions)",
        "Trade Volume (USD Billions)",
    ]

    # Add explanation of metrics
    st.markdown(
        """
    **Column Explanations:**
    - **Economic Disruption %**: Percentage of economic activity disrupted by tariffs (compound effect across sectors)
    - **GDP Impact**: Estimated GDP loss in USD billions based on trade dependency and tariff levels
    - **Trade Volume**: Bilateral trade volume with USA in USD billions annually
    """
    )

    st.dataframe(display_df, use_container_width=True, height=300)

    # Export
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📄 Download Results (CSV)",
        data=csv,
        file_name="tipm_analysis_results.csv",
        mime="text/csv",
    )


def main():
    """Main application"""

    st.title("📊 TIPM: Tariff Impact Analysis")
    st.markdown(
        "**Analyze the economic impact of tariffs across countries and sectors**"
    )

    if not ENHANCED_AVAILABLE:
        st.error("TIPM modules not available. Please check installation.")
        return

    # Sidebar setup
    st.sidebar.header("🔧 Analysis Configuration")

    try:
        manager = EnhancedTariffDataManager()
        all_countries = list(manager.get_available_countries())
        all_sectors = list(manager.get_available_sectors())

    except Exception as e:
        st.error(f"Error initializing TIPM: {e}")
        return

    # Preset analysis options
    preset = st.sidebar.selectbox(
        "Choose Analysis:",
        ["Major Economies", "BRICS Countries", "Asian Markets", "Custom Selection"],
    )

    if preset == "Major Economies":
        default_countries = ["China", "European Union", "Japan", "United Kingdom"]
        default_sectors = ["technology", "automotive", "machinery"]
    elif preset == "BRICS Countries":
        default_countries = ["Brazil", "India", "China", "South Africa"]
        default_sectors = ["technology", "agriculture", "metals"]
    elif preset == "Asian Markets":
        default_countries = ["China", "Japan", "South Korea", "Taiwan", "Vietnam"]
        default_sectors = ["technology", "textiles", "chemicals"]
    else:
        # Custom selection
        default_countries = ["China", "European Union", "Japan", "Vietnam"][:4]
        default_sectors = ["technology", "automotive", "agriculture"]

    # Filter to only available countries/sectors
    valid_countries = [c for c in default_countries if c in all_countries]
    valid_sectors = [s for s in default_sectors if s in all_sectors]

    if preset == "Custom Selection":
        countries = st.sidebar.multiselect(
            "Select Countries:",
            all_countries,
            default=valid_countries,
            max_selections=8,
        )
        sectors = st.sidebar.multiselect(
            "Select Sectors:", all_sectors, default=valid_sectors, max_selections=6
        )
    else:
        countries = valid_countries
        sectors = valid_sectors
        st.sidebar.write(f"**Countries:** {', '.join(countries)}")
        st.sidebar.write(f"**Sectors:** {', '.join(sectors)}")

    # Run analysis
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        if not countries or not sectors:
            st.error("Please select at least one country and one sector.")
            return

        try:
            with st.spinner(
                f"Analyzing {len(countries)} countries across {len(sectors)} sectors..."
            ):
                analysis_results = manager.get_sector_analysis(countries, sectors)

            st.success(
                f"✅ Analysis completed for {len(countries)} countries and {len(sectors)} sectors"
            )

            # Show results
            create_impact_visualization(analysis_results)

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.exception(e)

    # Information section
    with st.expander("ℹ️ About TIPM Analysis"):
        st.markdown(
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
        TIMP uses a 6-layer neural network analyzing:
        1. Policy triggers and tariff announcements
        2. Trade flow disruptions through supply chains
        3. Industry-specific response patterns
        4. Firm-level employment and survival impacts
        5. Consumer price and demand effects
        6. Geopolitical and social responses
        """
        )


if __name__ == "__main__":
    main()
