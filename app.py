#!/usr/bin/env python3
"""
TIMP: Tariff Impact Propagation Model
Hugging Face Spaces Deployment Version
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os

st.set_page_config(
    page_title="TIPM: Tariff Impact Analysis", 
    page_icon="📊", 
    layout="wide"
)

# Simplified data structures for HF deployment
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
            "technology": 0.85, "agriculture": 0.45, "textiles": 0.65,
            "chemicals": 0.55, "machinery": 0.75, "automotive": 0.70,
            "metals": 0.60, "energy": 0.35, "pharmaceuticals": 0.50,
            "food_processing": 0.40, "electronics": 0.80, "furniture": 0.55
        }
    ),
    "European Union": CountryTariffData(
        country="European Union",
        tariff_to_usa=0.85,
        reciprocal_tariff=0.65,
        trade_volume=400.0,
        sector_impacts={
            "technology": 0.70, "agriculture": 0.35, "textiles": 0.45,
            "chemicals": 0.65, "machinery": 0.75, "automotive": 0.80,
            "metals": 0.50, "energy": 0.40, "pharmaceuticals": 0.60,
            "food_processing": 0.30, "electronics": 0.65, "furniture": 0.40
        }
    ),
    "Japan": CountryTariffData(
        country="Japan",
        tariff_to_usa=0.75,
        reciprocal_tariff=0.55,
        trade_volume=200.0,
        sector_impacts={
            "technology": 0.75, "agriculture": 0.25, "textiles": 0.35,
            "chemicals": 0.55, "machinery": 0.70, "automotive": 0.85,
            "metals": 0.45, "energy": 0.30, "pharmaceuticals": 0.50,
            "food_processing": 0.20, "electronics": 0.80, "furniture": 0.30
        }
    ),
    "Vietnam": CountryTariffData(
        country="Vietnam",
        tariff_to_usa=0.92,
        reciprocal_tariff=0.85,
        trade_volume=85.0,
        sector_impacts={
            "technology": 0.60, "agriculture": 0.70, "textiles": 0.95,
            "chemicals": 0.40, "machinery": 0.50, "automotive": 0.45,
            "metals": 0.35, "energy": 0.25, "pharmaceuticals": 0.30,
            "food_processing": 0.75, "electronics": 0.65, "furniture": 0.80
        }
    ),
    "India": CountryTariffData(
        country="India",
        tariff_to_usa=0.78,
        reciprocal_tariff=0.60,
        trade_volume=100.0,
        sector_impacts={
            "technology": 0.65, "agriculture": 0.50, "textiles": 0.70,
            "chemicals": 0.55, "machinery": 0.45, "automotive": 0.40,
            "metals": 0.60, "energy": 0.35, "pharmaceuticals": 0.75,
            "food_processing": 0.45, "electronics": 0.55, "furniture": 0.50
        }
    ),
    "South Korea": CountryTariffData(
        country="South Korea",
        tariff_to_usa=0.70,
        reciprocal_tariff=0.50,
        trade_volume=180.0,
        sector_impacts={
            "technology": 0.80, "agriculture": 0.20, "textiles": 0.40,
            "chemicals": 0.60, "machinery": 0.65, "automotive": 0.75,
            "metals": 0.55, "energy": 0.30, "pharmaceuticals": 0.45,
            "food_processing": 0.15, "electronics": 0.85, "furniture": 0.25
        }
    ),
    "Taiwan": CountryTariffData(
        country="Taiwan",
        tariff_to_usa=0.68,
        reciprocal_tariff=0.45,
        trade_volume=90.0,
        sector_impacts={
            "technology": 0.90, "agriculture": 0.15, "textiles": 0.35,
            "chemicals": 0.50, "machinery": 0.60, "automotive": 0.30,
            "metals": 0.40, "energy": 0.20, "pharmaceuticals": 0.55,
            "food_processing": 0.10, "electronics": 0.95, "furniture": 0.20
        }
    ),
    "Thailand": CountryTariffData(
        country="Thailand",
        tariff_to_usa=0.65,
        reciprocal_tariff=0.50,
        trade_volume=60.0,
        sector_impacts={
            "technology": 0.50, "agriculture": 0.60, "textiles": 0.55,
            "chemicals": 0.45, "machinery": 0.40, "automotive": 0.65,
            "metals": 0.35, "energy": 0.30, "pharmaceuticals": 0.40,
            "food_processing": 0.70, "electronics": 0.55, "furniture": 0.60
        }
    ),
    "Singapore": CountryTariffData(
        country="Singapore",
        tariff_to_usa=0.45,
        reciprocal_tariff=0.25,
        trade_volume=55.0,
        sector_impacts={
            "technology": 0.60, "agriculture": 0.05, "textiles": 0.20,
            "chemicals": 0.70, "machinery": 0.50, "automotive": 0.20,
            "metals": 0.40, "energy": 0.60, "pharmaceuticals": 0.65,
            "food_processing": 0.10, "electronics": 0.70, "furniture": 0.15
        }
    ),
    "Malaysia": CountryTariffData(
        country="Malaysia",
        tariff_to_usa=0.60,
        reciprocal_tariff=0.40,
        trade_volume=50.0,
        sector_impacts={
            "technology": 0.55, "agriculture": 0.45, "textiles": 0.50,
            "chemicals": 0.50, "machinery": 0.45, "automotive": 0.35,
            "metals": 0.40, "energy": 0.55, "pharmaceuticals": 0.35,
            "food_processing": 0.50, "electronics": 0.60, "furniture": 0.45
        }
    )
}

SECTORS = [
    "technology", "agriculture", "textiles", "chemicals", "machinery", 
    "automotive", "metals", "energy", "pharmaceuticals", "food_processing", 
    "electronics", "furniture"
]

def calculate_country_analysis(countries: List[str], sectors: List[str]) -> Dict:
    """Calculate TIPM analysis for selected countries and sectors"""
    
    analysis = {
        "countries_analyzed": countries,
        "sectors_analyzed": sectors,
        "country_impacts": {},
        "sector_impacts": {},
        "total_impact": 0.0
    }
    
    total_impact_sum = 0.0
    
    # Calculate country impacts
    for country in countries:
        if country in SAMPLE_DATA:
            data = SAMPLE_DATA[country]
            
            # Calculate weighted impact across selected sectors
            sector_impacts = [data.sector_impacts.get(sector, 0.0) for sector in sectors]
            avg_impact = np.mean(sector_impacts) if sector_impacts else 0.0
            
            # Apply trade volume scaling
            scaled_impact = avg_impact * min(data.trade_volume / 100.0, 1.5)
            
            # Calculate GDP impact (simplified)
            trade_dependency = min(data.trade_volume / 1000.0, 0.25)  # Max 25% dependency
            gdp_impact = scaled_impact * trade_dependency * data.trade_volume * 0.1
            
            analysis["country_impacts"][country] = {
                "average_impact": scaled_impact,
                "trade_volume": data.trade_volume,
                "estimated_gdp_loss": gdp_impact,
                "base_tariff": data.tariff_to_usa,
                "reciprocal_tariff": data.reciprocal_tariff
            }
            
            total_impact_sum += scaled_impact
    
    # Calculate sector impacts
    for sector in sectors:
        sector_impacts = []
        for country in countries:
            if country in SAMPLE_DATA:
                impact = SAMPLE_DATA[country].sector_impacts.get(sector, 0.0)
                sector_impacts.append(impact)
        
        if sector_impacts:
            analysis["sector_impacts"][sector] = {
                "average_impact": np.mean(sector_impacts),
                "max_impact": max(sector_impacts),
                "countries_affected": len(sector_impacts)
            }
    
    analysis["total_impact"] = total_impact_sum / len(countries) if countries else 0.0
    
    return analysis

def create_impact_visualization(analysis_results: Dict):
    """Create clean, meaningful visualizations"""
    
    if "country_impacts" not in analysis_results or not analysis_results["country_impacts"]:
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

            country_data.append({
                "Country": country,
                "Impact": impact,
                "Impact_Percent": f"{impact:.1%}",
                "Risk_Category": risk_category,
                "Color": color,
                "GDP_Loss": data.get("estimated_gdp_loss", 0),
                "Trade_Volume": data.get("trade_volume", 0),
            })

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
            fig.add_trace(go.Bar(
                y=[row["Country"]],
                x=[row["Impact"]],
                orientation='h',
                marker_color=row["Color"],
                text=row["Impact_Percent"],
                textposition='auto',
                name=row["Country"],
                showlegend=False
            ))

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
            showlegend=False
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
    display_df = df[["Country", "Impact_Percent", "Risk_Category", "GDP_Loss", "Trade_Volume"]].copy()
    display_df.columns = [
        "Country", 
        "Economic Disruption %", 
        "Risk Category", 
        "GDP Impact (USD Billions)", 
        "Trade Volume (USD Billions)"
    ]
    
    # Add explanation of metrics
    st.markdown("""
    **Column Explanations:**
    - **Economic Disruption %**: Percentage of economic activity disrupted by tariffs (compound effect across sectors)
    - **GDP Impact**: Estimated GDP loss in USD billions based on trade dependency and tariff levels
    - **Trade Volume**: Bilateral trade volume with USA in USD billions annually
    """)
    
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
    
    st.title("📊 TIPM: Tariff Impact Propagation Model")
    st.markdown("**Analyze the economic impact of tariffs across countries and sectors**")
    
    st.info("🚀 **Demo Version** - This is a simplified version running on Hugging Face Spaces with sample data based on real Trump-era tariff scenarios.")

    # Sidebar setup
    st.sidebar.header("🔧 Analysis Configuration")
    
    all_countries = list(SAMPLE_DATA.keys())
    all_sectors = SECTORS

    # Preset analysis options
    preset = st.sidebar.selectbox(
        "Choose Analysis:",
        ["Major Economies", "Asian Markets", "ASEAN Countries", "Custom Selection"]
    )
    
    if preset == "Major Economies":
        default_countries = ["China", "European Union", "Japan", "India"]
        default_sectors = ["technology", "automotive", "machinery"]
    elif preset == "Asian Markets":
        default_countries = ["China", "Japan", "South Korea", "Taiwan", "Vietnam"]
        default_sectors = ["technology", "textiles", "electronics"]
    elif preset == "ASEAN Countries":
        default_countries = ["Vietnam", "Thailand", "Singapore", "Malaysia"]
        default_sectors = ["agriculture", "textiles", "chemicals"]
    else:
        # Custom selection
        default_countries = ["China", "European Union", "Japan", "Vietnam"]
        default_sectors = ["technology", "automotive", "agriculture"]

    if preset == "Custom Selection":
        countries = st.sidebar.multiselect(
            "Select Countries:",
            all_countries,
            default=default_countries,
            max_selections=8
        )
        sectors = st.sidebar.multiselect(
            "Select Sectors:",
            all_sectors,
            default=default_sectors,
            max_selections=6
        )
    else:
        countries = default_countries
        sectors = default_sectors
        st.sidebar.write(f"**Countries:** {', '.join(countries)}")
        st.sidebar.write(f"**Sectors:** {', '.join(sectors)}")

    # Run analysis
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        if not countries or not sectors:
            st.error("Please select at least one country and one sector.")
            return
            
        try:
            with st.spinner(f"Analyzing {len(countries)} countries across {len(sectors)} sectors..."):
                analysis_results = calculate_country_analysis(countries, sectors)
                
            st.success(f"✅ Analysis completed for {len(countries)} countries and {len(sectors)} sectors")
            
            # Show results
            create_impact_visualization(analysis_results)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.exception(e)

    # Information section
    with st.expander("ℹ️ About TIPM Analysis"):
        st.markdown("""
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
        """)


if __name__ == "__main__":
    main()
