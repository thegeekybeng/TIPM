"""
Specialized Data Crawlers for TIPM
==================================

Crawlers for different types of data sources including APIs, web scraping, and databases.
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json
import time
import hashlib

# Data models
from .models import DataSource, DataSourceType

logger = logging.getLogger(__name__)


class BaseCrawler:
    """Base class for all data crawlers"""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_delay = 1.0  # seconds between requests
        self.max_retries = 3
        self.timeout = 30  # seconds

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def crawl(self, source: DataSource) -> Any:
        """
        Crawl a data source

        Args:
            source: Data source configuration

        Returns:
            Raw data from the source
        """
        raise NotImplementedError("Subclasses must implement crawl method")

    async def _make_request(
        self, url: str, headers: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with rate limiting and retries"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")

        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                if attempt > 0:
                    await asyncio.sleep(self.rate_limit_delay * attempt)

                async with self.session.get(
                    url, headers=headers, params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully fetched data from {url}")
                        return data
                    elif response.status == 429:  # Rate limited
                        retry_after = int(response.headers.get("Retry-After", 60))
                        logger.warning(f"Rate limited, waiting {retry_after} seconds")
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        logger.error(f"HTTP {response.status} from {url}")
                        response.raise_for_status()

            except aiohttp.ClientError as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
                continue
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
                continue

        raise RuntimeError(
            f"Failed to fetch data from {url} after {self.max_retries} attempts"
        )

    def _validate_response(self, data: Any, expected_fields: List[str]) -> bool:
        """Validate response data structure"""
        if not isinstance(data, dict):
            return False

        return all(field in data for field in expected_fields)


class WorldBankCrawler(BaseCrawler):
    """Crawler for World Bank data APIs"""

    def __init__(self):
        super().__init__()
        self.base_url = "https://api.worldbank.org/v2"
        self.rate_limit_delay = 2.0  # World Bank has stricter rate limits

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Crawl World Bank data"""
        try:
            # Extract country codes from source configuration
            countries = (
                source.country_coverage
                if source.country_coverage != ["all"]
                else ["US", "CN", "DE", "JP", "GB"]
            )

            # Define indicators to fetch
            indicators = {
                "NY.GDP.MKTP.CD": "GDP (current US$)",
                "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
                "NE.TRD.GNFS.ZS": "Trade (% of GDP)",
                "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
            }

            all_data = {}

            for country_code in countries[:5]:  # Limit to 5 countries for demo
                country_data = {}

                for indicator_code, indicator_name in indicators.items():
                    try:
                        url = f"{self.base_url}/country/{country_code}/indicator/{indicator_code}"
                        params = {
                            "format": "json",
                            "per_page": 10,  # Last 10 years
                            "date": f"{datetime.now().year - 10}:{datetime.now().year}",
                        }

                        data = await self._make_request(url, params=params)

                        if self._validate_response(data, ["data"]):
                            country_data[indicator_code] = {
                                "name": indicator_name,
                                "values": data["data"],
                            }

                        # Rate limiting
                        await asyncio.sleep(self.rate_limit_delay)

                    except Exception as e:
                        logger.error(
                            f"Failed to fetch indicator {indicator_code} for {country_code}: {e}"
                        )
                        continue

                all_data[country_code] = country_data

            # Structure the response
            result = {
                "source": "world_bank",
                "timestamp": datetime.now().isoformat(),
                "countries": list(all_data.keys()),
                "indicators": list(indicators.keys()),
                "data": all_data,
                "record_count": sum(
                    len(country_data) for country_data in all_data.values()
                ),
                "field_count": len(indicators),
                "time_period": f"{datetime.now().year - 10}-{datetime.now().year}",
            }

            logger.info(
                f"Successfully crawled World Bank data for {len(all_data)} countries"
            )
            return result

        except Exception as e:
            logger.error(f"World Bank crawl failed: {e}")
            raise

    def _validate_response(self, data: Any, expected_fields: List[str]) -> bool:
        """Validate World Bank API response"""
        if not isinstance(data, list) or len(data) < 2:
            return False

        # World Bank API returns [metadata, data]
        metadata, actual_data = data[0], data[1]

        if not isinstance(metadata, dict) or not isinstance(actual_data, list):
            return False

        return True


