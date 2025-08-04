# Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file

## TIPM Project Context

This is a Tariff Impact Propagation Model (TIPM) project - an AI system for predicting how tariffs impact global markets, supply chains, and populations.

## Architecture

The system uses a 6-layer ML architecture:

1. **Policy Trigger Layer**: NLP processing of tariff announcements
2. **Trade Flow Layer**: Graph neural networks for supply chain analysis
3. **Industry Response Layer**: Multi-output regression for sectoral impacts
4. **Firm Impact Layer**: Survival analysis for employment effects
5. **Consumer Impact Layer**: Bayesian time series for price impacts
6. **Geopolitical Layer**: Transformer NLP for social response prediction

## Key Technologies

- **ML Frameworks**: PyTorch, scikit-learn, XGBoost, transformers
- **Graph Analysis**: NetworkX, PyTorch Geometric
- **Time Series**: Prophet, statsmodels, ARIMA
- **NLP**: HuggingFace transformers, spaCy, NLTK
- **Data**: pandas, numpy, requests
- **Visualization**: matplotlib, seaborn, plotly, streamlit

## Code Structure

- `tipm/core.py`: Main TIPMModel orchestrator
- `tipm/layers/`: Individual layer implementations
- `tipm/config/`: Configuration management
- `tipm/utils/`: Data processing and visualization utilities
- `notebooks/`: Jupyter analysis notebooks
- `scripts/`: Utility scripts

## Development Guidelines

1. **Layer Independence**: Each layer should be independently testable
2. **Configuration-Driven**: Use config classes for all parameters
3. **Type Hints**: Always include type annotations
4. **Documentation**: Comprehensive docstrings for all public methods
5. **Error Handling**: Graceful degradation when data is unavailable
6. **Testing**: Unit tests for core functionality

## Data Flow

Policy Text → Features → Trade Impact → Industry Response → Firm Impact → Consumer Impact → Geopolitical Response

## Common Patterns

- Use dataclasses for structured data
- Implement `.fit()` and `.predict()` methods for all layers
- Return confidence scores with all predictions
- Support both real and synthetic data for testing
- Provide visualization methods for all outputs

## When generating code:

- Focus on economic modeling accuracy
- Include proper error handling for missing data
- Use meaningful variable names (e.g., `tariff_rate` not `rate`)
- Add comprehensive logging for debugging
- Consider scalability for multiple countries/scenarios
- Include data validation and bounds checking
