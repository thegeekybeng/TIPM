
# Copilot Instructions for TIPM v1.5

## Project Overview

TIPM (Tariff Impact Propagation Model) is an AI system for predicting the impact of tariffs on global markets, supply chains, and populations. The architecture is modular, with six distinct ML layers:

- **Policy Trigger Layer**: NLP for tariff announcements
- **Trade Flow Layer**: Graph neural networks for supply chain analysis
- **Industry Response Layer**: Multi-output regression for sectoral impacts
- **Firm Impact Layer**: Survival analysis for employment effects
- **Consumer Impact Layer**: Bayesian time series for price impacts
- **Geopolitical Layer**: Transformer NLP for social response prediction

## Key Files & Structure

- `tipm/core.py`: Orchestrates the full pipeline and data flow
- `tipm/layers/`: Contains layer modules, each with `.fit()` and `.predict()` methods
- `tipm/config/`: Configuration classes and settings
- `tipm/utils/`: Data processing, validation, and visualization utilities
- `notebooks/`: Jupyter notebooks for analysis and prototyping
- `scripts/`: Utility scripts for data and workflow automation
- `tests/`: Unit tests for core and layer logic

## Essential Patterns

- **Dataclasses**: Used for all structured data (e.g., `EnhancedCountryData`)
- **Layer Independence**: Each layer is testable and loosely coupled
- **Configuration-Driven**: All parameters managed via config classes
- **Type Hints**: Required for all public methods
- **Error Handling**: Use graceful degradation for missing/unavailable data
- **Confidence Scores**: All predictions return a confidence metric
- **Visualization**: Each output should have a visualization method
- **Logging**: Use comprehensive logging for debugging and data provenance

## Developer Workflows

- Build and install dependencies via `requirements.txt`
- Run tests in `tests/` for all layers and core logic
- Use Jupyter notebooks in `notebooks/` for exploratory analysis
- Data flows: Policy Text → Features → Trade Impact → Industry Response → Firm Impact → Consumer Impact → Geopolitical Response

## Project-Specific Conventions

- Use meaningful variable names (e.g., `tariff_rate`, `bilateral_trade_usd`)
- Validate and bound-check all input data
- Support both real and synthetic data for testing
- Document all public methods with comprehensive docstrings
- Structure code for scalability across multiple countries and scenarios

## Integration Points

- External data: World Bank, USTR, UN Comtrade, OECD APIs
- ML frameworks: PyTorch, scikit-learn, XGBoost, transformers
- Visualization: matplotlib, seaborn, plotly, streamlit

## Example Pattern

```python
@dataclass
class EnhancedCountryData:
    name: str
    tariff_rate: float
    # ...other fields...
    def fit(self, X, y): ...
    def predict(self, X): ...
```

---

**Feedback Request:**  
If any section is unclear or missing key project-specific details, please specify which workflows, patterns, or integration points need further documentation. I will iterate to ensure this guide is immediately useful for AI agents in your codebase.
