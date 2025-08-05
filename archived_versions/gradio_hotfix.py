#!/usr/bin/env python3
"""
TIMP App Gradio Hotfix - Deploy to fix runtime error
"""


# Quick fix for the runtime error - create a minimal working version
def quick_fix_app():
    print("Creating hotfix for Gradio app...")

    # Read the current broken app
    with open("app_gradio.py", "r") as f:
        content = f.read()

    # Simple function replacement to fix the immediate error
    fixed_content = content.replace(
        "fn=run_analysis,", "fn=run_enhanced_timp_analysis,"
    )

    # Also ensure the function signature is correct
    # Add a simple wrapper function if needed
    if "def run_enhanced_timp_analysis(" in fixed_content:
        # Find the function and fix its signature
        lines = fixed_content.split("\n")
        for i, line in enumerate(lines):
            if "def run_enhanced_timp_analysis(" in line:
                # Fix the function signature to match Gradio expectations
                lines[i] = (
                    "def run_enhanced_timp_analysis(preset, custom_countries, custom_sectors):"
                )
                break
        fixed_content = "\n".join(lines)

    # Write the hotfix
    with open("app_gradio_hotfix.py", "w") as f:
        f.write(fixed_content)

    print("Hotfix created: app_gradio_hotfix.py")


if __name__ == "__main__":
    quick_fix_app()
