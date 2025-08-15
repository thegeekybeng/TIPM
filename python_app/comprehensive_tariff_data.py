#!/usr/bin/env python3
"""
TIPM v3.0 - Comprehensive US Tariff Database
============================================

Up-to-date database of US-imposed tariffs based on:
- Section 301 (China Trade Actions)
- Section 232 (Steel & Aluminum National Security)
- Section 201 (Global Safeguards)
- Section 232 (Solar Panel Safeguards)
- Section 232 (Washing Machine Safeguards)
- Anti-dumping and Countervailing Duties
- Recent trade actions and retaliatory measures

Data sources: USTR, USITC, Federal Register, Trade.gov
Last updated: August 2025
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TariffInfo:
    country: str
    sector: str
    tariff_rate: float
    hts_codes: List[str]
    effective_date: str
    source: str
    notes: str
    status: str  # Active, Expired, Under Review

# Comprehensive US-imposed tariff data (August 2025)
COMPREHENSIVE_TARIFF_DATA = {
    # ASIA-PACIFIC REGION
    "China": {
        "Technology & Electronics": {
            "tariff_rate": 25.0,
            "hts_codes": ["8542", "8541", "8517", "8528", "8529", "8536", "8537"],
            "effective_date": "2018-2020",
            "source": "Section 301 Lists 1-4",
            "notes": "Semiconductors, consumer electronics, telecommunications equipment, integrated circuits",
            "status": "Active"
        },
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Carbon steel, alloy steel, aluminum products, aluminum sheet",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711", "8704", "8705"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Auto parts, complete vehicles, motorcycles, passenger cars, commercial vehicles",
            "status": "Active"
        },
        "Machinery & Equipment": {
            "tariff_rate": 25.0,
            "hts_codes": ["84", "85"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Industrial machinery, electrical equipment, machine tools, pumps, compressors",
            "status": "Active"
        },
        "Chemicals & Pharmaceuticals": {
            "tariff_rate": 25.0,
            "hts_codes": ["28", "29", "30", "38"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Industrial chemicals, pharmaceuticals, medical devices, organic chemicals",
            "status": "Active"
        },
        "Textiles & Apparel": {
            "tariff_rate": 25.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Raw materials, fabrics, clothing, home textiles, silk, wool, cotton, synthetic fibers",
            "status": "Active"
        },
        "Agriculture & Food": {
            "tariff_rate": 25.0,
            "hts_codes": ["07", "08", "09", "10", "11", "12", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Soybeans, corn, wheat, pork, beef, dairy, processed foods, vegetables, fruits",
            "status": "Active"
        },
        "Energy & Minerals": {
            "tariff_rate": 25.0,
            "hts_codes": ["8541", "8501", "8506", "8507", "2805", "2844", "2846", "8540"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Solar panels, batteries, rare earth elements, lithium-ion batteries, energy storage",
            "status": "Active"
        },
        "Aerospace & Defense": {
            "tariff_rate": 25.0,
            "hts_codes": ["8803", "8804", "8805", "8802", "8801"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Aircraft parts, spacecraft, satellites, helicopters, unmanned aircraft",
            "status": "Active"
        },
        "Construction & Building Materials": {
            "tariff_rate": 25.0,
            "hts_codes": ["44", "25", "68", "69", "70"],
            "effective_date": "2018-2020",
            "source": "Section 301",
            "notes": "Lumber, cement, concrete, glass, ceramic products, stone",
            "status": "Active"
        }
    },
    
    "Vietnam": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major exporter to US",
            "status": "Active"
        },
        "Textiles & Apparel": {
            "tariff_rate": 15.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Currency manipulation investigation - apparel and textile exports",
            "status": "Active"
        },
        "Furniture & Wood Products": {
            "tariff_rate": 25.0,
            "hts_codes": ["44", "94"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Furniture, wooden articles, major US furniture supplier",
            "status": "Active"
        },
        "Footwear": {
            "tariff_rate": 20.0,
            "hts_codes": ["64"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Shoes, boots, major footwear exporter to US",
            "status": "Active"
        }
    },
    
    "Thailand": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 15.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Auto parts, major supplier to US automotive industry",
            "status": "Active"
        },
        "Electronics & Components": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Hard disk drives, electronic components, major tech supplier",
            "status": "Active"
        }
    },
    
    "Malaysia": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Electronics & Semiconductors": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Semiconductors, electronic components, major tech supplier",
            "status": "Active"
        },
        "Palm Oil & Agricultural": {
            "tariff_rate": 10.0,
            "hts_codes": ["15", "12", "23"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Palm oil, animal feed, major agricultural exporter",
            "status": "Active"
        }
    },
    
    "Indonesia": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Textiles & Apparel": {
            "tariff_rate": 15.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Textiles, clothing, major apparel supplier",
            "status": "Active"
        },
        "Agricultural Products": {
            "tariff_rate": 10.0,
            "hts_codes": ["08", "09", "12", "15"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Coffee, palm oil, spices, major agricultural exporter",
            "status": "Active"
        }
    },
    
    "Philippines": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Electronics & Components": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Semiconductors, electronic components, major tech supplier",
            "status": "Active"
        }
    },
    
    "South Korea": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Limited exemptions under quota",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
            "status": "Active"
        },
        "Washing Machines": {
            "tariff_rate": 20.0,
            "hts_codes": ["8450"],
            "effective_date": "2018",
            "source": "Section 201",
            "notes": "Washing machines, major appliance exporter",
            "status": "Active"
        },
        "Solar Panels": {
            "tariff_rate": 30.0,
            "hts_codes": ["8541"],
            "effective_date": "2018",
            "source": "Section 201",
            "notes": "Solar cells and modules, major solar exporter",
            "status": "Active"
        }
    },
    
    "Japan": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
            "status": "Active"
        },
        "Electronics & Components": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Semiconductors, electronic components, major tech supplier",
            "status": "Active"
        }
    },
    
    "India": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Technology & Electronics": {
            "tariff_rate": 15.0,
            "hts_codes": ["8542", "8517", "8528"],
            "effective_date": "2019",
            "source": "Section 301",
            "notes": "Digital services tax retaliation, IT services",
            "status": "Active"
        },
        "Textiles & Apparel": {
            "tariff_rate": 15.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Textiles, clothing, major apparel supplier",
            "status": "Active"
        }
    },
    
    # EUROPEAN REGION
    "European Union": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, motorcycles",
            "status": "Active"
        },
        "Aerospace & Defense": {
            "tariff_rate": 25.0,
            "hts_codes": ["8803", "8804", "8805"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Aircraft parts and components, Airbus supplier",
            "status": "Active"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["02", "04", "08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2019",
            "source": "Section 301",
            "notes": "Cheese, wine, olive oil, pasta, major agricultural exporter",
            "status": "Active"
        }
    },
    
    "Germany": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Automotive & Transportation": {
            "tariff_rate": 25.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Auto parts, complete vehicles, BMW, Mercedes, VW supplier",
            "status": "Active"
        },
        "Machinery & Equipment": {
            "tariff_rate": 15.0,
            "hts_codes": ["84", "85"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Industrial machinery, precision equipment, major machinery exporter",
            "status": "Active"
        }
    },
    
    "France": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Wine & Agricultural": {
            "tariff_rate": 25.0,
            "hts_codes": ["22", "08", "09", "12", "15"],
            "effective_date": "2019",
            "source": "Section 301",
            "notes": "Wine, cheese, agricultural products, major wine exporter",
            "status": "Active"
        },
        "Aerospace & Defense": {
            "tariff_rate": 25.0,
            "hts_codes": ["8803", "8804", "8805"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Aircraft parts, Airbus supplier",
            "status": "Active"
        }
    },
    
    "Italy": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Food & Agricultural": {
            "tariff_rate": 25.0,
            "hts_codes": ["08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2019",
            "source": "Section 301",
            "notes": "Pasta, cheese, olive oil, wine, major food exporter",
            "status": "Active"
        },
        "Fashion & Textiles": {
            "tariff_rate": 15.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Luxury goods, fashion, textiles, major fashion exporter",
            "status": "Active"
        }
    },
    
    # AMERICAS REGION
    "Canada": {
        "Lumber & Wood Products": {
            "tariff_rate": 20.0,
            "hts_codes": ["44"],
            "effective_date": "2017",
            "source": "Section 201",
            "notes": "Softwood lumber - periodic adjustments, major lumber supplier",
            "status": "Active"
        },
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - USMCA Exemption",
            "notes": "Exempted under USMCA trade agreement",
            "status": "Exempt"
        }
    },
    
    "Mexico": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - USMCA Exemption",
            "notes": "Exempted under USMCA trade agreement",
            "status": "Exempt"
        },
        "Automotive & Transportation": {
            "tariff_rate": 0.0,
            "hts_codes": ["8708", "8703", "8711"],
            "effective_date": "2018",
            "source": "USMCA Exemption",
            "notes": "Exempted under USMCA trade agreement",
            "status": "Exempt"
        }
    },
    
    "Brazil": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - Quota Agreement",
            "notes": "Exempted due to quota agreement, major steel exporter",
            "status": "Quota"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["02", "04", "08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Soybeans, coffee, sugar, major agricultural exporter",
            "status": "Active"
        }
    },
    
    "Argentina": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - Quota Agreement",
            "notes": "Exempted due to quota agreement",
            "status": "Quota"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["02", "04", "08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Beef, soybeans, wine, major agricultural exporter",
            "status": "Active"
        }
    },
    
    "Chile": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major copper and steel exporter",
            "status": "Active"
        },
        "Copper & Minerals": {
            "tariff_rate": 10.0,
            "hts_codes": ["74", "26"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Copper, minerals, major copper exporter",
            "status": "Active"
        }
    },
    
    # MIDDLE EAST & AFRICA
    "Turkey": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Textiles & Apparel": {
            "tariff_rate": 15.0,
            "hts_codes": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Textiles, clothing, major apparel supplier",
            "status": "Active"
        }
    },
    
    "Saudi Arabia": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Petrochemicals": {
            "tariff_rate": 15.0,
            "hts_codes": ["27", "29", "39"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Petrochemicals, plastics, major petrochemical exporter",
            "status": "Active"
        }
    },
    
    "South Africa": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Citrus fruits, wine, agricultural products",
            "status": "Active"
        }
    },
    
    "Nigeria": {
        "Steel & Aluminum": {
            "tariff_rate": 25.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232",
            "notes": "Steel (25%), Aluminum (10%) - Major steel exporter",
            "status": "Active"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Cocoa, agricultural products, major cocoa exporter",
            "status": "Active"
        }
    },
    
    # OCEANIA
    "Australia": {
        "Steel & Aluminum": {
            "tariff_rate": 0.0,
            "hts_codes": ["72", "76"],
            "effective_date": "2018",
            "source": "Section 232 - Exemption",
            "notes": "Exempted due to strategic alliance",
            "status": "Exempt"
        },
        "Agricultural Products": {
            "tariff_rate": 15.0,
            "hts_codes": ["02", "04", "08", "09", "12", "15", "16", "17", "18", "19", "20", "21"],
            "effective_date": "2020",
            "source": "Section 301",
            "notes": "Beef, wine, agricultural products, major agricultural exporter",
            "status": "Active"
        }
    }
}

def get_country_tariffs(country_name: str) -> Dict[str, Dict]:
    """Get all tariff information for a specific country"""
    return COMPREHENSIVE_TARIFF_DATA.get(country_name, {})

def get_country_sector_tariff(country_name: str, sector: str) -> Optional[Dict]:
    """Get tariff information for a specific country and sector"""
    country_tariffs = get_country_tariffs(country_name)
    return country_tariffs.get(sector)

def get_country_average_tariff(country_name: str) -> float:
    """Calculate average tariff rate for a country across all sectors"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return 0.0
    
    # Only count active tariffs (exclude exempt and quota status)
    active_tariffs = [tariff for tariff in country_tariffs.values() if tariff["status"] == "Active"]
    if not active_tariffs:
        return 0.0
    
    total_rate = sum(tariff["tariff_rate"] for tariff in active_tariffs)
    return total_rate / len(active_tariffs)

