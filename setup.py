"""
TIPM Setup Configuration
========================

Tariff Impact Propagation Model - 6-Layer ML Architecture
"""

import os
from setuptools import setup, find_packages


def read_requirements():
    """Read requirements from requirements.txt with enhanced filtering"""
    requirements = []
    try:
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Filter out comments, empty lines, and development tools
                    if (
                        line
                        and not line.startswith("#")
                        and not line.startswith("-e")
                        and "git+" not in line
                        and "github.com" not in line
                    ):
                        # Skip optional development dependencies for core install
                        dev_tools = [
                            "pytest",
                            "black",
                            "flake8",
                            "mypy",
                            "ruff",
                            "jupyter",
                        ]
                        if not any(dev_tool in line.lower() for dev_tool in dev_tools):
                            requirements.append(line)
    except (IOError, OSError) as e:
        print(f"Warning: Could not read requirements.txt: {e}")
    return requirements


def read_dev_requirements():
    """Read development requirements separately"""
    dev_requirements = []
    try:
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    dev_tools = [
                        "pytest",
                        "black",
                        "flake8",
                        "mypy",
                        "ruff",
                        "jupyter",
                        "optuna",
                        "shap",
                    ]
                    if (
                        line
                        and not line.startswith("#")
                        and any(dev_tool in line.lower() for dev_tool in dev_tools)
                    ):
                        dev_requirements.append(line)
    except (IOError, OSError) as e:
        print(f"Warning: Could not read requirements.txt for dev dependencies: {e}")
    return dev_requirements


def read_long_description():
    """Read long description with error handling"""
    try:
        if os.path.exists("README.md"):
            with open("README.md", "r", encoding="utf-8") as f:
                return f.read()
    except (IOError, OSError) as e:
        print(f"Warning: Could not read README.md: {e}")
    return "Tariff Impact Propagation Model - AI system for predicting tariff impacts on global markets"


setup(
    name="tipm",
    version="1.0.0",
    description=(
        "Tariff Impact Propagation Model - AI system for predicting "
        "tariff impacts on global markets"
    ),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="TIPM Development Team",
    packages=find_packages(),
    python_requires=">=3.9",  # Ensure compatibility with Python 3.9 and above
    install_requires=read_requirements(),
    extras_require={
        "dev": read_dev_requirements(),
        "visualization": [
            "plotly>=5.15.0",
            "seaborn>=0.12.0",
            "matplotlib>=3.7.0",
            "streamlit>=1.25.0",
    
        ],
        "ml": [
            "torch>=2.0.0",
            "torch-geometric>=2.3.0",
            "transformers>=4.30.0",
            "optuna>=3.3.0",
            "shap>=0.42.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tipm=tipm.core:main",  # Point to main function in core module
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    keywords="tariff analysis machine-learning economics trade policy",
    project_urls={
        "Source": "https://github.com/thegeekybeng/TIPM",
        "Documentation": ("https://github.com/thegeekybeng/TIPM/blob/main/README.md"),
    },
)
