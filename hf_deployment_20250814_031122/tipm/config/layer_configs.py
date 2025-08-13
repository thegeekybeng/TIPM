"""
TIPM v1.5 Layer Configurations
Authoritative data sources and category definitions
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TradeFlowConfig:
    """Configuration for Trade Flow Layer"""

    network_threshold: float = 0.1
    max_nodes: int = 1000
    centrality_measures: Optional[List[str]] = None

    def __post_init__(self):
        if self.centrality_measures is None:
            self.centrality_measures = ["betweenness", "closeness", "degree"]


@dataclass
class IndustryResponseConfig:
    """Configuration for Industry Response Layer"""

    sectors: Optional[List[str]] = None
    response_threshold: float = 0.05

    def __post_init__(self):
        if self.sectors is None:
            self.sectors = ["manufacturing", "services", "agriculture"]


@dataclass
class FirmImpactConfig:
    """Configuration for Firm Impact Layer"""

    firm_size_categories: Optional[List[str]] = None
    impact_threshold: float = 0.1

    def __post_init__(self):
        if self.firm_size_categories is None:
            self.firm_size_categories = ["small", "medium", "large"]


@dataclass
class ConsumerImpactConfig:
    """Configuration for Consumer Impact Layer"""

    price_elasticity: float = -0.5
    income_segments: Optional[List[str]] = None

    def __post_init__(self):
        if self.income_segments is None:
            self.income_segments = ["low", "middle", "high"]


@dataclass
class GeopoliticalConfig:
    """Configuration for geopolitical analysis layer"""

    model_type: str = "transformer"
    max_sequence_length: Optional[int] = 512
    num_attention_heads: Optional[int] = 8
    hidden_size: Optional[int] = 256
    num_layers: Optional[int] = 6
    dropout_rate: Optional[float] = 0.1
    learning_rate: Optional[float] = 1e-4
    batch_size: Optional[int] = 16
    max_epochs: Optional[int] = 50
    early_stopping_patience: Optional[int] = 5
    social_indicators: Optional[List[str]] = None
    economic_indicators: Optional[List[str]] = None
    political_indicators: Optional[List[str]] = None

    def __post_init__(self):
        if self.social_indicators is None:
            self.social_indicators = [
                "unemployment_rate",
                "income_inequality",
                "social_unrest_index",
            ]
        if self.economic_indicators is None:
            self.economic_indicators = ["gdp_growth", "inflation_rate", "trade_balance"]
        if self.political_indicators is None:
            self.political_indicators = [
                "political_stability",
                "policy_uncertainty",
                "election_cycle",
            ]


# Additional configuration aliases for compatibility
IndustryConfig = IndustryResponseConfig
FirmConfig = FirmImpactConfig
ConsumerConfig = ConsumerImpactConfig


# Authoritative data sources
OFFICIAL_DATA_SOURCES = {
    "trade_data": {
        "source": "US Census Bureau Foreign Trade Division",
        "api": "https://api.census.gov/data/timeseries/intltrade",
        "dataset": "USA Trade Online",
        "update_frequency": "Monthly",
        "coverage": "All 184 target countries",
    },
    "tariff_rates": {
        "source": "US Trade Representative (USTR)",
        "dataset": "Section 301 Investigation Records",
        "methodology": "Historical tariff implementation data",
        "verification": "Federal Register publications",
    },
    "economic_indicators": {
        "source": "World Bank Open Data",
        "api": "https://api.worldbank.org/v2/country",
        "indicators": ["NY.GDP.MKTP.CD", "NY.GDP.PCAP.CD", "NE.TRD.GNFS.ZS"],
        "update_frequency": "Annual",
    },
}

INTERNATIONAL_SOURCES = {
    "classification_systems": {
        "msci_emerging_markets": "https://www.msci.com/market-classification",
        "ftse_russell_classification": "https://www.ftserussell.com/data/country-classification-update",
        "oecd_ict_statistics": "https://stats.oecd.org/Index.aspx?DataSetCode=ICTS_R",
        "un_comtrade": "https://comtrade.un.org/api/swagger/ui/index",
    },
    "commodity_data": {
        "world_bank_commodities": "https://www.worldbank.org/en/research/commodity-markets",
        "usgs_minerals": "https://www.usgs.gov/centers/national-minerals-information-center",
        "fao_agricultural": "http://www.fao.org/faostat/en/#data",
    },
}

# Category definitions
EMERGING_MARKETS = {
    "Argentina",
    "Brazil",
    "Chile",
    "China",
    "Colombia",
    "Czech Republic",
    "Egypt",
    "Greece",
    "Hungary",
    "India",
    "Indonesia",
    "Kuwait",
    "Malaysia",
    "Mexico",
    "Peru",
    "Philippines",
    "Poland",
    "Qatar",
    "Saudi Arabia",
    "South Africa",
    "South Korea",
    "Taiwan",
    "Thailand",
    "Turkey",
    "UAE",
}

TECH_MANUFACTURING_EXPORTERS = {
    "China": {"rank": 1, "ict_exports_billion_usd": 890},
    "Germany": {"rank": 2, "ict_exports_billion_usd": 142},
    "United States": {"rank": 3, "ict_exports_billion_usd": 141},
    "South Korea": {"rank": 4, "ict_exports_billion_usd": 129},
    "Singapore": {"rank": 5, "ict_exports_billion_usd": 126},
    "Taiwan": {"rank": 6, "ict_exports_billion_usd": 125},
    "Japan": {"rank": 7, "ict_exports_billion_usd": 118},
    "Netherlands": {"rank": 8, "ict_exports_billion_usd": 85},
    "Mexico": {"rank": 9, "ict_exports_billion_usd": 78},
    "Malaysia": {"rank": 10, "ict_exports_billion_usd": 71},
}

MINING_RESOURCE_EXPORTERS = {
    "Australia": {"commodities": ["iron_ore", "coal", "lithium", "bauxite"]},
    "Chile": {"commodities": ["copper", "lithium", "molybdenum"]},
    "Peru": {"commodities": ["copper", "zinc", "silver", "gold"]},
    "Congo_DRC": {"commodities": ["cobalt", "copper", "tantalum"]},
    "South_Africa": {"commodities": ["platinum", "gold", "chromium"]},
    "Russia": {"commodities": ["palladium", "nickel", "diamond"]},
    "Canada": {"commodities": ["potash", "uranium", "nickel"]},
    "Brazil": {"commodities": ["iron_ore", "niobium", "bauxite"]},
}

AGRICULTURAL_EXPORTERS = {
    "Brazil": {"products": ["soybeans", "coffee", "sugar", "beef"]},
    "Argentina": {"products": ["soybeans", "wheat", "beef", "corn"]},
    "United_States": {"products": ["soybeans", "corn", "wheat", "pork"]},
    "Ukraine": {"products": ["wheat", "corn", "sunflower_oil"]},
    "India": {"products": ["rice", "tea", "spices", "cotton"]},
    "Thailand": {"products": ["rice", "rubber", "palm_oil"]},
    "Indonesia": {"products": ["palm_oil", "rubber", "cocoa"]},
    "Vietnam": {"products": ["rice", "coffee", "pepper"]},
}