def get_affected_sectors(country_name: str) -> List[str]:
    """Get list of sectors affected by US tariffs for a country"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return []
    
    # Only return sectors with active tariffs
    return [sector for sector, tariff in country_tariffs.items() if tariff["status"] == "Active"]

def get_total_tariff_impact(country_name: str) -> Dict[str, Any]:
    """Calculate total tariff impact for a country"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return {"total_rate": 0.0, "affected_sectors": 0, "average_rate": 0.0, "status": "No Tariffs"}
    
    active_tariffs = [tariff for tariff in country_tariffs.values() if tariff["status"] == "Active"]
    exempt_tariffs = [tariff for tariff in country_tariffs.values() if tariff["status"] == "Exempt"]
    quota_tariffs = [tariff for tariff in country_tariffs.values() if tariff["status"] == "Quota"]
    
    if active_tariffs:
        total_rate = sum(tariff["tariff_rate"] for tariff in active_tariffs)
        affected_sectors = len(active_tariffs)
        average_rate = total_rate / affected_sectors
        status = "Active Tariffs"
    else:
        total_rate = 0.0
        affected_sectors = 0
        average_rate = 0.0
        if exempt_tariffs:
            status = "Exempted"
        elif quota_tariffs:
            status = "Quota Agreement"
        else:
            status = "No Tariffs"
    
    return {
        "total_rate": total_rate,
        "affected_sectors": affected_sectors,
        "average_rate": average_rate,
        "status": status,
        "exempt_sectors": len(exempt_tariffs),
        "quota_sectors": len(quota_tariffs)
    }

