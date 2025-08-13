"""
Data Models for TIPM Data Crawler
=================================

Core data structures for data sources, crawl results, and validation outcomes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import json


class DataSourceType(Enum):
    """Types of data sources"""

    API = "api"
    WEB_SCRAPING = "web_scraping"
    DATABASE = "database"
    FILE = "file"
    STREAMING = "streaming"


class DataQualityScore(Enum):
    """Data quality assessment scores"""

    EXCELLENT = "excellent"  # 90-100%
    GOOD = "good"  # 75-89%
    FAIR = "fair"  # 60-74%
    POOR = "poor"  # 40-59%
    UNACCEPTABLE = "unacceptable"  # <40%


class ValidationStatus(Enum):
    """Validation result status"""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


@dataclass
class DataSource:
    """Represents a data source configuration"""

    id: str
    name: str
    description: str
    source_type: DataSourceType
    url: str
    api_key: Optional[str] = None
    credentials: Optional[Dict[str, str]] = None

    # Configuration
    update_frequency: str = "daily"  # hourly, daily, weekly, monthly
    last_updated: Optional[datetime] = None
    next_update: Optional[datetime] = None

    # Metadata
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    country_coverage: List[str] = field(default_factory=list)
    time_coverage: Optional[str] = None

    # Quality metrics
    reliability_score: float = 0.0
    data_freshness: int = 0  # days since last update
    completeness: float = 0.0
    accuracy: float = 0.0

    # Status
    is_active: bool = True
    is_verified: bool = False
    error_count: int = 0
    last_error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "source_type": self.source_type.value,
            "url": self.url,
            "update_frequency": self.update_frequency,
            "last_updated": (
                self.last_updated.isoformat() if self.last_updated else None
            ),
            "next_update": self.next_update.isoformat() if self.next_update else None,
            "tags": self.tags,
            "categories": self.categories,
            "country_coverage": self.country_coverage,
            "time_coverage": self.time_coverage,
            "reliability_score": self.reliability_score,
            "data_freshness": self.data_freshness,
            "completeness": self.completeness,
            "accuracy": self.accuracy,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "error_count": self.error_count,
            "last_error": self.last_error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSource":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            source_type=DataSourceType(data["source_type"]),
            url=data["url"],
            update_frequency=data.get("update_frequency", "daily"),
            last_updated=(
                datetime.fromisoformat(data["last_updated"])
                if data.get("last_updated")
                else None
            ),
            next_update=(
                datetime.fromisoformat(data["next_update"])
                if data.get("next_update")
                else None
            ),
            tags=data.get("tags", []),
            categories=data.get("categories", []),
            country_coverage=data.get("country_coverage", []),
            time_coverage=data.get("time_coverage"),
            reliability_score=data.get("reliability_score", 0.0),
            data_freshness=data.get("data_freshness", 0),
            completeness=data.get("completeness", 0.0),
            accuracy=data.get("accuracy", 0.0),
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False),
            error_count=data.get("error_count", 0),
            last_error=data.get("last_error"),
        )


@dataclass
class CrawlResult:
    """Result of a data crawling operation"""

    source_id: str
    timestamp: datetime
    success: bool

    # Data content
    raw_data: Optional[Any] = None
    processed_data: Optional[Dict[str, Any]] = None
    data_size: int = 0  # bytes

    # Metadata
    records_count: int = 0
    fields_count: int = 0
    countries_covered: List[str] = field(default_factory=list)
    time_period: Optional[str] = None

    # Performance metrics
    crawl_duration: float = 0.0  # seconds
    processing_duration: float = 0.0  # seconds

    # Quality indicators
    data_freshness: int = 0  # days
    completeness_estimate: float = 0.0

    # Error handling
    error_message: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source_id": self.source_id,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "data_size": self.data_size,
            "records_count": self.records_count,
            "fields_count": self.fields_count,
            "countries_covered": self.countries_covered,
            "time_period": self.time_period,
            "crawl_duration": self.crawl_duration,
            "processing_duration": self.processing_duration,
            "data_freshness": self.data_freshness,
            "completeness_estimate": self.completeness_estimate,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
        }


@dataclass
class ValidationResult:
    """Result of data validation process"""

    crawl_result_id: str
    timestamp: datetime
    overall_status: ValidationStatus

    # Quality scores
    completeness_score: float = 0.0
    accuracy_score: float = 0.0
    consistency_score: float = 0.0
    timeliness_score: float = 0.0

    # ML validation results
    anomaly_detection_score: float = 0.0
    statistical_validity: float = 0.0
    business_logic_score: float = 0.0

    # Detailed results
    field_validations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    constraint_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Decision
    should_integrate: bool = False
    confidence_level: float = 0.0
    integration_priority: int = 0  # 1=high, 2=medium, 3=low

    def get_overall_score(self) -> float:
        """Calculate overall quality score"""
        scores = [
            self.completeness_score,
            self.accuracy_score,
            self.consistency_score,
            self.timeliness_score,
            self.anomaly_detection_score,
            self.statistical_validity,
            self.business_logic_score,
        ]
        return sum(scores) / len(scores)

    def get_quality_level(self) -> DataQualityScore:
        """Get quality level based on overall score"""
        score = self.get_overall_score()
        if score >= 0.9:
            return DataQualityScore.EXCELLENT
        elif score >= 0.75:
            return DataQualityScore.GOOD
        elif score >= 0.6:
            return DataQualityScore.FAIR
        elif score >= 0.4:
            return DataQualityScore.POOR
        else:
            return DataQualityScore.UNACCEPTABLE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "crawl_result_id": self.crawl_result_id,
            "timestamp": self.timestamp.isoformat(),
            "overall_status": self.overall_status.value,
            "completeness_score": self.completeness_score,
            "accuracy_score": self.accuracy_score,
            "consistency_score": self.consistency_score,
            "timeliness_score": self.timeliness_score,
            "anomaly_detection_score": self.anomaly_detection_score,
            "statistical_validity": self.statistical_validity,
            "business_logic_score": self.business_logic_score,
            "field_validations": self.field_validations,
            "constraint_violations": self.constraint_violations,
            "warnings": self.warnings,
            "should_integrate": self.should_integrate,
            "confidence_level": self.confidence_level,
            "integration_priority": self.integration_priority,
            "overall_score": self.get_overall_score(),
            "quality_level": self.get_quality_level().value,
        }


@dataclass
class DataIntegrationResult:
    """Result of data integration process"""

    validation_result_id: str
    timestamp: datetime
    success: bool

    # Integration details
    target_database: str
    tables_updated: List[str] = field(default_factory=list)
    records_inserted: int = 0
    records_updated: int = 0
    records_deleted: int = 0

    # Performance
    integration_duration: float = 0.0
    data_transformation_time: float = 0.0

    # Quality checks
    post_integration_validation: bool = False
    data_consistency_check: bool = False

    # Metadata
    version: str = "1.0.0"
    change_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "validation_result_id": self.validation_result_id,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "target_database": self.target_database,
            "tables_updated": self.tables_updated,
            "records_inserted": self.records_inserted,
            "records_updated": self.records_updated,
            "records_deleted": self.records_deleted,
            "integration_duration": self.integration_duration,
            "data_transformation_time": self.data_transformation_time,
            "post_integration_validation": self.post_integration_validation,
            "data_consistency_check": self.data_consistency_check,
            "version": self.version,
            "change_summary": self.change_summary,
        }
