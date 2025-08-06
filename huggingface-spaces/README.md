---
title: TIPM v1.5 - Tariff Impact Propagation Model
emoji: 🌐
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.41.0
app_file: app.py
pinned: false
license: mit
tags:
  - economics
  - ai
  - tariffs
  - trade
  - policy-analysis
  - supply-chain
  - international-trade
  - economic-modeling
---

# 🌐 TIPM v1.5 - Tariff Impact Propagation Model

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/thegeekybeng/TIPM)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-5.41.0-orange)](https://gradio.app/)

## 🎯 Overview

**TIPM v1.5** is an advanced AI system for predicting and analyzing the economic impact of tariffs on global markets, supply chains, and populations. This interactive web application provides comprehensive analysis across **185 countries** using a sophisticated **6-layer machine learning architecture**.

### 🔬 Six-Layer AI Architecture

1. **🏛️ Policy Trigger Layer** - NLP analysis of tariff announcements and policy text
2. **🔄 Trade Flow Layer** - Graph neural networks for supply chain disruption analysis
3. **🏭 Industry Response Layer** - Multi-output regression for sectoral impact prediction
4. **🏢 Firm Impact Layer** - Survival analysis for employment and business effects
5. **🛒 Consumer Impact Layer** - Bayesian time series for price impact forecasting
6. **🌍 Geopolitical Layer** - Transformer NLP for social and political response prediction

## ✨ Key Features

### 📊 Comprehensive Data Coverage

- **185 countries** with real Trump-era tariff data
- **Enhanced classifications**: G7, G20, BRICS, Emerging Markets
- **10 product categories** with HS (Harmonized System) codes
- **Multiple sorting options** for country analysis

### 🎯 Interactive Analysis

- **Real-time confidence scoring** across all 6 layers
- **Custom tariff rate override** functionality
- **Interactive Plotly visualizations** with color-coded confidence levels
- **Comprehensive economic impact reports**

### 🌍 Global Economic Intelligence

- **GDP-weighted analysis** for major economies
- **Bilateral trade volume estimates**
- **Resource export classifications** (Mining, Agriculture, Technology)
- **Continental and regional groupings**

## 🚀 How to Use

### Step 1: Select Analysis Parameters

1. **Choose Country Sorting**: Sort by tariff rates, continent, global groups, or alphabetically
2. **Select Target Country**: Pick from 185 countries with real tariff data
3. **Choose Product Categories**: Select HS code categories for analysis
4. **Set Custom Tariff Rate** (Optional): Override default rates for scenario testing

### Step 2: Run Analysis

Click **"🚀 Run TIPM Analysis"** to generate:

- **📈 Economic Impact Assessment**: Trade disruption, price effects, employment impact
- **🌍 Country Profile**: Continental classification, global group memberships
- **📊 Confidence Visualization**: Interactive charts showing model certainty
- **🔍 Layer Breakdown**: Detailed confidence scores for each AI layer

### Step 3: Interpret Results

- **🟢 Green scores (85%+)**: High confidence predictions
- **🟡 Yellow scores (75-84%)**: Moderate confidence predictions
- **🔴 Red scores (<75%)**: Lower confidence, use with caution

## 📚 Data Sources & Methodology

### Authoritative Data Sources

- **Trade Data**: US Census Bureau International Trade Statistics
- **Economic Indicators**: World Bank Global Economic Monitor
- **Tariff Classifications**: US Trade Representative (USTR) Section 301 Reports
- **Country Classifications**: UN Statistics Division, IMF, OECD

### Technical Architecture

- **Frontend**: Gradio 5.41.0 with responsive design
- **Visualization**: Plotly 6.2.0 for interactive charts
- **ML Framework**: PyTorch with scikit-learn components
- **NLP Models**: DistilBERT for policy text analysis
- **Data Processing**: Pandas, NumPy for efficient computation

## 🎓 Use Cases & Applications

### 📊 Policy Analysis

- **Impact Assessment**: Analyze potential effects before policy implementation
- **Scenario Testing**: Compare different tariff rate scenarios
- **Cross-Country Comparison**: Evaluate relative impacts across regions

### 🏢 Business Intelligence

- **Supply Chain Planning**: Assess disruption risks to global operations
- **Market Entry Strategy**: Understand tariff environments in target markets
- **Risk Assessment**: Quantify trade policy risks for decision-making

### 🎯 Academic Research

- **Economic Modeling**: Study tariff transmission mechanisms
- **Policy Evaluation**: Analyze historical trade policy outcomes
- **International Relations**: Research geopolitical trade dynamics

## ⚖️ Important Disclaimers

### 🔬 Research Purpose

This application is designed for **educational and research purposes only**. While built with authoritative data sources and sophisticated AI models, results are **predictive estimates** and should not be used as the sole basis for:

- **Policy decisions** by governments or organizations
- **Investment strategies** or financial planning
- **Business operational decisions** without additional analysis

### 📊 Model Limitations

- **Historical Basis**: Analysis based on Trump-era tariff data (2018-2020)
- **Synthetic Components**: Some results use calibrated synthetic data for demonstration
- **Confidence Scoring**: Reflects model uncertainty, not guarantee of accuracy
- **Dynamic Markets**: Real-world conditions may differ from model predictions

### 🔄 Data Freshness

- **Tariff Rates**: Based on historical USTR Section 301 implementation
- **Economic Data**: Uses latest available World Bank and Census Bureau data
- **Country Classifications**: Updated to reflect current global organization memberships

## 🛠️ Technical Details

### System Requirements

- **Python**: 3.8+ with scientific computing libraries
- **Memory**: Minimum 4GB RAM for full country dataset
- **Processing**: Multi-core CPU recommended for ML computations
- **Network**: Internet connection for real-time data validation

### Performance Metrics

- **Load Time**: ~45 seconds for complete model initialization
- **Analysis Speed**: 2-5 seconds per country analysis
- **Country Coverage**: 185 countries with complete data profiles
- **Model Accuracy**: Confidence-weighted predictions across 6 layers

## 📖 Citation & Credits

### Academic Citation

```bibtex
@software{tipm_v15_2025,
  author = {Yeo, Andrew (TheGeekyBeng)},
  title = {TIPM v1.5: Tariff Impact Propagation Model},
  year = {2025},
  url = {https://huggingface.co/spaces/thegeekybeng/tipm-v15},
  version = {1.5}
}
```

### Development Team

- **Lead Developer**: Andrew Yeo (TheGeekyBeng)
- **AI Architecture**: 6-layer modular ML design
- **Data Integration**: Authoritative government and international sources
- **UI/UX Design**: Modern Gradio interface with accessibility features

## 🔗 Links & Resources

- **📁 GitHub Repository**: [github.com/thegeekybeng/TIPM](https://github.com/thegeekybeng/TIPM)
- **📊 Live Demo**: This HuggingFace Space
- **📖 Documentation**: Comprehensive guides in repository
- **🐛 Issues & Feedback**: GitHub Issues for bug reports and suggestions

---

**Built with ❤️ for the global economics and policy research community**

_Last Updated: August 2025 | Version 1.5.0_