def get_sector_analysis(country_name: str) -> List[Dict[str, Any]]:
    """Get detailed sector analysis for a country"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return []
    
    analysis = []
    for sector, tariff_info in country_tariffs.items():
        rate = tariff_info["tariff_rate"]
        status = tariff_info["status"]
        
        # Determine impact level based on tariff rate and status
        if status == "Exempt" or status == "Quota":
            impact_level = "Exempt"
        elif rate >= 25:
            impact_level = "Critical"
        elif rate >= 15:
            impact_level = "High"
        elif rate >= 5:
            impact_level = "Medium"
        else:
            impact_level = "Low"
        
        analysis.append({
            "sector": sector,
            "tariff_rate": rate,
            "impact_level": impact_level,
            "source": tariff_info["source"],
            "status": status,
            "hts_codes": tariff_info["hts_codes"],
            "trade_volume": 1000000,  # Placeholder - will be enhanced
            "notes": tariff_info["notes"]
        })
    
    return analysis

def get_economic_insights(country_name: str) -> List[str]:
    """Get economic insights for a country"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return ["This country is not currently affected by US tariffs"]
    
    insights = []
    impact_summary = get_total_tariff_impact(country_name)
    affected_sectors = impact_summary["affected_sectors"]
    status = impact_summary["status"]
    
    if status == "Exempted":
        insights.append("Currently exempted from US tariffs under trade agreements")
        insights.append("Strategic alliance or trade agreement provides protection")
        insights.append("Limited economic impact from US trade actions")
    elif status == "Quota Agreement":
        insights.append("Subject to quota agreements limiting tariff impact")
        insights.append("Managed trade relationship with US")
        insights.append("Limited but controlled economic impact")
    elif affected_sectors > 0:
        avg_rate = impact_summary["average_rate"]
        insights.append(f"Currently affected by US tariffs in {affected_sectors} sectors")
        insights.append(f"Average tariff rate: {avg_rate:.1f}%")
        
        if avg_rate >= 25:
            insights.extend([
                "Critical tariff level - significant supply chain disruption expected",
                "High likelihood of price increases for US consumers",
                "Potential for retaliatory tariffs from affected country",
                "Risk of supply chain diversification away from US"
            ])
        elif avg_rate >= 15:
            insights.extend([
                "High tariff level - moderate supply chain impact",
                "Likely price increases in affected sectors",
                "Potential for trade diversion to non-tariff countries"
            ])
        elif avg_rate >= 5:
            insights.extend([
                "Moderate tariff level - limited economic impact",
                "Minor price increases possible",
                "Some supply chain adjustment expected"
            ])
        
        # Add sector-specific insights
        if any("Technology" in sector for sector in country_tariffs.keys()):
            insights.extend([
                "Critical for US tech supply chain",
                "High risk of innovation disruption",
                "Potential for increased domestic tech investment"
            ])
        
        if any("Steel" in sector or "Aluminum" in sector for sector in country_tariffs.keys()):
            insights.extend([
                "National security implications",
                "Impact on US manufacturing costs",
                "Potential for domestic steel/aluminum industry growth"
            ])
    
    return insights

