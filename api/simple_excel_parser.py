#!/usr/bin/env python3
"""
TIPM v3.0 - Simple Atlantic Council Excel Parser
================================================

Simplified working version that directly parses the Excel file
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_atlantic_council_data() -> Dict[str, Dict[str, Any]]:
    """Load and parse Atlantic Council data directly"""
    excel_file = Path("data/Trump tariff tracker.xlsx")

    if not excel_file.exists():
        logger.error(f"Excel file not found: {excel_file}")
        return {}

    try:
        # Load the Excel file
        data = pd.read_excel(excel_file, sheet_name="All actions")
        logger.info(f"Successfully loaded Excel file with {len(data)} rows")

        # Parse the data
        parsed_data: Dict[str, Dict[str, Any]] = {}

        for _, row in data.iterrows():
            country = str(row["Geography"]).strip()
            if pd.isna(country) or country.lower() in ["nan", "none", ""]:
                continue

            # Parse tariff rate
            rate_value = row["Rate"]
            if pd.isna(rate_value):
                continue

            tariff_rate = parse_tariff_rate(rate_value)
            if tariff_rate == 0:
                continue  # Skip TBD or invalid rates

            # Get sector/category
            sector = (
                str(row["Target"]).strip() if pd.notna(row["Target"]) else "General"
            )

            # Get date
            date = (
                str(row["Date in effect"]).strip()
                if pd.notna(row["Date in effect"])
                else "TBD"
            )

            # Get source
            source = (
                str(row["Legal authority"]).strip()
                if pd.notna(row["Legal authority"])
                else "IEEPA"
            )

            # Store parsed data
            if country not in parsed_data:
                parsed_data[country] = {}

            parsed_data[country][sector] = {
                "tariff_rate": tariff_rate,
                "hts_codes": ["All"],
                "effective_date": date,
                "source": f"Trump Administration 2025 - {source}",
                "notes": f"Tariff rate: {tariff_rate}% - {source}",
                "status": "Active",
                "verification": f"Atlantic Council Trump Tariff Tracker, {source}",
            }

        logger.info(f"Successfully parsed data for {len(parsed_data)} countries")
        return parsed_data

    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        return {}


def parse_tariff_rate(rate_value) -> float:
    """Parse tariff rate from various formats"""
    if pd.isna(rate_value):
        return 0.0

    try:
        if isinstance(rate_value, str):
            rate_str = rate_value.strip()

            # Handle TBD cases
            if rate_str.lower() in ["tbd", "pending", "under investigation"]:
                return 0.0

            # Handle complex formats
            if "%" in rate_str:
                # Extract first percentage found
                import re

                match = re.search(r"(\d+(?:\.\d+)?)%", rate_str)
                if match:
                    return float(match.group(1))

            # Handle "120% or $100 per item" format
            if " or " in rate_str and "%" in rate_str:
                percent_part = rate_str.split(" or ")[0]
                import re

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
            # Handle numeric values (decimal format from Atlantic Council)
            numeric_rate = float(rate_value)
            # Convert decimal to percentage (0.15 -> 15.0)
            if numeric_rate <= 1.0:
                return numeric_rate * 100
            else:
                return numeric_rate

    except (ValueError, TypeError):
        logger.warning(f"Could not parse rate value: {rate_value}")
        return 0.0


# Global data storage
_parsed_data: Dict[str, Dict[str, Any]] = {}


def get_country_tariffs(country_name: str) -> Optional[Dict[str, Any]]:
    """Get tariff data for a specific country"""
    if not _parsed_data:
        _parsed_data.update(load_atlantic_council_data())
    return _parsed_data.get(country_name)


def get_country_average_tariff(country_name: str) -> float:
    """Calculate average tariff rate for a country"""
    country_data = get_country_tariffs(country_name)
    if not country_data:
        return 0.0

    active_tariffs = [
        tariff
        for tariff in country_data.values()
        if tariff.get("status") == "Active" and tariff.get("tariff_rate", 0) > 0
    ]

    if not active_tariffs:
        return 0.0

    return sum(tariff.get("tariff_rate", 0) for tariff in active_tariffs) / len(
        active_tariffs
    )


def get_affected_sectors(country_name: str) -> List[str]:
    """Get list of affected sectors for a country"""
    country_data = get_country_tariffs(country_name)
    if not country_data:
        return []

    return [
        sector
        for sector, tariff in country_data.items()
        if tariff.get("status") == "Active"
    ]


def get_all_countries() -> List[str]:
    """Get list of all countries from the dataset"""
    if not _parsed_data:
        _parsed_data.update(load_atlantic_council_data())
    return list(_parsed_data.keys())


def get_tariff_summary() -> Dict[str, Any]:
    """Get comprehensive tariff summary"""
    if not _parsed_data:
        _parsed_data.update(load_atlantic_council_data())

    total_countries = len(_parsed_data)
    total_tariffs = sum(len(country_data) for country_data in _parsed_data.values())

    return {
        "total_countries": total_countries,
        "total_tariffs": total_tariffs,
        "data_source": "Atlantic Council Trump Tariff Tracker",
        "last_updated": pd.Timestamp.now().isoformat(),
        "credits": "Atlantic Council Geoeconomics Center",
    }


if __name__ == "__main__":
    # Test the parser
    print("🧪 Testing Simple Excel Parser...")

    data = load_atlantic_council_data()
    print(f"✅ Loaded data for {len(data)} countries")

    if data:
        print(f"🌍 Sample countries: {list(data.keys())[:5]}")

        # Test with Afghanistan
        test_country = "Afghanistan"
        if test_country in data:
            print(f"\n🇦🇫 {test_country}:")
            print(f"   Average tariff: {get_country_average_tariff(test_country):.1f}%")
            print(f"   Affected sectors: {get_affected_sectors(test_country)}")
            print(f"   Raw data: {data[test_country]}")
    else:
        print("❌ No data loaded")
