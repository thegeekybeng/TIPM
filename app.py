#!/usr/bin/env python3
"""
TIPM: Tariff Impact Propagation Model
Hugging Face Spaces Deployment - Gradio Version with Standardized Formula

🎯 CRITICAL UPDATE: This deployment includes the standardized economic impact formula
that fixes the mathematical inconsistency where Singapore (10% tariff) showed 55% impact.

✅ New Results:
- Singapore (10%): ~15.8% impact (realistic and proportional)
- China (67%): ~40.6% impact (properly scaled)
- All countries use the same standardized calculation
"""

# Import the complete Gradio application with standardized formula
from app_gradio import create_gradio_app

if __name__ == "__main__":
    # Create and launch the Gradio app for HF Spaces
    app = create_gradio_app()

    # HF Spaces optimized launch configuration
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        max_threads=10,
    )
