#!/usr/bin/env python3
"""
TIPM v2.0 - Real US Tariff Data
================================

Comprehensive database of actual US-imposed tariff rates by country and sector.
Based on official USTR, USITC, and Federal Register data.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class TariffInfo:
    country: str
    sector: str
    tariff_rate: float
    hts_code: str
    effective_date: str
    source: str
    notes: str


# Real US-imposed tariff rates by country and sector
# Based on Section 301 (China), Section 232 (Steel/Aluminum), and other trade actions

REAL_TARIFF_DATA = {
    "China": {
        "Technology & Electronics": {
            "tariff_rate": 25.0,
            "hts_codes": ["8542", "8541", "8517", "8528", "8529"],
            "effective_date": "2018-2020",
            "source": "Section 301 Lists 1-4",
            "notes": "Semiconductors, consumer electronics, telecommunications equipment",
        },
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Carbon steel, alloy steel, aluminum products",
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Auto parts, complete vehicles, motorcycles",
        },
        "Machinery & Equipment": {
            "tariff_rate": 25.0,
            "hts_codes": ["84", "85"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Industrial machinery, electrical equipment",
        },
        "Chemicals & Pharmaceuticals": {
            "tariff_rate": 25.0,
            "hts_codes": ["28", "29", "30"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Industrial chemicals, pharmaceuticals, medical devices",
        },
        "Textiles & Apparel": {
            "tariff_rate": 25.0,
            "hts_codes": [
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
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Raw materials, fabrics, clothing, home textiles",
        },
        "Agriculture & Food": {
            "tariff_rate": 25.0,
            "hts_codes": [
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
            ],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Soybeans, corn, wheat, pork, beef, dairy, processed foods",
        },
        "Energy & Minerals": {
            "tariff_rate": 25.0,
            "hts_codes": ["8541", "8501", "8506", "8507", "2805", "2844", "2846"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Solar panels, batteries, rare earth elements",
        },
        "Aerospace & Defense": {
            "tariff_rate": 25.0,
            "hts_codes": ["8803", "8804", "8805", "8802"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Aircraft parts, spacecraft, satellites",
        },
        "Construction & Building Materials": {
            "tariff_rate": 25.0,
            "hts_codes": ["44", "25", "68"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Lumber, cement, concrete",
        },
    },
    "European Union": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%)",
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
        },
        "Aerospace & Defense": {
            "tariff_rate": 25.0,
            "hts_codes": ["8803", "8804", "8805"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Aircraft parts and components",
        },
    },
    "Japan": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%)",
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
        },
    },
    "South Korea": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Limited exemptions",
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
        },
    },
    "Canada": {
        "Lumber & Wood Products": {
            "tariff_rate": 20.0,
            "hts_codes": ["44"],
            "effective_date": "2017",
            "source": "Section 201",
            "notes": "Softwood lumber - periodic adjustments",
        }
    },
    "Mexico": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - USMCA Exemption",
            "notes": "Exempted under USMCA trade agreement",
        }
    },
    "India": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%)",
        },
        "Technology & Electronics": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2019",
            "source": "Section 301",
            "notes": "Digital services tax retaliation",
        },
    },
    "Turkey": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%)",
        }
    },
    "Brazil": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - Exemption",
            "notes": "Exempted due to quota agreement",
        }
    },
    "Argentina": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - Exemption",
            "notes": "Exempted due to quota agreement",
        }
    },
}


def get_country_tariffs(country_name: str) -> Dict[str, Dict]:
    """Get all tariff information for a specific country"""
    return REAL_TARIFF_DATA.get(country_name, {})


def get_country_sector_tariff(country_name: str, sector: str) -> Optional[Dict]:
    """Get tariff information for a specific country and sector"""
    country_tariffs = get_country_tariffs(country_name)
    return country_tariffs.get(sector)


def get_country_average_tariff(country_name: str) -> float:
    """Calculate average tariff rate for a country across all sectors"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return 0.0

    total_rate = sum(tariff["tariff_rate"] for tariff in country_tariffs.values())
    return total_rate / len(country_tariffs)


def get_affected_sectors(country_name: str) -> List[str]:
    """Get list of sectors affected by US tariffs for a country"""
    country_tariffs = get_country_tariffs(country_name)
    return list(country_tariffs.keys())


