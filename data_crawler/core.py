"""
Core RAG-Powered Data Crawler for TIPM
======================================

Intelligent data crawler that uses RAG (Retrieval-Augmented Generation) to discover,
validate, and integrate new data sources autonomously.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib

# Data models
from .models import (
    DataSource,
    CrawlResult,
    ValidationResult,
    DataIntegrationResult,
    DataSourceType,
    ValidationStatus,
)

# Crawlers
from .crawlers import WorldBankCrawler, USCensusCrawler, UNComtradeCrawler

# Validators
from .validators import DataQualityValidator, MLAnomalyDetector

# Vector store and embeddings
try:
    import chromadb
    from chromadb.config import Settings

    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

logger = logging.getLogger(__name__)


class DataCrawlerRAG:
    """
    RAG-powered data crawler that intelligently discovers and validates data sources
    """

    def __init__(
        self,
        vector_db_path: str = "data_crawler/vector_store",
        config_path: str = "data_crawler/config/sources.json",
    ):
        """
        Initialize the RAG-powered data crawler

        Args:
            vector_db_path: Path to vector database for storing embeddings
            config_path: Path to data source configuration file
        """
        self.vector_db_path = Path(vector_db_path)
        self.config_path = Path(config_path)

        # Initialize components
        self._init_vector_store()
        self._init_embedding_model()
        self._init_crawlers()
        self._init_validators()

        # Load data sources
        self.data_sources = self._load_data_sources()

        # Crawl history and results
        self.crawl_history: Dict[str, List[CrawlResult]] = {}
        self.validation_history: Dict[str, List[ValidationResult]] = {}
        self.integration_history: Dict[str, List[DataIntegrationResult]] = {}

        logger.info("DataCrawlerRAG initialized successfully")

    def _init_vector_store(self):
        """Initialize vector database for RAG operations"""
        if not CHROMA_AVAILABLE:
            logger.warning("ChromaDB not available. RAG features will be limited.")
            self.vector_store = None
            return

        try:
            self.vector_store = chromadb.PersistentClient(
                path=str(self.vector_db_path),
                settings=Settings(anonymized_telemetry=False, allow_reset=True),
            )

            # Create collections for different types of data
            self.source_collection = self.vector_store.get_or_create_collection(
                name="data_sources",
                metadata={"description": "Data source metadata and descriptions"},
            )

            self.data_collection = self.vector_store.get_or_create_collection(
                name="crawled_data",
                metadata={"description": "Crawled data content and metadata"},
            )

            logger.info("Vector store initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            self.vector_store = None

    def _init_embedding_model(self):
        """Initialize embedding model for text vectorization"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("SentenceTransformers not available. Using fallback.")
            self.embedding_model = None
            return

        try:
            # Use a lightweight but effective model
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Embedding model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            self.embedding_model = None

    def _init_crawlers(self):
        """Initialize specialized crawlers for different data sources"""
        self.crawlers = {
            "world_bank": WorldBankCrawler(),
            "us_census": USCensusCrawler(),
            "un_comtrade": UNComtradeCrawler(),
        }
        logger.info(f"Initialized {len(self.crawlers)} specialized crawlers")

    def _init_validators(self):
        """Initialize data validation components"""
        self.data_validator = DataQualityValidator()
        self.ml_anomaly_detector = MLAnomalyDetector()
        logger.info("Data validation components initialized")

    def _load_data_sources(self) -> List[DataSource]:
        """Load data source configurations"""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_sources()

        try:
            with open(self.config_path, "r") as f:
                config_data = json.load(f)

            sources = []
            for source_data in config_data.get("sources", []):
                try:
                    source = DataSource.from_dict(source_data)
                    sources.append(source)
                except Exception as e:
                    logger.error(
                        f"Failed to load source {source_data.get('id', 'unknown')}: {e}"
                    )

            logger.info(f"Loaded {len(sources)} data sources from config")
            return sources

        except Exception as e:
            logger.error(f"Failed to load data sources: {e}")
            return self._get_default_sources()

    def _get_default_sources(self) -> List[DataSource]:
        """Get default data sources if config is not available"""
        default_sources = [
            DataSource(
                id="world_bank_gdp",
                name="World Bank GDP Data",
                description="Global GDP and economic indicators from World Bank",
                source_type=DataSourceType.API,
                url="https://api.worldbank.org/v2/country",
                tags=["economics", "gdp", "world_bank"],
                categories=["macroeconomic", "development"],
                country_coverage=["all"],
                time_coverage="1960-2024",
                update_frequency="daily",
            ),
            DataSource(
                id="us_census_trade",
                name="US Census Trade Data",
                description="US international trade statistics",
                source_type=DataSourceType.API,
                url="https://api.census.gov/data/timeseries/intltrade",
                tags=["trade", "us", "census"],
                categories=["trade_statistics", "bilateral"],
                country_coverage=["all"],
                time_coverage="1992-2024",
                update_frequency="monthly",
            ),
            DataSource(
                id="un_comtrade",
                name="UN Comtrade Database",
                description="United Nations international trade statistics",
                source_type=DataSourceType.API,
                url="https://comtrade.un.org/api",
                tags=["trade", "un", "global"],
                categories=["trade_statistics", "multilateral"],
                country_coverage=["all"],
                time_coverage="1962-2024",
                update_frequency="monthly",
            ),
        ]

        logger.info(f"Using {len(default_sources)} default data sources")
        return default_sources

    async def discover_new_sources(self, query: str = None) -> List[DataSource]:
        """
        Discover new data sources using RAG capabilities

        Args:
            query: Natural language query for source discovery

        Returns:
            List of discovered data sources
        """
        if not self.vector_store or not self.embedding_model:
            logger.warning("RAG capabilities not available for source discovery")
            return []

        try:
            # Generate embedding for query
            if query:
                query_embedding = self.embedding_model.encode(query).tolist()

                # Search for similar sources
                results = self.source_collection.query(
                    query_embeddings=[query_embedding], n_results=10
                )

                # Process results and suggest new sources
                discovered_sources = self._process_discovery_results(results, query)
                return discovered_sources
            else:
                # General discovery based on existing patterns
                return self._general_source_discovery()

        except Exception as e:
            logger.error(f"Source discovery failed: {e}")
            return []

    def _process_discovery_results(self, results: Dict, query: str) -> List[DataSource]:
        """Process discovery results and suggest new sources"""
        discovered_sources = []

        # Analyze existing sources to identify gaps
        existing_categories = set()
        existing_countries = set()

        for source in self.data_sources:
            existing_categories.update(source.categories)
            existing_countries.update(source.country_coverage)

        # Suggest new sources based on gaps
        if "tariff_data" not in existing_categories:
            discovered_sources.append(
                DataSource(
                    id=f"tariff_source_{len(discovered_sources)}",
                    name="Global Tariff Database",
                    description="Comprehensive global tariff and trade policy data",
                    source_type=DataSourceType.API,
                    url="https://api.tariffdata.org",
                    tags=["tariffs", "trade_policy", "global"],
                    categories=["tariff_data", "policy"],
                    country_coverage=["all"],
                    time_coverage="2010-2024",
                    update_frequency="weekly",
                )
            )

        if "financial_markets" not in existing_categories:
            discovered_sources.append(
                DataSource(
                    id=f"financial_source_{len(discovered_sources)}",
                    name="Financial Markets Data",
                    description="Real-time financial market indicators and exchange rates",
                    source_type=DataSourceType.API,
                    url="https://api.financialdata.org",
                    tags=["financial", "markets", "exchange_rates"],
                    categories=["financial_markets", "real_time"],
                    country_coverage=["all"],
                    time_coverage="2000-2024",
                    update_frequency="hourly",
                )
            )

        logger.info(f"Discovered {len(discovered_sources)} new potential data sources")
        return discovered_sources

    def _general_source_discovery(self) -> List[DataSource]:
        """General source discovery based on patterns and gaps"""
        # This would implement more sophisticated discovery logic
        # For now, return empty list
        return []

    async def crawl_data_source(self, source_id: str) -> CrawlResult:
        """
        Crawl a specific data source

        Args:
            source_id: ID of the data source to crawl

        Returns:
            CrawlResult with crawl outcome
        """
        source = next((s for s in self.data_sources if s.id == source_id), None)
        if not source:
            raise ValueError(f"Data source not found: {source_id}")

        start_time = datetime.now()

        try:
            # Determine appropriate crawler
            crawler = self._get_crawler_for_source(source)

            # Perform crawl
            raw_data = await crawler.crawl(source)

            # Process and validate data
            processed_data = await self._process_crawled_data(raw_data, source)

            # Calculate metrics
            crawl_duration = (datetime.now() - start_time).total_seconds()

            # Create crawl result
            result = CrawlResult(
                source_id=source_id,
                timestamp=datetime.now(),
                success=True,
                raw_data=raw_data,
                processed_data=processed_data,
                data_size=len(str(raw_data)),
                records_count=processed_data.get("record_count", 0),
                fields_count=processed_data.get("field_count", 0),
                countries_covered=processed_data.get("countries", []),
                time_period=processed_data.get("time_period"),
                crawl_duration=crawl_duration,
                data_freshness=0,  # Will be calculated during validation
            )

            # Store in history
            if source_id not in self.crawl_history:
                self.crawl_history[source_id] = []
            self.crawl_history[source_id].append(result)

            # Update vector store with new data
            await self._update_vector_store(result, source)

            logger.info(
                f"Successfully crawled {source_id}: {result.records_count} records"
            )
            return result

        except Exception as e:
            crawl_duration = (datetime.now() - start_time).total_seconds()

            # Create error result
            result = CrawlResult(
                source_id=source_id,
                timestamp=datetime.now(),
                success=False,
                error_message=str(e),
                crawl_duration=crawl_duration,
            )

            # Store in history
            if source_id not in self.crawl_history:
                self.crawl_history[source_id] = []
            self.crawl_history[source_id].append(result)

            # Update source error count
            source.error_count += 1
            source.last_error = str(e)

            logger.error(f"Failed to crawl {source_id}: {e}")
            return result

    def _get_crawler_for_source(self, source: DataSource):
        """Get appropriate crawler for a data source"""
        # Simple mapping based on source tags and categories
        if "world_bank" in source.tags or "gdp" in source.categories:
            return self.crawlers["world_bank"]
        elif "census" in source.tags or "us" in source.categories:
            return self.crawlers["us_census"]
        elif "un" in source.tags or "comtrade" in source.tags:
            return self.crawlers["un_comtrade"]
        else:
            # Default to world bank crawler
            return self.crawlers["world_bank"]

    async def _process_crawled_data(
        self, raw_data: Any, source: DataSource
    ) -> Dict[str, Any]:
        """Process and structure crawled data"""
        try:
            # Basic processing - this would be enhanced based on data type
            if isinstance(raw_data, dict):
                processed = {
                    "record_count": len(raw_data.get("data", [])),
                    "field_count": len(raw_data.get("fields", [])),
                    "countries": raw_data.get("countries", []),
                    "time_period": raw_data.get("time_period"),
                    "data_structure": "structured",
                }
            elif isinstance(raw_data, list):
                processed = {
                    "record_count": len(raw_data),
                    "field_count": len(raw_data[0]) if raw_data else 0,
                    "countries": [],
                    "time_period": None,
                    "data_structure": "list",
                }
            else:
                processed = {
                    "record_count": 1,
                    "field_count": 1,
                    "countries": [],
                    "time_period": None,
                    "data_structure": "unknown",
                }

            return processed

        except Exception as e:
            logger.error(f"Data processing failed: {e}")
            return {
                "record_count": 0,
                "field_count": 0,
                "countries": [],
                "time_period": None,
                "data_structure": "error",
            }

    async def _update_vector_store(self, result: CrawlResult, source: DataSource):
        """Update vector store with new crawled data"""
        if not self.vector_store or not self.embedding_model:
            return

        try:
            # Create metadata for the crawled data
            metadata = {
                "source_id": source.id,
                "source_name": source.name,
                "crawl_timestamp": result.timestamp.isoformat(),
                "record_count": result.records_count,
                "countries": (
                    ",".join(result.countries_covered)
                    if result.countries_covered
                    else "unknown"
                ),
                "data_freshness": result.data_freshness,
            }

            # Generate text representation for embedding
            text_content = f"{source.name}: {source.description}. "
            if result.processed_data:
                text_content += f"Contains {result.records_count} records covering {len(result.countries_covered)} countries."

            # Generate embedding
            embedding = self.embedding_model.encode(text_content).tolist()

            # Store in vector database
            self.data_collection.add(
                embeddings=[embedding],
                documents=[text_content],
                metadatas=[metadata],
                ids=[f"{source.id}_{result.timestamp.strftime('%Y%m%d_%H%M%S')}"],
            )

            logger.info(f"Updated vector store with data from {source.id}")

        except Exception as e:
            logger.error(f"Failed to update vector store: {e}")

    async def validate_crawl_result(
        self, crawl_result: CrawlResult
    ) -> ValidationResult:
        """
        Validate a crawl result using multiple validation layers

        Args:
            crawl_result: The crawl result to validate

        Returns:
            ValidationResult with validation outcome
        """
        start_time = datetime.now()

        try:
            # Basic data quality validation
            quality_scores = await self.data_validator.validate_data(
                crawl_result.processed_data, crawl_result.raw_data
            )

            # ML-based anomaly detection
            ml_scores = await self.ml_anomaly_detector.detect_anomalies(
                crawl_result.processed_data
            )

            # Calculate overall scores
            completeness_score = quality_scores.get("completeness", 0.0)
            accuracy_score = quality_scores.get("accuracy", 0.0)
            consistency_score = quality_scores.get("consistency", 0.0)
            timeliness_score = quality_scores.get("timeliness", 0.0)

            anomaly_score = ml_scores.get("anomaly_detection", 0.0)
            statistical_score = ml_scores.get("statistical_validity", 0.0)
            business_logic_score = ml_scores.get("business_logic", 0.0)

            # Determine overall status
            overall_score = (
                sum(
                    [
                        completeness_score,
                        accuracy_score,
                        consistency_score,
                        timeliness_score,
                        anomaly_score,
                        statistical_score,
                        business_logic_score,
                    ]
                )
                / 7.0
            )

            if overall_score >= 0.8:
                status = ValidationStatus.PASSED
                should_integrate = True
                priority = 1  # High priority
            elif overall_score >= 0.6:
                status = ValidationStatus.WARNING
                should_integrate = True
                priority = 2  # Medium priority
            else:
                status = ValidationStatus.FAILED
                should_integrate = False
                priority = 3  # Low priority

            # Create validation result
            validation_result = ValidationResult(
                crawl_result_id=f"{crawl_result.source_id}_{crawl_result.timestamp.strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                overall_status=status,
                completeness_score=completeness_score,
                accuracy_score=accuracy_score,
                consistency_score=consistency_score,
                timeliness_score=timeliness_score,
                anomaly_detection_score=anomaly_score,
                statistical_validity=statistical_score,
                business_logic_score=business_logic_score,
                should_integrate=should_integrate,
                confidence_level=overall_score,
                integration_priority=priority,
            )

            # Store in history
            source_id = crawl_result.source_id
            if source_id not in self.validation_history:
                self.validation_history[source_id] = []
            self.validation_history[source_id].append(validation_result)

            logger.info(
                f"Validation completed for {source_id}: {status.value} (score: {overall_score:.2f})"
            )
            return validation_result

        except Exception as e:
            logger.error(f"Validation failed: {e}")

            # Return failed validation result
            return ValidationResult(
                crawl_result_id=f"{crawl_result.source_id}_{crawl_result.timestamp.strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                overall_status=ValidationStatus.FAILED,
                should_integrate=False,
                confidence_level=0.0,
                integration_priority=3,
            )

    async def run_full_crawl_cycle(self) -> Dict[str, Any]:
        """
        Run a complete crawl cycle for all active data sources

        Returns:
            Summary of the crawl cycle
        """
        logger.info("Starting full crawl cycle")
        start_time = datetime.now()

        cycle_results = {
            "start_time": start_time.isoformat(),
            "end_time": None,
            "total_sources": len(self.data_sources),
            "active_sources": len([s for s in self.data_sources if s.is_active]),
            "successful_crawls": 0,
            "failed_crawls": 0,
            "validations_passed": 0,
            "validations_failed": 0,
            "sources_to_integrate": 0,
            "errors": [],
        }

        try:
            # Crawl each active source
            for source in self.data_sources:
                if not source.is_active:
                    continue

                try:
                    # Check if it's time to update this source
                    if not self._should_update_source(source):
                        logger.info(f"Skipping {source.id} - not due for update")
                        continue

                    # Crawl the source
                    crawl_result = await self.crawl_data_source(source.id)

                    if crawl_result.success:
                        cycle_results["successful_crawls"] += 1

                        # Validate the result
                        validation_result = await self.validate_crawl_result(
                            crawl_result
                        )

                        if validation_result.overall_status == ValidationStatus.PASSED:
                            cycle_results["validations_passed"] += 1
                        else:
                            cycle_results["validations_failed"] += 1

                        if validation_result.should_integrate:
                            cycle_results["sources_to_integrate"] += 1

                        # Update source metadata
                        source.last_updated = datetime.now()
                        source.next_update = self._calculate_next_update(source)

                    else:
                        cycle_results["failed_crawls"] += 1
                        cycle_results["errors"].append(
                            f"{source.id}: {crawl_result.error_message}"
                        )

                except Exception as e:
                    cycle_results["failed_crawls"] += 1
                    cycle_results["errors"].append(f"{source.id}: {str(e)}")
                    logger.error(f"Error processing source {source.id}: {e}")

            cycle_results["end_time"] = datetime.now().isoformat()
            cycle_results["duration"] = (datetime.now() - start_time).total_seconds()

            logger.info(
                f"Crawl cycle completed: {cycle_results['successful_crawls']} successful, {cycle_results['failed_crawls']} failed"
            )
            return cycle_results

        except Exception as e:
            logger.error(f"Crawl cycle failed: {e}")
            cycle_results["end_time"] = datetime.now().isoformat()
            cycle_results["duration"] = (datetime.now() - start_time).total_seconds()
            cycle_results["errors"].append(f"Cycle error: {str(e)}")
            return cycle_results

    def _should_update_source(self, source: DataSource) -> bool:
        """Check if a source should be updated based on its frequency"""
        if not source.last_updated:
            return True

        now = datetime.now()
        if source.next_update and now >= source.next_update:
            return True

        # Calculate based on frequency
        if source.update_frequency == "hourly":
            return (now - source.last_updated).total_seconds() >= 3600
        elif source.update_frequency == "daily":
            return (now - source.last_updated).days >= 1
        elif source.update_frequency == "weekly":
            return (now - source.last_updated).days >= 7
        elif source.update_frequency == "monthly":
            return (now - source.last_updated).days >= 30

        return False

    def _calculate_next_update(self, source: DataSource) -> datetime:
        """Calculate next update time for a source"""
        now = datetime.now()

        if source.update_frequency == "hourly":
            return now + timedelta(hours=1)
        elif source.update_frequency == "daily":
            return now + timedelta(days=1)
        elif source.update_frequency == "weekly":
            return now + timedelta(weeks=1)
        elif source.update_frequency == "monthly":
            return now + timedelta(days=30)

        return now + timedelta(days=1)  # Default to daily

    def get_crawl_status(self) -> Dict[str, Any]:
        """Get current status of all data sources and recent crawls"""
        status = {
            "total_sources": len(self.data_sources),
            "active_sources": len([s for s in self.data_sources if s.is_active]),
            "verified_sources": len([s for s in self.data_sources if s.is_verified]),
            "sources_needing_update": len(
                [s for s in self.data_sources if self._should_update_source(s)]
            ),
            "recent_crawls": {},
            "recent_validations": {},
            "overall_health": "good",
        }

        # Add recent crawl information
        for source_id, crawls in self.crawl_history.items():
            if crawls:
                latest_crawl = crawls[-1]
                status["recent_crawls"][source_id] = {
                    "last_crawl": latest_crawl.timestamp.isoformat(),
                    "success": latest_crawl.success,
                    "records": latest_crawl.records_count,
                    "duration": latest_crawl.crawl_duration,
                }

        # Add recent validation information
        for source_id, validations in self.validation_history.items():
            if validations:
                latest_validation = validations[-1]
                status["recent_validations"][source_id] = {
                    "last_validation": latest_validation.timestamp.isoformat(),
                    "status": latest_validation.overall_status.value,
                    "score": latest_validation.get_overall_score(),
                    "should_integrate": latest_validation.should_integrate,
                }

        # Determine overall health
        error_count = sum(1 for s in self.data_sources if s.error_count > 0)
        if error_count > len(self.data_sources) * 0.3:
            status["overall_health"] = "poor"
        elif error_count > len(self.data_sources) * 0.1:
            status["overall_health"] = "fair"

        return status

    def save_configuration(self):
        """Save current data source configuration"""
        try:
            config_data = {
                "sources": [source.to_dict() for source in self.data_sources],
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0",
            }

            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=2)

            logger.info(f"Configuration saved to {self.config_path}")

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def add_data_source(self, source: DataSource):
        """Add a new data source to the system"""
        # Check if source with same ID already exists
        if any(s.id == source.id for s in self.data_sources):
            raise ValueError(f"Data source with ID {source.id} already exists")

        self.data_sources.append(source)
        logger.info(f"Added new data source: {source.name} ({source.id})")

        # Save configuration
        self.save_configuration()

    def remove_data_source(self, source_id: str):
        """Remove a data source from the system"""
        self.data_sources = [s for s in self.data_sources if s.id != source_id]
        logger.info(f"Removed data source: {source_id}")

        # Save configuration
        self.save_configuration()

    def update_data_source(self, source_id: str, updates: Dict[str, Any]):
        """Update an existing data source"""
        source = next((s for s in self.data_sources if s.id == source_id), None)
        if not source:
            raise ValueError(f"Data source not found: {source_id}")

        # Update fields
        for field, value in updates.items():
            if hasattr(source, field):
                setattr(source, field, value)

        logger.info(f"Updated data source: {source_id}")

        # Save configuration
        self.save_configuration()
