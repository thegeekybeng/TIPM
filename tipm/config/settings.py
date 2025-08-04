"""
Configuration management for TIPM layers
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class PolicyLayerConfig:
    """Configuration for Policy Trigger Layer"""
    model_name: str = "distilbert-base-uncased"
    max_text_length: int = 512
    tfidf_max_features: int = 1000
    urgency_threshold: float = 0.7
    similarity_threshold: float = 0.8


@dataclass 
class TradeFlowConfig:
    """Configuration for Trade Flow Layer"""
    graph_embedding_dim: int = 128
    gnn_hidden_dim: int = 64
    num_gnn_layers: int = 3
    trade_volume_threshold: float = 1000000  # USD
    elasticity_default: float = 0.5


@dataclass
class IndustryConfig:
    """Configuration for Industry Response Layer"""
    num_sectors: int = 20
    response_time_horizon: int = 12  # months
    substitution_elasticity: float = 0.3
    cost_passthrough_rate: float = 0.7


@dataclass
class FirmConfig:
    """Configuration for Firm Impact Layer"""
    firm_size_categories: List[str] = None
    employment_elasticity: float = 0.4
    adaptation_time_months: int = 6
    survival_probability_threshold: float = 0.1
    
    def __post_init__(self):
        if self.firm_size_categories is None:
            self.firm_size_categories = ["micro", "small", "medium", "large"]


@dataclass
class ConsumerConfig:
    """Configuration for Consumer Impact Layer"""
    cpi_basket_items: int = 200
    demand_elasticity_default: float = -0.8
    inflation_passthrough_lag: int = 3  # months
    income_percentiles: List[int] = None
    
    def __post_init__(self):
        if self.income_percentiles is None:
            self.income_percentiles = [10, 25, 50, 75, 90]


@dataclass
class GeopoliticalConfig:
    """Configuration for Geopolitical Layer"""
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    social_media_sources: List[str] = None
    event_prediction_horizon: int = 6  # months
    instability_threshold: float = 0.6
    
    def __post_init__(self):
        if self.social_media_sources is None:
            self.social_media_sources = ["twitter", "reddit", "news"]


@dataclass
class TIPMConfig:
    """Main TIPM Model Configuration"""
    # Layer configurations
    policy_config: PolicyLayerConfig = None
    trade_flow_config: TradeFlowConfig = None
    industry_config: IndustryConfig = None
    firm_config: FirmConfig = None
    consumer_config: ConsumerConfig = None
    geopolitical_config: GeopoliticalConfig = None
    
    # Global settings
    random_seed: int = 42
    model_version: str = "0.1.0"
    logging_level: str = "INFO"
    
    # Data sources
    data_update_frequency: str = "daily"
    cache_duration_hours: int = 24
    
    # Performance settings
    max_parallel_jobs: int = 4
    memory_limit_gb: int = 8
    
    # Output settings
    confidence_threshold: float = 0.5
    max_prediction_horizon: int = 24  # months
    
    def __post_init__(self):
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


# Country-specific configurations
COUNTRY_CONFIGS = {
    'SG': {  # Singapore
        'trade_dependency': 0.8,
        'import_elasticity': 0.6,
        'cpi_weights': {
            'food': 0.21,
            'transport': 0.15,
            'housing': 0.25,
            'healthcare': 0.08,
            'education': 0.10,
            'others': 0.21
        },
        'major_trading_partners': ['CHN', 'USA', 'MYS', 'IDN', 'JPN'],
        'vulnerable_sectors': ['electronics', 'petrochemicals', 'food_processing']
    },
    'US': {  # United States
        'trade_dependency': 0.3,
        'import_elasticity': 0.4,
        'cpi_weights': {
            'food': 0.14,
            'transport': 0.16,
            'housing': 0.33,
            'healthcare': 0.08,
            'education': 0.06,
            'others': 0.23
        },
        'major_trading_partners': ['CHN', 'CAN', 'MEX', 'JPN', 'DEU'],
        'vulnerable_sectors': ['manufacturing', 'agriculture', 'automotive']
    },
    'CN': {  # China
        'trade_dependency': 0.4,
        'import_elasticity': 0.5,
        'cpi_weights': {
            'food': 0.31,
            'transport': 0.13,
            'housing': 0.23,
            'healthcare': 0.09,
            'education': 0.08,
            'others': 0.16
        },
        'major_trading_partners': ['USA', 'JPN', 'KOR', 'DEU', 'AUS'],
        'vulnerable_sectors': ['manufacturing', 'textiles', 'electronics']
    }
}


# Sector classification mapping
SECTOR_MAPPING = {
    'agriculture': ['01', '02', '03', '04', '05'],  # HS codes
    'mining': ['25', '26', '27'],
    'food_processing': ['16', '17', '18', '19', '20', '21', '22', '23', '24'],
    'textiles': ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63'],
    'chemicals': ['28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38'],
    'plastics': ['39', '40'],
    'wood_paper': ['44', '45', '46', '47', '48', '49'],
    'metals': ['72', '73', '74', '75', '76', '78', '79', '80', '81', '82', '83'],
    'machinery': ['84', '85'],
    'electronics': ['85'],
    'automotive': ['87'],
    'optical_instruments': ['90', '91', '92']
}
