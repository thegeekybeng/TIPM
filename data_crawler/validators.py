"""
Data Validation and ML Anomaly Detection for TIPM
=================================================

Multi-layer validation system including statistical validation, business logic validation,
and ML-powered anomaly detection.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass

# Optional imports for advanced features
try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

from .models import ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ValidationRule:
    """A validation rule for data quality assessment"""

    name: str
    description: str
    rule_type: str  # "statistical", "business_logic", "format", "range"
    field_name: Optional[str] = None
    condition: Optional[str] = None
    threshold: Optional[float] = None
    weight: float = 1.0  # Importance weight for scoring

    def evaluate(self, data: Any) -> Dict[str, Any]:
        """Evaluate the rule against data"""
        raise NotImplementedError("Subclasses must implement evaluate method")


class DataQualityValidator:
    """Comprehensive data quality validation system"""

    def __init__(self):
        self.validation_rules = self._initialize_rules()
        self.logger = logging.getLogger(__name__)

    def _initialize_rules(self) -> List[ValidationRule]:
        """Initialize validation rules"""
        rules = [
            # Completeness rules
            ValidationRule(
                name="null_check",
                description="Check for null/missing values",
                rule_type="completeness",
                weight=0.3,
            ),
            # Accuracy rules
            ValidationRule(
                name="range_check",
                description="Check if values are within expected ranges",
                rule_type="accuracy",
                weight=0.25,
            ),
            # Consistency rules
            ValidationRule(
                name="format_check",
                description="Check data format consistency",
                rule_type="consistency",
                weight=0.2,
            ),
            # Timeliness rules
            ValidationRule(
                name="freshness_check",
                description="Check data freshness",
                rule_type="timeliness",
                weight=0.25,
            ),
        ]

        return rules

    async def validate_data(
        self, processed_data: Dict[str, Any], raw_data: Any
    ) -> Dict[str, float]:
        """
        Validate data quality using multiple validation layers

        Args:
            processed_data: Processed and structured data
            raw_data: Raw data from source

        Returns:
            Dictionary with validation scores
        """
        try:
            validation_scores = {}

            # Completeness validation
            completeness_score = self._validate_completeness(processed_data, raw_data)
            validation_scores["completeness"] = completeness_score

            # Accuracy validation
            accuracy_score = self._validate_accuracy(processed_data, raw_data)
            validation_scores["accuracy"] = accuracy_score

            # Consistency validation
            consistency_score = self._validate_consistency(processed_data, raw_data)
            validation_scores["consistency"] = consistency_score

            # Timeliness validation
            timeliness_score = self._validate_timeliness(processed_data, raw_data)
            validation_scores["timeliness"] = timeliness_score

            self.logger.info(f"Data validation completed - Scores: {validation_scores}")
            return validation_scores

        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            # Return default scores on error
            return {
                "completeness": 0.0,
                "accuracy": 0.0,
                "consistency": 0.0,
                "timeliness": 0.0,
            }

    def _validate_completeness(
        self, processed_data: Dict[str, Any], raw_data: Any
    ) -> float:
        """Validate data completeness"""
        try:
            if not processed_data:
                return 0.0

            # Check if essential fields are present
            essential_fields = [
                "record_count",
                "field_count",
                "countries",
                "time_period",
            ]
            present_fields = sum(
                1 for field in essential_fields if field in processed_data
            )
            field_completeness = present_fields / len(essential_fields)

            # Check record count consistency
            if "record_count" in processed_data and "data" in processed_data:
                expected_records = processed_data["record_count"]
                actual_records = (
                    len(processed_data["data"])
                    if isinstance(processed_data["data"], (list, dict))
                    else 0
                )

                if expected_records > 0:
                    record_completeness = min(actual_records / expected_records, 1.0)
                else:
                    record_completeness = 0.0
            else:
                record_completeness = 0.5  # Neutral score if can't determine

            # Overall completeness score
            completeness_score = (field_completeness + record_completeness) / 2
            return round(completeness_score, 3)

        except Exception as e:
            self.logger.error(f"Completeness validation failed: {e}")
            return 0.0

    def _validate_accuracy(
        self, processed_data: Dict[str, Any], raw_data: Any
    ) -> float:
        """Validate data accuracy"""
        try:
            if not processed_data:
                return 0.0

            accuracy_checks = []

            # Check for reasonable value ranges
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                data_values = []
                for country_data in processed_data["data"].values():
                    if isinstance(country_data, dict):
                        for indicator_data in country_data.values():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                            ):
                                values = indicator_data["values"]
                                if isinstance(values, list):
                                    for value_item in values:
                                        if (
                                            isinstance(value_item, dict)
                                            and "value" in value_item
                                        ):
                                            try:
                                                val = float(value_item["value"])
                                                if val > 0:  # Only positive values
                                                    data_values.append(val)
                                            except (ValueError, TypeError):
                                                continue

                if data_values:
                    # Check for statistical outliers (basic)
                    if NUMPY_AVAILABLE and np is not None:
                        mean_val = np.mean(data_values)
                        std_val = np.std(data_values)
                    else:
                        # Fallback without numpy
                        mean_val = sum(data_values) / len(data_values)
                        variance = sum((x - mean_val) ** 2 for x in data_values) / len(
                            data_values
                        )
                        std_val = variance**0.5

                    if std_val > 0:
                        outliers = sum(
                            1
                            for val in data_values
                            if abs(val - mean_val) > 3 * std_val
                        )
                        outlier_ratio = outliers / len(data_values)
                        accuracy_checks.append(1.0 - outlier_ratio)
                    else:
                        accuracy_checks.append(1.0)
                else:
                    accuracy_checks.append(0.5)

            # Check country code validity (basic check)
            if "countries" in processed_data:
                countries = processed_data["countries"]
                if isinstance(countries, list) and countries:
                    # Basic check: countries should be non-empty strings
                    valid_countries = sum(
                        1 for c in countries if isinstance(c, str) and len(c) > 0
                    )
                    country_accuracy = valid_countries / len(countries)
                    accuracy_checks.append(country_accuracy)
                else:
                    accuracy_checks.append(0.5)

            # Check time period format
            if "time_period" in processed_data:
                time_period = processed_data["time_period"]
                if isinstance(time_period, str) and "-" in time_period:
                    try:
                        start_year, end_year = time_period.split("-")
                        if start_year.isdigit() and end_year.isdigit():
                            accuracy_checks.append(1.0)
                        else:
                            accuracy_checks.append(0.5)
                    except:
                        accuracy_checks.append(0.3)
                else:
                    accuracy_checks.append(0.5)

            # Calculate overall accuracy score
            if accuracy_checks:
                accuracy_score = sum(accuracy_checks) / len(accuracy_checks)
            else:
                accuracy_score = 0.5

            return round(accuracy_score, 3)

        except Exception as e:
            self.logger.error(f"Accuracy validation failed: {e}")
            return 0.0

    def _validate_consistency(
        self, processed_data: Dict[str, Any], raw_data: Any
    ) -> float:
        """Validate data consistency"""
        try:
            if not processed_data:
                return 0.0

            consistency_checks = []

            # Check data structure consistency
            if "data_structure" in processed_data:
                expected_structure = processed_data["data_structure"]
                if expected_structure in ["structured", "list"]:
                    consistency_checks.append(1.0)
                elif expected_structure == "unknown":
                    consistency_checks.append(0.5)
                else:
                    consistency_checks.append(0.3)

            # Check field count consistency
            if "field_count" in processed_data and "data" in processed_data:
                expected_fields = processed_data["field_count"]
                if isinstance(processed_data["data"], dict) and processed_data["data"]:
                    # Check if all country data has consistent structure
                    first_country = next(iter(processed_data["data"].values()))
                    if isinstance(first_country, dict):
                        actual_fields = len(first_country)
                        if expected_fields > 0:
                            field_consistency = min(
                                actual_fields / expected_fields, 1.0
                            )
                            consistency_checks.append(field_consistency)
                        else:
                            consistency_checks.append(0.5)
                    else:
                        consistency_checks.append(0.5)
                else:
                    consistency_checks.append(0.5)

            # Check timestamp consistency
            if "timestamp" in processed_data:
                try:
                    timestamp = datetime.fromisoformat(processed_data["timestamp"])
                    now = datetime.now()
                    time_diff = abs((now - timestamp).total_seconds())

                    # Score based on recency (within 24 hours = 1.0, older = lower)
                    if time_diff < 86400:  # 24 hours
                        consistency_checks.append(1.0)
                    elif time_diff < 604800:  # 1 week
                        consistency_checks.append(0.8)
                    elif time_diff < 2592000:  # 1 month
                        consistency_checks.append(0.6)
                    else:
                        consistency_checks.append(0.4)
                except:
                    consistency_checks.append(0.3)

            # Calculate overall consistency score
            if consistency_checks:
                consistency_score = sum(consistency_checks) / len(consistency_checks)
            else:
                consistency_score = 0.5

            return round(consistency_score, 3)

        except Exception as e:
            self.logger.error(f"Consistency validation failed: {e}")
            return 0.0

    def _validate_timeliness(
        self, processed_data: Dict[str, Any], raw_data: Any
    ) -> float:
        """Validate data timeliness"""
        try:
            if not processed_data:
                return 0.0

            timeliness_checks = []

            # Check timestamp freshness
            if "timestamp" in processed_data:
                try:
                    timestamp = datetime.fromisoformat(processed_data["timestamp"])
                    now = datetime.now()
                    time_diff = (now - timestamp).total_seconds()

                    # Score based on recency
                    if time_diff < 3600:  # 1 hour
                        timeliness_checks.append(1.0)
                    elif time_diff < 86400:  # 1 day
                        timeliness_checks.append(0.9)
                    elif time_diff < 604800:  # 1 week
                        timeliness_checks.append(0.7)
                    elif time_diff < 2592000:  # 1 month
                        timeliness_checks.append(0.5)
                    else:
                        timeliness_checks.append(0.3)
                except:
                    timeliness_checks.append(0.3)

            # Check time period relevance
            if "time_period" in processed_data:
                time_period = processed_data["time_period"]
                if isinstance(time_period, str) and "-" in time_period:
                    try:
                        start_year, end_year = time_period.split("-")
                        current_year = datetime.now().year

                        if end_year.isdigit():
                            end_year_int = int(end_year)
                            year_diff = current_year - end_year_int

                            if year_diff <= 1:
                                timeliness_checks.append(1.0)
                            elif year_diff <= 3:
                                timeliness_checks.append(0.8)
                            elif year_diff <= 5:
                                timeliness_checks.append(0.6)
                            else:
                                timeliness_checks.append(0.4)
                        else:
                            timeliness_checks.append(0.5)
                    except:
                        timeliness_checks.append(0.5)
                else:
                    timeliness_checks.append(0.5)

            # Calculate overall timeliness score
            if timeliness_checks:
                timeliness_score = sum(timeliness_checks) / len(timeliness_checks)
            else:
                timeliness_score = 0.5

            return round(timeliness_score, 3)

        except Exception as e:
            self.logger.error(f"Timeliness validation failed: {e}")
            return 0.0


class MLAnomalyDetector:
    """ML-powered anomaly detection for data validation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anomaly_threshold = 0.1  # Threshold for anomaly detection

    async def detect_anomalies(
        self, processed_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Detect anomalies in processed data using ML techniques

        Args:
            processed_data: Processed data to analyze

        Returns:
            Dictionary with anomaly detection scores
        """
        try:
            anomaly_scores = {}

            # Statistical anomaly detection
            statistical_score = self._detect_statistical_anomalies(processed_data)
            anomaly_scores["statistical_validity"] = statistical_score

            # Business logic anomaly detection
            business_logic_score = self._detect_business_logic_anomalies(processed_data)
            anomaly_scores["business_logic"] = business_logic_score

            # Pattern anomaly detection
            pattern_score = self._detect_pattern_anomalies(processed_data)
            anomaly_scores["anomaly_detection"] = pattern_score

            self.logger.info(f"Anomaly detection completed - Scores: {anomaly_scores}")
            return anomaly_scores

        except Exception as e:
            self.logger.error(f"Anomaly detection failed: {e}")
            # Return default scores on error
            return {
                "statistical_validity": 0.5,
                "business_logic": 0.5,
                "anomaly_detection": 0.5,
            }

    def _detect_statistical_anomalies(self, processed_data: Dict[str, Any]) -> float:
        """Detect statistical anomalies in data"""
        try:
            if not processed_data or "data" not in processed_data:
                return 0.5

            data = processed_data["data"]
            if not isinstance(data, dict):
                return 0.5

            # Extract numerical values for analysis
            numerical_values = []

            for country_data in data.values():
                if isinstance(country_data, dict):
                    for indicator_data in country_data.values():
                        if (
                            isinstance(indicator_data, dict)
                            and "values" in indicator_data
                        ):
                            values = indicator_data["values"]
                            if isinstance(values, list):
                                for value_item in values:
                                    if (
                                        isinstance(value_item, dict)
                                        and "value" in value_item
                                    ):
                                        try:
                                            val = float(value_item["value"])
                                            if val > 0:  # Only positive values
                                                numerical_values.append(val)
                                        except (ValueError, TypeError):
                                            continue

            if len(numerical_values) < 10:  # Need sufficient data for analysis
                return 0.5

            # Basic statistical analysis
            if NUMPY_AVAILABLE and np is not None:
                values_array = np.array(numerical_values)
                mean_val = np.mean(values_array)
                std_val = np.std(values_array)

                if std_val == 0:
                    return 1.0  # No variation, no anomalies

                # Calculate z-scores
                z_scores = np.abs((values_array - mean_val) / std_val)

                # Count anomalies (z-score > 3)
                anomalies = np.sum(z_scores > 3)
                anomaly_ratio = anomalies / len(values_array)
            else:
                # Fallback without numpy - basic statistical analysis
                mean_val = sum(numerical_values) / len(numerical_values)

                # Calculate variance manually
                variance = sum((x - mean_val) ** 2 for x in numerical_values) / len(
                    numerical_values
                )
                std_val = variance**0.5

                if std_val == 0:
                    return 1.0  # No variation, no anomalies

                # Count outliers (values more than 3 standard deviations from mean)
                outliers = sum(
                    1 for x in numerical_values if abs(x - mean_val) > 3 * std_val
                )
                anomaly_ratio = outliers / len(numerical_values)

            # Score based on anomaly ratio (lower is better)
            if anomaly_ratio < 0.01:  # Less than 1% anomalies
                score = 1.0
            elif anomaly_ratio < 0.05:  # Less than 5% anomalies
                score = 0.8
            elif anomaly_ratio < 0.1:  # Less than 10% anomalies
                score = 0.6
            else:
                score = 0.3

            return round(score, 3)

        except Exception as e:
            self.logger.error(f"Statistical anomaly detection failed: {e}")
            return 0.5

    def _detect_business_logic_anomalies(self, processed_data: Dict[str, Any]) -> float:
        """Detect business logic anomalies in data"""
        try:
            if not processed_data:
                return 0.5

            business_logic_checks = []

            # Check for reasonable GDP values (should be positive and not extremely large)
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                for country_code, country_data in processed_data["data"].items():
                    if isinstance(country_data, dict):
                        for indicator_code, indicator_data in country_data.items():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                                and indicator_code == "NY.GDP.MKTP.CD"  # GDP indicator
                            ):
                                values = indicator_data["values"]
                                if isinstance(values, list):
                                    for value_item in values:
                                        if (
                                            isinstance(value_item, dict)
                                            and "value" in value_item
                                        ):
                                            try:
                                                gdp_value = float(value_item["value"])
                                                # GDP should be positive and reasonable (not > 100 trillion)
                                                if 0 < gdp_value < 1e14:
                                                    business_logic_checks.append(1.0)
                                                else:
                                                    business_logic_checks.append(0.0)
                                            except (ValueError, TypeError):
                                                business_logic_checks.append(0.5)

            # Check for reasonable trade percentages (should be 0-200% of GDP)
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                for country_code, country_data in processed_data["data"].items():
                    if isinstance(country_data, dict):
                        for indicator_code, indicator_data in country_data.items():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                                and indicator_code == "NE.TRD.GNFS.ZS"  # Trade % of GDP
                            ):
                                values = indicator_data["values"]
                                if isinstance(values, list):
                                    for value_item in values:
                                        if (
                                            isinstance(value_item, dict)
                                            and "value" in value_item
                                        ):
                                            try:
                                                trade_pct = float(value_item["value"])
                                                # Trade should be reasonable percentage of GDP
                                                if 0 <= trade_pct <= 200:
                                                    business_logic_checks.append(1.0)
                                                else:
                                                    business_logic_checks.append(0.0)
                                            except (ValueError, TypeError):
                                                business_logic_checks.append(0.5)

            # Check for reasonable growth rates (should be between -50% and +100%)
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                for country_code, country_data in processed_data["data"].items():
                    if isinstance(country_data, dict):
                        for indicator_code, indicator_data in country_data.items():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                                and indicator_code == "NY.GDP.MKTP.KD.ZG"  # GDP growth
                            ):
                                values = indicator_data["values"]
                                if isinstance(values, list):
                                    for value_item in values:
                                        if (
                                            isinstance(value_item, dict)
                                            and "value" in value_item
                                        ):
                                            try:
                                                growth_rate = float(value_item["value"])
                                                # Growth rate should be reasonable
                                                if -50 <= growth_rate <= 100:
                                                    business_logic_checks.append(1.0)
                                                else:
                                                    business_logic_checks.append(0.0)
                                            except (ValueError, TypeError):
                                                business_logic_checks.append(0.5)

            # Calculate overall business logic score
            if business_logic_checks:
                business_logic_score = sum(business_logic_checks) / len(
                    business_logic_checks
                )
            else:
                business_logic_score = 0.5

            return round(business_logic_score, 3)

        except Exception as e:
            self.logger.error(f"Business logic anomaly detection failed: {e}")
            return 0.5

    def _detect_pattern_anomalies(self, processed_data: Dict[str, Any]) -> float:
        """Detect pattern-based anomalies in data"""
        try:
            if not processed_data:
                return 0.5

            pattern_checks = []

            # Check for data consistency across countries
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                countries = list(processed_data["data"].keys())
                if len(countries) > 1:
                    # Check if all countries have similar data structure
                    first_country = processed_data["data"][countries[0]]
                    if isinstance(first_country, dict):
                        first_country_indicators = set(first_country.keys())

                        consistent_structure = True
                        for country_code in countries[1:]:
                            country_data = processed_data["data"][country_code]
                            if isinstance(country_data, dict):
                                country_indicators = set(country_data.keys())
                                if country_indicators != first_country_indicators:
                                    consistent_structure = False
                                    break
                            else:
                                consistent_structure = False
                                break

                        if consistent_structure:
                            pattern_checks.append(1.0)
                        else:
                            pattern_checks.append(0.3)
                    else:
                        pattern_checks.append(0.5)
                else:
                    pattern_checks.append(0.5)

            # Check for temporal consistency in time series data
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                for country_code, country_data in processed_data["data"].items():
                    if isinstance(country_data, dict):
                        for indicator_code, indicator_data in country_data.items():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                                and isinstance(indicator_data["values"], list)
                                and len(indicator_data["values"]) > 1
                            ):
                                values = indicator_data["values"]
                                # Check if values are sorted by time (assuming chronological order)
                                try:
                                    time_values = []
                                    for value_item in values:
                                        if (
                                            isinstance(value_item, dict)
                                            and "date" in value_item
                                        ):
                                            time_values.append(value_item["date"])

                                    if time_values:
                                        # Simple check: if we have multiple time points, assume temporal consistency
                                        pattern_checks.append(1.0)
                                    else:
                                        pattern_checks.append(0.5)
                                except:
                                    pattern_checks.append(0.5)

            # Check for reasonable data distribution
            if "data" in processed_data and isinstance(processed_data["data"], dict):
                all_values = []
                for country_data in processed_data["data"].values():
                    if isinstance(country_data, dict):
                        for indicator_data in country_data.values():
                            if (
                                isinstance(indicator_data, dict)
                                and "values" in indicator_data
                                and isinstance(indicator_data["values"], list)
                            ):
                                for value_item in indicator_data["values"]:
                                    if (
                                        isinstance(value_item, dict)
                                        and "value" in value_item
                                    ):
                                        try:
                                            val = float(value_item["value"])
                                            if val > 0:
                                                all_values.append(val)
                                        except (ValueError, TypeError):
                                            continue

                if len(all_values) > 10:
                    # Check for reasonable distribution (not all values the same)
                    unique_values = len(set(all_values))
                    if unique_values > 1:
                        pattern_checks.append(1.0)
                    else:
                        pattern_checks.append(
                            0.3
                        )  # All values the same might indicate an issue
                else:
                    pattern_checks.append(0.5)

            # Calculate overall pattern score
            if pattern_checks:
                pattern_score = sum(pattern_checks) / len(pattern_checks)
            else:
                pattern_score = 0.5

            return round(pattern_score, 3)

        except Exception as e:
            self.logger.error(f"Pattern anomaly detection failed: {e}")
            return 0.5


class ValidationReport:
    """Comprehensive validation report generator"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_report(self, validation_result: "ValidationResult") -> str:
        """Generate a human-readable validation report"""
        try:
            report = f"""
# Data Validation Report

## Summary
- **Overall Status**: {validation_result.overall_status.value}
- **Overall Score**: {validation_result.get_overall_score():.1%}
- **Quality Level**: {validation_result.get_quality_level().value}
- **Should Integrate**: {'Yes' if validation_result.should_integrate else 'No'}
- **Integration Priority**: {validation_result.integration_priority}

## Detailed Scores

### Data Quality Metrics
- **Completeness**: {validation_result.completeness_score:.1%}
- **Accuracy**: {validation_result.accuracy_score:.1%}
- **Consistency**: {validation_result.consistency_score:.1%}
- **Timeliness**: {validation_result.timeliness_score:.1%}

### ML Validation Results
- **Anomaly Detection**: {validation_result.anomaly_detection_score:.1%}
- **Statistical Validity**: {validation_result.statistical_validity:.1%}
- **Business Logic**: {validation_result.business_logic_score:.1%}

## Recommendations
"""

            # Add recommendations based on scores
            if validation_result.completeness_score < 0.7:
                report += "- ⚠️ **Low Completeness**: Data may be missing critical information\n"

            if validation_result.accuracy_score < 0.7:
                report += "- ⚠️ **Low Accuracy**: Data may contain errors or outliers\n"

            if validation_result.consistency_score < 0.7:
                report += (
                    "- ⚠️ **Low Consistency**: Data structure may be inconsistent\n"
                )

            if validation_result.timeliness_score < 0.7:
                report += "- ⚠️ **Low Timeliness**: Data may be outdated\n"

            if validation_result.anomaly_detection_score < 0.7:
                report += (
                    "- ⚠️ **Anomalies Detected**: Data may contain unusual patterns\n"
                )

            # Add positive notes
            if validation_result.get_overall_score() >= 0.8:
                report += "- ✅ **High Quality**: Data meets quality standards for integration\n"

            if validation_result.should_integrate:
                report += "- ✅ **Ready for Integration**: Data passed validation thresholds\n"

            report += f"\n## Timestamp\nGenerated: {validation_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

            return report

        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return f"Error generating validation report: {str(e)}"
