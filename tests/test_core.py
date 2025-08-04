"""
Test suite for TIPM core functionality
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from tipm.core import TIPMModel, TariffShock, TIPMPrediction
from tipm.config import TIPMConfig


class TestTIPMModel:
    """Test cases for the main TIPM model"""

    def setup_method(self):
        """Set up test fixtures"""
        self.config = TIPMConfig()
        self.model = TIPMModel(self.config)

        self.sample_shock = TariffShock(
            tariff_id="TEST_001",
            hs_codes=["8517"],
            rate_change=0.25,
            origin_country="CN",
            destination_country="US",
            effective_date="2024-08-01",
            policy_text="Test tariff for unit testing",
        )

    def test_model_initialization(self):
        """Test model initialization"""
        assert isinstance(self.model, TIPMModel)
        assert self.model.config is not None
        assert not self.model.is_trained

    def test_model_training(self):
        """Test model training with empty data"""
        training_data = {}

        # Train model
        trained_model = self.model.fit(training_data)

        assert trained_model.is_trained
        assert isinstance(trained_model, TIPMModel)

    def test_prediction_without_training(self):
        """Test that prediction fails without training"""
        with pytest.raises(ValueError, match="Model must be trained"):
            self.model.predict(self.sample_shock)

    def test_prediction_with_training(self):
        """Test prediction after training"""
        # Train model
        self.model.fit({})

        # Make prediction
        prediction = self.model.predict(self.sample_shock)

        assert isinstance(prediction, TIPMPrediction)
        assert prediction.tariff_shock == self.sample_shock
        assert isinstance(prediction.confidence_scores, dict)

    def test_scenario_simulation(self):
        """Test scenario simulation"""
        # Train model
        self.model.fit({})

        # Create multiple shocks
        shocks = [self.sample_shock]

        # Run simulation
        results = self.model.simulate_scenario(shocks, time_horizon=6)

        assert isinstance(results, dict)
        assert "timeline" in results
        assert len(results["timeline"]) == len(shocks)

    def test_country_exposure(self):
        """Test country exposure analysis"""
        # Train model
        self.model.fit({})

        # Get country exposure
        exposure = self.model.get_country_exposure("US")

        assert isinstance(exposure, dict)
        assert "import_dependency" in exposure
        assert "export_exposure" in exposure


class TestTariffShock:
    """Test cases for TariffShock data structure"""

    def test_tariff_shock_creation(self):
        """Test creating a tariff shock"""
        shock = TariffShock(
            tariff_id="TEST_SHOCK",
            hs_codes=["8517", "8525"],
            rate_change=0.15,
            origin_country="CN",
            destination_country="US",
            effective_date="2024-08-01",
            policy_text="Test policy text",
        )

        assert shock.tariff_id == "TEST_SHOCK"
        assert len(shock.hs_codes) == 2
        assert shock.rate_change == 0.15
        assert shock.origin_country == "CN"
        assert shock.destination_country == "US"


class TestTIPMConfig:
    """Test cases for TIPM configuration"""

    def test_default_config(self):
        """Test default configuration creation"""
        config = TIPMConfig()

        assert config.random_seed == 42
        assert config.model_version == "0.1.0"
        assert config.confidence_threshold == 0.5
        assert config.max_prediction_horizon == 24

    def test_config_layer_initialization(self):
        """Test that layer configs are initialized"""
        config = TIPMConfig()

        assert config.policy_config is not None
        assert config.trade_flow_config is not None
        assert config.industry_config is not None
        assert config.firm_config is not None
        assert config.consumer_config is not None
        assert config.geopolitical_config is not None


@pytest.fixture
def sample_trade_data():
    """Sample trade data for testing"""
    return pd.DataFrame(
        {
            "origin_country": ["US", "CN", "DE", "JP"],
            "destination_country": ["CN", "US", "US", "US"],
            "hs_code": ["8517", "8525", "8528", "8517"],
            "trade_value": [1000000, 2000000, 1500000, 800000],
            "transport_cost": [0.05, 0.06, 0.04, 0.07],
            "lead_time": [14, 21, 18, 16],
            "year": [2023, 2023, 2023, 2023],
        }
    )


@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing"""
    return pd.DataFrame(
        {
            "policy_id": ["POL_001", "POL_002"],
            "effective_date": ["2023-01-01", "2023-06-01"],
            "origin_country": ["US", "CN"],
            "destination_country": ["CN", "US"],
            "hs_codes": [["8517"], ["8525"]],
            "tariff_rate": [0.15, 0.20],
            "policy_text": ["Test policy 1", "Test policy 2"],
            "policy_type": ["tariff", "tariff"],
        }
    )


class TestDataIntegration:
    """Test cases for data integration"""

    def test_model_training_with_data(self, sample_trade_data, sample_policy_data):
        """Test model training with actual data"""
        config = TIPMConfig()
        model = TIPMModel(config)

        training_data = {
            "tariff_shocks": sample_policy_data,
            "trade_flows": sample_trade_data,
            "industry_responses": None,
            "firm_responses": None,
            "consumer_impacts": None,
            "geopolitical_events": None,
        }

        # Should not raise any exceptions
        trained_model = model.fit(training_data)
        assert trained_model.is_trained

    def test_prediction_with_data(self, sample_trade_data, sample_policy_data):
        """Test prediction with real data"""
        config = TIPMConfig()
        model = TIPMModel(config)

        # Train with data
        training_data = {
            "tariff_shocks": sample_policy_data,
            "trade_flows": sample_trade_data,
        }
        model.fit(training_data)

        # Create test shock
        shock = TariffShock(
            tariff_id="INTEGRATION_TEST",
            hs_codes=["8517"],
            rate_change=0.25,
            origin_country="CN",
            destination_country="US",
            effective_date="2024-08-01",
            policy_text="Integration test tariff",
        )

        # Make prediction
        prediction = model.predict(shock)

        assert isinstance(prediction, TIPMPrediction)
        assert "overall_confidence" in prediction.confidence_scores


if __name__ == "__main__":
    pytest.main([__file__])
