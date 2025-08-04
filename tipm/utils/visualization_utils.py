"""
Visualization utilities for TIPM outputs
"""

from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns


class TIPMVisualizer:
    """
    Visualization utilities for TIPM model outputs
    """
    
    def __init__(self):
        """Initialize visualizer with default styling"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_impact_summary(self, prediction_result) -> None:
        """Create summary visualization of tariff impact prediction"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Tariff Impact Propagation Summary', fontsize=16)
        
        # Trade flow impact
        if hasattr(prediction_result, 'trade_flow_impact'):
            self._plot_trade_flow_impact(axes[0, 0], prediction_result.trade_flow_impact)
        
        # Industry response
        if hasattr(prediction_result, 'industry_response'):
            self._plot_industry_response(axes[0, 1], prediction_result.industry_response)
        
        # Firm impact
        if hasattr(prediction_result, 'firm_impact'):
            self._plot_firm_impact(axes[0, 2], prediction_result.firm_impact)
        
        # Consumer impact
        if hasattr(prediction_result, 'consumer_impact'):
            self._plot_consumer_impact(axes[1, 0], prediction_result.consumer_impact)
        
        # Geopolitical impact
        if hasattr(prediction_result, 'geopolitical_impact'):
            self._plot_geopolitical_impact(axes[1, 1], prediction_result.geopolitical_impact)
        
        # Confidence scores
        if hasattr(prediction_result, 'confidence_scores'):
            self._plot_confidence_scores(axes[1, 2], prediction_result.confidence_scores)
        
        plt.tight_layout()
        plt.show()
    
    def _plot_trade_flow_impact(self, ax, trade_impact):
        """Plot trade flow disruption"""
        if hasattr(trade_impact, 'supply_chain_disruption'):
            disruption = trade_impact.supply_chain_disruption
            sectors = list(disruption.keys())
            values = list(disruption.values())
            
            ax.bar(sectors[:5], values[:5])  # Top 5 affected sectors
            ax.set_title('Supply Chain Disruption')
            ax.set_ylabel('Disruption Score')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, 'No trade flow data', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_industry_response(self, ax, industry_impact):
        """Plot industry-level responses"""
        if hasattr(industry_impact, 'sector_impacts'):
            sectors = list(industry_impact.sector_impacts.keys())[:5]
            impacts = [industry_impact.sector_impacts[s] for s in sectors]
            
            ax.barh(sectors, impacts)
            ax.set_title('Industry Sector Impacts')
            ax.set_xlabel('Impact Magnitude')
        else:
            ax.text(0.5, 0.5, 'No industry data', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_firm_impact(self, ax, firm_impact):
        """Plot firm-level impacts"""
        if hasattr(firm_impact, 'layoff_risk'):
            sectors = list(firm_impact.layoff_risk.keys())[:5]
            risks = [firm_impact.layoff_risk[s] for s in sectors]
            
            ax.scatter(risks, sectors)
            ax.set_title('Layoff Risk by Sector')
            ax.set_xlabel('Layoff Risk')
        else:
            ax.text(0.5, 0.5, 'No firm data', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_consumer_impact(self, ax, consumer_impact):
        """Plot consumer market impacts"""
        if hasattr(consumer_impact, 'price_increases'):
            sectors = list(consumer_impact.price_increases.keys())[:5]
            prices = [consumer_impact.price_increases[s] for s in sectors]
            
            ax.pie(prices, labels=sectors, autopct='%1.1f%%')
            ax.set_title('Price Increases by Sector')
        else:
            ax.text(0.5, 0.5, 'No consumer data', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_geopolitical_impact(self, ax, geo_impact):
        """Plot geopolitical and social impacts"""
        if hasattr(geo_impact, 'social_tension'):
            sectors = list(geo_impact.social_tension.keys())[:5]
            tensions = [geo_impact.social_tension[s] for s in sectors]
            
            ax.plot(sectors, tensions, marker='o')
            ax.set_title('Social Tension Index')
            ax.set_ylabel('Tension Level')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, 'No geopolitical data', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_confidence_scores(self, ax, confidence_scores):
        """Plot model confidence scores"""
        if confidence_scores:
            layers = list(confidence_scores.keys())
            scores = list(confidence_scores.values())
            
            colors = ['red' if s < 0.5 else 'yellow' if s < 0.7 else 'green' for s in scores]
            ax.bar(layers, scores, color=colors)
            ax.set_title('Model Confidence Scores')
            ax.set_ylabel('Confidence')
            ax.set_ylim(0, 1)
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, 'No confidence data', ha='center', va='center', transform=ax.transAxes)
    
    def create_network_visualization(self, trade_graph) -> None:
        """Create trade network visualization"""
        # Placeholder for network visualization
        # Would use networkx and matplotlib to create network plots
        print("Network visualization would be created here")
    
    def create_dashboard(self, model_results: Dict[str, Any]) -> None:
        """Create interactive dashboard with Streamlit"""
        # Placeholder for Streamlit dashboard
        print("Interactive dashboard would be created here")
