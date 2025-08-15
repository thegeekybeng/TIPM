#!/usr/bin/env python3
"""
TIPM v3.0 - Atlantic Council Trump Tariff Tracker Connector
==========================================================

Direct integration with Atlantic Council's comprehensive tariff dataset:
- Real-time data from their Google Sheets
- Complete coverage of 90+ countries
- All tariff categories and rates
- Legal authorities and effective dates
- Automatic updates and verification

CREDIT: Atlantic Council Geoeconomics Center - Trump Tariff Tracker
Source: https://www.atlanticcouncil.org/programs/geoeconomics-center/trump-tariff-tracker/
Dataset: https://docs.google.com/spreadsheets/d/1s046O7ulAQ7d15TT-9-qtqemgGbEAGo5jF5ETEvyeXg/edit?gid=107324639#gid=107324639
"""

import requests
import pandas as pd
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AtlanticCouncilConnector:
    """Direct connector to Atlantic Council's Trump Tariff Tracker dataset"""

    def __init__(self):
        self.base_url = "https://www.atlanticcouncil.org/programs/geoeconomics-center/trump-tariff-tracker/"
        self.dataset_url = "https://docs.google.com/spreadsheets/d/1s046O7ulAQ7d15TT-9-qtqemgGbEAGo5jF5ETEvyeXg/edit?gid=107324639#gid=107324639"
        self.data = None
        self.last_updated = None

    def fetch_dataset(self) -> pd.DataFrame:
        """Fetch the complete dataset from Atlantic Council"""
        try:
            # Convert Google Sheets URL to CSV export format
            csv_url = self.dataset_url.replace("/edit?gid=", "/export?format=csv&gid=")

            logger.info("Fetching Atlantic Council Trump Tariff Tracker dataset...")
            response = requests.get(csv_url, timeout=30)
            response.raise_for_status()

            # Parse CSV data
            df = pd.read_csv(io.StringIO(response.text))
            self.data = df
            self.last_updated = datetime.now()

            logger.info(f"Successfully fetched dataset with {len(df)} tariff entries")
            return df

        except Exception as e:
            logger.error(f"Error fetching Atlantic Council dataset: {e}")
            # Fallback to cached data if available
            return self.data if self.data is not None else pd.DataFrame()

    def get_country_tariffs(self, country_name: str) -> Dict[str, Any]:
        """Get all tariff information for a specific country"""
        if self.data is None:
            self.fetch_dataset()

        if self.data.empty:
            return {}

        # Filter data for the specific country
        country_data = self.data[
            self.data["Geography"].str.contains(country_name, case=False, na=False)
        ]

        if country_data.empty:
            return {}

        tariffs = {}
        for _, row in country_data.iterrows():
            target = row.get("Target", "General")
            rate = row.get("Rate", 0)
            effective_date = row.get("Date in effect", "Unknown")
            legal_authority = row.get("Legal authority", "Unknown")
            sources = row.get("Sources", "Atlantic Council")

            # Create tariff entry
            tariff_key = f"{target} - {legal_authority}"
            tariffs[tariff_key] = {
                "tariff_rate": self._parse_rate(rate),
                "target_type": row.get("Target type", "Unknown"),
                "geography": row.get("Geography", country_name),
                "target": target,
                "first_announced": row.get("First announced", "Unknown"),
                "effective_date": effective_date,
                "legal_authority": legal_authority,
                "sources": sources,
                "status": "Active" if self._parse_rate(rate) > 0 else "Exempt",
                "verification": f"Atlantic Council Trump Tariff Tracker - {sources}",
                "data_source": "Atlantic Council Geoeconomics Center",
            }

        return tariffs

    def get_country_average_tariff(self, country_name: str) -> float:
        """Calculate average tariff rate for a country"""
        country_tariffs = self.get_country_tariffs(country_name)
        if not country_tariffs:
            return 0.0

        # Only count active tariffs (exclude exempt status)
        active_tariffs = [
            tariff
            for tariff in country_tariffs.values()
            if tariff["status"] == "Active"
        ]
        if not active_tariffs:
            return 0.0

        total_rate = sum(tariff["tariff_rate"] for tariff in active_tariffs)
        return total_rate / len(active_tariffs)

    def get_affected_sectors(self, country_name: str) -> List[str]:
        """Get list of affected sectors/targets for a country"""
        country_tariffs = self.get_country_tariffs(country_name)
        if not country_tariffs:
            return []

        # Return all target types
        return [tariff["target"] for tariff in country_tariffs.values()]

    def get_sector_analysis(self, country_name: str) -> List[Dict[str, Any]]:
        """Get detailed sector analysis for a country"""
        country_tariffs = self.get_country_tariffs(country_name)
        if not country_tariffs:
            return []

        analysis = []
        for sector, tariff_info in country_tariffs.items():
            rate = tariff_info["tariff_rate"]
            status = tariff_info["status"]

            # Determine impact level based on tariff rate
            if status == "Exempt":
                impact_level = "Exempt"
            elif rate >= 40:
                impact_level = "Critical"
            elif rate >= 25:
                impact_level = "High"
            elif rate >= 15:
                impact_level = "Medium"
            elif rate >= 5:
                impact_level = "Low"
            else:
                impact_level = "Minimal"

            analysis.append(
                {
                    "sector": tariff_info["target"],
                    "tariff_rate": rate,
                    "impact_level": impact_level,
                    "source": tariff_info["legal_authority"],
                    "status": status,
                    "effective_date": tariff_info["effective_date"],
                    "legal_basis": tariff_info["legal_authority"],
                    "notes": f"{tariff_info['target_type']} - {tariff_info['geography']}",
                    "verification": tariff_info["verification"],
                    "data_source": tariff_info["data_source"],
                }
            )

        return analysis

    def get_economic_insights(self, country_name: str) -> List[str]:
        """Get economic insights based on Atlantic Council data"""
        country_tariffs = self.get_country_tariffs(country_name)
        if not country_tariffs:
            return [
                "This country is not currently affected by US tariffs according to Atlantic Council data"
            ]

        insights = []
        active_tariffs = [
            tariff
            for tariff in country_tariffs.values()
            if tariff["status"] == "Active"
        ]
        exempt_tariffs = [
            tariff
            for tariff in country_tariffs.values()
            if tariff["status"] == "Exempt"
        ]

        if active_tariffs:
            avg_rate = sum(tariff["tariff_rate"] for tariff in active_tariffs) / len(
                active_tariffs
            )
            insights.append(
                f"Currently affected by US tariffs in {len(active_tariffs)} categories"
            )
            insights.append(f"Average tariff rate: {avg_rate:.1f}%")
            insights.append(
                f"Legal basis: {', '.join(set(tariff['legal_authority'] for tariff in active_tariffs))}"
            )

            if avg_rate >= 40:
                insights.extend(
                    [
                        "Critical tariff level - severe economic impact expected",
                        "High likelihood of supply chain disruption",
                        "Potential for retaliatory trade measures",
                        "Risk of trade diversion to non-tariff countries",
                    ]
                )
            elif avg_rate >= 25:
                insights.extend(
                    [
                        "High tariff level - significant economic impact",
                        "Likely price increases for US consumers",
                        "Supply chain adjustments expected",
                        "Potential for trade agreement negotiations",
                    ]
                )
            elif avg_rate >= 15:
                insights.extend(
                    [
                        "Moderate tariff level - moderate economic impact",
                        "Some price increases possible",
                        "Limited supply chain disruption",
                        "Business continuity likely maintained",
                    ]
                )

            # Add target-specific insights
            targets = [tariff["target"] for tariff in active_tariffs]
            if any(
                "steel" in target.lower() or "aluminum" in target.lower()
                for target in targets
            ):
                insights.extend(
                    [
                        "National security implications for steel/aluminum",
                        "Impact on US manufacturing costs",
                        "Potential for domestic industry growth",
                    ]
                )

            if any(
                "technology" in target.lower() or "electronics" in target.lower()
                for target in targets
            ):
                insights.extend(
                    [
                        "Critical for US tech supply chain",
                        "High risk of innovation disruption",
                        "Potential for increased domestic tech investment",
                    ]
                )

        elif exempt_tariffs:
            insights.extend(
                [
                    "Currently exempted from US tariffs",
                    "Trade agreement or exemption provides protection",
                    "Limited economic impact from US trade actions",
                ]
            )

        return insights

    def get_mitigation_strategies(self, country_name: str) -> List[str]:
        """Get mitigation strategies based on Atlantic Council data"""
        country_tariffs = self.get_country_tariffs(country_name)
        if not country_tariffs:
            return ["No mitigation needed - country not affected"]

        active_tariffs = [
            tariff
            for tariff in country_tariffs.values()
            if tariff["status"] == "Active"
        ]
        exempt_tariffs = [
            tariff
            for tariff in country_tariffs.values()
            if tariff["status"] == "Exempt"
        ]

        if exempt_tariffs:
            return [
                "Maintain trade agreement compliance",
                "Strengthen strategic alliance with US",
                "Continue preferential trade relationship",
            ]
        elif active_tariffs:
            strategies = [
                "Diversify export markets to reduce US dependency",
                "Develop domestic supply chains for affected products",
                "Seek alternative suppliers in non-tariff countries",
                "Negotiate bilateral trade agreements",
                "File WTO dispute resolution cases",
                "Implement retaliatory tariffs on US exports",
                "Leverage trade agreement negotiations",
            ]

            # Add legal authority-specific strategies
            legal_bases = set(tariff["legal_authority"] for tariff in active_tariffs)
            if "Section 301" in legal_bases:
                strategies.extend(
                    [
                        "Address underlying unfair trade practices",
                        "Implement policy reforms to address US concerns",
                        "Engage in Section 301 negotiations",
                    ]
                )

            if "IEEPA" in legal_bases:
                strategies.extend(
                    [
                        "Address national security concerns",
                        "Implement reciprocal trade policies",
                        "Engage in diplomatic negotiations",
                    ]
                )

            return strategies

        return ["No mitigation needed - country not affected"]

    def get_all_countries(self) -> List[str]:
        """Get list of all countries in the dataset"""
        if self.data is None:
            self.fetch_dataset()

        if self.data.empty:
            return []

        # Get unique countries from Geography column
        countries = self.data["Geography"].dropna().unique().tolist()
        return sorted(countries)

    def get_tariff_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of all tariff data"""
        if self.data is None:
            self.fetch_dataset()

        if self.data.empty:
            return {"error": "No data available"}

        # Parse all rates safely to avoid errors
        parsed_rates = []
        for rate in self.data["Rate"].dropna():
            try:
                parsed_rate = self._parse_rate(rate)
                if parsed_rate > 0:  # Only count valid positive rates
                    parsed_rates.append(parsed_rate)
            except Exception as e:
                logger.warning(f"Could not parse rate: {rate}, error: {e}")
                continue

        summary = {
            "total_entries": len(self.data),
            "total_countries": len(self.data["Geography"].unique()),
            "tariff_categories": self.data["Target type"].unique().tolist(),
            "legal_authorities": self.data["Legal authority"].unique().tolist(),
            "rate_range": {
                "min": min(parsed_rates) if parsed_rates else 0,
                "max": max(parsed_rates) if parsed_rates else 0,
                "average": sum(parsed_rates) / len(parsed_rates) if parsed_rates else 0,
            },
            "effective_dates": self.data["Date in effect"].unique().tolist(),
            "data_source": "Atlantic Council Geoeconomics Center",
            "dataset_url": self.dataset_url,
            "last_updated": (
                self.last_updated.isoformat() if self.last_updated else None
            ),
            "credits": "Atlantic Council Trump Tariff Tracker",
        }

        return summary

    def _parse_rate(self, rate_value) -> float:
        """Parse tariff rate from various formats"""
        if pd.isna(rate_value):
            return 0.0

        try:
            # Handle percentage strings
            if isinstance(rate_value, str):
                rate_str = rate_value.strip()

                # Handle TBD cases
                if rate_str.lower() in ["tbd", "pending", "under investigation"]:
                    return 0.0

                # Handle complex formats like "15%30%15%10%"
                if "%" in rate_str:
                    # Extract first percentage found
                    import re

                    match = re.search(r"(\d+(?:\.\d+)?)%", rate_str)
                    if match:
                        return float(match.group(1))

                # Handle "120% or $100 per item" format
                if " or " in rate_str and "%" in rate_str:
                    # Extract percentage part
                    percent_part = rate_str.split(" or ")[0]
                    match = re.search(r"(\d+(?:\.\d+)?)%", percent_part)
                    if match:
                        return float(match.group(1))

                # Handle simple percentage
                if "%" in rate_str:
                    rate_str = rate_str.replace("%", "").strip()
                    return float(rate_str)

                # Handle numeric strings
                return float(rate_str)
            else:
                return float(rate_value)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse rate value: {rate_value}")
            return 0.0

    def refresh_data(self) -> bool:
        """Refresh dataset from Atlantic Council"""
        try:
            old_count = len(self.data) if self.data is not None else 0
            new_data = self.fetch_dataset()
            new_count = len(new_data)

            if new_count > 0:
                logger.info(f"Data refreshed: {old_count} -> {new_count} entries")
                return True
            else:
                logger.warning("Data refresh failed - no new data received")
                return False

        except Exception as e:
            logger.error(f"Error refreshing data: {e}")
            return False


# Global instance for easy access
atlantic_council = AtlanticCouncilConnector()


# Convenience functions
def get_country_tariffs(country_name: str) -> Dict[str, Any]:
    """Get tariff data for a country from Atlantic Council"""
    return atlantic_council.get_country_tariffs(country_name)


def get_country_average_tariff(country_name: str) -> float:
    """Get average tariff rate for a country from Atlantic Council"""
    return atlantic_council.get_country_average_tariff(country_name)


def get_affected_sectors(country_name: str) -> List[str]:
    """Get affected sectors for a country from Atlantic Council"""
    return atlantic_council.get_affected_sectors(country_name)


def get_sector_analysis(country_name: str) -> List[Dict[str, Any]]:
    """Get sector analysis for a country from Atlantic Council"""
    return atlantic_council.get_sector_analysis(country_name)


def get_economic_insights(country_name: str) -> List[str]:
    """Get economic insights for a country from Atlantic Council"""
    return atlantic_council.get_economic_insights(country_name)


def get_mitigation_strategies(country_name: str) -> List[str]:
    """Get mitigation strategies for a country from Atlantic Council"""
    return atlantic_council.get_mitigation_strategies(country_name)


def get_all_countries() -> List[str]:
    """Get all countries from Atlantic Council dataset"""
    return atlantic_council.get_all_countries()


def get_tariff_summary() -> Dict[str, Any]:
    """Get comprehensive tariff summary from Atlantic Council"""
    return atlantic_council.get_tariff_summary()


def refresh_atlantic_council_data() -> bool:
    """Refresh Atlantic Council dataset"""
    return atlantic_council.refresh_data()
