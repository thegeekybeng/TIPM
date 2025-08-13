"""
TIPM Data Crawler Module
========================

Intelligent, autonomous data crawler with RAG capabilities and ML-powered validation.
This module operates independently to discover, validate, and integrate new data sources.
"""

__version__ = "1.0.0"
__author__ = "TIPM Development Team"

from .core import DataCrawlerRAG
from .crawlers import WorldBankCrawler, USCensusCrawler, UNComtradeCrawler
from .validators import DataQualityValidator, MLAnomalyDetector
from .models import DataSource, CrawlResult, ValidationResult

__all__ = [
    "DataCrawlerRAG",
    "WorldBankCrawler",
    "USCensusCrawler",
    "UNComtradeCrawler",
    "DataQualityValidator",
    "MLAnomalyDetector",
    "DataSource",
    "CrawlResult",
    "ValidationResult",
]
