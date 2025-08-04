"""
Enhanced TIPM Configuration for Global Multi-Sectoral Analysis
=============================================================

Supports 186 countries with sectoral tariff analysis using real Trump tariff data.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import json

# Comprehensive sectoral classification
GLOBAL_SECTORS = {
    "agriculture": {
        "name": "Agriculture & Food",
        "hs_codes": [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
        ],
        "description": "Agricultural products, food processing, beverages, tobacco",
    },
    "textiles": {
        "name": "Textiles & Apparel",
        "hs_codes": [
            "50",
            "51",
            "52",
            "53",
            "54",
            "55",
            "56",
            "57",
            "58",
            "59",
            "60",
            "61",
            "62",
            "63",
        ],
        "description": "Textiles, clothing, footwear, accessories",
    },
    "chemicals": {
        "name": "Chemicals & Pharmaceuticals",
        "hs_codes": ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38"],
        "description": "Chemical products, pharmaceuticals, cosmetics, plastics",
    },
    "metals": {
        "name": "Metals & Minerals",
        "hs_codes": [
            "25",
            "26",
            "27",
            "72",
            "73",
            "74",
            "75",
            "76",
            "78",
            "79",
            "80",
            "81",
            "82",
            "83",
        ],
        "description": "Base metals, metal products, tools, mineral products",
    },
    "machinery": {
        "name": "Machinery & Equipment",
        "hs_codes": ["84", "85"],
        "description": "Industrial machinery, electrical equipment, appliances",
    },
    "technology": {
        "name": "Technology & Electronics",
        "hs_codes": ["8517", "8471", "8473", "8504", "8525", "8528", "8542", "9013"],
        "description": "Telecommunications, computers, semiconductors, electronics",
    },
    "automotive": {
        "name": "Automotive & Transport",
        "hs_codes": ["86", "87", "88", "89"],
        "description": "Vehicles, aircraft, ships, transportation equipment",
    },
    "instruments": {
        "name": "Precision Instruments",
        "hs_codes": ["90", "91", "92"],
        "description": "Optical instruments, clocks, musical instruments",
    },
    "arms": {
        "name": "Arms & Ammunition",
        "hs_codes": ["93"],
        "description": "Weapons, ammunition, military equipment",
    },
    "furniture": {
        "name": "Furniture & Household",
        "hs_codes": ["94", "95", "96"],
        "description": "Furniture, toys, games, household items",
    },
    "arts": {
        "name": "Arts & Antiques",
        "hs_codes": ["97"],
        "description": "Works of art, antiques, collectibles",
    },
    "miscellaneous": {
        "name": "Miscellaneous",
        "hs_codes": [
            "39",
            "40",
            "41",
            "42",
            "43",
            "44",
            "45",
            "46",
            "47",
            "48",
            "49",
            "64",
            "65",
            "66",
            "67",
            "68",
            "69",
            "70",
            "71",
            "98",
            "99",
        ],
        "description": "Plastics, rubber, leather, wood, paper, stone, ceramics, precious stones",
    },
}

# Country code mapping for enhanced analysis
COUNTRY_CODES = {
    "China": "156",
    "European Union": "276",
    "Vietnam": "704",
    "Taiwan": "158",
    "Japan": "392",
    "India": "356",
    "South Korea": "410",
    "Thailand": "764",
    "Switzerland": "756",
    "Indonesia": "360",
    "Malaysia": "458",
    "Cambodia": "116",
    "United Kingdom": "826",
    "South Africa": "710",
    "Brazil": "076",
    "Bangladesh": "050",
    "Singapore": "702",
    "Israel": "376",
    "Philippines": "608",
    "Chile": "152",
    "Australia": "036",
    "Pakistan": "586",
    "Turkey": "792",
    "Sri Lanka": "144",
    "Colombia": "170",
    "Peru": "604",
    "Nicaragua": "558",
    "Norway": "578",
    "Costa Rica": "188",
    "Jordan": "400",
    "Dominican Republic": "214",
    "United Arab Emirates": "784",
    "New Zealand": "554",
    "Argentina": "032",
    "Ecuador": "218",
    "Guatemala": "320",
    "Honduras": "340",
    "Madagascar": "450",
    "Myanmar (Burma)": "104",
    "Tunisia": "788",
    "Kazakhstan": "398",
    "Serbia": "688",
    "Egypt": "818",
    "Saudi Arabia": "682",
    "El Salvador": "222",
    "Côte d'Ivoire": "384",
    "Laos": "418",
    "Botswana": "072",
    "Trinidad and Tobago": "780",
    "Morocco": "504",
    "Papua New Guinea": "598",
    "Malawi": "454",
    "Liberia": "430",
    "British Virgin Islands": "092",
    "Afghanistan": "004",
    "Zimbabwe": "716",
    "Benin": "204",
    "Barbados": "052",
    "Monaco": "492",
    "Syria": "760",
    "Uzbekistan": "860",
    "Republic of the Congo": "178",
    "Djibouti": "262",
    "French Polynesia": "258",
    "Cayman Islands": "136",
    "Kosovo": "838",
    "Curaçao": "531",
    "Vanuatu": "548",
    "Rwanda": "646",
    "Sierra Leone": "694",
    "Mongolia": "496",
    "San Marino": "674",
    "Antigua and Barbuda": "028",
    "Bermuda": "060",
    "Eswatini (Swaziland)": "748",
    "Marshall Islands": "584",
    "Saint Pierre and Miquelon": "666",
    "Saint Kitts and Nevis": "659",
    "Turkmenistan": "795",
    "Grenada": "308",
    "Sudan": "729",
    "Turks and Caicos Islands": "796",
    "Aruba": "533",
    "Montenegro": "499",
    "Saint Helena": "654",
    "Kyrgyzstan": "417",
    "Yemen": "887",
    "Saint Vincent and the Grenadines": "670",
    "Niger": "562",
    "Saint Lucia": "662",
    "Nauru": "520",
    "Equatorial Guinea": "226",
    "Iran": "364",
    "Libya": "434",
    "Samoa": "882",
    "Guinea": "324",
    "Timor-Leste": "626",
    "Montserrat": "500",
    "Chad": "148",
    "Mali": "466",
    "Maldives": "462",
    "Tajikistan": "762",
    "Cabo Verde": "132",
    "Burundi": "108",
    "Guadeloupe": "312",
    "Bhutan": "064",
    "Martinique": "474",
    "Tonga": "776",
    "Mauritania": "478",
    "Dominica": "212",
    "Micronesia": "583",
    "Gambia": "270",
    "French Guiana": "254",
    "Christmas Island": "162",
    "Andorra": "020",
    "Central African Republic": "140",
    "Solomon Islands": "090",
    "Mayotte": "175",
    "Anguilla": "660",
    "Cocos (Keeling) Islands": "166",
    "Eritrea": "232",
    "Cook Islands": "184",
    "South Sudan": "728",
    "Comoros": "174",
    "Kiribati": "296",
    "Sao Tomé and Principe": "678",
    "Norfolk Island": "574",
    "Gibraltar": "292",
    "Tuvalu": "798",
    "British Indian Ocean Territory": "086",
    "Tokelau": "772",
    "Guinea-Bissau": "624",
    "Svalbard and Jan Mayen": "744",
    "Heard and McDonald Islands": "334",
    "Reunion": "638",
    "Algeria": "012",
    "Moldova": "498",
    "Oman": "512",
    "Angola": "024",
    "Uruguay": "858",
    "Democratic Republic of the Congo": "180",
    "Bahamas": "044",
    "Jamaica": "388",
    "Lesotho": "426",
    "Mozambique": "508",
    "Ukraine": "804",
    "Paraguay": "600",
    "Bahrain": "048",
    "Zambia": "894",
    "Qatar": "634",
    "Lebanon": "422",
    "Mauritius": "480",
    "Tanzania": "834",
    "Fiji": "242",
    "Iraq": "368",
    "Iceland": "352",
    "Georgia": "268",
    "Kenya": "404",
    "Senegal": "686",
    "Liechtenstein": "438",
    "Azerbaijan": "031",
    "Guyana": "328",
    "Cameroon": "120",
    "Haiti": "332",
    "Uganda": "800",
    "Bosnia and Herzegovina": "070",
    "Albania": "008",
    "Nigeria": "566",
    "Armenia": "051",
    "Namibia": "516",
    "Nepal": "524",
    "Brunei": "096",
    "Sint Maarten": "534",
    "Bolivia": "068",
    "Åland Islands": "248",
    "Panama": "591",
    "Gabon": "266",
    "Venezuela": "862",
    "Kuwait": "414",
    "North Macedonia": "807",
    "Togo": "768",
    "Ethiopia": "231",
    "Suriname": "740",
    "Ghana": "288",
    "Belize": "084",
}


@dataclass
class EnhancedTariffData:
    """Enhanced tariff data structure with sectoral breakdown"""

    country: str
    country_code: str
    tariff_to_usa: float
    reciprocal_tariff: float
    sector_impacts: Dict[str, float]
    trade_volume: Optional[float] = None
    gdp_impact_factor: Optional[float] = None


@dataclass
class SectoralAnalysisConfig:
    """Configuration for sectoral tariff analysis"""

    selected_countries: List[str]
    selected_sectors: List[str]
    base_year: int = 2023
    projection_years: int = 5
    tariff_escalation_rate: float = 0.0
    include_retaliation: bool = True


class EnhancedTariffDataManager:
    """Manages comprehensive tariff data for 186 countries with sectoral breakdown"""

    def __init__(self, data_path: str = "data/trump_tariffs_by_country.csv"):
        self.data_path = Path(data_path)
        self.tariff_data: Dict[str, EnhancedTariffData] = {}
        self.sectors = GLOBAL_SECTORS
        self.country_codes = COUNTRY_CODES
        self.load_tariff_data()

    def load_tariff_data(self):
        """Load and process tariff data with sectoral breakdown"""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Tariff data file not found: {self.data_path}")

        df = pd.read_csv(self.data_path)

        for _, row in df.iterrows():
            country = row["Country"]
            country_code = self.country_codes.get(country, "000")

            # Generate sector-specific impacts based on country characteristics
            sector_impacts = self._generate_sector_impacts(
                country, row["Tariffs charged to USA"], row["Reciprocal Tariffs"]
            )

            self.tariff_data[country] = EnhancedTariffData(
                country=country,
                country_code=country_code,
                tariff_to_usa=row["Tariffs charged to USA"],
                reciprocal_tariff=row["Reciprocal Tariffs"],
                sector_impacts=sector_impacts,
                trade_volume=self._estimate_trade_volume(country),
                gdp_impact_factor=self._estimate_gdp_impact_factor(country),
            )

    def _generate_sector_impacts(
        self, country: str, base_tariff: float, reciprocal: float
    ) -> Dict[str, float]:
        """Generate sector-specific tariff impacts based on country characteristics"""

        # Country-specific sector weights based on economic structure
        sector_weights = self._get_country_sector_weights(country)

        sector_impacts = {}
        for sector_id, sector_info in self.sectors.items():
            # Base impact from tariff rate
            base_impact = base_tariff * sector_weights.get(sector_id, 1.0)

            # Add sector-specific modifiers
            sector_modifier = self._get_sector_modifier(sector_id, country)

            # Calculate final impact
            final_impact = base_impact * sector_modifier
            sector_impacts[sector_id] = min(final_impact, 2.0)  # Cap at 200%

        return sector_impacts

    def _get_country_sector_weights(self, country: str) -> Dict[str, float]:
        """Get country-specific sector importance weights"""

        # Define country categories and their sector weights
        tech_leaders = ["China", "Taiwan", "South Korea", "Japan", "Singapore"]
        manufacturing_hubs = [
            "Vietnam",
            "Bangladesh",
            "Cambodia",
            "Thailand",
            "Malaysia",
        ]
        commodity_exporters = [
            "Australia",
            "Brazil",
            "Chile",
            "South Africa",
            "Kazakhstan",
        ]
        oil_exporters = [
            "Saudi Arabia",
            "United Arab Emirates",
            "Kuwait",
            "Qatar",
            "Algeria",
        ]
        agricultural_countries = ["Argentina", "Ukraine", "New Zealand", "Uruguay"]

        if country in tech_leaders:
            return {
                "technology": 1.5,
                "machinery": 1.3,
                "electronics": 1.4,
                "automotive": 1.2,
                "chemicals": 1.1,
                "textiles": 0.8,
            }
        elif country in manufacturing_hubs:
            return {
                "textiles": 1.6,
                "machinery": 1.3,
                "technology": 1.2,
                "chemicals": 1.0,
                "automotive": 0.9,
                "agriculture": 0.7,
            }
        elif country in commodity_exporters:
            return {
                "metals": 1.5,
                "agriculture": 1.3,
                "chemicals": 1.2,
                "machinery": 0.9,
                "textiles": 0.8,
                "technology": 0.8,
            }
        elif country in oil_exporters:
            return {
                "chemicals": 1.4,
                "metals": 1.2,
                "machinery": 1.1,
                "technology": 0.9,
                "textiles": 0.7,
                "agriculture": 0.8,
            }
        elif country in agricultural_countries:
            return {
                "agriculture": 1.6,
                "chemicals": 1.2,
                "machinery": 1.1,
                "textiles": 0.9,
                "technology": 0.8,
                "automotive": 0.8,
            }
        else:
            # Default balanced weights
            return {sector: 1.0 for sector in self.sectors.keys()}

    def _get_sector_modifier(self, sector_id: str, country: str) -> float:
        """Get sector-specific impact modifiers"""

        # Technology sectors are more sensitive to tariffs
        if sector_id == "technology":
            return 1.3
        elif sector_id == "automotive":
            return 1.2
        elif sector_id == "agriculture":
            return 0.9  # Often protected/subsidized
        elif sector_id == "arms":
            return 0.7  # Often exempt or special rules
        else:
            return 1.0

    def _estimate_trade_volume(self, country: str) -> float:
        """Estimate trade volume with US (in billions USD)"""

        # Major trading partners (rough estimates)
        major_traders = {
            "China": 650,
            "European Union": 400,
            "Japan": 200,
            "South Korea": 180,
            "United Kingdom": 120,
            "India": 100,
            "Taiwan": 90,
            "Vietnam": 85,
            "Thailand": 60,
            "Singapore": 55,
            "Malaysia": 50,
            "Indonesia": 45,
            "Brazil": 40,
            "Australia": 35,
            "Switzerland": 30,
            "Israel": 25,
        }

        return major_traders.get(country, np.random.uniform(0.5, 15.0))

    def _estimate_gdp_impact_factor(self, country: str) -> float:
        """Estimate how much tariffs affect country's GDP (trade dependency)"""

        # High trade dependency countries
        high_dependency = ["Singapore", "Taiwan", "South Korea", "Vietnam", "Malaysia"]
        medium_dependency = ["China", "Thailand", "Japan", "United Kingdom", "India"]

        if country in high_dependency:
            return np.random.uniform(0.15, 0.25)  # 15-25% of GDP from US trade
        elif country in medium_dependency:
            return np.random.uniform(0.08, 0.15)  # 8-15% of GDP from US trade
        else:
            return np.random.uniform(0.02, 0.08)  # 2-8% of GDP from US trade

    def get_countries_by_tariff_level(
        self, threshold: float = 0.5
    ) -> Dict[str, List[str]]:
        """Categorize countries by tariff levels"""

        high_tariff = []
        medium_tariff = []
        low_tariff = []

        for country, data in self.tariff_data.items():
            if data.tariff_to_usa >= threshold:
                high_tariff.append(country)
            elif data.tariff_to_usa >= 0.3:
                medium_tariff.append(country)
            else:
                low_tariff.append(country)

        return {"high": high_tariff, "medium": medium_tariff, "low": low_tariff}

    def get_available_countries(self) -> List[str]:
        """Get list of all available countries"""
        return list(self.tariff_data.keys())

    def get_available_sectors(self) -> List[str]:
        """Get list of all available sectors"""
        return list(self.sectors.keys())

    def get_sector_analysis(self, countries: List[str], sectors: List[str]) -> Dict:
        """Perform detailed sector analysis for selected countries"""

        analysis = {
            "countries_analyzed": len(countries),
            "sectors_analyzed": len(sectors),
            "total_impact": 0.0,
            "sector_impacts": {},
            "country_impacts": {},
            "risk_assessment": {},
            "summary_statistics": {},
        }

        # Calculate sector impacts with improved accuracy
        total_impact_sum = 0.0
        valid_countries = 0

        for sector in sectors:
            sector_data = []
            sector_impact_sum = 0.0

            for country in countries:
                if country in self.tariff_data:
                    data = self.tariff_data[country]
                    impact = data.sector_impacts.get(sector, 0.0)

                    # Apply realistic scaling based on trade volume
                    if data.trade_volume:
                        scaled_impact = impact * min(data.trade_volume / 100.0, 1.5)
                    else:
                        scaled_impact = impact * 0.8  # Default scaling for missing data

                    sector_data.append(
                        {
                            "country": country,
                            "impact": scaled_impact,
                            "raw_impact": impact,
                            "trade_volume": data.trade_volume or 0.0,
                            "base_tariff": data.tariff_to_usa,
                        }
                    )
                    sector_impact_sum += scaled_impact

            if sector_data:
                avg_impact = sector_impact_sum / len(sector_data)
                max_impact = max([d["impact"] for d in sector_data])

                analysis["sector_impacts"][sector] = {
                    "average_impact": avg_impact,
                    "max_impact": max_impact,
                    "countries_affected": len(sector_data),
                    "sector_total_impact": sector_impact_sum,
                    "details": sector_data,
                }
                total_impact_sum += avg_impact

        # Calculate country-level aggregated impacts with better methodology
        for country in countries:
            if country in self.tariff_data:
                data = self.tariff_data[country]

                # Calculate weighted impact based on selected sectors
                sector_impacts_list = []
                for sector in sectors:
                    if sector in data.sector_impacts:
                        sector_weight = self._get_sector_weight_for_country(
                            country, sector
                        )
                        weighted_impact = data.sector_impacts[sector] * sector_weight
                        sector_impacts_list.append(weighted_impact)

                if sector_impacts_list:
                    country_impact = sum(sector_impacts_list) / len(sector_impacts_list)
                    valid_countries += 1
                else:
                    country_impact = 0.0

                # Calculate GDP loss with more realistic estimates
                gdp_loss = (
                    country_impact * (data.gdp_impact_factor or 1.0) * 50
                )  # Scale down from 100

                analysis["country_impacts"][country] = {
                    "average_impact": country_impact,
                    "trade_volume": data.trade_volume or 0.0,
                    "gdp_factor": data.gdp_impact_factor or 1.0,
                    "estimated_gdp_loss": gdp_loss,
                    "base_tariff": data.tariff_to_usa,
                    "reciprocal_tariff": data.reciprocal_tariff,
                }

        # Improved risk assessment
        total_trade_volume = sum(
            [
                (self.tariff_data[country].trade_volume or 0.0)
                for country in countries
                if country in self.tariff_data
            ]
        )

        if valid_countries > 0:
            avg_impact = total_impact_sum / len(sectors) if sectors else 0.0
        else:
            avg_impact = 0.0

        # More nuanced risk categories
        if avg_impact > 0.5:
            risk_level = "Very High"
        elif avg_impact > 0.35:
            risk_level = "High"
        elif avg_impact > 0.2:
            risk_level = "Medium"
        elif avg_impact > 0.1:
            risk_level = "Low"
        else:
            risk_level = "Very Low"

        analysis["total_impact"] = avg_impact

        # Enhanced risk assessment
        if analysis["sector_impacts"] and analysis["country_impacts"]:
            most_affected_sector = max(
                analysis["sector_impacts"].keys(),
                key=lambda s: analysis["sector_impacts"][s]["average_impact"],
            )
            most_affected_country = max(
                analysis["country_impacts"].keys(),
                key=lambda c: analysis["country_impacts"][c]["average_impact"],
            )

            analysis["risk_assessment"] = {
                "overall_risk": risk_level,
                "total_trade_at_risk": total_trade_volume,
                "most_affected_sector": most_affected_sector,
                "most_affected_country": most_affected_country,
                "risk_score": avg_impact,
                "countries_at_high_risk": len(
                    [
                        c
                        for c, data in analysis["country_impacts"].items()
                        if data["average_impact"] > 0.4
                    ]
                ),
            }
        else:
            analysis["risk_assessment"] = {
                "overall_risk": "Unknown",
                "total_trade_at_risk": 0.0,
                "most_affected_sector": "None",
                "most_affected_country": "None",
                "risk_score": 0.0,
                "countries_at_high_risk": 0,
            }

        # Add summary statistics
        if analysis["country_impacts"]:
            country_impacts = [
                data["average_impact"] for data in analysis["country_impacts"].values()
            ]
            gdp_losses = [
                data["estimated_gdp_loss"]
                for data in analysis["country_impacts"].values()
            ]

            analysis["summary_statistics"] = {
                "mean_country_impact": np.mean(country_impacts),
                "median_country_impact": np.median(country_impacts),
                "std_country_impact": np.std(country_impacts),
                "total_estimated_gdp_loss": sum(gdp_losses),
                "countries_above_threshold": len(
                    [x for x in country_impacts if x > 0.3]
                ),
            }

        return analysis

    def _get_sector_weight_for_country(self, country: str, sector: str) -> float:
        """Get sector importance weight for specific country"""
        weights = self._get_country_sector_weights(country)
        return weights.get(sector, 1.0)

    def export_analysis_data(
        self,
        countries: List[str],
        sectors: List[str],
        file_path: str = "enhanced_tariff_analysis.json",
    ):
        """Export comprehensive analysis data"""

        analysis = self.get_sector_analysis(countries, sectors)

        export_data = {
            "metadata": {
                "analysis_date": pd.Timestamp.now().isoformat(),
                "countries_count": len(countries),
                "sectors_count": len(sectors),
                "data_source": "Trump Tariffs by Country (Enhanced)",
            },
            "configuration": {
                "selected_countries": countries,
                "selected_sectors": sectors,
                "sector_definitions": {
                    s: self.sectors[s] for s in sectors if s in self.sectors
                },
            },
            "analysis_results": analysis,
            "raw_data": {
                country: {
                    "tariff_to_usa": data.tariff_to_usa,
                    "reciprocal_tariff": data.reciprocal_tariff,
                    "sector_impacts": {
                        s: data.sector_impacts.get(s, 0.0) for s in sectors
                    },
                    "trade_volume": data.trade_volume,
                    "gdp_impact_factor": data.gdp_impact_factor,
                }
                for country, data in self.tariff_data.items()
                if country in countries
            },
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)

        return file_path