class USCensusCrawler(BaseCrawler):
    """Crawler for US Census Bureau data APIs"""

    def __init__(self):
        super().__init__()
        self.base_url = "https://api.census.gov/data"
        self.rate_limit_delay = 1.5  # Census API rate limits

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Crawl US Census trade data"""
        try:
            # Define trade-related variables
            variables = [
                "I_COMMODITY",  # Commodity code
                "I_COUNTRY",  # Country code
                "I_MODE",  # Mode of transportation
                "I_PORT",  # Port of entry/exit
                "I_VAL_FAS",  # Value of shipments
                "I_QTY1",  # Quantity 1
                "I_QTY2",  # Quantity 2
            ]

            # Get recent trade data
            current_year = datetime.now().year
            current_month = datetime.now().month

            # Adjust for data availability (Census data has lag)
            if current_month <= 2:
                data_year = current_year - 1
                data_month = 12
            else:
                data_year = current_year
                data_month = current_month - 2

            url = f"{self.base_url}/timeseries/intltrade/imports"
            params = {
                "get": ",".join(variables),
                "for": "I_PORT:*",
                "time": f"{data_year}-{data_month:02d}",
                "I_COMMODITY": "000000",  # All commodities
                "I_MODE": "1,2,3,4,5",  # All modes
            }

            data = await self._make_request(url, params=params)

            if not self._validate_response(data, []):
                raise ValueError("Invalid response format from Census API")

            # Process the data
            if len(data) > 1:  # First row is headers
                headers = data[0]
                records = data[1:]

                processed_data = []
                for record in records[:100]:  # Limit to 100 records for demo
                    record_dict = dict(zip(headers, record))
                    processed_data.append(record_dict)

                # Aggregate by country
                country_totals = {}
                for record in processed_data:
                    country = record.get("I_COUNTRY", "Unknown")
                    value = float(record.get("I_VAL_FAS", 0))

                    if country not in country_totals:
                        country_totals[country] = 0
                    country_totals[country] += value

                result = {
                    "source": "us_census",
                    "timestamp": datetime.now().isoformat(),
                    "data_year": data_year,
                    "data_month": data_month,
                    "countries": list(country_totals.keys()),
                    "data": processed_data,
                    "country_totals": country_totals,
                    "record_count": len(processed_data),
                    "field_count": len(headers),
                    "time_period": f"{data_year}-{data_month:02d}",
                }

                logger.info(
                    f"Successfully crawled US Census data: {len(processed_data)} records"
                )
                return result
            else:
                raise ValueError("No data returned from Census API")

        except Exception as e:
            logger.error(f"US Census crawl failed: {e}")
            raise

    def _validate_response(self, data: Any, expected_fields: List[str]) -> bool:
        """Validate Census API response"""
        return isinstance(data, list) and len(data) > 0


class UNComtradeCrawler(BaseCrawler):
    """Crawler for UN Comtrade database"""

    def __init__(self):
        super().__init__()
        self.base_url = "https://comtrade.un.org/api/get"
        self.rate_limit_delay = 3.0  # UN API has strict rate limits

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Crawl UN Comtrade data"""
        try:
            # Get recent trade data for major countries
            current_year = datetime.now().year
            if current_year > 2023:  # UN Comtrade has data lag
                data_year = 2023
            else:
                data_year = current_year - 1

            # Major trading countries
            countries = [
                "840",
                "156",
                "276",
                "392",
                "826",
            ]  # US, China, Germany, Japan, UK

            all_data = {}

            for country_code in countries:
                try:
                    url = f"{self.base_url}/sdmx/json"
                    params = {
                        "r": country_code,  # Reporter country
                        "p": "0",  # Partner (0 = world)
                        "ps": data_year,  # Period
                        "px": "HS",  # Classification
                        "cc": "TOTAL",  # Commodity (TOTAL = all)
                        "freq": "A",  # Annual frequency
                        "fmt": "json",
                    }

                    data = await self._make_request(url, params=params)

                    if self._validate_response(data, ["dataset"]):
                        dataset = data["dataset"]
                        if "data" in dataset and dataset["data"]:
                            country_data = dataset["data"][0]  # First dataset

                            # Extract trade values
                            trade_data = {
                                "reporter": country_data.get("key", {})
                                .get("reporter", {})
                                .get("label", "Unknown"),
                                "year": data_year,
                                "imports": country_data.get("imports", {}).get(
                                    "value", 0
                                ),
                                "exports": country_data.get("exports", {}).get(
                                    "value", 0
                                ),
                            }

                            all_data[country_code] = trade_data

                    # Rate limiting
                    await asyncio.sleep(self.rate_limit_delay)

                except Exception as e:
                    logger.error(
                        f"Failed to fetch data for country {country_code}: {e}"
                    )
                    continue

            # Structure the response
            result = {
                "source": "un_comtrade",
                "timestamp": datetime.now().isoformat(),
                "data_year": data_year,
                "countries": list(all_data.keys()),
                "data": all_data,
                "record_count": len(all_data),
                "field_count": 4,  # reporter, year, imports, exports
                "time_period": str(data_year),
            }

            logger.info(
                f"Successfully crawled UN Comtrade data for {len(all_data)} countries"
            )
            return result

        except Exception as e:
            logger.error(f"UN Comtrade crawl failed: {e}")
            raise

    def _validate_response(self, data: Any, expected_fields: List[str]) -> bool:
        """Validate UN Comtrade API response"""
        return isinstance(data, dict) and "dataset" in data


