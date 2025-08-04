#!/usr/bin/env python3
"""
TIPM Clear Visualization Demo - Debugged and Fixed
Shows exactly where each country falls on the impact scale
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

st.set_page_config(
    page_title="TIPM: Clear Impact Analysis", page_icon="🎯", layout="wide"
)


def create_clear_impact_visualization(analysis_results: Dict):
    """Create clear visualizations that show exactly where each country falls"""

    # Debug: Show what data we received
    st.write("**Debug - Analysis Results Structure:**")
    st.write(f"Keys in analysis_results: {list(analysis_results.keys())}")

    if "country_impacts" not in analysis_results:
        st.error("No 'country_impacts' key found in analysis results")
        st.write("Available keys:", list(analysis_results.keys()))
        return

    if not analysis_results["country_impacts"]:
        st.error("country_impacts is empty")
        return

    # Extract and prepare data
    country_data = []
    st.write(
        f"**Debug - Processing {len(analysis_results['country_impacts'])} countries:**"
    )

    for country, data in analysis_results["country_impacts"].items():
        st.write(
            f"Country: {country}, Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}"
        )

        if not isinstance(data, dict):
            st.warning(f"Data for {country} is not a dictionary: {type(data)}")
            continue

        if "average_impact" not in data:
            st.warning(f"No 'average_impact' found for {country}")
            continue

        impact = data["average_impact"]

        # Determine risk category
        if impact > 0.5:
            risk_category = "Very High Risk"
            color = "#8B0000"
        elif impact > 0.35:
            risk_category = "High Risk"
            color = "#FF0000"
        elif impact > 0.2:
            risk_category = "Medium Risk"
            color = "#FFA500"
        elif impact > 0.1:
            risk_category = "Low Risk"
            color = "#FFD700"
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
        st.error("No valid country data could be extracted")
        return

    df = pd.DataFrame(country_data).sort_values("Impact", ascending=False)
    st.write(f"**Debug - Created DataFrame with {len(df)} rows:**")
    st.write(df.head())

    st.subheader("🎯 Clear Country Impact Analysis")

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["📊 Country Impact Chart", "📋 Detailed Table", "🎚️ Interactive Filter"]
    )

    with tab1:
        st.markdown("**Every country shown with exact impact value and position**")

        # Create a clear scatter plot showing each country
        fig = go.Figure()

        # Add each country as a point
        for _, row in df.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[row["Impact"]],
                    y=[row["Country"]],
                    mode="markers+text",
                    marker=dict(
                        size=15, color=row["Color"], line=dict(width=2, color="white")
                    ),
                    text=row["Impact_Percent"],
                    textposition="middle right",
                    textfont=dict(size=12, color="black"),
                    name=row["Country"],
                    showlegend=False,
                )
            )

        # Add threshold lines
        fig.add_vline(
            x=0.5,
            line_dash="dash",
            line_color="red",
            annotation_text="Very High Risk Threshold (50%)",
        )
        fig.add_vline(
            x=0.35,
            line_dash="dash",
            line_color="orange",
            annotation_text="High Risk Threshold (35%)",
        )
        fig.add_vline(
            x=0.2,
            line_dash="dash",
            line_color="yellow",
            annotation_text="Medium Risk Threshold (20%)",
        )
        fig.add_vline(
            x=0.1,
            line_dash="dash",
            line_color="lightgreen",
            annotation_text="Low Risk Threshold (10%)",
        )

        fig.update_layout(
            title="Country Impact Positioning - Exact Values and Risk Categories",
            xaxis_title="Impact Level",
            yaxis_title="Countries",
            height=400 + len(df) * 30,
            xaxis=dict(tickformat=".1%"),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            very_high = len(df[df["Risk_Category"] == "Very High Risk"])
            st.metric("Very High Risk", very_high, help=">50% impact")

        with col2:
            high = len(df[df["Risk_Category"] == "High Risk"])
            st.metric("High Risk", high, help="35-50% impact")

        with col3:
            medium = len(df[df["Risk_Category"] == "Medium Risk"])
            st.metric("Medium Risk", medium, help="20-35% impact")

        with col4:
            low = len(df[df["Risk_Category"] == "Low Risk"])
            very_low = len(df[df["Risk_Category"] == "Very Low Risk"])
            st.metric("Low + Very Low Risk", low + very_low, help="<20% impact")

    with tab2:
        st.markdown("**Complete country rankings with all details**")

        # Create a comprehensive table
        display_df = df[
            ["Country", "Impact_Percent", "Risk_Category", "GDP_Loss", "Trade_Volume"]
        ].copy()
        display_df.columns = [
            "Country",
            "Impact %",
            "Risk Category",
            "GDP Loss Estimate",
            "Trade Volume",
        ]

        # Show the data
        st.dataframe(display_df, use_container_width=True, height=400)

        # Export option
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Country Data (CSV)",
            data=csv,
            file_name="tipm_country_impacts.csv",
            mime="text/csv",
        )

    with tab3:
        st.markdown("**Interactive analysis - adjust threshold to see impacts**")

        # Interactive threshold slider - FIXED FORMAT
        threshold = st.slider(
            "Select Impact Threshold:",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            format="%.1f%%",  # FIXED: Added 'f' before %%
        )

        # Filter countries above threshold
        above_threshold = df[df["Impact"] > threshold]
        below_threshold = df[df["Impact"] <= threshold]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Above {threshold:.0%} Threshold")
            st.metric("Countries Affected", len(above_threshold))

            if len(above_threshold) > 0:
                st.write("**Countries:**")
                for _, row in above_threshold.iterrows():
                    st.write(
                        f"• **{row['Country']}**: {row['Impact_Percent']} ({row['Risk_Category']})"
                    )

                # Show total impact
                total_gdp_loss = above_threshold["GDP_Loss"].sum()
                total_trade = above_threshold["Trade_Volume"].sum()
                st.metric("Total GDP Loss", f"{total_gdp_loss:.1f}")
                st.metric("Total Trade Volume", f"{total_trade:.1f}")

        with col2:
            st.subheader(f"Below {threshold:.0%} Threshold")
            st.metric("Countries Safe", len(below_threshold))

            if len(below_threshold) > 0:
                avg_impact_below = below_threshold["Impact"].mean()
                st.metric("Average Impact Below", f"{avg_impact_below:.1%}")

                # Show distribution of safe countries
                safe_categories = below_threshold["Risk_Category"].value_counts()
                st.write("**Safe Country Distribution:**")
                for category, count in safe_categories.items():
                    st.write(f"• {category}: {count} countries")


def main():
    """Main application with clear, error-free visualizations"""

    st.title("🎯 TIPM: Clear Impact Analysis")
    st.markdown("**Shows exactly where each country falls on the impact scale**")

    if not ENHANCED_AVAILABLE:
        st.error("Enhanced TIPM modules not available.")
        return

    # Simple sidebar setup
    st.sidebar.header("🔧 Analysis Setup")

    try:
        manager = EnhancedTariffDataManager()
        all_countries = list(manager.get_available_countries())
        all_sectors = list(manager.get_available_sectors())

        st.sidebar.write(f"Available countries: {len(all_countries)}")
        st.sidebar.write(f"Available sectors: {len(all_sectors)}")

    except Exception as e:
        st.error(f"Error initializing: {e}")
        st.exception(e)
        return

    # Quick preset selection
    preset = st.sidebar.selectbox(
        "Choose Analysis:",
        ["BRICS Countries", "Major Economies", "Asian Tigers", "Custom Selection"],
    )

    if preset == "BRICS Countries":
        countries = ["Brazil", "India", "China", "South Africa"]  # Russia not available
        sectors = ["technology", "agriculture", "metals"]
    elif preset == "Major Economies":
        countries = [
            "China",
            "European Union",
            "Japan",
            "United Kingdom",
            "Brazil",
            "India",
        ]
        sectors = ["technology", "automotive", "machinery"]
    elif preset == "Asian Tigers":
        countries = ["South Korea", "Taiwan", "Singapore", "Thailand"]
        sectors = ["technology", "chemicals", "machinery"]
    else:
        # Use only countries that actually exist in the data
        valid_defaults = []
        preferred = ["China", "European Union", "Japan", "Vietnam", "India"]
        for country in preferred:
            if country in all_countries:
                valid_defaults.append(country)

        countries = st.sidebar.multiselect(
            "Select Countries:",
            all_countries,
            default=valid_defaults[:5],  # Take first 5 valid countries
        )
        sectors = st.sidebar.multiselect(
            "Select Sectors:",
            all_sectors,
            default=(
                all_sectors[:3] if len(all_sectors) >= 3 else all_sectors
            ),  # Use actual available sectors
        )

    if st.sidebar.button("🚀 Run Clear Analysis", type="primary"):
        if not countries or not sectors:
            st.error("Please select countries and sectors.")
            return

        try:
            with st.spinner("Running analysis..."):
                st.write(f"**Debug - Analyzing:** {countries} with sectors {sectors}")
                analysis_results = manager.get_sector_analysis(countries, sectors)

            st.success(
                f"✅ Analysis completed for {len(countries)} countries and {len(sectors)} sectors"
            )

            # Show the clear visualizations
            create_clear_impact_visualization(analysis_results)

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.exception(e)

    # Educational content
    with st.expander("💡 Why This Approach Is Better"):
        st.markdown(
            """
        ### Problems Solved:
        
        1. **🎯 Clear Country Positioning**: Every country is labeled with exact impact value
        2. **📊 Visual Risk Boundaries**: Threshold lines show exactly what constitutes each risk level  
        3. **🔍 Interactive Exploration**: Adjust thresholds to see immediate impact on country classifications
        4. **📋 Complete Data**: Full table with all metrics for detailed analysis
        5. **⚡ No JavaScript Errors**: Simple, reliable visualizations that always work
        6. **🐛 Debug Information**: Shows data structure for troubleshooting
        
        ### Key Improvements:
        
        - **Country Labels**: See exactly which country has what impact
        - **Threshold Lines**: Clear visual boundaries for risk categories
        - **Interactive Filtering**: Explore different policy scenarios
        - **Comprehensive Data**: GDP loss, trade volume, risk categories all visible
        - **Export Capability**: Download data for further analysis
        - **Error Handling**: Clear error messages and debugging info
        
        This approach gives policymakers the exact information they need to make informed decisions.
        """
        )


if __name__ == "__main__":
    main()
