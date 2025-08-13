"""
Tariff Impact Propagation Model (TIPM)
=====================================

A comprehensive AI system for predicting how tariffs impact global markets,
supply chains, and populations through a multi-layered machine learning architecture.
"""

__version__ = "0.1.0"
__author__ = "TIPM Development Team"
__email__ = "tipm@example.com"

from .core import TIPMModel
from .layers import *
from .utils import *

__all__ = [
    "TIPMModel",
    "PolicyTriggerLayer",
    "TradeFlowLayer",
    "IndustryResponseLayer",
    "FirmImpactLayer",
    "ConsumerImpactLayer",
    "GeopoliticalLayer",
]