class WebScrapingCrawler(BaseCrawler):
    """Generic web scraping crawler for non-API sources"""

    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 5.0  # Be respectful with web scraping

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Scrape web page content"""
        try:
            if not self.session:
                raise RuntimeError("Session not initialized")

            async with self.session.get(source.url) as response:
                if response.status == 200:
                    content = await response.text()

                    # Basic content analysis
                    result = {
                        "source": "web_scraping",
                        "timestamp": datetime.now().isoformat(),
                        "url": source.url,
                        "content_length": len(content),
                        "content_hash": hashlib.md5(content.encode()).hexdigest(),
                        "record_count": 1,
                        "field_count": 3,
                        "data_structure": "html_text",
                    }

                    logger.info(f"Successfully scraped {source.url}")
                    return result
                else:
                    raise aiohttp.ClientResponseError(
                        request_info=None, history=None, status=response.status
                    )

        except Exception as e:
            logger.error(f"Web scraping failed for {source.url}: {e}")
            raise


class DatabaseCrawler(BaseCrawler):
    """Crawler for database connections"""

    def __init__(self):
        super().__init__()
        self.connection = None

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Query database for data"""
        # This would implement database-specific crawling logic
        # For now, return a placeholder
        raise NotImplementedError("Database crawling not yet implemented")


class FileCrawler(BaseCrawler):
    """Crawler for file-based data sources"""

    def __init__(self):
        super().__init__()

    async def crawl(self, source: DataSource) -> Dict[str, Any]:
        """Read data from files"""
        # This would implement file reading logic
        # For now, return a placeholder
        raise NotImplementedError("File crawling not yet implemented")


# Factory function to get appropriate crawler
def get_crawler_for_source(source: DataSource) -> BaseCrawler:
    """Get the appropriate crawler for a data source"""
    if source.source_type == DataSourceType.API:
        if "world_bank" in source.tags or "gdp" in source.categories:
            return WorldBankCrawler()
        elif "census" in source.tags or "us" in source.categories:
            return USCensusCrawler()
        elif "un" in source.tags or "comtrade" in source.tags:
            return UNComtradeCrawler()
        else:
            return WorldBankCrawler()  # Default API crawler
    elif source.source_type == DataSourceType.WEB_SCRAPING:
        return WebScrapingCrawler()
    elif source.source_type == DataSourceType.DATABASE:
        return DatabaseCrawler()
    elif source.source_type == DataSourceType.FILE:
        return FileCrawler()
    else:
        raise ValueError(f"Unsupported source type: {source.source_type}")
