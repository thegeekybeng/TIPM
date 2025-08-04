"""
Enhanced TIPM Core with Real Data Integration
===========================================

This module extends the TIPM core model to work with real-world datasets
from authoritative sources like UN Comtrade, World Bank, OECD, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
from dataclasses import dataclass

from .core import TIPMModel, TariffShock, TIPMPrediction
from .config.settings import TIPMConfig
from .data_connectors import DataIntegrationManager

logger = logging.getLogger(__name__)


@dataclass
class RealDataConfig:
    """Configuration for real data integration"""

    data_cache_dir: str = "real_data_cache"
    max_cache_age_hours: int = 24
    fallback_to_synthetic: bool = True
    min_data_points: int = 10

    # Data source preferences
    primary_trade_source: str = "comtrade"  # comtrade, wits
    primary_economic_source: str = "worldbank"  # worldbank, oecd
    primary_sentiment_source: str = "gdelt"  # gdelt, news_api

    # Quality thresholds
    min_trade_coverage: float = 0.7  # Minimum trade flow coverage
    min_temporal_coverage: float = 0.8  # Minimum time series coverage
    max_missing_data_ratio: float = 0.3


class RealDataTIPMModel(TIPMModel):
    """
    Enhanced TIPM model that integrates real-world datasets
    """

    def __init__(
        self,
        config: Optional[TIPMConfig] = None,
        real_data_config: Optional[RealDataConfig] = None,
    ):
        super().__init__(config)

        self.real_data_config = real_data_config or RealDataConfig()
        self.data_manager = DataIntegrationManager(self.real_data_config.data_cache_dir)

        # Real data storage
        self.real_datasets = {}
        self.data_quality_metrics = {}
        self.last_data_update = None

        logger.info("Initialized RealDataTIPMModel with real data connectors")

    def load_real_data(
        self,
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
        force_refresh: bool = False,
    ) -> Dict[str, pd.DataFrame]:
        """
        Load real datasets for the specified parameters

        Args:
            countries: List of country codes (ISO3 or UN codes)
            hs_codes: List of HS product codes
            years: List of years to analyze
            force_refresh: Force refresh of cached data
        """

        logger.info(
            f"Loading real data for {len(countries)} countries, {len(hs_codes)} products, {len(years)} years"
        )

        # Check if we need to refresh data
        if (
            force_refresh
            or self.last_data_update is None
            or datetime.now() - self.last_data_update
            > timedelta(hours=self.real_data_config.max_cache_age_hours)
        ):

            logger.info("Fetching fresh data from external sources...")

            # Fetch comprehensive dataset
            raw_datasets = self.data_manager.fetch_comprehensive_dataset(
                countries=countries,
                hs_codes=hs_codes,
                years=years,
                tariff_query=f"tariff {' '.join(hs_codes)} trade",
            )

            # Process and validate data
            self.real_datasets = self._process_raw_datasets(
                raw_datasets, countries, hs_codes, years
            )
            self.data_quality_metrics = self._assess_data_quality(self.real_datasets)
            self.last_data_update = datetime.now()

            logger.info("Real data loading completed")

        return self.real_datasets

    def _process_raw_datasets(
        self,
        raw_datasets: Dict[str, pd.DataFrame],
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
    ) -> Dict[str, pd.DataFrame]:
        """Process raw datasets into TIPM-compatible format"""

        processed = {}

        # 1. Process trade flows
        if "trade_flows" in raw_datasets and not raw_datasets["trade_flows"].empty:
            processed["trade_flows"] = self._process_trade_flows(
                raw_datasets["trade_flows"], countries, hs_codes, years
            )

        # 2. Process tariff data
        if "tariff_rates" in raw_datasets and not raw_datasets["tariff_rates"].empty:
            processed["tariff_shocks"] = self._process_tariff_data(
                raw_datasets["tariff_rates"], countries, hs_codes, years
            )

        # 3. Process economic indicators
        if (
            "economic_indicators" in raw_datasets
            and not raw_datasets["economic_indicators"].empty
        ):
            processed.update(
                self._process_economic_indicators(
                    raw_datasets["economic_indicators"], countries, years
                )
            )

        # 4. Process sentiment data
        if (
            "news_sentiment" in raw_datasets
            and not raw_datasets["news_sentiment"].empty
        ):
            processed["geopolitical_events"] = self._process_sentiment_data(
                raw_datasets["news_sentiment"], countries, years
            )

        # 5. Process political events
        if (
            "political_events" in raw_datasets
            and not raw_datasets["political_events"].empty
        ):
            processed["political_stability"] = self._process_political_events(
                raw_datasets["political_events"], countries, years
            )

        return processed

    def _process_trade_flows(
        self,
        df: pd.DataFrame,
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
    ) -> pd.DataFrame:
        """Process UN Comtrade trade flow data"""

        if df.empty:
            return pd.DataFrame()

        try:
            # Standardize columns
            processed = df.copy()

            # Map column names to TIPM standard
            column_mapping = {
                "reporterCode": "origin_country",
                "partnerCode": "destination_country",
                "cmdCode": "hs_code",
                "period": "year",
                "primaryValue": "trade_value",
                "netWeight": "trade_volume",
                "tradeValue": "trade_value",
            }

            for old_col, new_col in column_mapping.items():
                if old_col in processed.columns:
                    processed[new_col] = processed[old_col]

            # Ensure required columns exist
            required_cols = [
                "origin_country",
                "destination_country",
                "hs_code",
                "year",
                "trade_value",
            ]
            for col in required_cols:
                if col not in processed.columns:
                    processed[col] = 0

            # Add derived columns
            processed["transport_cost"] = (
                processed["trade_value"] * 0.05
            )  # Estimate 5% transport cost
            processed["lead_time"] = 30  # Default 30 days lead time

            # Filter for requested parameters
            if "origin_country" in processed.columns and "hs_code" in processed.columns:
                processed = processed[
                    (
                        processed["origin_country"]
                        .astype(str)
                        .isin([str(c) for c in countries])
                    )
                    & (
                        processed["hs_code"]
                        .astype(str)
                        .isin([str(h) for h in hs_codes])
                    )
                    & (processed["year"].isin(years))
                ]

            # Clean and validate
            processed = processed.dropna(subset=["trade_value"])
            processed["trade_value"] = pd.to_numeric(
                processed["trade_value"], errors="coerce"
            ).fillna(0)

            logger.info(f"Processed {len(processed)} trade flow records")
            return processed[required_cols + ["transport_cost", "lead_time"]]

        except Exception as e:
            logger.error(f"Error processing trade flows: {e}")
            return pd.DataFrame()

    def _process_tariff_data(
        self,
        df: pd.DataFrame,
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
    ) -> pd.DataFrame:
        """Process tariff rate data from WITS"""

        if df.empty:
            return pd.DataFrame()

        try:
            processed = df.copy()

            # Create policy text from tariff data
            processed["policy_text"] = processed.apply(
                lambda row: f"Tariff rate of {row.get('tariff_rate', 0):.1%} imposed on imports from {row.get('country', 'unknown')} for product {row.get('product_code', 'unknown')}",
                axis=1,
            )

            # Standardize date format
            processed["effective_date"] = processed["year"].astype(str) + "-01-01"

            # Add required columns
            processed["hs_codes"] = processed.get("product_code", "").astype(str)
            processed["tariff_rates"] = processed.get("tariff_rate", 0.15)
            processed["countries"] = (
                processed.get("country", "") + ",US"
            )  # Assume bilateral with US

            required_cols = [
                "policy_text",
                "effective_date",
                "hs_codes",
                "tariff_rates",
                "countries",
            ]

            logger.info(f"Processed {len(processed)} tariff policy records")
            return processed[required_cols]

        except Exception as e:
            logger.error(f"Error processing tariff data: {e}")
            return pd.DataFrame()

    def _process_economic_indicators(
        self, df: pd.DataFrame, countries: List[str], years: List[int]
    ) -> Dict[str, pd.DataFrame]:
        """Process World Bank economic indicators"""

        if df.empty:
            return {}

        try:
            processed_datasets = {}

            # Group by indicator
            for indicator_code in df["indicator_code"].unique():
                indicator_data = df[df["indicator_code"] == indicator_code].copy()

                if indicator_code == "FP.CPI.TOTL":  # CPI data for consumer impact
                    consumer_data = []
                    for _, row in indicator_data.iterrows():
                        consumer_data.append(
                            {
                                "product_category": "general_goods",
                                "price_change": float(row.get("value", 0))
                                / 100,  # Convert to decimal
                                "country": row.get("countryiso3code", "unknown"),
                                "year": row.get("date", 2023),
                            }
                        )

                    if consumer_data:
                        processed_datasets["consumer_impacts"] = pd.DataFrame(
                            consumer_data
                        )

                elif indicator_code == "SL.UEM.TOTL.ZS":  # Unemployment for firm impact
                    firm_data = []
                    for _, row in indicator_data.iterrows():
                        unemployment_rate = float(row.get("value", 5)) / 100
                        firm_data.append(
                            {
                                "firm_id": f"aggregate_{row.get('countryiso3code', 'unknown')}",
                                "response_metric": unemployment_rate,
                                "country": row.get("countryiso3code", "unknown"),
                                "year": row.get("date", 2023),
                            }
                        )

                    if firm_data:
                        processed_datasets["firm_responses"] = pd.DataFrame(firm_data)

                elif indicator_code == "NY.GDP.MKTP.CD":  # GDP for industry response
                    industry_data = []
                    for _, row in indicator_data.iterrows():
                        gdp_growth = float(row.get("value", 0)) / 1e12  # Normalize
                        industry_data.append(
                            {
                                "industry_code": "aggregate",
                                "response_metric": gdp_growth,
                                "country": row.get("countryiso3code", "unknown"),
                                "year": row.get("date", 2023),
                            }
                        )

                    if industry_data:
                        processed_datasets["industry_responses"] = pd.DataFrame(
                            industry_data
                        )

            logger.info(
                f"Processed economic indicators into {len(processed_datasets)} datasets"
            )
            return processed_datasets

        except Exception as e:
            logger.error(f"Error processing economic indicators: {e}")
            return {}

    def _process_sentiment_data(
        self, df: pd.DataFrame, countries: List[str], years: List[int]
    ) -> pd.DataFrame:
        """Process GDELT news sentiment data"""

        if df.empty:
            return pd.DataFrame()

        try:
            processed = df.copy()

            # Aggregate sentiment by country and time period
            processed["date"] = pd.to_datetime(processed["date"], errors="coerce")
            processed["year"] = processed["date"].dt.year
            processed["month"] = processed["date"].dt.month

            # Calculate average sentiment
            sentiment_agg = (
                processed.groupby(["country", "year"])
                .agg(
                    {
                        "tone": "mean",
                        "social_image_shares": "sum",
                        "title": lambda x: " ".join(x[:5]),  # Combine first 5 titles
                    }
                )
                .reset_index()
            )

            # Convert to geopolitical events format
            geo_events = []
            for _, row in sentiment_agg.iterrows():
                geo_events.append(
                    {
                        "event_text": f"News coverage: {row['title'][:100]}...",
                        "sentiment": row["tone"] / 100,  # Normalize tone
                        "country": row["country"],
                        "year": row["year"],
                        "social_engagement": row["social_image_shares"],
                    }
                )

            result = pd.DataFrame(geo_events)
            logger.info(f"Processed {len(result)} geopolitical sentiment records")
            return result

        except Exception as e:
            logger.error(f"Error processing sentiment data: {e}")
            return pd.DataFrame()

    def _process_political_events(
        self, df: pd.DataFrame, countries: List[str], years: List[int]
    ) -> pd.DataFrame:
        """Process ACLED political events data"""

        if df.empty:
            return pd.DataFrame()

        try:
            processed = df.copy()

            # Count events by country and type
            if "event_date" in processed.columns:
                processed["event_date"] = pd.to_datetime(
                    processed["event_date"], errors="coerce"
                )
                processed["year"] = processed["event_date"].dt.year

            # Aggregate by country and year
            event_counts = (
                processed.groupby(["country", "year"])
                .agg({"event_type": "count", "fatalities": "sum"})
                .reset_index()
            )

            # Convert to stability indicators
            stability_data = []
            for _, row in event_counts.iterrows():
                # Higher events = lower stability
                stability_score = max(0, 1 - (row["event_type"] / 100))

                stability_data.append(
                    {
                        "country": row["country"],
                        "year": row["year"],
                        "political_stability": stability_score,
                        "protest_events": row["event_type"],
                        "fatalities": row.get("fatalities", 0),
                    }
                )

            result = pd.DataFrame(stability_data)
            logger.info(f"Processed {len(result)} political stability records")
            return result

        except Exception as e:
            logger.error(f"Error processing political events: {e}")
            return pd.DataFrame()

    def _assess_data_quality(self, datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Assess quality of loaded real datasets"""

        quality_metrics = {}

        for name, df in datasets.items():
            if df.empty:
                quality_metrics[name] = {
                    "quality_score": 0.0,
                    "record_count": 0,
                    "completeness": 0.0,
                    "issues": ["No data available"],
                }
                continue

            # Calculate completeness
            total_cells = df.shape[0] * df.shape[1]
            missing_cells = df.isnull().sum().sum()
            completeness = (
                (total_cells - missing_cells) / total_cells if total_cells > 0 else 0
            )

            # Assess temporal coverage
            temporal_coverage = 1.0
            if "year" in df.columns:
                expected_years = set(range(2020, 2025))  # Recent years
                actual_years = set(df["year"].unique())
                temporal_coverage = len(
                    actual_years.intersection(expected_years)
                ) / len(expected_years)

            # Calculate overall quality score
            quality_score = (completeness + temporal_coverage) / 2

            # Identify issues
            issues = []
            if completeness < 0.8:
                issues.append(f"High missing data rate: {(1-completeness)*100:.1f}%")
            if temporal_coverage < 0.5:
                issues.append(f"Poor temporal coverage: {temporal_coverage*100:.1f}%")
            if len(df) < self.real_data_config.min_data_points:
                issues.append(f"Insufficient data points: {len(df)}")

            quality_metrics[name] = {
                "quality_score": quality_score,
                "record_count": len(df),
                "completeness": completeness,
                "temporal_coverage": temporal_coverage,
                "issues": issues,
            }

        return quality_metrics

    def fit_with_real_data(
        self,
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
        force_refresh: bool = False,
    ) -> "RealDataTIPMModel":
        """
        Train TIPM model using real datasets

        Args:
            countries: Country codes to analyze
            hs_codes: Product codes to analyze
            years: Years of data to use for training
            force_refresh: Force refresh of cached data
        """

        logger.info("Training TIPM with real datasets...")

        # Load real data
        real_datasets = self.load_real_data(countries, hs_codes, years, force_refresh)

        # Check data quality and decide whether to use real data or fall back
        training_data = {}

        for layer_name, dataset_name in [
            ("tariff_shocks", "tariff_shocks"),
            ("trade_flows", "trade_flows"),
            ("industry_responses", "industry_responses"),
            ("firm_responses", "firm_responses"),
            ("consumer_impacts", "consumer_impacts"),
            ("geopolitical_events", "geopolitical_events"),
        ]:

            if (
                dataset_name in real_datasets
                and not real_datasets[dataset_name].empty
                and self.data_quality_metrics.get(dataset_name, {}).get(
                    "quality_score", 0
                )
                > 0.3
            ):

                # Use real data
                training_data[layer_name] = real_datasets[dataset_name]
                logger.info(
                    f"Using real data for {layer_name}: {len(real_datasets[dataset_name])} records"
                )

            elif self.real_data_config.fallback_to_synthetic:
                # Fall back to synthetic data
                training_data[layer_name] = self._generate_fallback_data(
                    layer_name, countries, hs_codes, years
                )
                logger.info(f"Using synthetic fallback for {layer_name}")

            else:
                # No data available
                training_data[layer_name] = pd.DataFrame()
                logger.warning(f"No data available for {layer_name}")

        # Train the model
        self.fit(training_data)

        # Store metadata
        self.model_metadata.update(
            {
                "data_sources": list(real_datasets.keys()),
                "data_quality": self.data_quality_metrics,
                "training_countries": countries,
                "training_hs_codes": hs_codes,
                "training_years": years,
                "last_trained": datetime.now().isoformat(),
            }
        )

        logger.info("Real data training completed")
        return self

    def _generate_fallback_data(
        self,
        layer_name: str,
        countries: List[str],
        hs_codes: List[str],
        years: List[int],
    ) -> pd.DataFrame:
        """Generate synthetic fallback data when real data is unavailable"""

        np.random.seed(42)  # Reproducible synthetic data

        if layer_name == "tariff_shocks":
            return pd.DataFrame(
                {
                    "policy_text": [f"Fallback tariff policy for {hs_codes[0]}"]
                    * len(countries),
                    "effective_date": ["2023-01-01"] * len(countries),
                    "hs_codes": [",".join(hs_codes)] * len(countries),
                    "tariff_rates": np.random.uniform(0.1, 0.3, len(countries)),
                    "countries": [f"{c},US" for c in countries],
                }
            )

        elif layer_name == "trade_flows":
            n_records = len(countries) * len(hs_codes) * len(years)
            return pd.DataFrame(
                {
                    "hs_code": np.tile(hs_codes, len(countries) * len(years)),
                    "origin_country": np.repeat(countries, len(hs_codes) * len(years)),
                    "destination_country": ["US"] * n_records,
                    "trade_value": np.random.lognormal(
                        15, 1, n_records
                    ),  # Realistic trade values
                    "year": np.tile(np.repeat(years, len(hs_codes)), len(countries)),
                    "transport_cost": np.random.uniform(10000, 100000, n_records),
                    "lead_time": np.random.uniform(20, 60, n_records),
                }
            )

        elif layer_name == "industry_responses":
            return pd.DataFrame(
                {
                    "industry_code": ["electronics", "manufacturing", "services"],
                    "response_metric": np.random.normal(0.1, 0.05, 3),
                }
            )

        elif layer_name == "firm_responses":
            return pd.DataFrame(
                {
                    "firm_id": [f"firm_{i}" for i in range(5)],
                    "response_metric": np.random.normal(0.1, 0.05, 5),
                }
            )

        elif layer_name == "consumer_impacts":
            return pd.DataFrame(
                {
                    "product_category": ["electronics", "general_goods"],
                    "price_change": np.random.uniform(0.02, 0.08, 2),
                }
            )

        elif layer_name == "geopolitical_events":
            return pd.DataFrame(
                {"event_text": ["Fallback geopolitical event"], "sentiment": [0.0]}
            )

        return pd.DataFrame()

    def get_data_provenance(self) -> Dict[str, Any]:
        """Get information about data sources and quality"""

        return {
            "last_update": (
                self.last_data_update.isoformat() if self.last_data_update else None
            ),
            "datasets_available": list(self.real_datasets.keys()),
            "data_quality_metrics": self.data_quality_metrics,
            "model_metadata": self.model_metadata,
            "configuration": {
                "cache_directory": self.real_data_config.data_cache_dir,
                "fallback_enabled": self.real_data_config.fallback_to_synthetic,
                "quality_thresholds": {
                    "min_data_points": self.real_data_config.min_data_points,
                    "min_trade_coverage": self.real_data_config.min_trade_coverage,
                    "max_missing_data_ratio": self.real_data_config.max_missing_data_ratio,
                },
            },
        }


# Usage example
if __name__ == "__main__":
    # Test real data integration
    real_model = RealDataTIPMModel()

    # Train with real data for US-China electronics trade
    real_model.fit_with_real_data(
        countries=["840", "156"],  # US, China
        hs_codes=["8517", "8471"],  # Telecom, computers
        years=[2022, 2023, 2024],
    )

    # Get data provenance
    provenance = real_model.get_data_provenance()
    print("Data Provenance:")
    print(json.dumps(provenance, indent=2))
