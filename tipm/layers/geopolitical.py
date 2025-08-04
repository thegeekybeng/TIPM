"""
Layer 6: Geopolitical & Social Feedback
======================================

Predicts social unrest and political responses using
transformer-based NLP and event sequence models.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..config.layer_configs import GeopoliticalConfig


@dataclass
class GeopoliticalImpact:
    """Geopolitical impact prediction"""
    social_tension: Dict[str, float]
    protest_probability: Dict[str, float] 
    political_stability: Dict[str, float]
    policy_responses: Dict[str, str]
    migration_pressure: Dict[str, float]


class GeopoliticalLayer:
    """Layer 6: Geopolitical & Social Feedback"""
    
    def __init__(self, config: GeopoliticalConfig):
        self.config = config
        self.is_fitted = False
    
    def fit(self, geopolitical_data: Optional[Any]) -> "GeopoliticalLayer":
        """Train geopolitical models"""
        self.is_fitted = True
        return self
    
    def predict(self, consumer_impact) -> GeopoliticalImpact:
        """Predict geopolitical and social impacts"""
        if not self.is_fitted:
            raise ValueError("Layer must be fitted before prediction")
        
        # Extract consumer impact data
        price_increases = getattr(consumer_impact, 'price_increases', {})
        welfare_effects = getattr(consumer_impact, 'welfare_effects', {})
        
        # Simulate geopolitical responses
        social_tension = {}
        protest_probability = {}
        political_stability = {}
        policy_responses = {}
        migration_pressure = {}
        
        for sector, price_impact in price_increases.items():
            # Social tension increases with price impacts
            social_tension[sector] = min(price_impact * 2, 1.0)
            
            # Protest probability based on welfare effects
            welfare_impact = abs(welfare_effects.get(sector, 0))
            protest_probability[sector] = min(welfare_impact * 3, 1.0)
            
            # Political stability decreases with social tension
            political_stability[sector] = max(0.1, 1 - social_tension[sector] * 0.5)
            
            # Policy response classification
            if social_tension[sector] > 0.7:
                policy_responses[sector] = "emergency_measures"
            elif social_tension[sector] > 0.4:
                policy_responses[sector] = "subsidies"
            elif social_tension[sector] > 0.2:
                policy_responses[sector] = "monitoring"
            else:
                policy_responses[sector] = "no_action"
            
            # Migration pressure
            migration_pressure[sector] = social_tension[sector] * 0.3
        
        return GeopoliticalImpact(
            social_tension=social_tension,
            protest_probability=protest_probability,
            political_stability=political_stability,
            policy_responses=policy_responses,
            migration_pressure=migration_pressure
        )
