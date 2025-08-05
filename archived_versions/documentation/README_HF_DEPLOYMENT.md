---
title: TIPM - Tariff Impact Propagation Model
emoji: 📊
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.1
app_file: app_hf.py
pinned: false
license: mit
python_version: 3.9
---

## 📊 Overview

TIPM is an AI-powered system for predicting the economic impact of tariffs across global markets, supply chains, and populations. This demo analyzes how tariffs affect countries and sectors using real Trump-era tariff data.

## 🎯 Features

- **Country Impact Analysis**: Assess economic disruption across 25+ countries
- **Sector Analysis**: Analyze 18 major economic sectors
- **Risk Assessment**: Categorize countries by vulnerability levels
- **Interactive Visualizations**: Clear charts showing country positioning
- **Export Capabilities**: Download analysis results as CSV
- **Standardized Formula**: Mathematically consistent impact calculations

## 📈 Key Metrics

- **Economic Disruption %**: Percentage of economic activity disrupted by tariffs
- **GDP Impact**: Estimated GDP loss in USD billions
- **Trade Volume**: Bilateral trade volume with USA in USD billions annually
- **Sector Vulnerability**: Industry-specific impact assessments

## 🔬 Technology Stack

TIPM uses a 6-layer ML architecture:

1. **Policy Trigger Layer**: NLP processing of tariff announcements
2. **Trade Flow Layer**: Graph neural networks for supply chain analysis
3. **Industry Response Layer**: Multi-output regression for sectoral impacts
4. **Firm Impact Layer**: Survival analysis for employment effects
5. **Consumer Impact Layer**: Bayesian time series for price impacts
6. **Geopolitical Layer**: Transformer NLP for social response prediction

## 📚 Legitimate Data Sources

✅ **UN Comtrade**: Bilateral trade statistics (verified authoritative source)
✅ **World Bank**: Economic indicators and GDP data (verified authoritative source)
✅ **OECD**: Trade in Value-Added data (verified authoritative source)
✅ **Historical Trump Tariffs**: Real policy implementation data (verified government sources)

*All datasets have been verified for legitimacy and accuracy. See DATA_SOURCE_VERIFICATION_REPORT.md for complete details.*

## 🚀 Usage

1. **Select Analysis Preset**: Choose from Major Economies, Asian Markets, ASEAN, or Custom
2. **Configure Parameters**: Adjust countries and sectors for analysis
3. **Run Analysis**: Click "Run Analysis" to generate results
4. **Review Results**: Examine impact visualizations and detailed metrics
5. **Export Data**: Download results as CSV for further analysis

## 📊 Sample Results

**Major Economies Analysis:**

- China (67% tariff): ~40.6% economic disruption
- Germany (25% tariff): ~22.8% economic disruption
- Japan (18% tariff): ~19.4% economic disruption
- Singapore (10% tariff): ~15.8% economic disruption

## 🔧 Technical Notes

- Built with Gradio 4.44.1 for optimal HF Spaces compatibility
- Optimized for CPU-only deployment
- Self-contained with no external API dependencies
- Comprehensive error handling and graceful degradation

---

*This is a production-ready demo version optimized for Hugging Face Spaces deployment with legitimate, verified data sources.*
