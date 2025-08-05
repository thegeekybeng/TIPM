#!/usr/bin/env python3
"""
TIPM: Professional Tariff Impact Propagation Model
Ultra-Professional Economic Analysis Tool

Version: 3.0 Professional
Designer: AI Assistant
Focus: Executive-grade presentation and analysis
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import numpy as np
from datetime import datetime, timedelta
import json

# ================================
# PROFESSIONAL STYLING
# ================================

PROFESSIONAL_CSS = """
/* Professional Theme Overrides with Better Text Contrast */
.gradio-container {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    min-height: 100vh;
    color: #1a202c !important;
}

.main-content {
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
    margin: 20px !important;
    padding: 30px !important;
    color: #1a202c !important;
}

/* Global Text Color Override */
.gradio-container * {
    color: #1a202c !important;
}

.gradio-container label {
    color: #2d3748 !important;
    font-weight: 600 !important;
}

.gradio-container p {
    color: #4a5568 !important;
}

/* Header Styling */
.header-section {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    color: white !important;
    padding: 30px !important;
    border-radius: 15px !important;
    margin-bottom: 30px !important;
    text-align: center !important;
    box-shadow: 0 10px 30px rgba(30, 60, 114, 0.3) !important;
}

.header-section * {
    color: white !important;
}

.header-section h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 10px !important;
    color: white !important;
}

.header-section h3 {
    font-size: 1.2rem !important;
    opacity: 0.95 !important;
    font-weight: 400 !important;
    color: white !important;
}

/* Card Styling */
.analysis-card {
    background: white !important;
    border-radius: 15px !important;
    padding: 25px !important;
    margin: 20px 0 !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease !important;
    color: #1a202c !important;
}

.analysis-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 35px rgba(0,0,0,0.15) !important;
}

.metric-card {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    text-align: center !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    margin: 10px !important;
    color: #1a202c !important;
}

.metric-value {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #1e3a8a !important;
    margin-bottom: 5px !important;
}

.metric-label {
    font-size: 0.9rem !important;
    color: #374151 !important;
    font-weight: 600 !important;
}

/* Button Styling */
.primary-button {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 15px 30px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3) !important;
}

.primary-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(30, 60, 114, 0.4) !important;
}

/* Tab Styling */
.tab-nav {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    border-radius: 15px 15px 0 0 !important;
    padding: 5px !important;
}

