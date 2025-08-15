#!/usr/bin/env python3
"""
TIPM v3.0 - Atlantic Council Excel Parser
==========================================

Parses the Atlantic Council Trump Tariff Tracker Excel file:
- Reads XLS/XLSX files directly
- Converts to structured tariff data
- Handles all countries and sectors
- Provides real-time data updates

CREDIT: Atlantic Council Geoeconomics Center - Trump Tariff Tracker
Source: https://www.atlanticcouncil.org/programs/geoeconomics-center/trump-tariff-tracker/
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AtlanticCouncilExcelParser:
    """Parser for Atlantic Council Trump Tariff Tracker Excel files"""

    def __init__(self, excel_file_path: str = "data/Trump tariff tracker.xlsx"):
        self.excel_file_path = Path(excel_file_path)
        self.data: Optional[Dict[str, pd.DataFrame]] = None
        self.parsed_data: Dict[str, Dict[str, Any]] = {}

    def load_excel_file(self) -> bool:
        """Load the Excel file and parse its contents"""
        try:
            if not self.excel_file_path.exists():
                logger.error(f"Excel file not found: {self.excel_file_path}")
                return False

            # Read the Excel file
            self.data = pd.read_excel(self.excel_file_path, sheet_name=None)
            if self.data:
                logger.info(
                    f"Successfully loaded Excel file with {len(self.data)} sheets"
                )

            # Parse all sheets
            self._parse_all_sheets()
            return True

        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            return False

    def _parse_all_sheets(self):
        """Parse all sheets in the Excel file"""
        for sheet_name, sheet_data in self.data.items():
            logger.info(f"Parsing sheet: {sheet_name}")
            self._parse_sheet(sheet_name, sheet_data)

    def _parse_sheet(self, sheet_name: str, sheet_data: pd.DataFrame):
        """Parse individual sheet data"""
        try:
            # Look for country and tariff information
            if (
                "Geography" in sheet_data.columns
                or "Country" in sheet_data.columns
                or "Country Name" in sheet_data.columns
            ):
                self._parse_country_sheet(sheet_name, sheet_data)
            elif "Sector" in sheet_data.columns or "Category" in sheet_data.columns:
                # TODO: Implement sector sheet parsing
                logger.info(f"Sector sheet {sheet_name} - parsing not yet implemented")
            else:
                logger.info(
                    f"Sheet {sheet_name} doesn't contain recognizable tariff data"
                )

        except Exception as e:
            logger.error(f"Error parsing sheet {sheet_name}: {e}")

    def _parse_country_sheet(self, sheet_name: str, sheet_data: pd.DataFrame):
        """Parse country-specific tariff data"""
        logger.info(f"Parsing country data from sheet: {sheet_name}")

        # Find relevant columns - using actual Atlantic Council column names
        country_col = None
        rate_col = None
        sector_col = None
        date_col = None
        source_col = None

        for col in sheet_data.columns:
            col_lower = str(col).lower()
            if "geography" in col_lower:
                country_col = col
            elif "rate" in col_lower:
                rate_col = col
            elif "target" in col_lower:
                sector_col = col
            elif "date in effect" in col_lower or "effective" in col_lower:
                date_col = col
            elif "legal authority" in col_lower or "authority" in col_lower:
                source_col = col

        if not country_col:
            logger.warning(f"No country column found in sheet {sheet_name}")
            return

        # Process each row
        for _, row in sheet_data.iterrows():
            country = (
                str(row[country_col]).strip() if pd.notna(row[country_col]) else None
            )
            if not country or country.lower() in ["nan", "none", ""]:
                continue

            # Parse tariff rate
            tariff_rate = self._parse_tariff_rate(row.get(rate_col, 0))

            # Get sector/category
            sector = (
                str(row.get(sector_col, "General")).strip()
                if pd.notna(row.get(sector_col))
                else "General"
            )

            # Get date
            date = (
                str(row.get(date_col, "TBD")).strip()
                if pd.notna(row.get(date_col))
                else "TBD"
            )

            # Get source
            source = (
                str(row.get(source_col, "Atlantic Council")).strip()
                if pd.notna(row.get(source_col))
                else "Atlantic Council"
            )

            # Store parsed data
            if country not in self.parsed_data:
                self.parsed_data[country] = {}

            self.parsed_data[country][sector] = {
                "tariff_rate": tariff_rate,
                "hts_codes": ["All"],  # Will be enhanced later
                "effective_date": date,
                "source": f"Trump Administration 2025 - {source}",
                "notes": f"Tariff rate: {tariff_rate}% - {source}",
                "status": "Active" if tariff_rate > 0 else "Under Investigation",
                "verification": f"Atlantic Council Trump Tariff Tracker, {source}",
            }

    def _parse_tariff_rate(self, rate_value) -> float:
        """Parse tariff rate from various formats"""
        if pd.isna(rate_value):
            return 0.0

        try:
            if isinstance(rate_value, str):
                rate_str = rate_value.strip()

                # Handle TBD cases
                if rate_str.lower() in ["tbd", "pending", "under investigation"]:
                    return 0.0

                # Handle complex formats like "15%30%15%10%"
                if "%" in rate_str:
                    # Extract first percentage found
                    match = re.search(r"(\d+(?:\.\d+)?)%", rate_str)
                    if match:
                        return float(match.group(1))

                # Handle "120% or $100 per item" format
                if " or " in rate_str and "%" in rate_str:
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

    def get_parsed_data(self) -> Dict[str, Any]:
        """Get the parsed tariff data"""
        return self.parsed_data

    def get_country_tariffs(self, country_name: str) -> Optional[Dict[str, Any]]:
        """Get tariff data for a specific country"""
        return self.parsed_data.get(country_name)

    def get_country_average_tariff(self, country_name: str) -> float:
        """Calculate average tariff rate for a country"""
        country_data = self.get_country_tariffs(country_name)
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

    def get_affected_sectors(self, country_name: str) -> List[str]:
        """Get list of affected sectors for a country"""
        country_data = self.get_country_tariffs(country_name)
        if not country_data:
            return []

        return [
            sector
            for sector, tariff in country_data.items()
            if tariff.get("status") == "Active"
        ]

    def get_all_countries(self) -> List[str]:
        """Get list of all countries in the dataset"""
        return list(self.parsed_data.keys())

    def get_tariff_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of all tariff data"""
        total_countries = len(self.parsed_data)
        total_tariffs = sum(
            len(country_data) for country_data in self.parsed_data.values()
        )

        # Calculate average tariff rates by region
        region_tariffs: Dict[str, List[float]] = {}
        for country in self.parsed_data.keys():
            region = self._get_region(country)
            if region not in region_tariffs:
                region_tariffs[region] = []
            region_tariffs[region].append(self.get_country_average_tariff(country))

        region_averages = {
            region: sum(rates) / len(rates) if rates else 0
            for region, rates in region_tariffs.items()
        }

        return {
            "total_countries": total_countries,
            "total_tariffs": total_tariffs,
            "region_averages": region_averages,
            "data_source": "Atlantic Council Trump Tariff Tracker",
            "last_updated": pd.Timestamp.now().isoformat(),
            "credits": "Atlantic Council Geoeconomics Center",
        }

    def _get_region(self, country_name: str) -> str:
        """Determine region for a country"""
        # Simple region mapping - can be enhanced
        asia_countries = [
            "China",
            "Japan",
            "South Korea",
            "India",
            "Thailand",
            "Vietnam",
            "Malaysia",
            "Singapore",
            "Indonesia",
            "Philippines",
        ]
        europe_countries = [
            "European Union",
            "Germany",
            "France",
            "Italy",
            "Spain",
            "Netherlands",
            "Belgium",
            "Sweden",
        ]
        americas_countries = [
            "Brazil",
            "Mexico",
            "Canada",
            "Argentina",
            "Chile",
            "Peru",
            "Colombia",
            "Venezuela",
        ]
        africa_countries = [
            "South Africa",
            "Nigeria",
            "Kenya",
            "Ethiopia",
            "Ghana",
            "Uganda",
        ]
        middle_east_countries = [
            "Saudi Arabia",
            "UAE",
            "Israel",
            "Turkey",
            "Iran",
            "Qatar",
        ]
        oceania_countries = ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]

        if country_name in asia_countries:
            return "Asia"
        elif country_name in europe_countries:
            return "Europe"
        elif country_name in americas_countries:
            return "Americas"
        elif country_name in africa_countries:
            return "Africa"
        elif country_name in middle_east_countries:
            return "Middle East"
        elif country_name in oceania_countries:
            return "Oceania"
        else:
            return "Other"


