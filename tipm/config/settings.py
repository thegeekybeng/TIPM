"""
Configuration management for TIPM layers
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator


class PolicyLayerConfig(BaseModel):
    """Configuration for Policy Trigger Layer"""

    model_name: str = Field(
        default="distilbert-base-uncased", description="NLP model for policy analysis"
    )
    max_text_length: int = Field(default=512, ge=128, le=1024)
    tfidf_max_features: int = Field(default=1000, ge=100, le=10000)
    urgency_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    similarity_threshold: float = Field(default=0.8, ge=0.0, le=1.0)


class TradeFlowConfig(BaseModel):
    """Configuration for Trade Flow Layer"""

    graph_embedding_dim: int = Field(default=128, ge=32, le=512)
    gnn_hidden_dim: int = Field(default=64, ge=16, le=256)
    num_gnn_layers: int = Field(default=3, ge=1, le=10)
    trade_volume_threshold: float = Field(
        default=1000000, ge=1000, description="USD threshold"
    )
    elasticity_default: float = Field(default=0.5, ge=0.0, le=2.0)


class IndustryConfig(BaseModel):
    """Configuration for Industry Response Layer"""

    num_sectors: int = Field(default=20, ge=5, le=100)
    response_time_horizon: int = Field(default=12, ge=1, le=60, description="months")
    substitution_elasticity: float = Field(default=0.3, ge=0.0, le=1.0)
    cost_passthrough_rate: float = Field(default=0.7, ge=0.0, le=1.0)


class FirmConfig(BaseModel):
    """Configuration for Firm Impact Layer"""

    firm_size_categories: List[str] = Field(
        default_factory=lambda: ["micro", "small", "medium", "large"]
    )
    employment_elasticity: float = Field(default=0.4, ge=0.0, le=1.0)
    adaptation_time_months: int = Field(default=6, ge=1, le=24)
    survival_probability_threshold: float = Field(default=0.1, ge=0.0, le=1.0)


class ConsumerConfig(BaseModel):
    """Configuration for Consumer Impact Layer"""

    cpi_basket_items: int = Field(default=200, ge=50, le=1000)
    demand_elasticity_default: float = Field(default=-0.8, ge=-2.0, le=0.0)
    inflation_passthrough_lag: int = Field(default=3, ge=1, le=12, description="months")
    income_percentiles: List[int] = Field(default_factory=lambda: [10, 25, 50, 75, 90])


class GeopoliticalConfig(BaseModel):
    """Configuration for Geopolitical Layer"""

    sentiment_model: str = Field(
        default="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    social_media_sources: List[str] = Field(
        default_factory=lambda: ["twitter", "reddit", "news"]
    )
    event_prediction_horizon: int = Field(default=6, ge=1, le=24, description="months")
    instability_threshold: float = Field(default=0.6, ge=0.0, le=1.0)


class TIPMConfig(BaseModel):
    """Main TIPM Model Configuration"""

    # Layer configurations
    policy_config: Optional[PolicyLayerConfig] = None
    trade_flow_config: Optional[TradeFlowConfig] = None
    industry_config: Optional[IndustryConfig] = None
    firm_config: Optional[FirmConfig] = None
    consumer_config: Optional[ConsumerConfig] = None
    geopolitical_config: Optional[GeopoliticalConfig] = None

    # Global settings
    random_seed: int = Field(default=42, ge=0)
    model_version: str = Field(default="1.5.0", pattern=r"^\d+\.\d+\.\d+$")
    logging_level: str = Field(
        default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )

    # Data sources
    data_update_frequency: str = Field(
        default="daily", pattern=r"^(hourly|daily|weekly|monthly)$"
    )
    cache_duration_hours: int = Field(default=24, ge=1, le=168)

    # Performance settings
    max_parallel_jobs: int = Field(default=4, ge=1, le=16)
    memory_limit_gb: int = Field(default=8, ge=2, le=64)

    # Output settings
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    max_prediction_horizon: int = Field(default=24, ge=1, le=60, description="months")

    class Config:
        validate_assignment = True

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize layer configs if not provided
        if self.policy_config is None:
            self.policy_config = PolicyLayerConfig()
        if self.trade_flow_config is None:
            self.trade_flow_config = TradeFlowConfig()
        if self.industry_config is None:
            self.industry_config = IndustryConfig()
        if self.firm_config is None:
            self.firm_config = FirmConfig()
        if self.consumer_config is None:
            self.consumer_config = ConsumerConfig()
        if self.geopolitical_config is None:
            self.geopolitical_config = GeopoliticalConfig()


# Country-specific configurations with validated data
COUNTRY_CONFIGS = {
    "SG": {  # Singapore - 2024 data
        "trade_dependency": 0.8,
        "import_elasticity": 0.6,
        "cpi_weights": {
            "food": 0.21,
            "transport": 0.15,
            "housing": 0.25,
            "healthcare": 0.08,
            "education": 0.10,
            "others": 0.21,
        },
        "major_trading_partners": ["CHN", "USA", "MYS", "IDN", "JPN"],
        "vulnerable_sectors": ["electronics", "petrochemicals", "food_processing"],
    },
    "US": {  # United States - 2024 data
        "trade_dependency": 0.3,
        "import_elasticity": 0.4,
        "cpi_weights": {
            "food": 0.14,
            "transport": 0.16,
            "housing": 0.33,
            "healthcare": 0.08,
            "education": 0.06,
            "others": 0.23,
        },
        "major_trading_partners": ["CHN", "CAN", "MEX", "JPN", "DEU"],
        "vulnerable_sectors": ["manufacturing", "agriculture", "automotive"],
    },
    "CN": {  # China - 2024 data
        "trade_dependency": 0.4,
        "import_elasticity": 0.5,
        "cpi_weights": {
            "food": 0.31,
            "transport": 0.13,
            "housing": 0.23,
            "healthcare": 0.09,
            "education": 0.08,
            "others": 0.16,
        },
        "major_trading_partners": ["USA", "JPN", "KOR", "DEU", "AUS"],
        "vulnerable_sectors": ["manufacturing", "textiles", "electronics"],
    },
}


# Sector classification mapping with validated HS codes
SECTOR_MAPPING = {
    "agriculture": ["01", "02", "03", "04", "05"],  # HS codes
    "mining": ["25", "26", "27"],
    "food_processing": ["16", "17", "18", "19", "20", "21", "22", "23", "24"],
    "textiles": [
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
    ],
    "chemicals": ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38"],
    "plastics": ["39", "40"],
    "wood_paper": ["44", "45", "46", "47", "48", "49"],
    "metals": ["72", "73", "74", "75", "76", "78", "79", "80", "81", "82", "83"],
    "machinery": ["84", "85"],
    "electronics": ["85"],
    "automotive": ["87"],
    "optical_instruments": ["90", "91", "92"],
}
