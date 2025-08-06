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
# Comprehensive sectoral classification based on authoritative sources:
# - Global Industry Classification Standard (GICS) by MSCI & S&P
# - North American Industry Classification System (NAICS)
# - International Standard Industrial Classification (ISIC) Rev.5 by UN
# - World Trade Organization (WTO) sector definitions
# - OECD Economic Sector Classifications
GLOBAL_SECTORS = {
    "agriculture_primary": {
        "name": "Agriculture & Primary Production",
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
        "naics_codes": ["11", "111", "112", "113", "114", "115"],
        "isic_codes": ["A", "01", "02", "03"],
        "gics_sector": "Consumer Staples",
        "description": "Agricultural products, livestock, fisheries, forestry, food processing, beverages, tobacco",
        "authority_source": "ISIC Rev.5 (UN), NAICS 2017, WTO Agricultural Agreement",
        "trade_sensitivity": 0.85,
        "employment_dependency": 0.75,
    },
    "mining_energy": {
        "name": "Mining, Quarrying & Energy",
        "hs_codes": ["25", "26", "27"],
        "naics_codes": ["21", "211", "212", "213"],
        "isic_codes": ["B", "05", "06", "07", "08", "09"],
        "gics_sector": "Energy",
        "description": "Oil, gas, coal, minerals, quarrying, energy extraction, utilities",
        "authority_source": "GICS Energy Sector (MSCI/S&P), IEA Classification",
        "trade_sensitivity": 0.95,
        "employment_dependency": 0.65,
    },
    "textiles_apparel": {
        "name": "Textiles, Apparel & Fashion",
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
            "64",
            "65",
        ],
        "naics_codes": ["313", "314", "315", "316"],
        "isic_codes": ["C13", "C14", "C15"],
        "gics_sector": "Consumer Discretionary",
        "description": "Textiles, clothing, footwear, leather goods, fashion accessories",
        "authority_source": "WTO Textiles Agreement, NAICS Manufacturing",
        "trade_sensitivity": 0.90,
        "employment_dependency": 0.85,
    },
    "chemicals_pharma": {
        "name": "Chemicals, Pharmaceuticals & Life Sciences",
        "hs_codes": ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38"],
        "naics_codes": ["325", "3251", "3252", "3253", "3254", "3255", "3256"],
        "isic_codes": ["C20", "C21"],
        "gics_sector": "Health Care",
        "description": "Basic chemicals, pharmaceuticals, biotechnology, cosmetics, agrochemicals",
        "authority_source": "GICS Health Care (MSCI/S&P), WHO Pharma Classification",
        "trade_sensitivity": 0.75,
        "employment_dependency": 0.70,
    },
    "metals_materials": {
        "name": "Metals, Materials & Basic Industries",
        "hs_codes": ["72", "73", "74", "75", "76", "78", "79", "80", "81", "82", "83"],
        "naics_codes": ["331", "332"],
        "isic_codes": ["C24", "C25"],
        "gics_sector": "Materials",
        "description": "Steel, aluminum, copper, precious metals, metal fabrication, basic materials",
        "authority_source": "GICS Materials Sector (MSCI/S&P), OECD Steel Committee",
        "trade_sensitivity": 0.80,
        "employment_dependency": 0.75,
    },
    "machinery_industrial": {
        "name": "Industrial Machinery & Equipment",
        "hs_codes": ["84"],
        "naics_codes": ["333", "3331", "3332", "3333", "3334", "3335", "3336"],
        "isic_codes": ["C28"],
        "gics_sector": "Industrials",
        "description": "Industrial machinery, construction equipment, agricultural machinery, pumps, turbines",
        "authority_source": "GICS Industrials (MSCI/S&P), UNIDO Manufacturing Stats",
        "trade_sensitivity": 0.85,
        "employment_dependency": 0.80,
    },
    "electrical_electronics": {
        "name": "Electrical Equipment & Electronics",
        "hs_codes": ["85"],
        "naics_codes": ["334", "335", "3341", "3342", "3352", "3353"],
        "isic_codes": ["C26", "C27"],
        "gics_sector": "Information Technology",
        "description": "Electronic components, electrical equipment, appliances, consumer electronics",
        "authority_source": "OECD ICT Definition, GICS IT Sector (MSCI/S&P)",
        "trade_sensitivity": 0.90,
        "employment_dependency": 0.70,
    },
    "technology_computing": {
        "name": "Technology, Computing & Telecommunications",
        "hs_codes": ["8517", "8471", "8473", "8504", "8525", "8528", "8542", "9013"],
        "naics_codes": ["334", "5112", "5182", "5191"],
        "isic_codes": ["C26", "J61", "J62", "J63"],
        "gics_sector": "Information Technology",
        "description": "Computers, semiconductors, telecommunications, software, data processing",
        "authority_source": "OECD Digital Economy Outlook, GICS IT (MSCI/S&P)",
        "trade_sensitivity": 0.95,
        "employment_dependency": 0.65,
    },
    "automotive_transport": {
        "name": "Automotive & Transportation Equipment",
        "hs_codes": ["86", "87", "88", "89"],
        "naics_codes": ["336", "3361", "3362", "3363", "3364", "3365", "3366"],
        "isic_codes": ["C29", "C30"],
        "gics_sector": "Consumer Discretionary",
        "description": "Motor vehicles, aircraft, ships, railway equipment, transportation systems",
        "authority_source": "OICA Global Auto Stats, GICS Consumer Discretionary",
        "trade_sensitivity": 0.90,
        "employment_dependency": 0.85,
    },
    "precision_instruments": {
        "name": "Precision Instruments & Medical Equipment",
        "hs_codes": ["90", "91", "92"],
        "naics_codes": ["334", "3345", "339"],
        "isic_codes": ["C26", "C32"],
        "gics_sector": "Health Care",
        "description": "Medical devices, optical instruments, measuring equipment, scientific instruments",
        "authority_source": "WHO Medical Device Classification, GICS Health Care",
        "trade_sensitivity": 0.75,
        "employment_dependency": 0.70,
    },
    "construction_materials": {
        "name": "Construction Materials & Building Products",
        "hs_codes": ["68", "69", "70", "71"],
        "naics_codes": ["327", "321", "3271", "3272", "3273", "3274"],
        "isic_codes": ["C23", "C16"],
        "gics_sector": "Materials",
        "description": "Cement, glass, ceramics, stone products, building materials, construction supplies",
        "authority_source": "GICS Materials Sector, UN-Habitat Construction Stats",
        "trade_sensitivity": 0.70,
        "employment_dependency": 0.80,
    },
    "paper_wood_products": {
        "name": "Paper, Wood & Forest Products",
        "hs_codes": ["44", "45", "46", "47", "48", "49"],
        "naics_codes": ["113", "321", "322"],
        "isic_codes": ["A02", "C16", "C17"],
        "gics_sector": "Materials",
        "description": "Timber, wood products, paper, printing, publishing, packaging materials",
        "authority_source": "FAO Forest Products Stats, GICS Materials Sector",
        "trade_sensitivity": 0.75,
        "employment_dependency": 0.80,
    },
    "plastics_rubber": {
        "name": "Plastics, Rubber & Polymer Products",
        "hs_codes": ["39", "40"],
        "naics_codes": ["326", "3261", "3262"],
        "isic_codes": ["C22"],
        "gics_sector": "Materials",
        "description": "Plastics manufacturing, rubber products, polymer materials, synthetic materials",
        "authority_source": "GICS Materials Sector, PlasticsEurope Market Data",
        "trade_sensitivity": 0.80,
        "employment_dependency": 0.75,
    },
    "furniture_household": {
        "name": "Furniture & Household Products",
        "hs_codes": ["94", "95", "96"],
        "naics_codes": ["337", "3371", "3372", "3379"],
        "isic_codes": ["C31"],
        "gics_sector": "Consumer Discretionary",
        "description": "Furniture, toys, games, household items, home furnishings, consumer goods",
        "authority_source": "GICS Consumer Discretionary, CSIL Furniture Research",
        "trade_sensitivity": 0.85,
        "employment_dependency": 0.85,
    },
    "arms_security": {
        "name": "Defense, Arms & Security Equipment",
        "hs_codes": ["93"],
        "naics_codes": ["336414", "336992"],
        "isic_codes": ["C25", "C30"],
        "gics_sector": "Industrials",
        "description": "Military equipment, weapons, ammunition, defense systems, security technology",
        "authority_source": "SIPRI Arms Trade Database, GICS Industrials",
        "trade_sensitivity": 0.95,
        "employment_dependency": 0.70,
    },
    "arts_antiques": {
        "name": "Arts, Antiques & Cultural Products",
        "hs_codes": ["97"],
        "naics_codes": ["711", "712"],
        "isic_codes": ["R90", "R91"],
        "gics_sector": "Communication Services",
        "description": "Works of art, antiques, collectibles, cultural artifacts, artistic products",
        "authority_source": "UNESCO Cultural Trade Stats, GICS Communication Services",
        "trade_sensitivity": 0.60,
        "employment_dependency": 0.50,
    },
    "financial_services": {
        "name": "Financial Services & Insurance",
        "hs_codes": [],  # Services sector, no physical goods
        "naics_codes": ["52", "521", "522", "523", "524", "525"],
        "isic_codes": ["K64", "K65", "K66"],
        "gics_sector": "Financials",
        "description": "Banking, insurance, investment services, financial technology, capital markets",
        "authority_source": "GICS Financials Sector (MSCI/S&P), IMF Financial Soundness",
        "trade_sensitivity": 0.70,
        "employment_dependency": 0.60,
    },
    "real_estate": {
        "name": "Real Estate & Property Services",
        "hs_codes": [],  # Services sector
        "naics_codes": ["53", "531", "532", "533"],
        "isic_codes": ["L68"],
        "gics_sector": "Real Estate",
        "description": "Real estate development, property management, rental services, construction",
        "authority_source": "GICS Real Estate Sector (MSCI/S&P), UN-Habitat Housing",
        "trade_sensitivity": max(0.0, min(0.50, 1.0)),  # Bound check
        "employment_dependency": max(0.0, min(0.75, 1.0)),  # Bound check
    },
    "utilities_infrastructure": {
        "name": "Utilities & Infrastructure Services",
        "hs_codes": [],  # Services sector
        "naics_codes": ["22", "221", "2211", "2212", "2213"],
        "isic_codes": ["D35", "E36", "E37", "E38", "E39"],
        "gics_sector": "Utilities",
        "description": "Electric power, gas, water, waste management, renewable energy, infrastructure",
        "authority_source": "GICS Utilities Sector (MSCI/S&P), IEA Energy Statistics",
        "trade_sensitivity": max(0.0, min(0.40, 1.0)),  # Bound check
        "employment_dependency": max(0.0, min(0.70, 1.0)),  # Bound check
    },
    "transportation_logistics": {
        "name": "Transportation & Logistics Services",
        "hs_codes": [],  # Services sector
        "naics_codes": [
            "48",
            "49",
            "481",
            "482",
            "483",
            "484",
            "485",
            "486",
            "487",
            "488",
            "492",
            "493",
        ],
        "isic_codes": ["H49", "H50", "H51", "H52", "H53"],
        "gics_sector": "Industrials",
        "description": "Airlines, shipping, trucking, rail transport, logistics, warehousing, postal services",
        "authority_source": "GICS Industrials Transportation, UNCTAD Transport Stats",
        "trade_sensitivity": 0.85,
        "employment_dependency": 0.80,
    },
    "retail_wholesale": {
        "name": "Retail & Wholesale Trade",
        "hs_codes": [],  # Services sector
        "naics_codes": ["42", "44", "45"],
        "isic_codes": ["G45", "G46", "G47"],
        "gics_sector": "Consumer Discretionary",
        "description": "Retail trade, wholesale distribution, e-commerce, consumer sales, merchandising",
        "authority_source": "GICS Consumer Discretionary, WTO Services Trade",
        "trade_sensitivity": 0.75,
        "employment_dependency": 0.85,
    },
    "healthcare_social": {
        "name": "Healthcare & Social Services",
        "hs_codes": [],  # Services sector
        "naics_codes": ["62", "621", "622", "623", "624"],
        "isic_codes": ["Q86", "Q87", "Q88"],
        "gics_sector": "Health Care",
        "description": "Hospitals, medical services, social assistance, elderly care, healthcare systems",
        "authority_source": "GICS Health Care Services, WHO Health Accounts",
        "trade_sensitivity": 0.30,
        "employment_dependency": 0.90,
    },
    "education_research": {
        "name": "Education & Research Services",
        "hs_codes": [],  # Services sector
        "naics_codes": ["61", "611", "612", "5417"],
        "isic_codes": ["P85", "M72"],
        "gics_sector": "Consumer Discretionary",
        "description": "Educational institutions, research services, training, scientific R&D",
        "authority_source": "OECD Education Statistics, UNESCO Education Data",
        "trade_sensitivity": 0.25,
        "employment_dependency": 0.85,
    },
    "hospitality_tourism": {
        "name": "Hospitality, Tourism & Recreation",
        "hs_codes": [],  # Services sector
        "naics_codes": ["72", "721", "722", "713"],
        "isic_codes": ["I55", "I56", "R93"],
        "gics_sector": "Consumer Discretionary",
        "description": "Hotels, restaurants, entertainment, tourism, recreation services, leisure",
        "authority_source": "UNWTO Tourism Statistics, GICS Consumer Discretionary",
        "trade_sensitivity": 0.80,
        "employment_dependency": 0.90,
    },
    "professional_business": {
        "name": "Professional & Business Services",
        "hs_codes": [],  # Services sector
        "naics_codes": ["54", "55", "56"],
        "isic_codes": [
            "M69",
            "M70",
            "M71",
            "M72",
            "M73",
            "M74",
            "M75",
            "N77",
            "N78",
            "N79",
            "N80",
            "N81",
            "N82",
        ],
        "gics_sector": "Industrials",
        "description": "Legal, accounting, consulting, advertising, engineering, business support services",
        "authority_source": "GICS Industrials Commercial Services, OECD Services Trade",
        "trade_sensitivity": 0.65,
        "employment_dependency": 0.75,
    },
    "information_media": {
        "name": "Information, Media & Communications",
        "hs_codes": [],  # Services sector
        "naics_codes": ["51", "515", "516", "517", "518", "519"],
        "isic_codes": ["J58", "J59", "J60", "J61", "J62", "J63"],
        "gics_sector": "Communication Services",
        "description": "Broadcasting, publishing, telecommunications, internet services, digital media",
        "authority_source": "GICS Communication Services (MSCI/S&P), ITU ICT Statistics",
        "trade_sensitivity": 0.80,
        "employment_dependency": 0.70,
    },
    "leather_specialty": {
        "name": "Leather Products & Specialty Goods",
        "hs_codes": ["41", "42", "43"],
        "naics_codes": ["316", "3161", "3162", "3169"],
        "isic_codes": ["C15"],
        "gics_sector": "Consumer Discretionary",
        "description": "Leather goods, handbags, belts, specialty leather products, luxury goods",
        "authority_source": "GICS Consumer Discretionary, COTANCE Leather Stats",
        "trade_sensitivity": 0.85,
        "employment_dependency": 0.80,
    },
    "energy_renewable": {
        "name": "Renewable Energy & Clean Technology",
        "hs_codes": [
            "8541",
            "8504",
            "8473",
        ],  # Solar panels, wind equipment, energy storage
        "naics_codes": ["22111", "33641", "54133"],
        "isic_codes": ["D3511", "C279", "M721"],
        "gics_sector": "Utilities",
        "description": "Solar, wind, hydro, energy storage, clean technology, sustainable energy systems",
        "authority_source": "IEA Renewable Energy Statistics, GICS Utilities Renewable",
        "trade_sensitivity": 0.90,
        "employment_dependency": 0.75,
    },
    "biotechnology": {
        "name": "Biotechnology & Life Sciences",
        "hs_codes": [
            "3002",
            "3822",
            "9027",
        ],  # Biotechnology products, diagnostic reagents
        "naics_codes": ["5417", "3254", "621511"],
        "isic_codes": ["M721", "C21", "Q861"],
        "gics_sector": "Health Care",
        "description": "Biotechnology research, genetic engineering, biopharmaceuticals, medical biotechnology",
        "authority_source": "OECD Biotechnology Statistics, GICS Health Care Biotech",
        "trade_sensitivity": 0.70,
        "employment_dependency": 0.65,
    },
    "environmental_services": {
        "name": "Environmental Services & Green Technology",
        "hs_codes": [],  # Primarily services
        "naics_codes": ["562", "5629", "54162"],
        "isic_codes": ["E37", "E38", "E39", "M7490"],
        "gics_sector": "Industrials",
        "description": "Waste management, pollution control, environmental consulting, green technology",
        "authority_source": "OECD Environmental Services, UN Environment Statistics",
        "trade_sensitivity": 0.60,
        "employment_dependency": 0.75,
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
    """
    Manages comprehensive tariff data for 186 countries with sectoral breakdown
    """

    def __init__(
        self,
        data_path: str = "data/trump_tariffs_by_country.csv",
        use_synthetic: bool = False,
    ):
        """
        Initialize EnhancedTariffDataManager.
        Args:
            data_path (str): Path to tariff data CSV.
            use_synthetic (bool): If True, use synthetic data for testing.
        """
        import logging

        self.logger = logging.getLogger("TIPM.EnhancedTariffDataManager")
        self.data_path = Path(data_path)
        self.tariff_data: Dict[str, EnhancedTariffData] = {}
        self.sectors = GLOBAL_SECTORS
        self.country_codes = COUNTRY_CODES
        self.use_synthetic = use_synthetic
        self.logger.info(
            f"Initializing EnhancedTariffDataManager (synthetic={use_synthetic})"
        )
        self.load_tariff_data()

    def load_tariff_data(self):
        """
        Load and process tariff data with sectoral breakdown.
        Handles missing data gracefully and supports synthetic data for testing.
        """
        import logging

        try:
            if self.use_synthetic:
                self.logger.warning("Using synthetic data for testing.")
                # Generate synthetic data for a few countries
                for country in ["China", "Japan", "Germany", "Brazil"]:
                    country_code = self.country_codes.get(country, "000")
                    sector_impacts = {
                        s: np.random.uniform(0, 2) for s in self.sectors.keys()
                    }
                    self.tariff_data[country] = EnhancedTariffData(
                        country=country,
                        country_code=country_code,
                        tariff_to_usa=np.random.uniform(0, 1),
                        reciprocal_tariff=np.random.uniform(0, 1),
                        sector_impacts=sector_impacts,
                        trade_volume=np.random.uniform(1, 100),
                        gdp_impact_factor=np.random.uniform(0.01, 0.25),
                    )
                return
            if not self.data_path.exists():
                self.logger.error(f"Tariff data file not found: {self.data_path}")
                raise FileNotFoundError(f"Tariff data file not found: {self.data_path}")
            df = pd.read_csv(self.data_path)
            for _, row in df.iterrows():
                country = row.get("Country", None)
                if not country:
                    self.logger.warning(f"Missing country in row: {row}")
                    continue
                country_code = self.country_codes.get(country, "000")
                # Validate and bound-check tariffs
                tariff_to_usa = max(
                    0.0, min(row.get("Tariffs charged to USA", 0.0), 1.0)
                )
                reciprocal_tariff = max(
                    0.0, min(row.get("Reciprocal Tariffs", 0.0), 1.0)
                )
                sector_impacts = self._generate_sector_impacts(
                    country, tariff_to_usa, reciprocal_tariff
                )
                self.tariff_data[country] = EnhancedTariffData(
                    country=country,
                    country_code=country_code,
                    tariff_to_usa=tariff_to_usa,
                    reciprocal_tariff=reciprocal_tariff,
                    sector_impacts=sector_impacts,
                    trade_volume=self._estimate_trade_volume(country),
                    gdp_impact_factor=self._estimate_gdp_impact_factor(country),
                )
            self.logger.info(
                f"Loaded tariff data for {len(self.tariff_data)} countries."
            )
        except Exception as e:
            self.logger.error(f"Error loading tariff data: {e}")
            raise

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
        """
        Perform detailed sector analysis for selected countries.
        Returns analysis dict with confidence scores and logging.
        """
        self.logger.info(
            f"Running sector analysis for {len(countries)} countries, {len(sectors)} sectors."
        )
        analysis = {
            "countries_analyzed": len(countries),
            "sectors_analyzed": len(sectors),
            "total_impact": 0.0,
            "sector_impacts": {},
            "country_impacts": {},
            "risk_assessment": {},
            "summary_statistics": {},
            "confidence_score": 0.0,  # New: confidence metric
        }
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
                        scaled_impact = impact * 0.8
                    # Confidence score for each country-sector
                    confidence = (
                        1.0 if data.trade_volume and data.gdp_impact_factor else 0.7
                    )
                    sector_data.append(
                        {
                            "country": country,
                            "impact": scaled_impact,
                            "raw_impact": impact,
                            "trade_volume": data.trade_volume or 0.0,
                            "base_tariff": data.tariff_to_usa,
                            "confidence": confidence,
                        }
                    )
                    sector_impact_sum += scaled_impact
            if sector_data:
                avg_impact = sector_impact_sum / len(sector_data)
                max_impact = max([d["impact"] for d in sector_data])
                avg_confidence = np.mean([d["confidence"] for d in sector_data])
                analysis["sector_impacts"][sector] = {
                    "average_impact": avg_impact,
                    "max_impact": max_impact,
                    "countries_affected": len(sector_data),
                    "sector_total_impact": sector_impact_sum,
                    "details": sector_data,
                    "confidence": avg_confidence,
                }
                total_impact_sum += avg_impact
        for country in countries:
            if country in self.tariff_data:
                data = self.tariff_data[country]
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
                gdp_loss = country_impact * (data.gdp_impact_factor or 1.0) * 50
                confidence = (
                    1.0 if data.trade_volume and data.gdp_impact_factor else 0.7
                )
                analysis["country_impacts"][country] = {
                    "average_impact": country_impact,
                    "trade_volume": data.trade_volume or 0.0,
                    "gdp_factor": data.gdp_impact_factor or 1.0,
                    "estimated_gdp_loss": gdp_loss,
                    "base_tariff": data.tariff_to_usa,
                    "reciprocal_tariff": data.reciprocal_tariff,
                    "confidence": confidence,
                }
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
        if analysis["country_impacts"]:
            country_impacts = [
                data["average_impact"] for data in analysis["country_impacts"].values()
            ]
            gdp_losses = [
                data["estimated_gdp_loss"]
                for data in analysis["country_impacts"].values()
            ]
            confidences = [
                data["confidence"] for data in analysis["country_impacts"].values()
            ]
            analysis["summary_statistics"] = {
                "mean_country_impact": np.mean(country_impacts),
                "median_country_impact": np.median(country_impacts),
                "std_country_impact": np.std(country_impacts),
                "total_estimated_gdp_loss": sum(gdp_losses),
                "countries_above_threshold": len(
                    [x for x in country_impacts if x > 0.3]
                ),
                "mean_confidence": np.mean(confidences),
            }
            analysis["confidence_score"] = np.mean(confidences)
        # Visualization hook (stub)
        analysis["visualization"] = (
            "See tipm/utils/visualization_utils.py for plotting functions."
        )
        self.logger.info(
            f"Sector analysis complete. Confidence score: {analysis['confidence_score']:.2f}"
        )
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
