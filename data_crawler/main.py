"""
Main Entry Point for TIPM Data Crawler
======================================

Command-line interface and main orchestration for the intelligent data crawler system.
"""

import asyncio
import logging
import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Import the main crawler
from .core import DataCrawlerRAG
from .models import DataSource, DataSourceType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data_crawler.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class DataCrawlerCLI:
    """Command-line interface for the data crawler"""

    def __init__(self):
        self.crawler = None

    async def initialize(self, config_path: str = None):
        """Initialize the data crawler"""
        try:
            logger.info("Initializing TIPM Data Crawler...")

            if config_path:
                config_path = Path(config_path)
            else:
                config_path = Path("data_crawler/config/sources.json")

            self.crawler = DataCrawlerRAG(config_path=str(config_path))
            logger.info("Data crawler initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize data crawler: {e}")
            raise

    async def run_crawl_cycle(self):
        """Run a complete crawl cycle"""
        try:
            logger.info("Starting crawl cycle...")
            results = await self.crawler.run_full_crawl_cycle()

            # Print results
            print("\n" + "=" * 60)
            print("CRAWL CYCLE RESULTS")
            print("=" * 60)
            print(f"Start Time: {results['start_time']}")
            print(f"End Time: {results['end_time']}")
            print(f"Duration: {results['duration']:.2f} seconds")
            print(f"Total Sources: {results['total_sources']}")
            print(f"Active Sources: {results['active_sources']}")
            print(f"Successful Crawls: {results['successful_crawls']}")
            print(f"Failed Crawls: {results['failed_crawls']}")
            print(f"Validations Passed: {results['validations_passed']}")
            print(f"Validations Failed: {results['validations_failed']}")
            print(f"Sources to Integrate: {results['sources_to_integrate']}")

            if results["errors"]:
                print(f"\nErrors: {len(results['errors'])}")
                for error in results["errors"]:
                    print(f"  - {error}")

            print("=" * 60)

            return results

        except Exception as e:
            logger.error(f"Crawl cycle failed: {e}")
            raise

    async def crawl_single_source(self, source_id: str):
        """Crawl a single data source"""
        try:
            logger.info(f"Crawling single source: {source_id}")

            # Crawl the source
            crawl_result = await self.crawler.crawl_data_source(source_id)

            if crawl_result.success:
                print(f"\n✅ Successfully crawled {source_id}")
                print(f"Records: {crawl_result.records_count}")
                print(f"Fields: {crawl_result.fields_count}")
                print(f"Duration: {crawl_result.crawl_duration:.2f}s")

                # Validate the result
                validation_result = await self.crawler.validate_crawl_result(
                    crawl_result
                )

                print(f"\n📊 Validation Results:")
                print(f"Status: {validation_result.overall_status.value}")
                print(f"Overall Score: {validation_result.get_overall_score():.1%}")
                print(
                    f"Should Integrate: {'Yes' if validation_result.should_integrate else 'No'}"
                )

            else:
                print(f"\n❌ Failed to crawl {source_id}")
                print(f"Error: {crawl_result.error_message}")

            return crawl_result

        except Exception as e:
            logger.error(f"Single source crawl failed: {e}")
            raise

    async def discover_sources(self, query: str = None):
        """Discover new data sources"""
        try:
            logger.info("Discovering new data sources...")

            discovered_sources = await self.crawler.discover_new_sources(query)

            if discovered_sources:
                print(
                    f"\n🔍 Discovered {len(discovered_sources)} new potential sources:"
                )
                for source in discovered_sources:
                    print(f"\n  📍 {source.name} ({source.id})")
                    print(f"     Description: {source.description}")
                    print(f"     Type: {source.source_type.value}")
                    print(f"     URL: {source.url}")
                    print(f"     Categories: {', '.join(source.categories)}")
                    print(f"     Update Frequency: {source.update_frequency}")
            else:
                print("\n🔍 No new sources discovered")

            return discovered_sources

        except Exception as e:
            logger.error(f"Source discovery failed: {e}")
            raise

    def show_status(self):
        """Show current crawler status"""
        try:
            status = self.crawler.get_crawl_status()

            print("\n" + "=" * 60)
            print("CRAWLER STATUS")
            print("=" * 60)
            print(f"Total Sources: {status['total_sources']}")
            print(f"Active Sources: {status['active_sources']}")
            print(f"Verified Sources: {status['verified_sources']}")
            print(f"Sources Needing Update: {status['sources_needing_update']}")
            print(f"Overall Health: {status['overall_health'].upper()}")

            if status["recent_crawls"]:
                print(f"\n📊 Recent Crawls:")
                for source_id, crawl_info in status["recent_crawls"].items():
                    print(
                        f"  {source_id}: {crawl_info['last_crawl']} - {'✅' if crawl_info['success'] else '❌'} - {crawl_info['records']} records"
                    )

            if status["recent_validations"]:
                print(f"\n🔍 Recent Validations:")
                for source_id, validation_info in status["recent_validations"].items():
                    print(
                        f"  {source_id}: {validation_info['last_validation']} - {validation_info['status']} - {validation_info['score']:.1%}"
                    )

            print("=" * 60)

        except Exception as e:
            logger.error(f"Status display failed: {e}")
            raise

    def list_sources(self):
        """List all configured data sources"""
        try:
            sources = self.crawler.data_sources

            print("\n" + "=" * 80)
            print("CONFIGURED DATA SOURCES")
            print("=" * 80)

            for source in sources:
                print(f"\n📊 {source.name} ({source.id})")
                print(f"   Description: {source.description}")
                print(f"   Type: {source.source_type.value}")
                print(f"   URL: {source.url}")
                print(f"   Categories: {', '.join(source.categories)}")
                print(
                    f"   Countries: {', '.join(source.country_coverage) if source.country_coverage != ['all'] else 'All'}"
                )
                print(f"   Update Frequency: {source.update_frequency}")
                print(
                    f"   Last Updated: {source.last_updated.strftime('%Y-%m-%d %H:%M:%S') if source.last_updated else 'Never'}"
                )
                print(
                    f"   Next Update: {source.next_update.strftime('%Y-%m-%d %H:%M:%S') if source.next_update else 'Unknown'}"
                )
                print(
                    f"   Status: {'🟢 Active' if source.is_active else '🔴 Inactive'}"
                )
                print(f"   Verified: {'✅ Yes' if source.is_verified else '❌ No'}")
                print(f"   Reliability: {source.reliability_score:.1%}")
                print(f"   Error Count: {source.error_count}")

                if source.last_error:
                    print(f"   Last Error: {source.last_error}")

            print("=" * 80)

        except Exception as e:
            logger.error(f"Source listing failed: {e}")
            raise

    async def add_source(self, source_config: dict):
        """Add a new data source"""
        try:
            logger.info("Adding new data source...")

            # Create source object
            source = DataSource(
                id=source_config["id"],
                name=source_config["name"],
                description=source_config["description"],
                source_type=DataSourceType(source_config["source_type"]),
                url=source_config["url"],
                tags=source_config.get("tags", []),
                categories=source_config.get("categories", []),
                country_coverage=source_config.get("country_coverage", ["all"]),
                time_coverage=source_config.get("time_coverage"),
                update_frequency=source_config.get("update_frequency", "daily"),
            )

            self.crawler.add_data_source(source)
            print(f"✅ Added new data source: {source.name}")

        except Exception as e:
            logger.error(f"Failed to add source: {e}")
            raise

    def save_config(self):
        """Save current configuration"""
        try:
            self.crawler.save_configuration()
            print("✅ Configuration saved successfully")

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TIPM Data Crawler - Intelligent data source discovery and validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full crawl cycle
  python -m data_crawler.main --cycle
  
  # Crawl specific source
  python -m data_crawler.main --crawl world_bank_gdp
  
  # Discover new sources
  python -m data_crawler.main --discover "tariff data"
  
  # Show status
  python -m data_crawler.main --status
  
  # List all sources
  python -m data_crawler.main --list-sources
        """,
    )

    parser.add_argument(
        "--cycle",
        action="store_true",
        help="Run a complete crawl cycle for all active sources",
    )

    parser.add_argument(
        "--crawl", metavar="SOURCE_ID", help="Crawl a specific data source by ID"
    )

    parser.add_argument(
        "--discover",
        metavar="QUERY",
        help="Discover new data sources using natural language query",
    )

    parser.add_argument(
        "--status", action="store_true", help="Show current crawler status"
    )

    parser.add_argument(
        "--list-sources", action="store_true", help="List all configured data sources"
    )

    parser.add_argument(
        "--add-source",
        metavar="CONFIG_FILE",
        help="Add a new data source from JSON configuration file",
    )

    parser.add_argument(
        "--save-config", action="store_true", help="Save current configuration to file"
    )

    parser.add_argument(
        "--config",
        metavar="PATH",
        default="data_crawler/config/sources.json",
        help="Path to configuration file (default: data_crawler/config/sources.json)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize CLI
    cli = DataCrawlerCLI()

    try:
        # Initialize crawler
        await cli.initialize(args.config)

        # Execute requested action
        if args.cycle:
            await cli.run_crawl_cycle()

        elif args.crawl:
            await cli.crawl_single_source(args.crawl)

        elif args.discover:
            await cli.discover_sources(args.discover)

        elif args.status:
            cli.show_status()

        elif args.list_sources:
            cli.list_sources()

        elif args.add_source:
            with open(args.add_source, "r") as f:
                source_config = json.load(f)
            await cli.add_source(source_config)

        elif args.save_config:
            cli.save_config()

        else:
            # No action specified, show help
            parser.print_help()
            print("\n💡 Use --help for more information")

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
