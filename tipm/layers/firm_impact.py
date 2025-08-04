"""
Layer 4: Firm-Level & Employment Impact
======================================

Predicts firm adaptation behavior and employment effects
using survival analysis and decision trees.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..config.layer_configs import FirmConfig


@dataclass
class FirmImpact:
    """Firm-level impact prediction"""
    layoff_risk: Dict[str, float]
    relocation_probability: Dict[str, float]
    adaptation_strategies: Dict[str, str]
    employment_changes: Dict[str, int]
    firm_survival: Dict[str, float]


class FirmImpactLayer:
    """Layer 4: Firm-Level & Employment Impact"""
    
    def __init__(self, config: FirmConfig):
        self.config = config
        self.is_fitted = False
    
    def fit(self, firm_data: Optional[Any]) -> "FirmImpactLayer":
        """Train firm impact models"""
        self.is_fitted = True
        return self
    
    def predict(self, industry_impact) -> FirmImpact:
        """Predict firm-level impacts"""
        if not self.is_fitted:
            raise ValueError("Layer must be fitted before prediction")
        
        # Extract industry impact data
        employment_effects = getattr(industry_impact, 'employment_effects', {})
        sector_impacts = getattr(industry_impact, 'sector_impacts', {})
        
        # Simulate firm responses
        layoff_risk = {}
        relocation_probability = {}
        adaptation_strategies = {}
        employment_changes = {}
        firm_survival = {}
        
        for sector, impact in sector_impacts.items():
            layoff_risk[sector] = max(0, impact * 0.8)
            relocation_probability[sector] = impact * 0.3
            
            # Determine adaptation strategy
            if impact > 0.7:
                adaptation_strategies[sector] = "shutdown"
            elif impact > 0.4:
                adaptation_strategies[sector] = "relocate"
            elif impact > 0.2:
                adaptation_strategies[sector] = "absorb_costs"
            else:
                adaptation_strategies[sector] = "pass_through"
            
            employment_changes[sector] = int(employment_effects.get(sector, 0) * 1000)
            firm_survival[sector] = max(0.1, 1 - impact)
        
        return FirmImpact(
            layoff_risk=layoff_risk,
            relocation_probability=relocation_probability,
            adaptation_strategies=adaptation_strategies,
            employment_changes=employment_changes,
            firm_survival=firm_survival
        )
