#!/bin/bash

echo "🚀 Deploying TIPM v3.0 to Hugging Face Spaces..."

# Check if we're logged into Hugging Face
if ! hf auth whoami > /dev/null 2>&1; then
    echo "❌ Not logged into Hugging Face. Please run: hf auth login"
    exit 1
fi

# Get current user
HF_USER=$(hf auth whoami)
echo "✅ Logged in as: $HF_USER"

# Create Hugging Face Space directory
SPACE_DIR="tipm-v3-spaces"
echo "📁 Creating space directory: $SPACE_DIR"

# Clean up existing directory
rm -rf "$SPACE_DIR"
mkdir -p "$SPACE_DIR"

# Copy necessary files for Hugging Face Spaces
echo "📋 Copying application files..."

# Copy source code
cp -r src/ "$SPACE_DIR/"
cp -r api/ "$SPACE_DIR/"
cp -r data/ "$SPACE_DIR/"

# Copy configuration files
cp package.json "$SPACE_DIR/"
cp package-lock.json "$SPACE_DIR/"
cp next.config.js "$SPACE_DIR/"
cp tailwind.config.js "$SPACE_DIR/"
cp tsconfig.json "$SPACE_DIR/"
cp postcss.config.js "$SPACE_DIR/"
cp requirements.txt "$SPACE_DIR/"

# Create Hugging Face Spaces specific files
cat > "$SPACE_DIR/README.md" << 'EOF'
# 🚀 TIPM v3.0 - Tariff Impact Propagation Model

An AI-Powered tool for Economic analysis & insights.

## Features

- **Enhanced Dashboard**: Modern React interface with real-time analysis
- **Authoritative Data**: US Government Official Tariff Data (EO + HTS + USTR + CBP)
- **32 Countries**: Comprehensive coverage of countries affected by US trade policies
- **Advanced Analysis**: Multi-layer tariff impact assessment

## Data Sources

- Executive Orders
- HTS (Harmonized Tariff Schedule) codes
- USTR (United States Trade Representative) rulings
- CBP (Customs and Border Protection) data

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Data**: Real US government tariff data
- **Analysis**: Advanced algorithms for economic impact modeling

## Live Demo

This space provides a live demonstration of the TIPM v3.0 system.
EOF

cat > "$SPACE_DIR/app.py" << 'EOF'
import streamlit as st
import subprocess
import os
import sys

st.set_page_config(
    page_title="TIPM v3.0 - Tariff Impact Propagation Model",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 TIPM v3.0 - Tariff Impact Propagation Model")
st.subheader("An AI-Powered tool for Economic analysis & insights")

st.markdown("""
## 🎯 About TIPM

The Tariff Impact Propagation Model (TIPM) is an advanced AI system that analyzes the economic impact of US tariffs on global markets, supply chains, and populations.

## 🔬 Key Features

- **Enhanced Dashboard**: Modern React interface with real-time analysis
- **Authoritative Data**: US Government Official Tariff Data (EO + HTS + USTR + CBP)
- **32 Countries**: Comprehensive coverage of countries affected by US trade policies
- **Advanced Analysis**: Multi-layer tariff impact assessment

## 📊 Data Sources

- **Executive Orders**: Presidential directives on trade policy
- **HTS Codes**: Harmonized Tariff Schedule classifications
- **USTR Rulings**: United States Trade Representative decisions
- **CBP Data**: Customs and Border Protection information

## 🚀 Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Data**: Real US government tariff data
- **Analysis**: Advanced algorithms for economic impact modeling

## 🔗 Access the Full Application

The complete TIPM v3.0 application is available at the GitHub repository with full functionality including:

- Country selection and analysis
- Real-time tariff impact calculations
- Economic modeling and insights
- Professional dashboard interface

## 📈 Analysis Methodology

Our tariff impact analysis is derived from sophisticated algorithms that process official US government data through multiple calculation layers:

1. **Reciprocal Tariff Calculation**: Base duty rates + reciprocal add-ons from Executive Orders
2. **Sector Impact Analysis**: HTS chapter grouping with weighted average tariff rates
3. **Economic Impact Modeling**: Trade disruption, price elasticity, and employment effects
4. **Risk Assessment**: Critical/High/Medium/Low impact classification

## 🏛️ Data Verification

All tariff data is sourced from official US government sources, providing comprehensive coverage of countries affected by US trade policies.

---

*Powered by US Government Official Tariff Data*
EOF

cat > "$SPACE_DIR/requirements.txt" << 'EOF'
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
EOF

cat > "$SPACE_DIR/.gitattributes" << 'EOF'
*.py linguist-language=Python
*.md linguist-language=Markdown
*.txt linguist-language=Text
EOF

# Navigate to space directory
cd "$SPACE_DIR"

echo "🔐 Initializing Git repository..."
git init
git add .
git commit -m "Initial TIPM v3.0 deployment to Hugging Face Spaces"

echo "🚀 Creating Hugging Face Space..."
hf repo create thegeekybeng/tipm-v3-demo --repo-type space --space_sdk streamlit

echo "📤 Pushing to Hugging Face Space..."
git remote add origin https://huggingface.co/spaces/$HF_USER/tipm-v3-demo
git branch -M main
git push -u origin main

echo "✅ Deployment complete!"
echo "🌐 Your TIPM v3.0 space is available at: https://huggingface.co/spaces/$HF_USER/tipm-v3-demo"

cd ..
rm -rf "$SPACE_DIR" 
