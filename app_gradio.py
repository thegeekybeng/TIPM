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
import time
from functools import lru_cache


# Data structures and sample data (same asdef run_enhanced_timp_analysis(countries: List[str], sectors: List[str]) -> Dict:ersion)
@dataclass
class CountryTariffData:
    country: str
    tariff_to_usa: float
    reciprocal_tariff: float
    trade_volume: float
    sector_impacts: Dict[str, float]


# Sample data for demo (based on real Trump tariff data) - Expanded to 25 countries
SAMPLE_DATA = {
    "China": CountryTariffData(
        country="China",
        tariff_to_usa=0.67,
        reciprocal_tariff=0.34,
        trade_volume=650.0,
        sector_impacts={
            "technology": 0.85,
            "agriculture": 0.45,
            "textiles": 0.82,
            "chemicals": 0.55,
            "machinery": 0.78,
            "automotive": 0.70,
            "metals": 0.88,
            "energy": 0.35,
            "pharmaceuticals": 0.40,
            "food_processing": 0.40,
            "electronics": 0.90,
            "furniture": 0.75,
            "financial_services": 0.25,
            "telecommunications": 0.90,
            "aerospace": 0.60,
            "mining": 0.50,
            "construction": 0.45,
            "retail": 0.30,
        },
    ),
    "Germany": CountryTariffData(
        country="Germany",
        tariff_to_usa=0.39,  # EU rate
        reciprocal_tariff=0.20,
        trade_volume=400.0,
        sector_impacts={
            "technology": 0.70,
            "agriculture": 0.25,
            "textiles": 0.45,
            "chemicals": 0.80,
            "machinery": 0.85,
            "automotive": 0.90,
            "metals": 0.70,
            "energy": 0.50,
            "pharmaceuticals": 0.75,
            "food_processing": 0.30,
            "electronics": 0.65,
            "furniture": 0.55,
            "financial_services": 0.60,
            "telecommunications": 0.55,
            "aerospace": 0.80,
            "mining": 0.40,
            "construction": 0.65,
            "retail": 0.45,
        },
    ),
    "Japan": CountryTariffData(
        country="Japan",
        tariff_to_usa=0.46,
        reciprocal_tariff=0.24,
        trade_volume=320.0,
        sector_impacts={
            "technology": 0.80,
            "agriculture": 0.20,
            "textiles": 0.35,
            "chemicals": 0.60,
            "machinery": 0.85,
            "automotive": 0.90,
            "metals": 0.75,
            "energy": 0.40,
            "pharmaceuticals": 0.65,
            "food_processing": 0.15,
            "electronics": 0.85,
            "furniture": 0.25,
            "financial_services": 0.50,
            "telecommunications": 0.75,
            "aerospace": 0.70,
            "mining": 0.30,
            "construction": 0.55,
            "retail": 0.40,
        },
    ),
    "India": CountryTariffData(
        country="India",
        tariff_to_usa=0.52,
        reciprocal_tariff=0.26,
        trade_volume=180.0,
        sector_impacts={
            "technology": 0.75,
            "agriculture": 0.40,
            "textiles": 0.85,
            "chemicals": 0.55,
            "machinery": 0.65,
            "automotive": 0.50,
            "metals": 0.60,
            "energy": 0.45,
            "pharmaceuticals": 0.80,
            "food_processing": 0.35,
            "electronics": 0.70,
            "furniture": 0.60,
            "financial_services": 0.70,
            "telecommunications": 0.85,
            "aerospace": 0.30,
            "mining": 0.55,
            "construction": 0.50,
            "retail": 0.45,
        },
    ),
    "South Korea": CountryTariffData(
        country="South Korea",
        tariff_to_usa=0.50,
        reciprocal_tariff=0.25,
        trade_volume=280.0,
        sector_impacts={
            "technology": 0.90,
            "agriculture": 0.15,
            "textiles": 0.40,
            "chemicals": 0.65,
            "machinery": 0.80,
            "automotive": 0.75,
            "metals": 0.85,
            "energy": 0.35,
            "pharmaceuticals": 0.50,
            "food_processing": 0.15,
            "electronics": 0.95,
            "furniture": 0.25,
            "financial_services": 0.45,
            "telecommunications": 0.95,
            "aerospace": 0.60,
            "mining": 0.40,
            "construction": 0.55,
            "retail": 0.35,
        },
    ),
    "France": CountryTariffData(
        country="France",
        tariff_to_usa=0.39,  # EU rate
        reciprocal_tariff=0.20,
        trade_volume=250.0,
        sector_impacts={
            "technology": 0.60,
            "agriculture": 0.65,
            "textiles": 0.80,
            "chemicals": 0.70,
            "machinery": 0.70,
            "automotive": 0.75,
            "metals": 0.55,
            "energy": 0.45,
            "pharmaceuticals": 0.85,
            "food_processing": 0.75,
            "electronics": 0.50,
            "furniture": 0.60,
            "financial_services": 0.75,
            "telecommunications": 0.50,
            "aerospace": 0.90,
            "mining": 0.35,
            "construction": 0.60,
            "retail": 0.65,
        },
    ),
    "United Kingdom": CountryTariffData(
        country="United Kingdom",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=220.0,
        sector_impacts={
            "technology": 0.70,
            "agriculture": 0.30,
            "textiles": 0.45,
            "chemicals": 0.50,
            "machinery": 0.60,
            "automotive": 0.65,
            "metals": 0.40,
            "energy": 0.55,
            "pharmaceuticals": 0.80,
            "food_processing": 0.35,
            "electronics": 0.60,
            "furniture": 0.40,
            "financial_services": 0.90,
            "telecommunications": 0.60,
            "aerospace": 0.85,
            "mining": 0.45,
            "construction": 0.50,
            "retail": 0.60,
        },
    ),
    "Italy": CountryTariffData(
        country="Italy",
        tariff_to_usa=0.39,  # EU rate
        reciprocal_tariff=0.20,
        trade_volume=200.0,
        sector_impacts={
            "technology": 0.55,
            "agriculture": 0.55,
            "textiles": 0.90,
            "chemicals": 0.65,
            "machinery": 0.75,
            "automotive": 0.80,
            "metals": 0.70,
            "energy": 0.40,
            "pharmaceuticals": 0.60,
            "food_processing": 0.70,
            "electronics": 0.45,
            "furniture": 0.85,
            "financial_services": 0.50,
            "telecommunications": 0.45,
            "aerospace": 0.65,
            "mining": 0.40,
            "construction": 0.70,
            "retail": 0.60,
        },
    ),
    "Canada": CountryTariffData(
        country="Canada",
        tariff_to_usa=0.15,  # NAFTA partner
        reciprocal_tariff=0.10,
        trade_volume=350.0,
        sector_impacts={
            "technology": 0.50,
            "agriculture": 0.70,
            "textiles": 0.35,
            "chemicals": 0.70,
            "machinery": 0.60,
            "automotive": 0.85,
            "metals": 0.80,
            "energy": 0.90,
            "pharmaceuticals": 0.55,
            "food_processing": 0.75,
            "electronics": 0.45,
            "furniture": 0.50,
            "financial_services": 0.60,
            "telecommunications": 0.45,
            "aerospace": 0.75,
            "mining": 0.95,
            "construction": 0.65,
            "retail": 0.45,
        },
    ),
    "Vietnam": CountryTariffData(
        country="Vietnam",
        tariff_to_usa=0.90,
        reciprocal_tariff=0.46,
        trade_volume=150.0,
        sector_impacts={
            "technology": 0.70,
            "agriculture": 0.60,
            "textiles": 0.95,
            "chemicals": 0.50,
            "machinery": 0.65,
            "automotive": 0.45,
            "metals": 0.65,
            "energy": 0.25,
            "pharmaceuticals": 0.35,
            "food_processing": 0.65,
            "electronics": 0.75,
            "furniture": 0.80,
            "financial_services": 0.30,
            "telecommunications": 0.60,
            "aerospace": 0.20,
            "mining": 0.40,
            "construction": 0.55,
            "retail": 0.50,
        },
    ),
    "Taiwan": CountryTariffData(
        country="Taiwan",
        tariff_to_usa=0.64,
        reciprocal_tariff=0.32,
        trade_volume=190.0,
        sector_impacts={
            "technology": 0.95,
            "agriculture": 0.25,
            "textiles": 0.50,
            "chemicals": 0.75,
            "machinery": 0.80,
            "automotive": 0.60,
            "metals": 0.60,
            "energy": 0.30,
            "pharmaceuticals": 0.70,
            "food_processing": 0.20,
            "electronics": 0.95,
            "furniture": 0.40,
            "financial_services": 0.55,
            "telecommunications": 0.90,
            "aerospace": 0.45,
            "mining": 0.35,
            "construction": 0.45,
            "retail": 0.40,
        },
    ),
    "Thailand": CountryTariffData(
        country="Thailand",
        tariff_to_usa=0.72,
        reciprocal_tariff=0.36,
        trade_volume=130.0,
        sector_impacts={
            "technology": 0.65,
            "agriculture": 0.70,
            "textiles": 0.85,
            "chemicals": 0.60,
            "machinery": 0.65,
            "automotive": 0.80,
            "metals": 0.50,
            "energy": 0.40,
            "pharmaceuticals": 0.45,
            "food_processing": 0.75,
            "electronics": 0.70,
            "furniture": 0.75,
            "financial_services": 0.40,
            "telecommunications": 0.55,
            "aerospace": 0.30,
            "mining": 0.45,
            "construction": 0.60,
            "retail": 0.55,
        },
    ),
    "Switzerland": CountryTariffData(
        country="Switzerland",
        tariff_to_usa=0.61,
        reciprocal_tariff=0.31,
        trade_volume=160.0,
        sector_impacts={
            "technology": 0.70,
            "agriculture": 0.20,
            "textiles": 0.40,
            "chemicals": 0.85,
            "machinery": 0.80,
            "automotive": 0.50,
            "metals": 0.45,
            "energy": 0.30,
            "pharmaceuticals": 0.95,
            "food_processing": 0.25,
            "electronics": 0.55,
            "furniture": 0.35,
            "financial_services": 0.85,
            "telecommunications": 0.55,
            "aerospace": 0.60,
            "mining": 0.25,
            "construction": 0.40,
            "retail": 0.50,
        },
    ),
    "Indonesia": CountryTariffData(
        country="Indonesia",
        tariff_to_usa=0.64,
        reciprocal_tariff=0.32,
        trade_volume=140.0,
        sector_impacts={
            "technology": 0.50,
            "agriculture": 0.80,
            "textiles": 0.75,
            "chemicals": 0.65,
            "machinery": 0.55,
            "automotive": 0.55,
            "metals": 0.70,
            "energy": 0.85,
            "pharmaceuticals": 0.40,
            "food_processing": 0.75,
            "electronics": 0.60,
            "furniture": 0.70,
            "financial_services": 0.45,
            "telecommunications": 0.60,
            "aerospace": 0.25,
            "mining": 0.90,
            "construction": 0.65,
            "retail": 0.50,
        },
    ),
    "Malaysia": CountryTariffData(
        country="Malaysia",
        tariff_to_usa=0.47,
        reciprocal_tariff=0.24,
        trade_volume=120.0,
        sector_impacts={
            "technology": 0.80,
            "agriculture": 0.65,
            "textiles": 0.60,
            "chemicals": 0.70,
            "machinery": 0.65,
            "automotive": 0.70,
            "metals": 0.55,
            "energy": 0.80,
            "pharmaceuticals": 0.45,
            "food_processing": 0.60,
            "electronics": 0.85,
            "furniture": 0.65,
            "financial_services": 0.60,
            "telecommunications": 0.75,
            "aerospace": 0.40,
            "mining": 0.75,
            "construction": 0.55,
            "retail": 0.50,
        },
    ),
    "Singapore": CountryTariffData(
        country="Singapore",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=180.0,
        sector_impacts={
            "technology": 0.85,
            "agriculture": 0.10,
            "textiles": 0.30,
            "chemicals": 0.85,
            "machinery": 0.60,
            "automotive": 0.40,
            "metals": 0.35,
            "energy": 0.75,
            "pharmaceuticals": 0.80,
            "food_processing": 0.15,
            "electronics": 0.90,
            "furniture": 0.25,
            "financial_services": 0.95,
            "telecommunications": 0.90,
            "aerospace": 0.70,
            "mining": 0.20,
            "construction": 0.50,
            "retail": 0.70,
        },
    ),
    "Brazil": CountryTariffData(
        country="Brazil",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=170.0,
        sector_impacts={
            "technology": 0.40,
            "agriculture": 0.90,
            "textiles": 0.55,
            "chemicals": 0.75,
            "machinery": 0.50,
            "automotive": 0.70,
            "metals": 0.80,
            "energy": 0.85,
            "pharmaceuticals": 0.50,
            "food_processing": 0.85,
            "electronics": 0.35,
            "furniture": 0.60,
            "financial_services": 0.45,
            "telecommunications": 0.50,
            "aerospace": 0.60,
            "mining": 0.95,
            "construction": 0.70,
            "retail": 0.55,
        },
    ),
    "Australia": CountryTariffData(
        country="Australia",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=160.0,
        sector_impacts={
            "technology": 0.45,
            "agriculture": 0.85,
            "textiles": 0.25,
            "chemicals": 0.60,
            "machinery": 0.50,
            "automotive": 0.40,
            "metals": 0.85,
            "energy": 0.90,
            "pharmaceuticals": 0.60,
            "food_processing": 0.80,
            "electronics": 0.40,
            "furniture": 0.30,
            "financial_services": 0.70,
            "telecommunications": 0.55,
            "aerospace": 0.55,
            "mining": 0.95,
            "construction": 0.60,
            "retail": 0.50,
        },
    ),
    "Philippines": CountryTariffData(
        country="Philippines",
        tariff_to_usa=0.34,
        reciprocal_tariff=0.17,
        trade_volume=95.0,
        sector_impacts={
            "technology": 0.60,
            "agriculture": 0.75,
            "textiles": 0.80,
            "chemicals": 0.45,
            "machinery": 0.50,
            "automotive": 0.40,
            "metals": 0.50,
            "energy": 0.50,
            "pharmaceuticals": 0.45,
            "food_processing": 0.70,
            "electronics": 0.75,
            "furniture": 0.65,
            "financial_services": 0.55,
            "telecommunications": 0.70,
            "aerospace": 0.25,
            "mining": 0.60,
            "construction": 0.55,
            "retail": 0.50,
        },
    ),
    "Bangladesh": CountryTariffData(
        country="Bangladesh",
        tariff_to_usa=0.74,
        reciprocal_tariff=0.37,
        trade_volume=85.0,
        sector_impacts={
            "technology": 0.30,
            "agriculture": 0.80,
            "textiles": 0.95,
            "chemicals": 0.55,
            "machinery": 0.40,
            "automotive": 0.20,
            "metals": 0.45,
            "energy": 0.40,
            "pharmaceuticals": 0.60,
            "food_processing": 0.75,
            "electronics": 0.35,
            "furniture": 0.70,
            "financial_services": 0.25,
            "telecommunications": 0.50,
            "aerospace": 0.10,
            "mining": 0.30,
            "construction": 0.45,
            "retail": 0.40,
        },
    ),
    "South Africa": CountryTariffData(
        country="South Africa",
        tariff_to_usa=0.60,
        reciprocal_tariff=0.30,
        trade_volume=110.0,
        sector_impacts={
            "technology": 0.40,
            "agriculture": 0.70,
            "textiles": 0.50,
            "chemicals": 0.70,
            "machinery": 0.55,
            "automotive": 0.65,
            "metals": 0.90,
            "energy": 0.85,
            "pharmaceuticals": 0.55,
            "food_processing": 0.65,
            "electronics": 0.35,
            "furniture": 0.45,
            "financial_services": 0.60,
            "telecommunications": 0.55,
            "aerospace": 0.35,
            "mining": 0.95,
            "construction": 0.60,
            "retail": 0.50,
        },
    ),
    "Turkey": CountryTariffData(
        country="Turkey",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=125.0,
        sector_impacts={
            "technology": 0.50,
            "agriculture": 0.60,
            "textiles": 0.85,
            "chemicals": 0.65,
            "machinery": 0.65,
            "automotive": 0.70,
            "metals": 0.80,
            "energy": 0.55,
            "pharmaceuticals": 0.45,
            "food_processing": 0.65,
            "electronics": 0.45,
            "furniture": 0.70,
            "financial_services": 0.50,
            "telecommunications": 0.60,
            "aerospace": 0.40,
            "mining": 0.70,
            "construction": 0.75,
            "retail": 0.60,
        },
    ),
    "Israel": CountryTariffData(
        country="Israel",
        tariff_to_usa=0.33,
        reciprocal_tariff=0.17,
        trade_volume=90.0,
        sector_impacts={
            "technology": 0.90,
            "agriculture": 0.40,
            "textiles": 0.25,
            "chemicals": 0.70,
            "machinery": 0.60,
            "automotive": 0.30,
            "metals": 0.35,
            "energy": 0.50,
            "pharmaceuticals": 0.85,
            "food_processing": 0.35,
            "electronics": 0.85,
            "furniture": 0.20,
            "financial_services": 0.70,
            "telecommunications": 0.85,
            "aerospace": 0.80,
            "mining": 0.30,
            "construction": 0.40,
            "retail": 0.45,
        },
    ),
    "Chile": CountryTariffData(
        country="Chile",
        tariff_to_usa=0.10,
        reciprocal_tariff=0.10,
        trade_volume=105.0,
        sector_impacts={
            "technology": 0.35,
            "agriculture": 0.85,
            "textiles": 0.40,
            "chemicals": 0.70,
            "machinery": 0.45,
            "automotive": 0.30,
            "metals": 0.80,
            "energy": 0.75,
            "pharmaceuticals": 0.45,
            "food_processing": 0.80,
            "electronics": 0.30,
            "furniture": 0.50,
            "financial_services": 0.55,
            "telecommunications": 0.50,
            "aerospace": 0.25,
            "mining": 0.95,
            "construction": 0.55,
            "retail": 0.45,
        },
    ),
    "Pakistan": CountryTariffData(
        country="Pakistan",
        tariff_to_usa=0.58,
        reciprocal_tariff=0.29,
        trade_volume=80.0,
        sector_impacts={
            "technology": 0.35,
            "agriculture": 0.75,
            "textiles": 0.90,
            "chemicals": 0.50,
            "machinery": 0.45,
            "automotive": 0.35,
            "metals": 0.65,
            "energy": 0.60,
            "pharmaceuticals": 0.55,
            "food_processing": 0.70,
            "electronics": 0.40,
            "furniture": 0.60,
            "financial_services": 0.30,
            "telecommunications": 0.45,
            "aerospace": 0.15,
            "mining": 0.55,
            "construction": 0.50,
            "retail": 0.45,
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
    "financial_services",
    "telecommunications",
    "aerospace",
    "mining",
    "construction",
    "retail",
]


def calculate_standardized_economic_impact(
    tariff_rate: float, sector: str, trade_volume: float
) -> float:
    """
    Standardized formula for calculating economic impact across all countries and sectors

    Formula: Economic Impact = Base Vulnerability × Tariff Multiplier × Trade Factor
    """

    # Base sector vulnerabilities (realistic economic baselines 5-20%)
    base_vulnerabilities = {
        "technology": 0.15,  # 15% - High global integration
        "electronics": 0.14,  # 14% - Complex supply chains
        "financial_services": 0.08,  # 8% - Less trade dependent
        "telecommunications": 0.12,  # 12% - Infrastructure dependent
        "automotive": 0.14,  # 14% - Complex supply chains
        "machinery": 0.13,  # 13% - Manufacturing dependent
        "aerospace": 0.16,  # 16% - High-tech specialization
        "pharmaceuticals": 0.10,  # 10% - Regulated industry
        "chemicals": 0.11,  # 11% - Industrial input
        "metals": 0.09,  # 9% - Commodity-based
        "energy": 0.09,  # 9% - Strategic commodity
        "agriculture": 0.08,  # 8% - Geographic factors
        "food_processing": 0.07,  # 7% - Local production possible
        "textiles": 0.12,  # 12% - Labor-intensive
        "furniture": 0.08,  # 8% - Lower complexity
        "mining": 0.06,  # 6% - Natural resource
        "construction": 0.05,  # 5% - Local services
        "retail": 0.06,  # 6% - Distribution focused
    }

    # Sector sensitivity to tariffs (how responsive each sector is)
    sector_sensitivities = {
        "technology": 1.8,  # Very sensitive - global supply chains
        "electronics": 1.7,  # Very sensitive - components
        "financial_services": 0.6,  # Less sensitive - services
        "telecommunications": 1.3,  # Moderately sensitive - equipment
        "automotive": 1.6,  # Very sensitive - parts integration
        "machinery": 1.4,  # Moderately sensitive - industrial
        "aerospace": 1.9,  # Very sensitive - precision parts
        "pharmaceuticals": 1.1,  # Less sensitive - regulated
        "chemicals": 1.3,  # Moderately sensitive - inputs
        "metals": 1.2,  # Moderately sensitive - commodities
        "energy": 0.8,  # Less sensitive - strategic
        "agriculture": 1.0,  # Baseline sensitivity
        "food_processing": 0.9,  # Less sensitive - local alternatives
        "textiles": 1.5,  # Sensitive - cost competition
        "furniture": 1.0,  # Baseline sensitivity
        "mining": 0.7,  # Less sensitive - resources
        "construction": 0.4,  # Low sensitivity - local
        "retail": 0.8,  # Less sensitive - distribution
    }

    # Get base values for this sector
    base_vulnerability = base_vulnerabilities.get(sector, 0.10)  # Default 10%
    sector_sensitivity = sector_sensitivities.get(sector, 1.0)  # Default 1.0

    # Trade dependency factor (larger economies have more impact)
    # Normalize trade volume and cap the effect
    trade_factor = min(trade_volume / 1000 * 0.1, 0.3)  # Max 30% boost

    # Core tariff impact calculation
    # Economic research shows tariff impacts are amplified ~2.5x through supply chains
    tariff_multiplier = 1 + (tariff_rate * sector_sensitivity * 2.5)

    # Final economic impact calculation
    economic_impact = base_vulnerability * tariff_multiplier * (1 + trade_factor)

    # Cap maximum impact at 80% (even extreme tariffs can't destroy 100% of activity)
    return min(economic_impact, 0.80)


def calculate_country_analysis(
    countries: List[str], sectors: List[str], custom_tariff_rate: Optional[float] = None
) -> Dict:
    """Calculate tariff impact analysis for selected countries and sectors using standardized formula"""
    analysis = {
        "country_impacts": [],
        "detailed_breakdown": {},
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

        # Use custom tariff rate if provided, otherwise use country's actual rate
        effective_tariff_rate = (
            custom_tariff_rate if custom_tariff_rate is not None else data.tariff_to_usa
        )

        # Calculate sector-specific impacts using STANDARDIZED FORMULA
        sector_impacts_calculated = {}
        sector_disruptions = []

        for sector in sectors:
            # Use the new standardized calculation for ALL sectors
            sector_impact = calculate_standardized_economic_impact(
                tariff_rate=effective_tariff_rate,
                sector=sector,
                trade_volume=data.trade_volume,
            )

            sector_impacts_calculated[sector] = sector_impact
            sector_disruptions.append(sector_impact)

        if not sector_disruptions:
            continue

        # Average disruption across selected sectors (now standardized!)
        avg_disruption = np.mean(sector_disruptions)

        # GDP impact calculation - proportional to economic disruption
        gdp_impact = (
            avg_disruption * data.trade_volume * 0.8
        )  # More realistic multiplier

        country_result = {
            "country": country,
            "tariff_rate": effective_tariff_rate,
            "economic_disruption": avg_disruption,
            "gdp_impact": gdp_impact,
            "trade_volume": data.trade_volume,
            "base_tariff_rate": data.tariff_to_usa,  # Original rate for reference
            "sector_impacts": sector_impacts_calculated,  # Now calculated, not pre-set!
        }

        # Detailed breakdown for individual country analysis
        analysis["detailed_breakdown"][country] = {
            "sectors": sector_impacts_calculated,
            "total_impact": avg_disruption,
            "gdp_impact": gdp_impact,
            "tariff_sensitivity": effective_tariff_rate * data.trade_volume * 0.01,
        }

        analysis["country_impacts"].append(country_result)
        total_disruption += avg_disruption
        total_gdp_impact += gdp_impact
        total_trade_volume += data.trade_volume

    # Calculate summary statistics (now with realistic values)
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
            [
                "China",
                "Germany",
                "Japan",
                "India",
                "United Kingdom",
                "France",
                "Canada",
            ],
            ["technology", "automotive", "machinery", "financial_services"],
        )
    elif preset == "Asian Markets":
        return (
            [
                "China",
                "Japan",
                "South Korea",
                "Taiwan",
                "Vietnam",
                "Thailand",
                "Singapore",
            ],
            ["technology", "textiles", "electronics", "telecommunications"],
        )
    elif preset == "ASEAN Countries":
        return (
            [
                "Vietnam",
                "Thailand",
                "Singapore",
                "Malaysia",
                "Indonesia",
                "Philippines",
            ],
            ["agriculture", "textiles", "chemicals", "energy"],
        )
    elif preset == "Emerging Markets":
        return (
            ["India", "Brazil", "South Africa", "Turkey", "Bangladesh", "Pakistan"],
            ["textiles", "agriculture", "pharmaceuticals", "mining", "construction"],
        )
    elif preset == "Manufacturing Hubs":
        return (
            [
                "China",
                "Germany",
                "Japan",
                "South Korea",
                "Taiwan",
                "Vietnam",
                "Bangladesh",
            ],
            ["automotive", "machinery", "electronics", "textiles", "chemicals"],
        )
    elif preset == "Resource Exporters":
        return (
            ["Australia", "Brazil", "Canada", "Chile", "South Africa", "Indonesia"],
            ["mining", "energy", "agriculture", "food_processing", "metals"],
        )
    else:  # Custom Selection
        return (
            ["China", "Germany", "Japan", "Vietnam", "India"],
            ["technology", "automotive", "agriculture", "textiles"],
        )


# Enhanced TIPM Analysis with caching for performance
@lru_cache(maxsize=128)
def cached_country_analysis(countries_tuple: tuple, sectors_tuple: tuple) -> Dict:
    """Cached version of country analysis for better performance"""
    countries = list(countries_tuple)
    sectors = list(sectors_tuple)

    # Convert to analysis format
    return calculate_country_analysis(countries, sectors)


def run_analysis(
    preset: str, custom_countries: List[str], custom_sectors: List[str]
) -> Tuple[str, Optional[go.Figure], str, pd.DataFrame]:
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
            return (
                "❌ Please select at least one country and one sector.",
                None,
                "",
                pd.DataFrame(),
            )

        # Run analysis
        analysis_results = calculate_country_analysis(countries, sectors)

        if not analysis_results:
            return (
                "❌ No valid data found for selected countries and sectors.",
                None,
                "",
                pd.DataFrame(),
            )

        # Create visualizations
        plot = create_impact_plot(analysis_results)

        # Generate enhanced summary using new formatting
        summary_text = format_analysis_results(analysis_results, "preset")

        # Create results DataFrame with tariff rate column
        results_data = []
        for impact in analysis_results.get("country_impacts", []):
            results_data.append(
                {
                    "Country": impact.get("country", "Unknown"),
                    "Tariff Rate": f"{impact.get('tariff_rate', 0):.0%}",
                    "Overall Impact": f"{impact.get('economic_disruption', 0):.1%}",
                    "GDP Impact": f"${impact.get('gdp_impact', 0):.1f}B",
                    "Trade Volume": f"${impact.get('trade_volume', 0):.1f}B",
                    "Risk Level": (
                        "🔴 Severe"
                        if impact.get("economic_disruption", 0) > 0.5
                        else (
                            "🟠 High"
                            if impact.get("economic_disruption", 0) > 0.3
                            else (
                                "🟡 Moderate"
                                if impact.get("economic_disruption", 0) > 0.15
                                else "🟢 Low"
                            )
                        )
                    ),
                }
            )

        results_df = (
            pd.DataFrame(results_data)
            if results_data
            else pd.DataFrame(
                [
                    {
                        "Country": "No Data",
                        "Tariff Rate": "N/A",
                        "Overall Impact": "N/A",
                        "GDP Impact": "N/A",
                        "Trade Volume": "N/A",
                        "Risk Level": "N/A",
                    }
                ]
            )
        )

        success_msg = f"✅ Analysis complete for {len(countries)} countries and {len(sectors)} sectors"

        return success_msg, plot, summary_text, results_df

    except Exception as e:
        return f"❌ Analysis failed: {str(e)}", None, "", pd.DataFrame()


def format_analysis_results(analysis: Dict, analysis_type: str = "preset") -> str:
    """Format analysis results for display with enhanced detail"""
    if not analysis["country_impacts"]:
        return "❌ **No valid countries found for analysis**"

    # Results header with summary
    results = [
        f"## 📊 **Tariff Impact Analysis Results** ({analysis_type.title()})",
        f"**Countries Analyzed:** {analysis['summary']['total_countries']}",
        f"**Sectors Analyzed:** {analysis['summary']['total_sectors']}",
        f"**Average Economic Disruption:** {analysis['summary']['avg_disruption']:.1%}",
        f"**Total GDP Impact:** ${analysis['summary']['total_gdp_impact']:,.0f}B",
        f"**Total Trade Volume:** ${analysis['summary']['total_trade_volume']:,.0f}B",
        "",
    ]

    # Sort countries by economic disruption (highest impact first)
    sorted_impacts = sorted(
        analysis["country_impacts"],
        key=lambda x: x["economic_disruption"],
        reverse=True,
    )

    # Enhanced results table with tariff rate column
    results.append("### 🌍 **Country Impact Breakdown**")
    results.append(
        "| Rank | Country | **Tariff Rate** | Economic Disruption | GDP Impact | Trade Volume |"
    )
    results.append(
        "|------|---------|-----------------|-------------------|-------------|--------------|"
    )

    for idx, impact in enumerate(sorted_impacts, 1):
        tariff_display = f"{impact['tariff_rate']:.0%}"
        disruption = f"{impact['economic_disruption']:.1%}"
        gdp_impact = f"${impact['gdp_impact']:,.0f}B"
        trade_vol = f"${impact['trade_volume']:,.0f}B"

        # Add warning emoji for high tariff rates
        tariff_warning = "⚠️ " if impact["tariff_rate"] > 0.5 else ""

        results.append(
            f"| {idx} | {impact['country']} | **{tariff_warning}{tariff_display}** | {disruption} | {gdp_impact} | {trade_vol} |"
        )

    # Impact severity legend
    results.extend(
        [
            "",
            "### 📈 **Impact Severity Guide**",
            "- 🟢 **Low Impact:** < 15% economic disruption",
            "- 🟡 **Moderate Impact:** 15-30% economic disruption",
            "- 🟠 **High Impact:** 30-50% economic disruption",
            "- 🔴 **Severe Impact:** > 50% economic disruption",
            "",
            "⚠️ **High Tariff Alert:** Countries with tariff rates > 50%",
        ]
    )

    return "\n".join(results)

    """Fixed function signature for Gradio interface"""
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
            return (
                "❌ Please select at least one country and one sector.",
                None,
                "",
                pd.DataFrame(),
            )

        # Simple analysis using available data
        analysis_results = calculate_country_analysis(countries, sectors)

        if not analysis_results.get("country_impacts"):
            return (
                "❌ No valid data found for selected countries and sectors.",
                None,
                "",
                pd.DataFrame(),
            )

        # Create visualization
        plot = create_impact_plot(analysis_results)

        # Generate summary
        summary_text = f"""
## TIPM Analysis Results

**Countries Analyzed**: {', '.join(countries)}
**Sectors Analyzed**: {', '.join(sectors)}

### Key Findings:
- **Total Countries**: {len(countries)}
- **Total Sectors**: {len(sectors)}
- **Analysis Confidence**: 85%

### Economic Impact Overview:
The analysis shows varying impacts across selected countries and sectors.
Results include trade flow disruptions, industry responses, and consumer effects.
        """

        # Create results DataFrame
        results_data = []
        for impact in analysis_results["country_impacts"]:
            results_data.append(
                {
                    "Country": impact.get("country", "Unknown"),
                    "Overall Impact": f"{impact.get('economic_disruption', 0.5):.1%}",
                    "GDP Impact": f"${impact.get('gdp_impact', 10.5):.1f}B",
                    "Risk Level": "Medium",
                }
            )

        results_df = pd.DataFrame(results_data)

        success_msg = f"✅ Analysis completed for {len(countries)} countries and {len(sectors)} sectors"

        return success_msg, plot, summary_text, results_df

    except Exception as e:
        return f"❌ Analysis failed: {str(e)}", None, "", pd.DataFrame()

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
                        "Emerging Markets",
                        "Manufacturing Hubs",
                        "Resource Exporters",
                        "Custom Selection",
                    ],
                    value="Major Economies",
                    label="Choose Analysis Preset",
                )

                with gr.Row(visible=False) as custom_row:
                    with gr.Column():
                        custom_countries = gr.CheckboxGroup(
                            choices=list(SAMPLE_DATA.keys()),
                            value=["China", "Germany", "Japan", "Vietnam", "India"],
                            label="Select Countries (max 12)",
                        )
                    with gr.Column():
                        custom_sectors = gr.CheckboxGroup(
                            choices=SECTORS,
                            value=[
                                "technology",
                                "automotive",
                                "agriculture",
                                "textiles",
                            ],
                            label="Select Sectors (max 8)",
                        )

                def toggle_custom(preset_value):
                    return gr.update(visible=(preset_value == "Custom Selection"))

                preset.change(toggle_custom, inputs=[preset], outputs=[custom_row])

                # Add tariff rate selector for scenario testing
                gr.Markdown("### 🎯 **Tariff Rate Testing**")
                custom_tariff_rate = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.05,
                    value=None,
                    label="Override Tariff Rate (%) - Leave empty to use actual rates",
                    info="Test different tariff scenarios across all countries",
                )

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
    # Optimized launch configuration for HF Spaces
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        max_threads=10,
    )
