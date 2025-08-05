"""
Layer 2: Upstream Trade Flow Modeling
====================================

Models disruption to global trade networks using graph neural networks
and trade flow reallocation predictions.
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from ..config.layer_configs import TradeFlowConfig


@dataclass
class TradeFlowPrediction:
    """Trade flow impact prediction results"""

    affected_routes: List[Dict[str, Any]]
    reallocation_matrix: np.ndarray
    supply_chain_disruption: Dict[str, float]
    alternative_sources: Dict[str, List[str]]
    cost_increases: Dict[str, float]
    time_delays: Dict[str, float]


class TradeFlowLayer:
    """
    Layer 2: Trade Flow Modeling

    Predicts supply chain disruption and trade flow reallocation
    using graph-based representation of global trade networks.
    """

    def __init__(self, config: TradeFlowConfig):
        """Initialize trade flow layer"""
        self.config = config

        # Trade network graph
        self.trade_graph = nx.DiGraph()
        self.trade_data = None

        # ML models
        self.flow_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.cost_predictor = RandomForestRegressor(n_estimators=100, random_state=42)

        # Feature processing
        self.feature_scaler = StandardScaler()
        self.is_fitted = False

        # Trade route mappings
        self.country_to_index = {}
        self.index_to_country = {}
        self.hs_code_mappings = {}

    def fit(self, trade_data: Optional[pd.DataFrame]) -> "TradeFlowLayer":
        """
        Train trade flow models on historical data

        Args:
            trade_data: DataFrame with columns:
                - origin_country: Origin country code
                - destination_country: Destination country code
                - hs_code: Harmonized System product code
                - trade_value: Trade value in USD
                - year: Year of trade
                - transport_cost: Transportation cost
                - lead_time: Lead time in days
        """
        if trade_data is None or trade_data.empty:
            self._initialize_default_network()
            self.is_fitted = True
            return self

        self.trade_data = trade_data.copy()

        # Build trade network graph
        self._build_trade_graph(trade_data)

        # Prepare training features
        features, targets = self._prepare_training_data(trade_data)

        if len(features) > 0:
            # Fit feature scaler
            self.feature_scaler.fit(features)
            features_scaled = self.feature_scaler.transform(features)

            # Train flow prediction model
            flow_targets = [t["flow_change"] for t in targets]
            self.flow_predictor.fit(features_scaled, flow_targets)

            # Train cost prediction model
            cost_targets = [t["cost_change"] for t in targets]
            self.cost_predictor.fit(features_scaled, cost_targets)

        self.is_fitted = True
        return self

    def _initialize_default_network(self):
        """Initialize default trade network for demo purposes"""
        # Major trading countries
        major_countries = ["US", "CN", "DE", "JP", "UK", "FR", "NL", "SG", "KR", "IN"]

        # Create country mappings
        self.country_to_index = {
            country: i for i, country in enumerate(major_countries)
        }
        self.index_to_country = {
            i: country for i, country in enumerate(major_countries)
        }

        # Add nodes to graph
        for country in major_countries:
            self.trade_graph.add_node(country, trade_volume=1000000)

        # Add default trade relationships (simplified)
        default_routes = [
            ("CN", "US", 500000),
            ("US", "CN", 400000),
            ("CN", "DE", 300000),
            ("DE", "CN", 250000),
            ("US", "DE", 200000),
            ("DE", "US", 180000),
            ("CN", "JP", 250000),
            ("JP", "CN", 220000),
            ("SG", "CN", 150000),
            ("CN", "SG", 160000),
            ("SG", "US", 100000),
            ("US", "SG", 90000),
        ]

        for origin, dest, volume in default_routes:
            self.trade_graph.add_edge(
                origin, dest, trade_volume=volume, transport_cost=0.05, lead_time=14
            )

    def _build_trade_graph(self, trade_data: pd.DataFrame):
        """Build trade network graph from historical data"""
        # Get unique countries
        countries = list(
            set(
                trade_data["origin_country"].unique().tolist()
                + trade_data["destination_country"].unique().tolist()
            )
        )

        # Create country mappings
        self.country_to_index = {country: i for i, country in enumerate(countries)}
        self.index_to_country = {i: country for i, country in enumerate(countries)}

        # Add nodes
        for country in countries:
            country_volume = trade_data[
                (trade_data["origin_country"] == country)
                | (trade_data["destination_country"] == country)
            ]["trade_value"].sum()

            self.trade_graph.add_node(country, trade_volume=country_volume)

        # Add edges (trade routes)
        route_aggregates = (
            trade_data.groupby(["origin_country", "destination_country"])
            .agg({"trade_value": "sum", "transport_cost": "mean", "lead_time": "mean"})
            .reset_index()
        )

        for _, row in route_aggregates.iterrows():
            self.trade_graph.add_edge(
                row["origin_country"],
                row["destination_country"],
                trade_volume=row["trade_value"],
                transport_cost=row["transport_cost"],
                lead_time=row["lead_time"],
            )

    def _prepare_training_data(
        self, trade_data: pd.DataFrame
    ) -> Tuple[List[List[float]], List[Dict[str, float]]]:
        """Prepare training features and targets"""
        features = []
        targets = []

        # Simulate historical tariff shocks for training
        # In practice, this would use actual historical policy data
        sample_size = min(1000, len(trade_data))
        sample_data = trade_data.sample(n=sample_size, random_state=42)

        for _, row in sample_data.iterrows():
            # Extract features
            feature_vector = self._extract_route_features(
                row["origin_country"], row["destination_country"], row["hs_code"]
            )

            # Simulate targets (would be actual historical impacts)
            target = {
                "flow_change": np.random.normal(0, 0.2),  # ±20% flow change
                "cost_change": np.random.uniform(0, 0.1),  # 0-10% cost increase
            }

            features.append(feature_vector)
            targets.append(target)

        return features, targets

    def _extract_route_features(
        self, origin: str, destination: str, hs_code: str
    ) -> List[float]:
        """Extract features for a trade route"""
        features = []

        # Basic route features
        if self.trade_graph.has_edge(origin, destination):
            edge_data = self.trade_graph[origin][destination]
            features.extend(
                [
                    np.log1p(edge_data.get("trade_volume", 1)),
                    edge_data.get("transport_cost", 0.05),
                    edge_data.get("lead_time", 14),
                ]
            )
        else:
            features.extend([0, 0.1, 30])  # Default values for missing routes

        # Country-level features
        origin_volume = (
            self.trade_graph.nodes[origin].get("trade_volume", 0)
            if origin in self.trade_graph
            else 0
        )
        dest_volume = (
            self.trade_graph.nodes[destination].get("trade_volume", 0)
            if destination in self.trade_graph
            else 0
        )

        features.extend([np.log1p(origin_volume), np.log1p(dest_volume)])

        # HS code features (simplified)
        hs_numeric = float(hs_code[:2]) if hs_code and hs_code[:2].isdigit() else 0
        features.append(hs_numeric)

        # Network centrality features
        if origin in self.trade_graph:
            origin_centrality = nx.degree_centrality(self.trade_graph)[origin]
        else:
            origin_centrality = 0

        if destination in self.trade_graph:
            dest_centrality = nx.degree_centrality(self.trade_graph)[destination]
        else:
            dest_centrality = 0

        features.extend([origin_centrality, dest_centrality])

        return features

    def predict(self, policy_features) -> TradeFlowPrediction:
        """
        Predict trade flow impacts from policy features

        Args:
            policy_features: Output from PolicyTriggerLayer

        Returns:
            TradeFlowPrediction: Predicted trade flow impacts
        """
        if not self.is_fitted:
            raise ValueError("Layer must be fitted before prediction")

        # Extract relevant information from policy features
        affected_countries = getattr(policy_features, "affected_countries", [])
        hs_codes = getattr(policy_features, "hs_codes", [])
        tariff_rates = getattr(policy_features, "tariff_rates", [])
        country_tariff_map = getattr(policy_features, "country_tariff_map", {})

        # Default to demo values if no policy features
        if not affected_countries:
            affected_countries = ["US", "CN"]
        if not hs_codes:
            hs_codes = ["85"]
        if not tariff_rates:
            tariff_rates = [0.25]

        # Identify affected trade routes
        affected_routes = self._identify_affected_routes(affected_countries, hs_codes)

        # Predict flow changes for each route
        flow_predictions = []
        cost_predictions = []

        for route in affected_routes:
            features = self._extract_route_features(
                route["origin"], route["destination"], route["hs_code"]
            )

            if len(features) > 0:
                # Get country-specific tariff rate
                country = (
                    route["origin"]
                    if route["origin"] in affected_countries
                    else route["destination"]
                )
                country_tariff_rate = country_tariff_map.get(country, 0.0)

                # Scale features
                features_scaled = self.feature_scaler.transform([features])

                # Predict base impacts (use baseline models)
                base_flow_change = self.flow_predictor.predict(features_scaled)[0]
                base_cost_change = self.cost_predictor.predict(features_scaled)[0]

                # Apply country-specific tariff rate directly
                # Higher tariff = more flow disruption and cost increase
                flow_change = base_flow_change * (
                    1 + country_tariff_rate * 2
                )  # Scale tariff impact
                cost_change = country_tariff_rate * 0.8  # Direct tariff impact on costs

                route["flow_change"] = flow_change
                route["cost_change"] = cost_change
                route["tariff_rate"] = country_tariff_rate

                flow_predictions.append(flow_change)
                cost_predictions.append(cost_change)

        # Calculate aggregate impacts
        supply_chain_disruption = self._calculate_supply_chain_disruption(
            affected_routes
        )
        alternative_sources = self._find_alternative_sources(affected_routes)
        reallocation_matrix = self._calculate_reallocation_matrix(affected_routes)

        # Calculate cost increases and time delays
        cost_increases = {
            route["route_id"]: route.get("cost_change", 0) for route in affected_routes
        }
        time_delays = {
            route["route_id"]: route.get("cost_change", 0) * 5
            for route in affected_routes
        }  # Simplified

        return TradeFlowPrediction(
            affected_routes=affected_routes,
            reallocation_matrix=reallocation_matrix,
            supply_chain_disruption=supply_chain_disruption,
            alternative_sources=alternative_sources,
            cost_increases=cost_increases,
            time_delays=time_delays,
        )

    def _identify_affected_routes(
        self, countries: List[str], hs_codes: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify trade routes affected by tariff changes"""
        affected_routes = []

        # Check all edges in trade graph
        for origin, destination, edge_data in self.trade_graph.edges(data=True):
            # Check if route involves affected countries
            if origin in countries or destination in countries:
                route = {
                    "route_id": f"{origin}-{destination}",
                    "origin": origin,
                    "destination": destination,
                    "hs_code": (
                        hs_codes[0] if hs_codes else "85"
                    ),  # Default to electronics
                    "baseline_volume": edge_data.get("trade_volume", 0),
                    "baseline_cost": edge_data.get("transport_cost", 0.05),
                    "baseline_time": edge_data.get("lead_time", 14),
                }
                affected_routes.append(route)

        return affected_routes

    def _calculate_supply_chain_disruption(
        self, affected_routes: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate supply chain disruption scores by sector"""
        disruption_scores = {}

        # Group by HS code (sector)
        sectors = {}
        for route in affected_routes:
            hs_code = route["hs_code"]
            if hs_code not in sectors:
                sectors[hs_code] = []
            sectors[hs_code].append(route)

        # Calculate disruption for each sector
        for hs_code, routes in sectors.items():
            total_impact = sum(abs(route.get("flow_change", 0)) for route in routes)
            total_volume = sum(route["baseline_volume"] for route in routes)

            if total_volume > 0:
                disruption_score = min(total_impact / total_volume, 1.0)
            else:
                disruption_score = 0.0

            disruption_scores[hs_code] = disruption_score

        return disruption_scores

    def _find_alternative_sources(
        self, affected_routes: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Find alternative sourcing options for disrupted routes"""
        alternatives = {}

        for route in affected_routes:
            destination = route["destination"]
            origin = route["origin"]

            # Find other countries that export to the same destination
            alternative_origins = []
            for node in self.trade_graph.nodes():
                if (
                    node != origin
                    and self.trade_graph.has_edge(node, destination)
                    and node not in [origin]
                ):
                    alternative_origins.append(node)

            alternatives[route["route_id"]] = alternative_origins[
                :5
            ]  # Top 5 alternatives

        return alternatives

    def _calculate_reallocation_matrix(
        self, affected_routes: List[Dict[str, Any]]
    ) -> np.ndarray:
        """Calculate trade flow reallocation matrix"""
        num_countries = len(self.country_to_index)
        reallocation_matrix = np.zeros((num_countries, num_countries))

        for route in affected_routes:
            origin_idx = self.country_to_index.get(route["origin"])
            dest_idx = self.country_to_index.get(route["destination"])

            if origin_idx is not None and dest_idx is not None:
                flow_change = route.get("flow_change", 0)
                reallocation_matrix[origin_idx, dest_idx] = flow_change

        return reallocation_matrix

    def get_network_statistics(self) -> Dict[str, Any]:
        """Get trade network statistics"""
        if not self.trade_graph:
            return {}

        return {
            "num_countries": self.trade_graph.number_of_nodes(),
            "num_routes": self.trade_graph.number_of_edges(),
            "network_density": nx.density(self.trade_graph),
            "average_clustering": nx.average_clustering(self.trade_graph),
            "most_connected_countries": [
                node
                for node, degree in sorted(
                    list(self.trade_graph.degree()), key=lambda x: x[1], reverse=True
                )[:5]
            ],
        }