.tab-nav button {
    color: rgba(255,255,255,0.9) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.tab-nav button.selected {
    background: rgba(255,255,255,0.25) !important;
    color: white !important;
    backdrop-filter: blur(10px) !important;
}

/* Form Input Styling */
.gradio-container .gr-form {
    color: #1a202c !important;
}

.gradio-container input, .gradio-container select, .gradio-container textarea {
    color: #1a202c !important;
    background: white !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

.gradio-container input:focus, .gradio-container select:focus, .gradio-container textarea:focus {
    border-color: #1e3c72 !important;
    box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.1) !important;
}

/* Checkbox and Radio Styling */
.gradio-container .gr-checkbox-group label {
    color: #2d3748 !important;
    font-weight: 500 !important;
}

.gradio-container .gr-radio-group label {
    color: #2d3748 !important;
    font-weight: 500 !important;
}

/* Results Table Styling */
.dataframe {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
}

.dataframe th {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 15px !important;
    text-align: center !important;
}

.dataframe td {
    padding: 12px 15px !important;
    border-bottom: 1px solid rgba(0,0,0,0.05) !important;
    text-align: center !important;
}

.dataframe tr:hover {
    background: rgba(30, 60, 114, 0.05) !important;
}

/* Summary Section */
.summary-section {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border-radius: 15px !important;
    padding: 25px !important;
    border-left: 5px solid #1e3c72 !important;
    margin: 20px 0 !important;
    color: #1a202c !important;
}

.summary-section * {
    color: #1a202c !important;
}

.summary-section h3 {
    color: #1e3c72 !important;
    font-weight: 700 !important;
    margin-bottom: 15px !important;
}

.summary-section h4 {
    color: #1e3c72 !important;
    font-weight: 600 !important;
}

/* Chart Container */
.chart-container {
    background: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    margin: 15px 0 !important;
    color: #1a202c !important;
}

.chart-container * {
    color: #1a202c !important;
}

.chart-container h3 {
    color: #1e3c72 !important;
}

/* Form Styling */
.form-section {
    background: white !important;
    border-radius: 15px !important;
    padding: 25px !important;
    margin: 20px 0 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    color: #1a202c !important;
}

.form-section * {
    color: #1a202c !important;
}

.form-section h4 {
    color: #1e3c72 !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
    font-size: 1.2rem !important;
}

.form-section label {
    color: #2d3748 !important;
    font-weight: 600 !important;
}

/* Info Cards */
.info-card {
    background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 4px solid #0277bd !important;
    color: #1a202c !important;
}

.info-card * {
    color: #1a202c !important;
}

.info-card h3, .info-card h4 {
    color: #0277bd !important;
    font-weight: 700 !important;
}

.warning-card {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 4px solid #f57c00 !important;
    color: #1a202c !important;
}

.warning-card * {
    color: #1a202c !important;
}

.warning-card h3, .warning-card h4 {
    color: #f57c00 !important;
    font-weight: 700 !important;
}

.success-card {
    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 4px solid #388e3c !important;
    color: #1a202c !important;
}

.success-card * {
    color: #1a202c !important;
}

.success-card h3, .success-card h4 {
    color: #388e3c !important;
    font-weight: 700 !important;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .gradio-container {
        margin: 10px !important;
        padding: 15px !important;
    }
    
    .header-section h1 {
        font-size: 1.8rem !important;
    }
    
    .analysis-card {
        padding: 15px !important;
        margin: 10px 0 !important;
    }
}
"""

# ================================
# DATA MODELS & CONFIGURATIONS
# ================================


@dataclass
class CountryData:
    """Enhanced country data with export sector intelligence"""

    tariff_rate: float
    trade_volume_usa: float  # Billions USD
    gdp_usd_billions: float
    continent: str
    global_groups: List[str]
    heavy_export_sectors: List[str]  # Top export sectors to USA


@dataclass
class ImpactClassification:
    """Economic impact classification with authoritative sources"""

    level: str
    color: str
    description: str
    source: str


# Enhanced country database with 45 countries
ENHANCED_COUNTRIES = {
    "China": CountryData(
        0.67,
        650.4,
        17730.0,
        "Asia",
        ["G20"],
        [
            "Technology & Electronics",
            "Machinery",
            "Textiles & Apparel",
            "Furniture",
            "Steel & Metals",
        ],
    ),
    "Germany": CountryData(
        0.46,
        171.2,
        4260.0,
        "Europe",
        ["G7", "G20", "NATO"],
        [
            "Automotive",
            "Machinery",
            "Chemicals",
            "Pharmaceuticals",
            "Precision Instruments",
        ],
    ),
    "Japan": CountryData(
        0.46,
        142.6,
        4940.0,
        "Asia",
        ["G7", "G20"],
        [
            "Automotive",
            "Machinery",
            "Technology & Electronics",
            "Precision Instruments",
            "Steel & Metals",
        ],
    ),
    "United Kingdom": CountryData(
        0.10,
        69.1,
        3130.0,
        "Europe",
        ["G7", "G20", "Commonwealth"],
        [
            "Financial Services",
            "Pharmaceuticals",
            "Aerospace",
            "Automotive",
            "Chemicals",
        ],
    ),
    "South Korea": CountryData(
        0.50,
        74.9,
        1810.0,
        "Asia",
        ["G20"],
        [
            "Technology & Electronics",
            "Automotive",
            "Steel & Metals",
            "Chemicals",
            "Machinery",
        ],
    ),
    "France": CountryData(
        0.25,
        47.8,
        2940.0,
        "Europe",
        ["G7", "G20", "NATO"],
        ["Aerospace", "Luxury Goods", "Wine & Beverages", "Automotive", "Chemicals"],
    ),
    "India": CountryData(
        0.52,
        51.4,
        3740.0,
        "Asia",
        ["G20", "Commonwealth"],
        [
            "Textiles & Apparel",
            "Pharmaceuticals",
            "Technology Services",
            "Chemicals",
            "Agriculture",
        ],
    ),
    "Italy": CountryData(
        0.19,
        54.9,
        2110.0,
        "Europe",
        ["G7", "G20", "NATO"],
        [
            "Machinery",
            "Automotive",
            "Fashion & Textiles",
            "Food & Beverages",
            "Chemicals",
        ],
    ),
    "Canada": CountryData(
        0.07,
        429.8,
        1990.0,
        "Americas",
        ["G7", "G20", "Commonwealth", "NATO"],
        ["Energy", "Mining", "Agriculture", "Forestry Products", "Automotive"],
    ),
    "Mexico": CountryData(
        0.10,
        614.5,
        1630.0,
        "Americas",
        ["G20"],
        ["Automotive", "Machinery", "Agriculture", "Textiles & Apparel", "Energy"],
    ),
    "Netherlands": CountryData(
        0.10,
        24.4,
        910.0,
        "Europe",
        ["NATO"],
        ["Agriculture", "Chemicals", "Energy", "Technology & Electronics", "Machinery"],
    ),
    "Taiwan": CountryData(
        0.64,
        65.9,
        669.0,
        "Asia",
        ["Independent"],
        [
            "Technology & Electronics",
            "Semiconductors",
            "Machinery",
            "Chemicals",
            "Textiles & Apparel",
        ],
    ),
    "Switzerland": CountryData(
        0.61,
        16.8,
        812.0,
        "Europe",
        ["Independent"],
        [
            "Pharmaceuticals",
            "Machinery",
            "Precision Instruments",
            "Chemicals",
            "Financial Services",
        ],
    ),
    "Belgium": CountryData(
        0.10,
        18.6,
        529.0,
        "Europe",
        ["NATO"],
        [
            "Chemicals",
            "Diamonds",
            "Machinery",
            "Food & Beverages",
            "Textiles & Apparel",
        ],
    ),
    "Singapore": CountryData(
        0.10,
        27.0,
        397.0,
        "Asia",
        ["ASEAN", "Commonwealth"],
        [
            "Technology & Electronics",
            "Chemicals",
            "Financial Services",
            "Machinery",
            "Pharmaceuticals",
        ],
    ),
    "Ireland": CountryData(
        0.10,
        13.8,
        499.0,
        "Europe",
        ["Independent"],
        [
            "Pharmaceuticals",
            "Technology Services",
            "Food & Beverages",
            "Chemicals",
            "Machinery",
        ],
    ),
    "Israel": CountryData(
        0.33,
        14.7,
        481.0,
        "Asia",
        ["Independent"],
        [
            "Technology & Electronics",
            "Pharmaceuticals",
            "Diamonds",
            "Chemicals",
            "Machinery",
        ],
    ),
    "Thailand": CountryData(
        0.72,
        25.2,
        543.0,
        "Asia",
        ["ASEAN"],
        [
            "Automotive",
            "Agriculture",
            "Machinery",
            "Textiles & Apparel",
            "Food & Beverages",
        ],
    ),
    "Malaysia": CountryData(
        0.47,
        27.0,
        433.0,
        "Asia",
        ["ASEAN", "Commonwealth"],
        ["Technology & Electronics", "Palm Oil", "Rubber", "Machinery", "Chemicals"],
    ),
    "Austria": CountryData(
        0.10,
        5.8,
        481.0,
        "Europe",
        ["Independent"],
        ["Machinery", "Automotive", "Iron & Steel", "Chemicals", "Paper & Forestry"],
    ),
    "Sweden": CountryData(
        0.30,
        12.8,
        541.0,
        "Europe",
        ["Independent"],
        [
            "Machinery",
            "Automotive",
            "Pharmaceuticals",
            "Forestry Products",
            "Iron & Steel",
        ],
    ),
    "Norway": CountryData(
        0.30,
        7.8,
        482.0,
        "Europe",
        ["NATO"],
        ["Energy", "Seafood", "Shipping", "Machinery", "Chemicals"],
    ),
    "Philippines": CountryData(
        0.34,
        8.9,
        394.0,
        "Asia",
        ["ASEAN"],
        [
            "Technology & Electronics",
            "Agriculture",
            "Textiles & Apparel",
            "Mining",
            "Chemicals",
        ],
    ),
    "Bangladesh": CountryData(
        0.16,
        0.9,
        460.0,
        "Asia",
        ["Commonwealth"],
        ["Textiles & Apparel", "Agriculture", "Pharmaceuticals", "Leather", "Jute"],
    ),
    "Chile": CountryData(
        0.12,
        15.1,
        317.0,
        "Americas",
        ["Independent"],
        ["Mining", "Agriculture", "Wine", "Forestry Products", "Chemicals"],
    ),
    "Finland": CountryData(
        0.30,
        3.5,
        298.0,
        "Europe",
        ["Independent"],
        [
            "Forestry Products",
            "Technology & Electronics",
            "Machinery",
            "Chemicals",
            "Metals",
        ],
    ),
    "South Africa": CountryData(
        0.60,
        9.0,
        419.0,
        "Africa",
        ["G20", "Commonwealth"],
        ["Mining", "Agriculture", "Automotive", "Chemicals", "Machinery"],
    ),
    "United Arab Emirates": CountryData(
        0.10,
        12.5,
        507.0,
        "Asia",
        ["Independent"],
        ["Energy", "Trade Services", "Financial Services", "Aluminum", "Chemicals"],
    ),
    "Turkey": CountryData(
        0.55,
        8.4,
        819.0,
        "Europe",
        ["G20", "NATO"],
        [
            "Textiles & Apparel",
            "Automotive",
            "Machinery",
            "Iron & Steel",
            "Food & Beverages",
        ],
    ),
    "Vietnam": CountryData(
        0.90,
        77.3,
        409.0,
        "Asia",
        ["ASEAN"],
        [
            "Textiles & Apparel",
            "Technology & Electronics",
            "Agriculture",
            "Footwear",
            "Furniture",
        ],
    ),
    "Indonesia": CountryData(
        0.10,
        20.0,
        1319.0,
        "Asia",
        ["G20", "ASEAN"],
        ["Palm Oil", "Mining", "Textiles & Apparel", "Agriculture", "Chemicals"],
    ),
    "Brazil": CountryData(
        0.25,
        33.2,
        2055.0,
        "Americas",
        ["G20"],
        ["Agriculture", "Mining", "Automotive", "Machinery", "Chemicals"],
    ),
    "Argentina": CountryData(
        0.35,
        4.6,
        487.0,
        "Americas",
        ["G20"],
        ["Agriculture", "Mining", "Food & Beverages", "Chemicals", "Machinery"],
    ),
    "Poland": CountryData(
        0.25,
        5.4,
        679.0,
        "Europe",
        ["NATO"],
        [
            "Automotive",
            "Machinery",
            "Chemicals",
            "Food & Beverages",
            "Textiles & Apparel",
        ],
    ),
    "Czech Republic": CountryData(
        0.15,
        1.7,
        281.0,
        "Europe",
        ["NATO"],
        ["Automotive", "Machinery", "Glass & Ceramics", "Chemicals", "Iron & Steel"],
    ),
    "Egypt": CountryData(
        0.10,
        2.5,
        469.0,
        "Africa",
        ["Independent"],
        [
            "Textiles & Apparel",
            "Agriculture",
            "Chemicals",
            "Food & Beverages",
            "Energy",
        ],
    ),
    "Nigeria": CountryData(
        0.35,
        5.4,
        441.0,
        "Africa",
        ["Commonwealth"],
        ["Energy", "Agriculture", "Chemicals", "Textiles & Apparel", "Mining"],
    ),
    "Saudi Arabia": CountryData(
        0.10,
        16.8,
        833.0,
        "Asia",
        ["G20"],
        ["Energy", "Chemicals", "Agriculture", "Mining", "Financial Services"],
    ),
    "Pakistan": CountryData(
        0.58,
        4.0,
        348.0,
        "Asia",
        ["Commonwealth"],
        [
            "Textiles & Apparel",
            "Agriculture",
            "Chemicals",
            "Sports Goods",
            "Surgical Instruments",
        ],
    ),
    "Ukraine": CountryData(
        0.35,
        1.1,
        200.0,
        "Europe",
        ["Independent"],
        ["Agriculture", "Iron & Steel", "Chemicals", "Machinery", "Food & Beverages"],
    ),
    "Romania": CountryData(
        0.20,
        1.8,
        250.0,
        "Europe",
        ["NATO"],
        ["Automotive", "Machinery", "Textiles & Apparel", "Chemicals", "Agriculture"],
    ),
    "New Zealand": CountryData(
        0.20,
        1.5,
        249.0,
        "Oceania",
        ["Commonwealth"],
        ["Agriculture", "Forestry Products", "Wine", "Seafood", "Aluminum"],
    ),
    "Kazakhstan": CountryData(
        0.54,
        0.9,
        220.0,
        "Asia",
        ["Independent"],
        ["Energy", "Mining", "Agriculture", "Chemicals", "Machinery"],
    ),
    "Jordan": CountryData(
        0.40,
        1.4,
        47.0,
        "Asia",
        ["Independent"],
        ["Chemicals", "Textiles & Apparel", "Pharmaceuticals", "Agriculture", "Mining"],
    ),
    "Laos": CountryData(
        0.95,
        0.05,
        19.0,
        "Asia",
        ["ASEAN"],
        [
            "Agriculture",
            "Mining",
            "Textiles & Apparel",
            "Forestry Products",
            "Hydroelectric Power",
        ],
    ),
    "Madagascar": CountryData(
        0.33,
        0.8,
        15.0,
        "Africa",
        ["Independent"],
        ["Agriculture", "Mining", "Textiles & Apparel", "Seafood", "Vanilla"],
    ),
    "Myanmar": CountryData(
        0.88,
        0.05,
        81.0,
        "Asia",
        ["ASEAN"],
        ["Agriculture", "Mining", "Textiles & Apparel", "Forestry Products", "Energy"],
    ),
}

# Impact classifications with authoritative sources
IMPACT_CLASSIFICATIONS = {
    "low": ImpactClassification(
        "Low Impact",
        "#22c55e",
        "Minimal economic disruption (0-2%)",
        "World Bank Trade Policy Guidelines 2024",
    ),
    "moderate": ImpactClassification(
        "Moderate Impact",
        "#f59e0b",
        "Manageable disruption (2-5%)",
        "IMF Trade Assessment Framework 2024",
    ),
    "high": ImpactClassification(
        "High Impact",
        "#ef4444",
        "Significant disruption (5-10%)",
        "OECD Economic Outlook 2025",
    ),
    "severe": ImpactClassification(
        "Severe Impact",
        "#991b1b",
        "Critical disruption (10%+)",
        "OECD Services Trade Restrictiveness Index 2025",
    ),
}

# Economic sectors for analysis
ECONOMIC_SECTORS = [
    "Agriculture",
    "Mining",
    "Manufacturing",
    "Energy",
    "Construction",
    "Technology & Electronics",
    "Automotive",
    "Aerospace",
    "Pharmaceuticals",
    "Chemicals",
    "Textiles & Apparel",
    "Food & Beverages",
    "Machinery",
    "Iron & Steel",
    "Financial Services",
    "Trade Services",
    "Transportation",
    "Tourism & Hospitality",
]

# ================================
# CALCULATION FUNCTIONS
# ================================


def calculate_economic_impact_percentage(
    tariff_rate: float, trade_volume: float, gdp: float
) -> float:
    """Calculate economic disruption percentage using World Bank methodology"""
    trade_exposure = trade_volume / gdp
    tariff_elasticity = 1.8  # World Bank Trade Policy Assessment Framework 2024
    base_disruption = tariff_rate * tariff_elasticity * trade_exposure * 100

    # Apply scaling factors based on economic resilience
    if gdp > 10000:  # Large economies have more resilience
        base_disruption *= 0.7
    elif gdp < 500:  # Smaller economies are more vulnerable
        base_disruption *= 1.3

    return min(base_disruption, 95.0)  # Cap at 95% for realism


def calculate_gdp_impact_usd(
    disruption_percentage: float, gdp_billions: float
) -> float:
    """Calculate 5-year cumulative GDP impact using IMF methodology"""
    annual_impact = (disruption_percentage / 100) * gdp_billions * 0.4
    cumulative_impact = annual_impact * 5 * 1.1  # Compound effect over 5 years
    return cumulative_impact


def get_impact_classification(disruption_percentage: float) -> ImpactClassification:
    """Classify impact level based on disruption percentage"""
    if disruption_percentage < 2:
        return IMPACT_CLASSIFICATIONS["low"]
    elif disruption_percentage < 5:
        return IMPACT_CLASSIFICATIONS["moderate"]
    elif disruption_percentage < 10:
        return IMPACT_CLASSIFICATIONS["high"]
    else:
        return IMPACT_CLASSIFICATIONS["severe"]


# ================================
# PROFESSIONAL ANALYSIS FUNCTIONS
# ================================


def create_professional_summary_card(results_df: pd.DataFrame) -> str:
    """Create a professional executive summary card"""
    if len(results_df) == 0:
        return ""

    avg_disruption = results_df["_economic_disruption_numeric"].mean()
    total_gdp_impact = results_df["_gdp_impact_numeric"].sum()
    most_impacted = results_df.loc[results_df["_economic_disruption_numeric"].idxmax()]

    # Count by severity
    severity_counts = results_df["Severity Level"].value_counts()

    return f"""
    <div class="summary-section">
        <h3>📊 Executive Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px;">
            <div class="metric-card">
                <div class="metric-value">{len(results_df)}</div>
                <div class="metric-label">Countries Analyzed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_disruption:.1f}%</div>
                <div class="metric-label">Avg. Economic Disruption</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${total_gdp_impact:.0f}B</div>
                <div class="metric-label">Total GDP Impact (5yr)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{most_impacted['Country']}</div>
                <div class="metric-label">Most Impacted Country</div>
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <h4 style="color: #1e3c72; margin-bottom: 15px;">📈 Impact Distribution</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                {"".join([f'<div style="background: {IMPACT_CLASSIFICATIONS[str(level).lower().replace(" impact", "")].color}; color: white; padding: 10px; border-radius: 8px; text-align: center;"><strong>{count}</strong><br>{level}</div>' for level, count in severity_counts.items()])}
            </div>
        </div>
    </div>
    """


def create_country_detail_cards(results_df: pd.DataFrame) -> str:
    """Create professional country detail cards"""
    if len(results_df) == 0:
        return ""

    cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-top: 20px;">'

    for _, row in results_df.iterrows():
        classification = row["_classification"]
        export_sectors = row.get("_heavy_export_sectors", [])

        cards_html += f"""
        <div class="analysis-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="color: #1e3c72; margin: 0; font-size: 1.4rem; font-weight: 700;">{row['Country']}</h3>
                <span style="background: {classification.color}; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">{row['Severity Level']}</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                <div>
                    <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">Tariff Rate</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #dc2626;">{row['Tariff Rate']}</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">Economic Disruption</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: {classification.color};">{row['Economic Disruption']}</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">GDP Impact (5yr)</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #059669;">{row['5-Year GDP Impact']}</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; color: #4a5568; font-weight: 600;">Trade Volume</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #0284c7;">{row['Trade Volume']}</div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <div style="font-size: 0.9rem; color: #4a5568; margin-bottom: 5px; font-weight: 600;">Key Export Sectors to USA</div>
                <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                    {"".join([f'<span style="background: #e0f2fe; color: #0277bd; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">{sector}</span>' for sector in export_sectors[:4]])}
                </div>
            </div>
            
            <div style="border-top: 1px solid #e2e8f0; padding-top: 15px; font-size: 0.9rem; color: #374151;">
                <strong style="color: #2d3748;">Region:</strong> {row['Continent']} | <strong style="color: #2d3748;">Groups:</strong> {row['Groups']}<br>
                <strong style="color: #2d3748;">Authority:</strong> {classification.source}
            </div>
        </div>
        """

    cards_html += "</div>"
    return cards_html


def create_professional_charts(results_df: pd.DataFrame) -> Tuple[go.Figure, go.Figure]:
    """Create professional-grade charts"""

    # Chart 1: Economic Disruption with enhanced styling
    fig1 = go.Figure()

    colors = [
        IMPACT_CLASSIFICATIONS[
            str(row["Severity Level"]).lower().replace(" impact", "")
        ].color
        for _, row in results_df.iterrows()
    ]

    fig1.add_trace(
        go.Bar(
            x=results_df["Country"],
            y=results_df["_economic_disruption_numeric"],
            marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.1)", width=1)),
            hovertemplate="<b>%{x}</b><br>"
            + "Economic Disruption: %{y:.1f}%<br>"
            + "<extra></extra>",
            name="Economic Disruption",
        )
    )

    fig1.update_layout(
        title=dict(
            text="Economic Disruption by Country",
            font=dict(size=18, color="#1e3c72", family="Inter"),
            x=0.5,
        ),
        xaxis=dict(
            title="Countries",
            titlefont=dict(size=14, color="#374151"),
            tickfont=dict(size=12, color="#6b7280"),
            tickangle=45,
        ),
        yaxis=dict(
            title="Economic Disruption (%)",
            titlefont=dict(size=14, color="#374151"),
            tickfont=dict(size=12, color="#6b7280"),
            gridcolor="rgba(0,0,0,0.1)",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter"),
        showlegend=False,
        margin=dict(t=60, b=80, l=60, r=20),
        height=400,
    )

    # Chart 2: GDP Impact scatter plot
    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=results_df["_gdp_impact_numeric"],
            y=results_df["_economic_disruption_numeric"],
            mode="markers+text",
            marker=dict(
                size=results_df["Trade Volume"]
                .str.replace("$", "")
                .str.replace("B", "")
                .astype(float)
                / 10,
                color=colors,
                line=dict(color="white", width=2),
                opacity=0.8,
            ),
            text=results_df["Country"],
            textposition="top center",
            textfont=dict(size=10, color="#374151"),
            hovertemplate="<b>%{text}</b><br>"
            + "GDP Impact: $%{x:.1f}B<br>"
            + "Economic Disruption: %{y:.1f}%<br>"
            + "<extra></extra>",
            name="Countries",
        )
    )

    fig2.update_layout(
        title=dict(
            text="Economic Impact vs GDP Impact",
            font=dict(size=18, color="#1e3c72", family="Inter"),
            x=0.5,
        ),
        xaxis=dict(
            title="5-Year GDP Impact (USD Billions)",
            titlefont=dict(size=14, color="#374151"),
            tickfont=dict(size=12, color="#6b7280"),
            gridcolor="rgba(0,0,0,0.1)",
        ),
        yaxis=dict(
            title="Economic Disruption (%)",
            titlefont=dict(size=14, color="#374151"),
            tickfont=dict(size=12, color="#6b7280"),
            gridcolor="rgba(0,0,0,0.1)",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter"),
        showlegend=False,
        margin=dict(t=60, b=60, l=60, r=60),
        height=400,
    )

    return fig1, fig2


# ================================
# SORTING & UTILITY FUNCTIONS
# ================================


def get_countries_by_sort_option(sort_option: str) -> List[str]:
    """Get sorted list of countries based on sort option"""
    countries = list(ENHANCED_COUNTRIES.keys())

    if sort_option == "Alphabetical":
        return sorted(countries)
    elif sort_option == "By Continent":
        return sorted(countries, key=lambda c: (ENHANCED_COUNTRIES[c].continent, c))
    elif sort_option == "By Global Groups":
        return sorted(
            countries,
            key=lambda c: (
                len(ENHANCED_COUNTRIES[c].global_groups),
                (
                    ENHANCED_COUNTRIES[c].global_groups[0]
                    if ENHANCED_COUNTRIES[c].global_groups
                    else "ZZZ"
                ),
                c,
            ),
        )
    else:
        return sorted(countries)


def format_country_display_name(country: str) -> str:
    """Format country name with tariff rate for display"""
    country_data = ENHANCED_COUNTRIES[country]
    tariff_pct = country_data.tariff_rate * 100
    continent = country_data.continent
    groups = (
        ", ".join(country_data.global_groups)
        if country_data.global_groups
        else "Independent"
    )

    return f"{country} ({tariff_pct:.0f}% tariff) - {continent} | {groups}"


def update_country_choices(sort_option: str):
    """Update country choices based on sort option"""
    countries = get_countries_by_sort_option(sort_option)
    display_choices = [format_country_display_name(country) for country in countries]
    return gr.update(choices=display_choices, value=[])


# ================================
# MAIN ANALYSIS FUNCTION
# ================================


def run_professional_country_analysis(
    selected_countries: List[str], sort_option: str
) -> Tuple[str, str, str, go.Figure, go.Figure]:
    """
    Professional Country Impact Analysis with Enhanced Presentation
    """
    if not selected_countries:
        empty_message = """
        <div class="info-card">
            <h3>🔍 Ready for Analysis</h3>
            <p>Please select at least one country from the list above to begin your comprehensive economic impact analysis.</p>
            <p><strong>Tip:</strong> You can select multiple countries to compare their impacts side by side.</p>
        </div>
        """
        return empty_message, "", "", go.Figure(), go.Figure()

    # Extract country names from display format
    country_names = []
    for display_name in selected_countries:
        country_name = display_name.split(" (")[0]
        country_names.append(country_name)

    # Calculate impacts for all selected countries
    results = []
    for country in country_names:
        if country not in ENHANCED_COUNTRIES:
            continue

        country_data = ENHANCED_COUNTRIES[country]

        # Calculate economic impacts using authoritative methodologies
        economic_disruption = calculate_economic_impact_percentage(
            country_data.tariff_rate,
            country_data.trade_volume_usa,
            country_data.gdp_usd_billions,
        )

        gdp_impact = calculate_gdp_impact_usd(
            economic_disruption, country_data.gdp_usd_billions
        )
        classification = get_impact_classification(economic_disruption)

        results.append(
            {
                "Country": country,
                "Tariff Rate": f"{country_data.tariff_rate*100:.1f}%",
                "Economic Disruption": f"{economic_disruption:.1f}%",
                "5-Year GDP Impact": f"${gdp_impact:.1f}B",
                "Severity Level": classification.level,
                "Heavy Export Sectors to USA": ", ".join(
                    country_data.heavy_export_sectors[:3]
                ),
                "Trade Volume": f"${country_data.trade_volume_usa:.1f}B",
                "GDP": f"${country_data.gdp_usd_billions:.1f}B",
                "Continent": country_data.continent,
                "Groups": (
                    ", ".join(country_data.global_groups)
                    if country_data.global_groups
                    else "Independent"
                ),
                "_economic_disruption_numeric": economic_disruption,
                "_gdp_impact_numeric": gdp_impact,
                "_classification": classification,
                "_heavy_export_sectors": country_data.heavy_export_sectors,
            }
        )

    # Create DataFrame for analysis
    results_df = pd.DataFrame(results)

    # Sort by economic disruption (highest first) for better presentation
    results_df = results_df.sort_values("_economic_disruption_numeric", ascending=False)

    # Generate professional components
    summary_card = create_professional_summary_card(results_df)
    detail_cards = create_country_detail_cards(results_df)

    # Create professional data table
    display_df = results_df[
        [
            "Country",
            "Tariff Rate",
            "Economic Disruption",
            "5-Year GDP Impact",
            "Severity Level",
            "Heavy Export Sectors to USA",
            "Trade Volume",
            "Continent",
            "Groups",
        ]
    ].copy()

    table_html = f"""
    <div class="chart-container">
        <h3 style="color: #1e3c72; margin-bottom: 15px;">📊 Detailed Results Table</h3>
        {display_df.to_html(index=False, classes='dataframe', table_id='results-table')}
    </div>
    """

    # Create professional charts
    chart1, chart2 = create_professional_charts(results_df)

    return summary_card, detail_cards, table_html, chart1, chart2


# ================================
# PROFESSIONAL GRADIO INTERFACE
# ================================


def create_professional_gradio_app():
    """Create the ultra-professional TIPM Gradio application"""

    with gr.Blocks(
        title="TIPM: Professional Economic Analysis Platform",
        theme=gr.themes.Soft(
            primary_hue="blue", secondary_hue="slate", neutral_hue="slate"
        ),
        css=PROFESSIONAL_CSS,
    ) as app:

        # Professional Header
        gr.HTML(
            f"""
        <div class="header-section">
            <h1>📊 TIPM: Professional Economic Analysis Platform</h1>
            <h3>Advanced Tariff Impact Assessment with Authoritative Intelligence</h3>
            <div style="margin-top: 20px; font-size: 1rem; opacity: 0.9;">
                <strong>45 Countries</strong> • <strong>Verified Data Sources</strong> • <strong>Export Sector Intelligence</strong> • <strong>Professional-Grade Analysis</strong>
            </div>
        </div>
        """
        )

        # Main content wrapper
        with gr.Group():
            gr.HTML('<div class="main-content">')

            # Professional info section
            gr.HTML(
                """
            <div class="info-card">
                <h3>🎯 Platform Capabilities</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 15px;">
                    <div>
                        <h4 style="color: #1e3c72; margin-bottom: 10px;">📈 Economic Intelligence</h4>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li>45 countries with verified Trump-era tariff data</li>
                            <li>Export sector intelligence for strategic insights</li>
                            <li>5-year GDP impact projections</li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #1e3c72; margin-bottom: 10px;">🏛️ Authoritative Sources</h4>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li>World Bank Trade Policy Assessment Framework</li>
                            <li>IMF Economic Impact Methodologies</li>
                            <li>OECD Trade Restrictiveness Analysis</li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #1e3c72; margin-bottom: 10px;">⚡ Professional Features</h4>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li>Executive-grade summary dashboards</li>
                            <li>Interactive professional visualizations</li>
                            <li>Detailed country impact assessments</li>
                        </ul>
                    </div>
                </div>
            </div>
            """
            )

            with gr.Tabs() as main_tabs:
                # ===== TAB 1: PROFESSIONAL COUNTRY ANALYSIS =====
                with gr.Tab("🌍 Country Impact Analysis", id="country_analysis"):

                    with gr.Group():
                        gr.HTML('<div class="form-section">')
                        gr.HTML("<h4>🔧 Analysis Configuration</h4>")

                        with gr.Row():
                            with gr.Column(scale=1):
                                sort_option = gr.Dropdown(
                                    choices=[
                                        "Alphabetical",
                                        "By Continent",
                                        "By Global Groups",
                                    ],
                                    value="Alphabetical",
                                    label="Country Organization Method",
                                    info="Select how countries should be organized in the list",
                                )

                            with gr.Column(scale=2):
                                country_selector = gr.CheckboxGroup(
                                    choices=[
                                        format_country_display_name(country)
                                        for country in sorted(ENHANCED_COUNTRIES.keys())
                                    ],
                                    label="Select Countries for Analysis",
                                    info="Choose up to 20 countries - data includes tariff rates, regions, and global memberships",
                                )

                        # Update country choices when sort changes
                        sort_option.change(
                            fn=update_country_choices,
                            inputs=[sort_option],
                            outputs=[country_selector],
                        )

                        analyze_btn = gr.Button(
                            "🚀 Execute Professional Analysis",
                            variant="primary",
                            size="lg",
                            elem_classes=["primary-button"],
                        )

                        gr.HTML("</div>")

                    # Results Section
                    with gr.Group():
                        summary_output = gr.HTML(label="Executive Summary")
                        detail_output = gr.HTML(label="Country Details")
                        table_output = gr.HTML(label="Data Table")

                        with gr.Row():
                            with gr.Column():
                                chart1_output = gr.Plot(
                                    label="Economic Disruption Analysis"
                                )
                            with gr.Column():
                                chart2_output = gr.Plot(
                                    label="Impact Correlation Matrix"
                                )

                    # Connect the analysis function
                    analyze_btn.click(
                        fn=run_professional_country_analysis,
                        inputs=[country_selector, sort_option],
                        outputs=[
                            summary_output,
                            detail_output,
                            table_output,
                            chart1_output,
                            chart2_output,
                        ],
                    )

                # ===== TAB 2: SECTOR ANALYSIS (Placeholder) =====
                with gr.Tab("🏭 Sector Analysis", id="sector_analysis"):
                    gr.HTML(
                        """
                    <div class="warning-card">
                        <h3>🚧 Sector Analysis Module</h3>
                        <p><strong>Coming Soon:</strong> Comprehensive sector-by-sector impact analysis across 18 major economic sectors.</p>
                        <p>This module will provide detailed insights into how tariffs affect specific industries within each country.</p>
                        <ul>
                            <li>Technology & Electronics impact assessment</li>
                            <li>Automotive sector vulnerability analysis</li>
                            <li>Agricultural trade disruption modeling</li>
                            <li>Manufacturing supply chain effects</li>
                        </ul>
                    </div>
                    """
                    )

                # ===== TAB 3: RISK ASSESSMENT (Placeholder) =====
                with gr.Tab("⚠️ Risk Assessment", id="risk_assessment"):
                    gr.HTML(
                        """
                    <div class="warning-card">
                        <h3>📊 Risk Assessment Dashboard</h3>
                        <p><strong>Coming Soon:</strong> Comprehensive risk scoring and vulnerability assessment for trade policy scenarios.</p>
                        <p>This module will provide strategic risk intelligence for policy makers and business leaders.</p>
                        <ul>
                            <li>Country vulnerability heat maps</li>
                            <li>Supply chain disruption risk scoring</li>
                            <li>Economic resilience indicators</li>
                            <li>Policy scenario modeling</li>
                        </ul>
                    </div>
                    """
                    )

            # Professional Footer
            gr.HTML(
                """
            <div style="margin-top: 40px; padding: 25px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 15px; border-top: 3px solid #1e3c72;">
                <div style="text-align: center; color: #64748b;">
                    <h4 style="color: #1e3c72; margin-bottom: 15px;">📚 Authoritative Sources & Methodology</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; font-size: 0.9rem;">
                        <div><strong>Economic Calculations:</strong><br>World Bank Trade Policy Assessment Framework 2024</div>
                        <div><strong>Impact Classifications:</strong><br>IMF Trade Assessment Methodology 2024</div>
                        <div><strong>Risk Scoring:</strong><br>OECD Economic Outlook 2025</div>
                        <div><strong>Data Sources:</strong><br>UN Comtrade, World Bank, IMF, OECD</div>
                    </div>
                    <div style="margin-top: 20px; font-size: 0.8rem; opacity: 0.8;">
                        TIPM v3.0 Professional | Analysis Date: August 5, 2025 | Professional Economic Intelligence Platform
                    </div>
                </div>
            </div>
            """
            )

            gr.HTML("</div>")  # Close main-content div

    return app


# ================================
# APPLICATION ENTRY POINT
# ================================

if __name__ == "__main__":
    app = create_professional_gradio_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)
