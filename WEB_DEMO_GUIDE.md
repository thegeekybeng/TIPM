# TIPM Web Application Guide

## 🌟 Overview

This guide provides instructions for running the TIPM (Tariff Impact Propagation Model) web application. The TIPM system offers a production-ready web interface for comprehensive tariff impact analysis using a 6-layer ML architecture.

**Production Web Application**: `app_gradio.py` - Interactive Gradio interface deployed on Hugging Face Spaces

## 🚀 Quick Start

### Production Gradio Application

#### Prerequisites

```bash
# Install dependencies (already available in production environment)
pip install gradio plotly pandas numpy
# or use the complete requirements file
pip install -r requirements.txt
```

#### Launch the Application

```bash
# Start the Gradio application locally
python app_gradio.py

# Or run with custom host/port  
python app_gradio.py --host 0.0.0.0 --port 7860
```

#### Production Deployment

The TIPM application is deployed on Hugging Face Spaces at:
**https://huggingface.co/spaces/thegeekybeng/timp-demo**

#### Features

- **Interactive Interface**: Select countries and sectors, configure analysis parameters
- **Real-time Analysis**: Run TIPM predictions using enhanced tariff data for 186 countries  
- **Advanced Visualizations**: Confidence scores, impact charts, sectoral analysis
- **Risk Assessment**: Comprehensive risk scoring with GDP impact estimates
- **Export Capabilities**: Download detailed analysis results in CSV format
- **Economic Intelligence**: Multi-sectoral analysis covering 12 economic sectors

## 📊 TIPM Analysis Scenarios

### 1. US-China Technology Trade Analysis

- **Countries**: United States (840), China (156)  
- **Sectors**: Technology, Electronics, Telecommunications
- **Focus**: High-tech trade disruption and supply chain impact analysis
- **Key Metrics**: Semiconductor trade flows, technology transfer effects

### 2. EU-US Automotive Trade Analysis

- **Countries**: Germany (276), United States (840)
- **Sectors**: Automotive, Machinery, Transport Equipment  
- **Focus**: Automotive sector impact and manufacturing realignment
- **Key Metrics**: Vehicle exports, parts supply chain disruption

### 3. Global Multi-Country Analysis

- **Countries**: US (840), China (156), Germany (276), Japan (392), Singapore (702)
- **Sectors**: All 12 economic sectors available in TIPM
- **Focus**: Comprehensive multi-country trade relationship analysis
- **Key Metrics**: Cross-sector impacts, geopolitical risk assessment

### 4. Custom Analysis Configuration

- **Configure**: Select from 186 available countries
- **Flexible**: Choose from 12 economic sectors
- **Comprehensive**: Full 6-layer ML architecture analysis

## 🔧 Configuration Options

### TIPM Application Settings

- **Country Selection**: Choose from 186 available countries with comprehensive tariff data
- **Sector Analysis**: Select from 12 economic sectors for detailed impact analysis  
- **Risk Assessment**: Configure confidence thresholds and impact scoring parameters
- **Export Options**: Download analysis results in CSV format for further processing

### Analysis Parameters

- **Countries**: ISO 3166 country codes (840=US, 156=China, 276=Germany, etc.)
- **Sectors**: Economic sectors including Technology, Automotive, Agriculture, etc.
- **Tariff Data**: Enhanced Trump tariff data covering bilateral trade relationships
- **Impact Metrics**: GDP impact factors, trade volumes, sectoral vulnerabilities

## 📈 Results Interpretation

### Confidence Scores

- **Overall Confidence**: Weighted average of all 6-layer architecture confidences
- **Layer-Specific**: Individual confidence for each TIPM layer (Policy→Geopolitical)
- **Quality Indicators**:
  - 🟢 >70% = High confidence prediction
  - 🟡 40-70% = Medium confidence prediction
  - 🔴 <40% = Low confidence prediction

### Impact Analysis

- **Trade Flow Impact**: Changes in bilateral trade routes and volumes across supply chains
- **Industry Response**: Sector-specific adaptation strategies and economic resilience
- **Firm Impact**: Employment effects and business survival rates across industries
- **Consumer Impact**: Price changes and welfare effects on end consumers
- **Geopolitical Impact**: Social tension indicators and political stability assessment

