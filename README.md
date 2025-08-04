---
title: TIPM - Tariff Impact Propagation Model
emoji: 📊
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app_gradio.py
pinned: false
license: mit
---

# TIPM: Tariff Impact Propagation Model

## 📊 Overview

TIPM is an AI-powered system for predicting the economic impact of tariffs across global markets, supply chains, and populations. This demo analyzes how tariffs affect countries and sectors using real Trump-era tariff data.

## 🎯 Features

- **Country Impact Analysis**: Assess economic disruption across 10+ countries
- **Sector Analysis**: Analyze 12 major economic sectors
- **Risk Assessment**: Categorize countries by vulnerability levels
- **Interactive Visualizations**: Clear charts showing country positioning
- **Export Capabilities**: Download analysis results as CSV

## 📈 Metrics

- **Economic Disruption %**: Percentage of economic activity disrupted by tariffs
- **GDP Impact**: Estimated GDP loss in USD billions
- **Trade Volume**: Bilateral trade volume with USA in USD billions annually

## 🔬 Technology

TIMP uses a 6-layer ML architecture:
1. Policy Trigger Layer (NLP)
2. Trade Flow Layer (Graph Neural Networks)
3. Industry Response Layer (Multi-output Regression)
4. Firm Impact Layer (Survival Analysis)
5. Consumer Impact Layer (Bayesian Time Series)
6. Geopolitical Layer (Transformer NLP)

## 📚 Data Sources

- Real Trump-era tariff data
- UN Comtrade bilateral trade statistics
- World Bank economic indicators
- OECD trade in value-added data

## 🚀 Usage

1. Select analysis preset or customize countries/sectors
2. Click "Run Analysis"
3. Review impact visualizations and detailed results
4. Export data for further analysis

---

*This is a demo version with simplified data for Hugging Face Spaces deployment.*
