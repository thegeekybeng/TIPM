"""
TIPM - Tariff Impact Propagation Model
Real Data Integration Package
"""

from .real_data_connectors import (
    RealDataManager,
    TariffData,
    TradeData,
    USITCConnector,
    UNComtradeConnector,
    WTOConnector,
    WorldBankConnector,
)

__version__ = "2.0.0"
__author__ = "TIPM Development Team"
__description__ = "Real Data Integration for US Tariff Analysis"

__all__ = [
    "RealDataManager",
    "TariffData",
    "TradeData",
    "USITCConnector",
    "UNComtradeConnector",
    "WTOConnector",
    "WorldBankConnector",
]
