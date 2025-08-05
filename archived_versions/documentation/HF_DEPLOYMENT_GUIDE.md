# Hugging Face Spaces Deployment Instructions

## Files Created for HF Spaces:

1. **app.py** - Main Streamlit application (self-contained)
2. **requirements_hf.txt** - Dependencies for HF Spaces
3. **HF_README.md** - README for the HF Space
4. **hf_header.md** - Space configuration header

## Deployment Steps:

### 1. Create New Space on Hugging Face
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Choose:
  - **Space name**: `tipm-tariff-impact-model`
  - **License**: MIT
  - **SDK**: Streamlit
  - **Hardware**: CPU (free tier is sufficient)

### 2. Upload Files
Copy these files to your HF Space repository:

```
app.py                    # Main application
requirements.txt          # Use requirements_hf.txt content
README.md                 # Use HF_README.md content
```

### 3. Space Header Configuration
Add this to the top of your README.md:

```yaml
---
title: TIMP - Tariff Impact Propagation Model
emoji: 📊
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.47.1
app_file: app.py
pinned: false
license: mit
---
```

### 4. Requirements File
Use this content for requirements.txt:

```
streamlit>=1.47.1
pandas>=2.0.0
plotly>=5.0.0
numpy>=1.24.0
```

## Features in HF Version:

✅ **Self-contained** - No external dependencies on local TIMP modules
✅ **Sample data included** - Based on real Trump tariff data
✅ **All visualizations working** - Charts, tables, risk analysis
✅ **Interactive presets** - Major Economies, Asian Markets, ASEAN, Custom
✅ **Export functionality** - CSV download capability
✅ **Clear documentation** - Metric explanations and methodology

## Test URL:
Your HF Space will be available at:
`https://huggingface.co/spaces/[your-username]/timp-tariff-impact-model`

## Local Testing:
The app is currently running at: http://localhost:8509