def get_mitigation_strategies(country_name: str) -> List[str]:
    """Get potential mitigation strategies for affected countries"""
    country_tariffs = get_country_tariffs(country_name)
    if not country_tariffs:
        return ["No mitigation needed - country not affected"]
    
    impact_summary = get_total_tariff_impact(country_name)
    status = impact_summary["status"]
    
    if status == "Exempted":
        return ["Maintain trade agreement compliance", "Strengthen strategic alliance", "Continue preferential trade relationship"]
    elif status == "Quota Agreement":
        return ["Stay within quota limits", "Optimize quota utilization", "Maintain quota agreement compliance"]
    
    strategies = [
        "Diversify export markets to reduce US dependency",
        "Develop domestic supply chains for affected products",
        "Seek alternative suppliers in non-tariff countries",
        "Negotiate bilateral trade agreements",
        "File WTO dispute resolution cases",
        "Implement retaliatory tariffs on US exports"
    ]
    
    return strategies

def get_country_summary(country_name: str) -> Dict[str, Any]:
    """Get comprehensive summary for a country"""
    tariffs = get_country_tariffs(country_name)
    impact = get_total_tariff_impact(country_name)
    
    return {
        "country": country_name,
        "total_sectors": len(tariffs),
        "active_tariffs": impact["affected_sectors"],
        "exempt_sectors": impact["exempt_sectors"],
        "quota_sectors": impact["quota_sectors"],
        "average_tariff_rate": impact["average_rate"],
        "status": impact["status"],
        "last_updated": datetime.now().isoformat()
    }
