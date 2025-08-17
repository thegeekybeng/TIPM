#!/usr/bin/env python3
"""
Comprehensive Data Source Testing Script
Tests all planned data sources for Trump 2025 Tariff Impact Model
"""

import requests
import json
import time
from typing import Dict, List, Tuple, Optional
import sys


class DataSourceTester:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "TIPM-Research/1.0 (Research Project)"}
        )

    def test_atlantic_council(self) -> Dict:
        """Test Atlantic Council Trump Tariff Tracker"""
        print("🔍 Testing Atlantic Council Trump Tariff Tracker...")

        try:
            url = "https://www.atlanticcouncil.org/programs/global-business-and-economics/trump-tariff-tracker/"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text.lower()

                # Check for key content indicators
                has_tariff_content = any(
                    term in content for term in ["tariff", "trade", "policy", "trump"]
                )
                has_data_tables = "table" in content or "data" in content
                has_anti_scraping = any(
                    term in content for term in ["cloudflare", "captcha", "blocked"]
                )

                return {
                    "status": "SUCCESS",
                    "accessible": True,
                    "has_tariff_content": has_tariff_content,
                    "has_data_tables": has_data_tables,
                    "has_anti_scraping": has_anti_scraping,
                    "content_length": len(response.text),
                    "confidence": (
                        "HIGH"
                        if has_tariff_content and not has_anti_scraping
                        else "MEDIUM"
                    ),
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_ustr(self) -> Dict:
        """Test USTR website accessibility"""
        print("🔍 Testing USTR website...")

        try:
            url = "https://ustr.gov/trade-agreements"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text.lower()

                has_trade_content = any(
                    term in content
                    for term in ["trade", "agreement", "tariff", "policy"]
                )
                has_documents = any(
                    term in content for term in ["pdf", "document", "report"]
                )

                return {
                    "status": "SUCCESS",
                    "accessible": True,
                    "has_trade_content": has_trade_content,
                    "has_documents": has_documents,
                    "content_length": len(response.text),
                    "confidence": "HIGH",
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_federal_register(self) -> Dict:
        """Test Federal Register API"""
        print("🔍 Testing Federal Register API...")

        try:
            url = "https://www.federalregister.gov/api/v1/documents.json"
            params = {
                "conditions": json.dumps([{"name": "search", "value": "tariff"}]),
                "per_page": 5,
            }

            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                has_results = "results" in data and len(data["results"]) > 0
                total_count = data.get("total_count", 0)

                return {
                    "status": "SUCCESS",
                    "accessible": True,
                    "has_results": has_results,
                    "total_count": total_count,
                    "response_size": len(response.text),
                    "confidence": "HIGH",
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_world_bank(self) -> Dict:
        """Test World Bank API"""
        print("🔍 Testing World Bank API...")

        try:
            url = "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD"
            params = {"format": "json", "per_page": 5}

            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                has_data = len(data) > 1 and len(data[1]) > 0
                data_points = len(data[1]) if has_data else 0

                return {
                    "status": "SUCCESS",
                    "accessible": True,
                    "has_data": has_data,
                    "data_points": data_points,
                    "response_size": len(response.text),
                    "confidence": "HIGH",
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_census_bureau(self) -> Dict:
        """Test US Census Bureau Foreign Trade API"""
        print("🔍 Testing US Census Bureau API...")

        try:
            url = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
            params = {"get": "CTY_SUBCODE,CNT_VAL_YR,GEN_QY1_YR", "time": "2023"}

            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.text

                has_data = len(data) > 100 and "CTY_SUBCODE" in data
                data_lines = len(data.split("\n"))

                return {
                    "status": "SUCCESS",
                    "accessible": True,
                    "has_data": has_data,
                    "data_lines": data_lines,
                    "response_size": len(response.text),
                    "confidence": "HIGH",
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_un_comtrade(self) -> Dict:
        """Test UN Comtrade API"""
        print("🔍 Testing UN Comtrade API...")

        try:
            # Test the basic API endpoint
            url = "https://comtrade.un.org/api/v1/reporter/842"
            params = {
                "freq": "A",
                "ps": "2023",
                "r": "842",
                "px": "HS",
                "cc": "0101",
                "fmt": "json",
            }

            response = self.session.get(url, params=params, timeout=15)

            if response.status_code == 200:
                try:
                    data = response.json()
                    has_data = "data" in data and len(data["data"]) > 0

                    return {
                        "status": "SUCCESS",
                        "accessible": True,
                        "has_data": has_data,
                        "response_size": len(response.text),
                        "confidence": "MEDIUM",
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "PARTIAL",
                        "accessible": True,
                        "has_data": False,
                        "response_size": len(response.text),
                        "confidence": "LOW",
                    }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def test_wits(self) -> Dict:
        """Test World Bank WITS API"""
        print("🔍 Testing World Bank WITS API...")

        try:
            # Test the WITS service endpoint
            url = "https://wits.worldbank.org/API/V1/wits/WITSApiService.svc"

            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text.lower()

                has_service = "service" in content
                has_api_info = any(
                    term in content for term in ["api", "service", "wits"]
                )

                return {
                    "status": "PARTIAL",
                    "accessible": True,
                    "has_service": has_service,
                    "has_api_info": has_api_info,
                    "response_size": len(response.text),
                    "confidence": "MEDIUM",
                    "note": "Service endpoint accessible but requires specific API calls",
                }
            else:
                return {
                    "status": "FAILED",
                    "accessible": False,
                    "status_code": response.status_code,
                    "confidence": "LOW",
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "accessible": False,
                "error": str(e),
                "confidence": "LOW",
            }

    def run_all_tests(self) -> Dict:
        """Run all data source tests"""
        print("🚀 Starting Comprehensive Data Source Testing...")
        print("=" * 60)

        tests = [
            ("atlantic_council", self.test_atlantic_council),
            ("ustr", self.test_ustr),
            ("federal_register", self.test_federal_register),
            ("world_bank", self.test_world_bank),
            ("census_bureau", self.test_census_bureau),
            ("un_comtrade", self.test_un_comtrade),
            ("wits", self.test_wits),
        ]

        for test_name, test_func in tests:
            try:
                result = test_func()
                self.results[test_name] = result

                # Add delay between tests to be respectful
                time.sleep(1)

            except Exception as e:
                self.results[test_name] = {
                    "status": "ERROR",
                    "accessible": False,
                    "error": str(e),
                    "confidence": "LOW",
                }

        return self.results

    def generate_report(self) -> str:
        """Generate comprehensive test report"""
        report = []
        report.append("📊 COMPREHENSIVE DATA SOURCE TEST REPORT")
        report.append("=" * 60)
        report.append("")

        # Summary statistics
        total_tests = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get("accessible", False))
        high_confidence = sum(
            1 for r in self.results.values() if r.get("confidence") == "HIGH"
        )
        medium_confidence = sum(
            1 for r in self.results.values() if r.get("confidence") == "MEDIUM"
        )
        low_confidence = sum(
            1 for r in self.results.values() if r.get("confidence") == "LOW"
        )

        report.append(f"📈 SUMMARY:")
        report.append(f"   Total Sources Tested: {total_tests}")
        report.append(f"   Accessible: {successful}/{total_tests}")
        report.append(f"   High Confidence: {high_confidence}")
        report.append(f"   Medium Confidence: {medium_confidence}")
        report.append(f"   Low Confidence: {low_confidence}")
        report.append("")

        # Detailed results
        for source_name, result in self.results.items():
            status_emoji = "✅" if result.get("accessible") else "❌"
            confidence_emoji = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}.get(
                result.get("confidence"), "⚪"
            )

            report.append(
                f"{status_emoji} {confidence_emoji} {source_name.upper().replace('_', ' ')}:"
            )
            report.append(f"   Status: {result.get('status', 'UNKNOWN')}")
            report.append(f"   Accessible: {result.get('accessible', False)}")
            report.append(f"   Confidence: {result.get('confidence', 'UNKNOWN')}")

            if "error" in result:
                report.append(f"   Error: {result['error']}")
            if "note" in result:
                report.append(f"   Note: {result['note']}")

            report.append("")

        # Recommendations
        report.append("🎯 RECOMMENDATIONS:")
        report.append("=" * 60)

        if high_confidence >= 4:
            report.append("✅ EXCELLENT: Most data sources are accessible and reliable")
            report.append("   → Proceed with full implementation")
        elif high_confidence >= 2:
            report.append("🟡 GOOD: Several reliable sources available")
            report.append("   → Implement with fallback strategies")
        else:
            report.append("🔴 CHALLENGING: Limited reliable data sources")
            report.append("   → Need alternative data strategies")

        report.append("")

        # Next steps
        report.append("🚀 NEXT STEPS:")
        report.append("=" * 60)

        working_sources = [
            name
            for name, result in self.results.items()
            if result.get("accessible")
            and result.get("confidence") in ["HIGH", "MEDIUM"]
        ]

        if working_sources:
            report.append("✅ RELIABLE SOURCES TO IMPLEMENT FIRST:")
            for source in working_sources:
                report.append(f"   - {source.replace('_', ' ').title()}")
            report.append("")

        problematic_sources = [
            name
            for name, result in self.results.items()
            if not result.get("accessible") or result.get("confidence") == "LOW"
        ]

        if problematic_sources:
            report.append("⚠️ SOURCES NEEDING ALTERNATIVE STRATEGIES:")
            for source in problematic_sources:
                report.append(f"   - {source.replace('_', ' ').title()}")
            report.append("")

        return "\n".join(report)


def main():
    """Main testing function"""
    print("🧪 TIPM Data Source Testing Suite")
    print("Testing all planned data sources for Trump 2025 Tariff Impact Model")
    print()

    tester = DataSourceTester()
    results = tester.run_all_tests()

    print("\n" + "=" * 60)
    print("📋 GENERATING COMPREHENSIVE REPORT...")
    print("=" * 60)

    report = tester.generate_report()
    print(report)

    # Save report to file
    with open("data_source_test_report.txt", "w") as f:
        f.write(report)

    print("\n" + "=" * 60)
    print("💾 Report saved to: data_source_test_report.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()
