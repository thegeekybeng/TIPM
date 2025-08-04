"""
Setup configuration for TIPM package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tipm",
    version="0.1.0",
    author="TIPM Development Team",
    author_email="tipm@example.com",
    description="Tariff Impact Propagation Model - AI system for predicting global tariff impacts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/tipm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "visualization": [
            "plotly>=5.15.0",
            "streamlit>=1.24.0",
            "dash>=2.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tipm=tipm.cli:main",
        ],
    },
)