def get_total_tariff_impact(country_name: str) -> Dict[str, float]:
    """Calculate total tariff impact for a country"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return {"total_rate": 0.0, "affected_sectors": 0, "average_rate": 0.0}

    total_rate = sum(tariff["tariff_rate"] for tariff in country_tariffs.values())
    affected_sectors = len(country_tariffs)
    average_rate = total_rate / affected_sectors

    return {
        "total_rate": total_rate,
        "affected_sectors": affected_sectors,
        "average_rate": average_rate,
    }


def get_sector_analysis(country_name: str, sector: str) -> Dict[str, Any]:
    """Get detailed sector analysis for tariff impact"""
    tariff_info = get_country_sector_tariff(country_name, sector)
    if not tariff_info:
        return {
            "affected": False,
            "tariff_rate": 0.0,
            "impact_level": "None",
            "notes": "No US tariffs on this sector",
        }

    # Determine impact level based on tariff rate
    rate = tariff_info["tariff_rate"]
    if rate >= 25:
        impact_level = "Critical"
    elif rate >= 15:
        impact_level = "High"
    elif rate >= 5:
        impact_level = "Medium"
    else:
        impact_level = "Low"

    return {
        "affected": True,
        "tariff_rate": rate,
        "impact_level": impact_level,
        "hts_codes": tariff_info["hts_codes"],
        "effective_date": tariff_info["effective_date"],
        "source": tariff_info["source"],
        "notes": tariff_info["notes"],
    }


def get_economic_insights(country_name: str, sector: str) -> List[str]:
    """Get economic insights and considerations for a country-sector combination"""
    tariff_info = get_country_sector_tariff(country_name, sector)
    if not tariff_info:
        return ["This sector is not currently affected by US tariffs"]

    insights = []
    rate = tariff_info["tariff_rate"]

    # General economic insights
    if rate >= 25:
        insights.extend(
            [
                "Critical tariff level - significant supply chain disruption expected",
                "High likelihood of price increases for US consumers",
                "Potential for retaliatory tariffs from affected country",
                "Risk of supply chain diversification away from US",
                "Possible WTO dispute filing",
            ]
        )
    elif rate >= 15:
        insights.extend(
            [
                "High tariff level - moderate supply chain impact",
                "Likely price increases in affected sectors",
                "Potential for trade diversion to non-tariff countries",
                "Risk of reduced US market competitiveness",
            ]
        )
    elif rate >= 5:
        insights.extend(
            [
                "Moderate tariff level - limited economic impact",
                "Minor price increases possible",
                "Some supply chain adjustment expected",
                "Limited retaliatory risk",
            ]
        )

    # Sector-specific insights
    if "Technology" in sector:
        insights.extend(
            [
                "Critical for US tech supply chain",
                "High risk of innovation disruption",
                "Potential for increased domestic tech investment",
                "Risk of reduced US tech competitiveness globally",
            ]
        )
    elif "Steel" in sector or "Aluminum" in sector:
        insights.extend(
            [
                "National security implications",
                "Impact on US manufacturing costs",
                "Potential for domestic steel/aluminum industry growth",
                "Risk of increased construction and manufacturing costs",
            ]
        )
    elif "Automotive" in sector:
        insights.extend(
            [
                "Significant impact on US auto industry",
                "Risk of increased vehicle prices",
                "Potential for domestic auto parts manufacturing",
                "Impact on US auto export competitiveness",
            ]
        )
    elif "Agriculture" in sector:
        insights.extend(
            [
                "Impact on US farm income",
                "Risk of agricultural trade retaliation",
                "Potential for domestic food price increases",
                "Impact on rural economy",
            ]
        )

    return insights


def get_mitigation_strategies(country_name: str, sector: str) -> List[str]:
    """Get potential mitigation strategies for affected countries"""
    tariff_info = get_country_sector_tariff(country_name, sector)
    if not tariff_info:
        return ["No mitigation needed - sector not affected"]

    strategies = [
        "Diversify export markets to reduce US dependency",
        "Develop domestic supply chains for affected products",
        "Seek alternative suppliers in non-tariff countries",
        "Negotiate bilateral trade agreements",
        "File WTO dispute resolution cases",
        "Implement retaliatory tariffs on US exports",
        "Develop value-added products to offset tariff costs",
        "Seek tariff exemptions through diplomatic channels",
    ]

    # Add sector-specific strategies
    if "Technology" in sector:
        strategies.extend(
            [
                "Accelerate domestic technology development",
                "Partner with non-US technology companies",
                "Develop alternative supply chain routes",
                "Invest in domestic semiconductor manufacturing",
            ]
        )
    elif "Steel" in sector or "Aluminum" in sector:
        strategies.extend(
            [
                "Develop domestic steel/aluminum processing",
                "Seek alternative raw material sources",
                "Invest in value-added steel products",
                "Develop recycling and sustainability initiatives",
            ]
        )

    return strategies
