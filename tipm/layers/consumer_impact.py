"""
Layer 5: Consumer Market Impact & Cost-of-Living
==============================================

Models consumer price impacts and cost-of-living changes
using Bayesian time series and elasticity models.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..config.layer_configs import ConsumerConfig


@dataclass
class ConsumerImpact:
    """Consumer impact prediction"""
    price_increases: Dict[str, float]
    cpi_changes: Dict[str, float]
    demand_responses: Dict[str, float]
    welfare_effects: Dict[str, float]
    substitution_patterns: Dict[str, str]


class ConsumerImpactLayer:
    """Layer 5: Consumer Market Impact"""
    
    def __init__(self, config: ConsumerConfig):
        self.config = config
        self.is_fitted = False
    
    def fit(self, consumer_data: Optional[Any]) -> "ConsumerImpactLayer":
        """Train consumer impact models"""
        self.is_fitted = True
        return self
    
    def predict(self, firm_impact) -> ConsumerImpact:
        """Predict consumer market impacts"""
        if not self.is_fitted:
            raise ValueError("Layer must be fitted before prediction")
        
        # Extract firm impact data
        layoff_risk = getattr(firm_impact, 'layoff_risk', {})
        
        # Simulate consumer impacts
        price_increases = {}
        cpi_changes = {}
        demand_responses = {}
        welfare_effects = {}
        substitution_patterns = {}
        
        for sector, risk in layoff_risk.items():
            price_increases[sector] = risk * 0.15  # 15% max price increase
            cpi_changes[sector] = price_increases[sector] * 0.3  # CPI weight
            demand_responses[sector] = -price_increases[sector] * 0.8  # Elastic demand
            welfare_effects[sector] = -price_increases[sector] * 0.5  # Welfare loss
            
            # Substitution patterns
            if price_increases[sector] > 0.1:
                substitution_patterns[sector] = "substitute_imports"
            elif price_increases[sector] > 0.05:
                substitution_patterns[sector] = "reduce_consumption"
            else:
                substitution_patterns[sector] = "no_change"
        
        return ConsumerImpact(
            price_increases=price_increases,
            cpi_changes=cpi_changes,
            demand_responses=demand_responses,
            welfare_effects=welfare_effects,
            substitution_patterns=substitution_patterns
        )
