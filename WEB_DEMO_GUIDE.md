# TIPM Web Demo Guide

## 🌟 Overview

This guide provides instructions for running the TIMP (Tariff Impact Propagation Model) web demonstrations. Two demo options are available:

1. **Interactive Streamlit App** (`tipm_web_demo.py`) - Full-featured web interface
2. **Simple HTML Demo** (`simple_web_demo.py`) - Lightweight standalone demo

## 🚀 Quick Start

### Option 1: Interactive Streamlit Demo

#### Prerequisites
```bash
# Install web dependencies
pip install streamlit plotly
# or
pip install -r requirements_web.txt
```

#### Launch the App
```bash
# Start the Streamlit server
streamlit run tipm_web_demo.py

# Or specify custom port
streamlit run tipm_web_demo.py --server.port 8501
```

#### Features
- **Interactive Interface**: Select scenarios, configure parameters, view results
- **Real-time Analysis**: Run TIPM predictions with live progress tracking
- **Rich Visualizations**: Confidence scores, impact charts, trade flow analysis
- **Data Quality Monitoring**: Real-time data source quality assessment
- **Export Capabilities**: Download results in JSON format
- **Multiple Scenarios**: US-China Tech, EU-US Auto, Global Steel, Custom

### Option 2: Simple HTML Demo

#### Run the Demo
```bash
# Generate standalone HTML demo
python simple_web_demo.py
```

#### Output
- **`tipm_demo_results.html`**: Interactive web page with results
- **`tipm_demo_results.json`**: Raw prediction data
- **Open the HTML file in any web browser**

## 📊 Demo Scenarios

### 1. US-China Technology Trade
- **Countries**: United States (840), China (156)
- **Products**: Telecommunications (8517), Computers (8471), Semiconductors (8542)
- **Focus**: High-tech trade disruption analysis

### 2. EU-US Automotive Trade
- **Countries**: Germany (276), United States (840)
- **Products**: Motor Cars (8703), Auto Parts (8708)
- **Focus**: Automotive sector impact analysis

### 3. Global Steel Trade
- **Countries**: US (840), China (156), Germany (276), Japan (392)
- **Products**: Flat Steel (7208), Coated Steel (7210)
- **Focus**: Multi-country steel tariff impacts

### 4. Custom Scenario
- **Configure**: Your own countries, products, and parameters
- **Flexible**: Test any trade relationship

## 🔧 Configuration Options

### Streamlit App Settings
- **Real Data Integration**: Toggle between real and synthetic data
- **Analysis Years**: Select historical years for analysis
- **Tariff Rates**: Adjust tariff rate changes (0-100%)
- **Data Refresh**: Force refresh of cached data

### Analysis Parameters
- **Countries**: UN country codes (840=US, 156=China, 276=Germany, etc.)
- **HS Codes**: Harmonized System product codes
- **Years**: Historical years for data analysis
- **Tariff Rate**: Percentage change in tariff rates

## 📈 Results Interpretation

### Confidence Scores
- **Overall Confidence**: Weighted average of all layer confidences
- **Layer-Specific**: Individual confidence for each TIPM layer
- **Quality Indicators**: 
  - 🟢 >70% = High confidence
  - 🟡 40-70% = Medium confidence  
  - 🔴 <40% = Low confidence

### Impact Analysis
- **Trade Flow Impact**: Changes in bilateral trade routes and volumes
- **Industry Response**: Sector-specific adaptation strategies
- **Firm Impact**: Employment effects and business survival rates
- **Consumer Impact**: Price changes and welfare effects
- **Geopolitical Impact**: Social tension and political stability

### Data Quality Metrics
- **Completeness**: Percentage of non-missing data
- **Temporal Coverage**: Historical data availability
- **Source Reliability**: API response success rates
- **Fallback Status**: When synthetic data is used

## 🌍 Data Sources

### Real Data Integration
When "Use Real Data Integration" is enabled, the system attempts to fetch from:

- **UN Comtrade**: Global trade statistics
- **WITS (World Bank)**: Tariff and trade policy data
- **OECD TiVA**: Global value chain indicators
- **World Bank**: Economic indicators (GDP, CPI, unemployment)
- **GDELT**: News sentiment and geopolitical events
- **ACLED**: Political conflict and event data

### Fallback System
- **Intelligent Fallback**: Automatically switches to synthetic data when real data unavailable
- **Quality Thresholds**: Uses real data only when quality standards are met
- **Transparent Reporting**: Clearly indicates data source for each prediction

## 🔍 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or use different port
streamlit run timp_web_demo.py --server.port 8502
```

#### Missing Dependencies
```bash
# Install missing packages
pip install streamlit plotly pandas numpy

# Or install from requirements
pip install -r requirements_web.txt
```

#### Data Fetch Errors
- **Expected Behavior**: Some APIs may return 404s or require authentication
- **Fallback System**: System automatically uses synthetic data
- **Check Logs**: Review console output for specific error details

### API Limitations
- **Rate Limiting**: Public APIs have usage restrictions
- **Authentication**: Some sources require API keys
- **Data Availability**: Recent years may have limited data
- **Geographic Coverage**: Not all countries/products available

## 📁 File Structure

```
tipm_web_demo.py          # Interactive Streamlit application
simple_web_demo.py        # Standalone HTML demo generator
requirements_web.txt      # Web demo dependencies
timp_demo_results.html    # Generated demo results (after running)
timp_demo_results.json    # Raw prediction data (JSON)
real_data_cache/          # Cached real datasets
```

## 🎯 Usage Examples

### Streamlit Demo
1. **Launch**: `streamlit run tipm_web_demo.py`
2. **Select**: Choose scenario from sidebar
3. **Configure**: Set parameters (years, tariff rates)
4. **Run**: Click "🚀 Run Analysis"
5. **Explore**: View results in interactive tabs
6. **Export**: Download JSON results

### HTML Demo
1. **Generate**: `python simple_web_demo.py`
2. **Open**: `tipm_demo_results.html` in browser
3. **Navigate**: Use tabs to explore results
4. **Share**: Send HTML file to stakeholders

## 🚀 Advanced Usage

### Custom Scenarios
```python
# In Streamlit app: Select "Custom Scenario"
# Configure:
countries = "840,156,276"  # US, China, Germany
hs_codes = "8517,8471"     # Telecom, Computers
```

### API Integration
```python
# Programmatic access to demo results
import json

with open('tipm_demo_results.json', 'r') as f:
    results = json.load(f)
    
confidence = results['overall_confidence']
print(f"Prediction confidence: {confidence:.1%}")
```

### Production Deployment
```bash
# Run in production mode
streamlit run tipm_web_demo.py \
  --server.port 80 \
  --server.headless true \
  --server.enableCORS false
```

## 📞 Support

For issues or questions:
1. **Check Logs**: Review console output for error details
2. **Verify Setup**: Ensure all dependencies installed
3. **Test Simple Demo**: Try `simple_web_demo.py` first
4. **Check Network**: Verify internet connectivity for real data fetching

---

*Last Updated: August 4, 2025*  
*TIMP Real Data Integration Demo v2.0*