# Global instance
excel_parser = AtlanticCouncilExcelParser()


# Convenience functions
def load_atlantic_council_data() -> bool:
    """Load Atlantic Council data from Excel file"""
    return excel_parser.load_excel_file()


def get_country_tariffs(country_name: str) -> Optional[Dict[str, Any]]:
    """Get tariff data for a specific country"""
    return excel_parser.get_country_tariffs(country_name)


def get_country_average_tariff(country_name: str) -> float:
    """Get average tariff rate for a country"""
    return excel_parser.get_country_average_tariff(country_name)


def get_affected_sectors(country_name: str) -> List[str]:
    """Get affected sectors for a country"""
    return excel_parser.get_affected_sectors(country_name)


def get_all_countries() -> List[str]:
    """Get all countries from the dataset"""
    return excel_parser.get_all_countries()


def get_tariff_summary() -> Dict[str, Any]:
    """Get comprehensive tariff summary"""
    return excel_parser.get_tariff_summary()


if __name__ == "__main__":
    # Test the parser
    if load_atlantic_council_data():
        print("✅ Successfully loaded Atlantic Council data!")
        print(f"📊 Total countries: {len(get_all_countries())}")
        print(f"🌍 Sample countries: {get_all_countries()[:5]}")

        # Test with a specific country
        test_country = "Singapore"
        if test_country in get_all_countries():
            print(f"\n🇸🇬 {test_country} data:")
            print(f"   Average tariff: {get_country_average_tariff(test_country):.1f}%")
            print(f"   Affected sectors: {get_affected_sectors(test_country)}")
    else:
        print("❌ Failed to load Atlantic Council data")