### Enhanced Economic Metrics

- **GDP Impact**: Estimated percentage impact on national GDP
- **Trade at Risk**: Total trade volume potentially affected by tariff changes
- **Sectoral Vulnerability**: Industry-specific risk scores and adaptation capacity
- **Cross-Border Effects**: Multi-country impact propagation analysis

## 🌍 Data Sources

### Real Data Integration
## 🌍 TIPM Data Sources

### Enhanced Tariff Data

The TIPM system uses comprehensive Trump tariff data covering:

- **186 Countries**: Complete global coverage with bilateral tariff relationships
- **12 Economic Sectors**: From Agriculture to Technology, covering all major industries
- **Real Trade Data**: Historical tariff rates and reciprocal trade policies
- **GDP Impact Factors**: Country-specific economic dependency metrics
- **Sectoral Weights**: Industry importance scoring for accurate impact modeling

### Economic Intelligence Sources

- **UN Comtrade**: Referenced for trade flow validation
- **World Bank**: Economic indicators for GDP impact calculations
- **OECD TiVA**: Supply chain complexity modeling
- **Enhanced Configuration**: Real Trump tariff data with sectoral breakdown

## 🔍 Troubleshooting

### Common Issues

#### Application Startup

```bash
# If Gradio fails to start
python -m pip install --upgrade gradio
python app_gradio.py

# Check dependencies
pip install -r requirements.txt
```

#### Missing Dependencies

```bash
# Install core TIMP dependencies
pip install pandas numpy plotly gradio

# Verify installation
python -c "import tipm; print('TIPM ready')"
```

#### Performance Issues

- **Expected Behavior**: Analysis of 186 countries may take 10-30 seconds
- **Progress Tracking**: Use the Gradio interface progress indicators
- **Memory Usage**: Large country selections require more system memory

## 📁 File Structure

```text
app_gradio.py                 # Production Gradio application
requirements.txt              # Complete dependency list
tipm/                        # Core TIPM 6-layer architecture
├── core.py                  # Main TIPMModel orchestrator
├── enhanced_config.py       # Enhanced configuration system
└── layers/                  # Individual layer implementations
data/                        # Real Trump tariff data
├── trump_tariffs_by_country.csv
notebooks/                   # Jupyter analysis notebooks
└── tipm_demo.ipynb         # Interactive analysis notebook
```

## 🎯 Usage Examples

### Production Application

1. **Launch**: `python app_gradio.py`
2. **Select**: Choose countries and sectors from dropdowns
3. **Configure**: Set analysis parameters
4. **Analyze**: Click "Run TIPM Analysis"  
5. **Explore**: View confidence scores, risk assessment, and detailed impacts
6. **Export**: Download CSV results for further analysis

### Programmatic Access

```python
# Direct TIPM model usage
from tipm.enhanced_config import EnhancedTariffDataManager

manager = EnhancedTariffDataManager()
countries = ['China', 'Germany', 'Japan']
sectors = ['technology', 'automotive']
analysis = manager.get_sector_analysis(countries, sectors)
print(f"Risk Level: {analysis['risk_assessment']['overall_risk']}")
```

## 🚀 Production Deployment

### Hugging Face Spaces

The TIPM application is deployed on Hugging Face Spaces for global access:

**Live Application**: [https://huggingface.co/spaces/thegeekybeng/tipm-demo](https://huggingface.co/spaces/thegeekybeng/tipm-demo)

### Local Production Setup

```bash
# Production environment setup
pip install -r requirements.txt
python app_gradio.py --host 0.0.0.0 --port 7860

# Docker deployment (if needed)
docker build -t tipm-app .
docker run -p 7860:7860 tipm-app
```

## 📞 Support

For TIPM system support:

1. **Check Application Logs**: Review console output for specific error details
2. **Verify Configuration**: Ensure all 186 countries and 12 sectors load correctly
3. **Test Core Functions**: Verify TIPM 6-layer architecture initialization
4. **Performance Monitoring**: Monitor analysis times for large country selections

---

*Last Updated: August 5, 2025*  
*TIPM Production System v1.0*
