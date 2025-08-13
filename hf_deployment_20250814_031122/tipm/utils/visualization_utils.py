"""
TIPM v1.5 Visualization Utilities
"""

from typing import Dict, Any
import logging

# Optional imports with graceful fallback
try:
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    plt = None
try:
    import seaborn as sns

    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    sns = None


class TIPMVisualizer:
    """
    Visualization utilities for TIPM model outputs
    """

    def __init__(self):
        """Initialize visualizer with default styling"""
        self.logger = logging.getLogger("TIPM.Visualizer")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        if HAS_MATPLOTLIB:
            plt.style.use("seaborn-v0_8")
        else:
            self.logger.warning("matplotlib not available, skipping style setup")
        if HAS_SEABORN:
            sns.set_palette("husl")
        else:
            self.logger.warning("seaborn not available, skipping palette setup")

    def plot_impact_summary(self, prediction_result) -> None:
        """Create summary visualization of tariff impact prediction"""
        if not HAS_MATPLOTLIB:
            self.logger.warning("matplotlib not available, cannot plot impact summary")
            return
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Tariff Impact Propagation Summary", fontsize=16)
        # ...existing code for plotting...
        try:
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.logger.warning("matplotlib plotting failed: %s", e)

    def _plot_trade_flow_impact(self, ax, trade_impact):
        """Plot trade flow disruption"""
        if hasattr(trade_impact, "supply_chain_disruption"):
            disruption = trade_impact.supply_chain_disruption
            sectors = list(disruption.keys())
            values = list(disruption.values())

            ax.bar(sectors[:5], values[:5])  # Top 5 affected sectors
            ax.set_title("Supply Chain Disruption")
            ax.set_ylabel("Disruption Score")
            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                "No trade flow data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def _plot_industry_response(self, ax, industry_impact):
        """Plot industry-level responses"""
        if hasattr(industry_impact, "sector_impacts"):
            sectors = list(industry_impact.sector_impacts.keys())[:5]
            impacts = [industry_impact.sector_impacts[s] for s in sectors]

            ax.barh(sectors, impacts)
            ax.set_title("Industry Sector Impacts")
            ax.set_xlabel("Impact Magnitude")
        else:
            ax.text(
                0.5,
                0.5,
                "No industry data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def _plot_firm_impact(self, ax, firm_impact):
        """Plot firm-level impacts"""
        if hasattr(firm_impact, "layoff_risk"):
            sectors = list(firm_impact.layoff_risk.keys())[:5]
            risks = [firm_impact.layoff_risk[s] for s in sectors]

            ax.scatter(risks, sectors)
            ax.set_title("Layoff Risk by Sector")
            ax.set_xlabel("Layoff Risk")
        else:
            ax.text(
                0.5,
                0.5,
                "No firm data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def _plot_consumer_impact(self, ax, consumer_impact):
        """Plot consumer market impacts"""
        if hasattr(consumer_impact, "price_increases"):
            sectors = list(consumer_impact.price_increases.keys())[:5]
            prices = [consumer_impact.price_increases[s] for s in sectors]

            ax.pie(prices, labels=sectors, autopct="%1.1f%%")
            ax.set_title("Price Increases by Sector")
        else:
            ax.text(
                0.5,
                0.5,
                "No consumer data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def _plot_geopolitical_impact(self, ax, geo_impact):
        """Plot geopolitical and social impacts"""
        if hasattr(geo_impact, "social_tension"):
            sectors = list(geo_impact.social_tension.keys())[:5]
            tensions = [geo_impact.social_tension[s] for s in sectors]

            ax.plot(sectors, tensions, marker="o")
            ax.set_title("Social Tension Index")
            ax.set_ylabel("Tension Level")
            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                "No geopolitical data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def _plot_confidence_scores(self, ax, confidence_scores):
        """Plot model confidence scores"""
        if confidence_scores:
            layers = list(confidence_scores.keys())
            scores = list(confidence_scores.values())

            colors = [
                "red" if s < 0.5 else "yellow" if s < 0.7 else "green" for s in scores
            ]
            ax.bar(layers, scores, color=colors)
            ax.set_title("Model Confidence Scores")
            ax.set_ylabel("Confidence")
            ax.set_ylim(0, 1)
            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                "No confidence data",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

    def create_network_visualization(self, trade_graph) -> None:
        """Create trade network visualization"""
        # Placeholder for network visualization
        # Would use networkx and matplotlib to create network plots
        print("Network visualization would be created here")

    def create_dashboard(self, model_results: Dict[str, Any]) -> None:
        """Create interactive dashboard with Streamlit"""
        # Placeholder for Streamlit dashboard
        print("Interactive dashboard would be created here")


def visualize_country_impact(country_data: Any) -> None:
    """Visualize country impact data (stub)."""
    logging.info("Visualizing impact for %s", getattr(country_data, "name", "Unknown"))
    # Placeholder for actual implementation
