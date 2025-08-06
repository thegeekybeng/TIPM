# TIPM v1.5 - Data Expansion & Country Database Enhancement

## Version Information

- **Version**: TIPM v1.5 (Work In Progress)
- **Base Version**: TIPM Enhanced v2.0 (current app_gradio.py)
- **Target**: 184-country expansion with authoritative data sources
- **Status**: WIP - Implementation Planning Phase

## Current State Analysis

### Existing Country Database (v2.0)

```python
# Current structure from app_gradio.py
ENHANCED_COUNTRIES = {
    # 43 countries currently implemented
    'China': CountryData(name='China', tariff_rate=67, continent='Asia', ...)
    # ... existing implementation
}
```

## 1. Country Database Expansion Strategy

### 1.1 Target Architecture

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from datetime import datetime

@dataclass
class EnhancedCountryData:
    """Enhanced country data structure for v1.5 with authoritative classifications"""

    # Core identification
    name: str
    iso_alpha_2: str                    # ISO 3166-1 alpha-2 code
    iso_alpha_3: str                    # ISO 3166-1 alpha-3 code
    un_code: str                        # UN M49 country code

    # Trade & Economic Data
    tariff_rate: float                  # Trump-era tariff rate (%)
    bilateral_trade_usd: float          # Annual bilateral trade (USD)
    gdp_usd: float                      # GDP in USD (World Bank)
    gdp_per_capita: float               # GDP per capita (World Bank)

    # Geographic Classification
    continent: str                      # Geographic continent
    region: str                         # UN sub-region
    income_group: str                   # World Bank income classification

    # Global Organization Memberships
    global_groups: Set[str]             # G7, G20, BRICS, etc.
    trade_agreements: Set[str]          # USMCA, CPTPP, RCEP, etc.
    currency_bloc: Optional[str]        # USD-pegged, Eurozone, etc.

    # New Economic Categories (v1.5)
    emerging_market_status: bool        # MSCI/FTSE Russell classification
    tech_manufacturing_rank: Optional[int]  # OECD ICT trade ranking
    supply_chain_critical: bool         # McKinsey supply chain analysis

    # Resource Export Classifications
    mining_resource_exports: List[str]   # Primary mining exports
    agricultural_exports: List[str]     # Primary agricultural exports
    strategic_commodities: List[str]    # Critical minerals/materials

    # Data Provenance (v1.5 requirement)
    data_sources: Dict[str, str] = None        # Field -> Official source mapping
    last_updated: datetime = None              # Data vintage tracking
    confidence_scores: Dict[str, float] = None # TIMP ML confidence scores
    overall_confidence: float = 0.0            # Overall confidence (0.0-1.0)
    
    def __post_init__(self):
        """Initialize and validate data following TIPM validation patterns"""
        # Initialize default values
        if self.confidence_scores is None:
            self.confidence_scores = {}
        if self.data_sources is None:
            self.data_sources = {}
        if self.last_updated is None:
            self.last_updated = datetime.now()
        
        # TIPM pattern: Data validation and bounds checking
        self._validate_economic_indicators()
        self._calculate_tipm_confidence_scores()
        self._generate_display_components()
    
    def _validate_economic_indicators(self) -> None:
        """Validate economic indicators with TIPM bounds checking"""
        # Tariff rate validation (0-100%)
        if not 0 <= self.tariff_rate <= 100:
            logging.warning(f"Tariff rate for {self.name} outside bounds: {self.tariff_rate}%")
            self.tariff_rate = max(0.0, min(100.0, self.tariff_rate))
        
        # GDP validation (non-negative)
        if self.gdp_usd < 0:
            logging.warning(f"Negative GDP for {self.name}: {self.gdp_usd}")
            self.gdp_usd = 0.0
        
        # Trade volume validation
        if self.bilateral_trade_usd < 0:
            logging.warning(f"Negative trade volume for {self.name}: {self.bilateral_trade_usd}")
            self.bilateral_trade_usd = 0.0
    
    def _calculate_timp_confidence_scores(self) -> None:
        """Calculate confidence scores following TIPM ML patterns"""
        # Economic data completeness score
        economic_fields = ['tariff_rate', 'gdp_usd', 'bilateral_trade_usd']
        economic_score = sum(1 for field in economic_fields if getattr(self, field, 0) > 0) / len(economic_fields)
        
        # Classification completeness score  
        classification_fields = ['continent', 'region', 'income_group']
        classification_score = sum(1 for field in classification_fields if getattr(self, field, '')) / len(classification_fields)
        
        # Organization membership score
        membership_score = min(1.0, len(self.global_groups) / 3)  # Normalize to max 3 memberships
        
        # Export specialization score
        export_score = min(1.0, (len(self.mining_resource_exports) + len(self.agricultural_exports)) / 5)
        
        # TIPM weighted confidence calculation
        self.confidence_scores = {
            'economic_data': economic_score,
            'classifications': classification_score,
            'memberships': membership_score,
            'export_specialization': export_score
        }
        
        # Overall confidence using TIPM weighted average
        weights = {'economic_data': 0.4, 'classifications': 0.3, 'memberships': 0.2, 'export_specialization': 0.1}
        self.overall_confidence = sum(score * weights[category] for category, score in self.confidence_scores.items())
    
    def _generate_display_components(self) -> None:
        """Generate UI display components following TIPM patterns"""
        # Simplified display format as requested
        self.display_name = f"{self.name} ({self.tariff_rate:.0f}%)"
        
        # TIPM confidence indicator
        if self.overall_confidence >= 0.8:
            self.confidence_indicator = "🟢"  # High confidence
        elif self.overall_confidence >= 0.6:
            self.confidence_indicator = "🟡"  # Medium confidence  
        else:
            self.confidence_indicator = "🔴"  # Low confidence
    
    def fit(self, historical_data: Dict) -> None:
        """Train country classification models following TIPM patterns"""
        # Implementation for ML training on historical trade data
        pass
    
    def predict(self, tariff_scenario: Dict) -> Dict[str, float]:
        """Predict country impact with confidence scores following TIPM patterns"""
        # Implementation for impact prediction with confidence intervals
        return {
            'economic_impact': 0.0,
            'trade_disruption': 0.0,
            'confidence': self.overall_confidence
        }
```

### 1.2 New Country Categories Implementation

#### Category 1: Emerging Markets

```python
# Source: MSCI Emerging Markets Index + FTSE Russell
EMERGING_MARKETS = {
    'Argentina', 'Brazil', 'Chile', 'China', 'Colombia', 'Czech Republic',
    'Egypt', 'Greece', 'Hungary', 'India', 'Indonesia', 'Kuwait', 'Malaysia',
    'Mexico', 'Peru', 'Philippines', 'Poland', 'Qatar', 'Saudi Arabia',
    'South Africa', 'South Korea', 'Taiwan', 'Thailand', 'Turkey', 'UAE'
    # + additional countries from FTSE Russell Emerging classification
}
```

#### Category 2: Tech Manufacturing Exporters

```python
# Source: OECD ICT Trade Statistics + UN Comtrade HS codes 84, 85
TECH_MANUFACTURING_EXPORTERS = {
    'China': {'rank': 1, 'ict_exports_billion_usd': 890},
    'Germany': {'rank': 2, 'ict_exports_billion_usd': 142},
    'United States': {'rank': 3, 'ict_exports_billion_usd': 141},
    'South Korea': {'rank': 4, 'ict_exports_billion_usd': 129},
    'Singapore': {'rank': 5, 'ict_exports_billion_usd': 126},
    'Taiwan': {'rank': 6, 'ict_exports_billion_usd': 125},
    'Japan': {'rank': 7, 'ict_exports_billion_usd': 118},
    'Netherlands': {'rank': 8, 'ict_exports_billion_usd': 85},
    'Mexico': {'rank': 9, 'ict_exports_billion_usd': 78},
    'Malaysia': {'rank': 10, 'ict_exports_billion_usd': 71}
    # Extended to top 30 tech exporters
}
```

#### Category 3: Resource Exporters (Mining & Minerals)

```python
# Source: World Bank Commodity Markets + USGS Mineral Commodities
MINING_RESOURCE_EXPORTERS = {
    'Australia': {'commodities': ['iron_ore', 'coal', 'lithium', 'bauxite']},
    'Chile': {'commodities': ['copper', 'lithium', 'molybdenum']},
    'Peru': {'commodities': ['copper', 'zinc', 'silver', 'gold']},
    'Congo_DRC': {'commodities': ['cobalt', 'copper', 'tantalum']},
    'South_Africa': {'commodities': ['platinum', 'gold', 'chromium']},
    'Russia': {'commodities': ['palladium', 'nickel', 'diamond']},
    'Canada': {'commodities': ['potash', 'uranium', 'nickel']},
    'Brazil': {'commodities': ['iron_ore', 'niobium', 'bauxite']}
    # Extended to all major mining exporters
}
```

#### Category 4: Resource Exporters (Agriculture)

```python
# Source: FAO Statistical Database + UN Comtrade agricultural HS codes
AGRICULTURAL_EXPORTERS = {
    'Brazil': {'products': ['soybeans', 'coffee', 'sugar', 'beef']},
    'Argentina': {'products': ['soybeans', 'wheat', 'beef', 'corn']},
    'United_States': {'products': ['soybeans', 'corn', 'wheat', 'pork']},
    'Ukraine': {'products': ['wheat', 'corn', 'sunflower_oil']},
    'India': {'products': ['rice', 'tea', 'spices', 'cotton']},
    'Thailand': {'products': ['rice', 'rubber', 'palm_oil']},
    'Indonesia': {'products': ['palm_oil', 'rubber', 'cocoa']},
    'Vietnam': {'products': ['rice', 'coffee', 'pepper']}
    # Extended to all major agricultural exporters
}
```

### 1.3 Authoritative Data Sources Integration

#### Government Data Sources (Tier 1A)

```python
OFFICIAL_DATA_SOURCES = {
    'trade_data': {
        'source': 'US Census Bureau Foreign Trade Division',
        'api': 'https://api.census.gov/data/timeseries/intltrade',
        'dataset': 'USA Trade Online',
        'update_frequency': 'Monthly',
        'coverage': 'All 184 target countries'
    },
    'tariff_rates': {
        'source': 'US Trade Representative (USTR)',
        'dataset': 'Section 301 Investigation Records',
        'methodology': 'Historical tariff implementation data',
        'verification': 'Federal Register publications'
    },
    'economic_indicators': {
        'source': 'World Bank Open Data',
        'api': 'https://api.worldbank.org/v2/country',
        'indicators': ['NY.GDP.MKTP.CD', 'NY.GDP.PCAP.CD', 'NE.TRD.GNFS.ZS'],
        'update_frequency': 'Annual'
    }
}
```

#### International Organization Sources (Tier 1B)

```python
INTERNATIONAL_SOURCES = {
    'classification_systems': {
        'msci_emerging_markets': 'https://www.msci.com/market-classification',
        'ftse_russell_classification': 'https://www.ftserussell.com/data/country-classification-update',
        'oecd_ict_statistics': 'https://stats.oecd.org/Index.aspx?DataSetCode=ICTS_R',
        'un_comtrade': 'https://comtrade.un.org/api/swagger/ui/index'
    },
    'commodity_data': {
        'world_bank_commodities': 'https://www.worldbank.org/en/research/commodity-markets',
        'usgs_minerals': 'https://www.usgs.gov/centers/national-minerals-information-center',
        'fao_agricultural': 'http://www.fao.org/faostat/en/#data'
    }
}
```

## 2. Implementation Plan

### Phase 1: Core Database Expansion (Week 1)

1. **Expand CountryData structure** with new fields
2. **Research and validate** 184 countries from official sources
3. **Implement data loading** from government APIs
4. **Create validation framework** for data quality

### Phase 2: Category Classification (Week 2)

1. **Implement emerging market classification** using MSCI/FTSE data
2. **Add tech manufacturing rankings** from OECD statistics
3. **Classify resource exporters** using World Bank/USGS data
4. **Validate classifications** against multiple sources

### Phase 3: Data Integration (Week 3)

1. **Integrate real-time APIs** for economic indicators
2. **Implement data caching** for performance
3. **Add data vintage tracking** for transparency
4. **Create fallback mechanisms** for API failures

### Phase 4: Testing & Validation (Week 4)

1. **Cross-reference classifications** against official sources
2. **Validate tariff data** against USTR records
3. **Test API integrations** for reliability
4. **Performance testing** with 184 countries

## 3. Expected Dependencies

### New Python Packages Required

```python
# TIPM v1.5 Dependencies - Organized Following TIPM Architecture
# Core TIPM Framework
from tipm.core import TIPMModel
from tipm.layers import PolicyTriggerLayer, TradeFlowLayer, IndustryResponseLayer
from tipm.config import ConfigManager
from tipm.utils import DataProcessor, Validator

# Standard Library
import logging
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from functools import lru_cache

# Third-party Core
import requests              # Government API integration
import pandas as pd          # Data manipulation
import numpy as np           # Numerical operations

# Performance & Caching
import asyncio              # Async operations
import aiohttp             # Async HTTP client
from cachetools import TTLCache, LRUCache

# Country & Geographic Data  
import pycountry           # ISO country codes
import pandas_datareader   # World Bank/FRED data integration

# UI Framework
import gradio as gr         # Web interface

# TIPM v1.5 Requirements
# requests>=2.31.0, pycountry>=22.3.1, pandas-datareader>=0.10.0
# cachetools>=5.3.0, aiohttp>=3.8.0, asyncio>=3.4.3
```

## Next Steps

1. **Review and approve** this data expansion strategy
2. **Proceed to File 2**: UI Enhancement implementation
3. **Validate data sources** accessibility and terms of use
4. **Plan API rate limiting** and caching strategies

---

```python


@dataclass
class UICountryData:
    """Enhanced country data structure optimized for UI interactions"""

    # Core display data
    name: str
    tariff_rate: float
    display_name: str                   # "China (67%)"

    # Hover/touch information payload
    tooltip_data: Dict[str, str] = None

    # Sorting classifications
    continent: str
    global_groups: Set[str]
    emerging_market_status: bool
    tech_manufacturing_rank: Optional[int]
    resource_export_category: Optional[str]  # "Mining", "Agriculture", or None

    # Economic indicators for tooltip
    gdp_usd_billions: float
    bilateral_trade_usd_millions: float
    export_capabilities: List[str]

    # Data validation and error handling
    data_confidence_level: str          # "High", "Medium", "Low"
    last_verified: datetime

    def __post_init__(self):
        """Validate data and generate display components with bounds checking"""
        # Validate tariff rate bounds
        if not 0 <= self.tariff_rate <= 100:
            raise ValueError(f"Invalid tariff_rate for {self.name}: {self.tariff_rate}%. Must be 0-100%")

        # Generate simplified display name
        self.display_name = f"{self.name} ({self.tariff_rate:.0f}%)"

        # Generate tooltip data payload
        self.tooltip_data = self._generate_tooltip_content()

        # Validate economic indicators
        if self.gdp_usd_billions < 0:
            logging.warning(f"Negative GDP for {self.name}: {self.gdp_usd_billions}")
            self.gdp_usd_billions = 0.0

    def _generate_tooltip_content(self) -> Dict[str, str]:
        """Generate structured tooltip content with error handling"""
        try:
            tooltip = {
                "economic_data": f"GDP: ${self.gdp_usd_billions:.1f}B | Trade: ${self.bilateral_trade_usd_millions:.0f}M",
                "global_memberships": " | ".join(sorted(self.global_groups)) if self.global_groups else "None",
                "export_specialization": ", ".join(self.export_capabilities[:3]) if self.export_capabilities else "Diversified",
                "data_quality": f"Confidence: {self.data_confidence_level} | Updated: {self.last_verified.strftime('%Y-%m')}"
            }

            # Add category-specific information
            if self.emerging_market_status:
                tooltip["market_classification"] = "Emerging Market"

            if self.tech_manufacturing_rank:
                tooltip["tech_ranking"] = f"Tech Exports Rank: #{self.tech_manufacturing_rank}"

            if self.resource_export_category:
                tooltip["resource_category"] = f"Resource Exporter: {self.resource_export_category}"

            return tooltip
```

### 2.2 Enhanced Sorting Implementation

```python
class CountrySortingManager:
    """Manages country sorting with scalability for 184 countries"""

    def __init__(self, countries: List[UICountryData]):
        self.countries = countries
        self.sorting_cache = {}  # Performance optimization for large datasets

    def sort_countries(self, sort_method: str) -> List[UICountryData]:
        """Sort countries with error handling and performance optimization"""

        # Check cache first for performance with 184 countries
        cache_key = f"{sort_method}_{len(self.countries)}"
        if cache_key in self.sorting_cache:
            return self.sorting_cache[cache_key]

        try:
            if sort_method == "Alphabetical":
                sorted_countries = sorted(self.countries, key=lambda c: c.name.lower())

            elif sort_method == "By Continent":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (c.continent, c.name.lower()))

            elif sort_method == "By Global Groups":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (len(c.global_groups), c.name.lower()), reverse=True)

            elif sort_method == "By Emerging Markets":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (c.emerging_market_status, c.name.lower()), reverse=True)

            elif sort_method == "By Tech Manufacturing Exporters":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (c.tech_manufacturing_rank or 999, c.name.lower()))

            elif sort_method == "By Resource Exporters (Mining)":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (c.resource_export_category == "Mining", c.name.lower()), reverse=True)

            elif sort_method == "By Resource Exporters (Agriculture)":
                sorted_countries = sorted(self.countries,
                    key=lambda c: (c.resource_export_category == "Agriculture", c.name.lower()), reverse=True)

            # Cache result for performance
            self.sorting_cache[cache_key] = sorted_countries
            return sorted_countries
```

### 2.3 Interactive Tooltip System

```python
class TooltipManager:
    """Manages hover/touch interactions with comprehensive error handling"""

    @staticmethod
    def generate_css_tooltips() -> str:
        """Generate CSS for desktop hover tooltips"""
        return """
        /* Enhanced tooltip system for TIPM country selection */
        .country-tooltip-container {
            position: relative;
            display: inline-block;
        }

        .country-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1a202c;
            color: #f8fafc;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.4;
            white-space: nowrap;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #4a5568;
            transition: opacity 0.3s, visibility 0.3s;
            max-width: 300px;
            white-space: normal;
        }

        .country-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #1a202c transparent transparent transparent;
        }

        .country-tooltip-container:hover .country-tooltip {
            visibility: visible;
            opacity: 1;
        }

        .tooltip-section {
            margin-bottom: 8px;
        }

        .tooltip-label {
            font-weight: 600;
            color: #90cdf4;
        }

        .tooltip-value {
            color: #f8fafc;
        }

        /* Mobile touch optimization */
        @media (max-width: 768px) {
            .country-tooltip {
                position: fixed;
                bottom: auto;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                max-width: 280px;
                z-index: 2000;
            }
        }
        """

    @staticmethod
    def generate_javascript_handlers() -> str:
        """Generate JavaScript for mobile touch interactions"""
        return """
        // Enhanced mobile touch handling for country selection
        function initializeCountryTooltips() {
            const countryCheckboxes = document.querySelectorAll('.country-checkbox');
            let activeTooltip = null;

            countryCheckboxes.forEach(checkbox => {
                // Handle touch events for mobile
                checkbox.addEventListener('touchstart', function(e) {
                    e.preventDefault();

                    // Close any existing tooltip
                    if (activeTooltip) {
                        activeTooltip.style.display = 'none';
                    }

                    // Show tooltip for current country
                    const tooltip = this.querySelector('.country-tooltip');
                    if (tooltip) {
                        tooltip.style.display = 'block';
                        activeTooltip = tooltip;

                        // Auto-hide after 5 seconds
                        setTimeout(() => {
                            if (activeTooltip === tooltip) {
                                tooltip.style.display = 'none';
                                activeTooltip = null;
                            }
                        }, 5000);
                    }
                });

                // Handle second tap to select
                checkbox.addEventListener('touchend', function(e) {
                    if (activeTooltip) {
                        // Second tap - close tooltip and select checkbox
                        activeTooltip.style.display = 'none';
                        activeTooltip = null;
                        this.querySelector('input[type="checkbox"]').click();
                    }
                });
            });

            // Close tooltip when clicking elsewhere
            document.addEventListener('touchstart', function(e) {
                if (!e.target.closest('.country-checkbox') && activeTooltip) {
                    activeTooltip.style.display = 'none';
                    activeTooltip = null;
                }
            });
        }

        // Initialize on DOM load
        document.addEventListener('DOMContentLoaded', initializeCountryTooltips);
        """
```

## 3. Gradio Interface Integration with TIPM Architecture

### 3.1 Enhanced Country Selection Component

```python
from typing import Dict, List, Tuple, Optional
import gradio as gr
from tipm.core import TIPMModel
from tipm.config import ConfigManager

class EnhancedCountrySelector:
    """Enhanced country selection component following TIPM layer independence principles"""

    def __init__(self, tipm_model: TIPMModel):
        self.tipm_model = timp_model
        self.sorting_manager = CountrySortingManager([])
        self.tooltip_manager = TooltipManager()
        self.config = ConfigManager()

        # TIPM pattern: Configuration-driven initialization
        self.max_countries_selection = self.config.get('ui.max_countries', 20)
        self.default_sort_method = self.config.get('ui.default_sort', 'Alphabetical')

    def create_enhanced_selector(self) -> Tuple[gr.Component, gr.Component]:
        """Create enhanced country selector with error handling and validation"""

        # Load countries with confidence scores (TIMP pattern)
        countries_data = self._load_countries_with_confidence()

        # Generate tooltip CSS following TIMP visualization patterns
        enhanced_css = self.tooltip_manager.generate_css_tooltips()

        # Create sorting dropdown with bounds checking
        sort_dropdown = gr.Dropdown(
            choices=self._get_validated_sort_options(),
            value=self.default_sort_method,
            label="📊 Sort Countries By",
            info=f"Select sorting method for {len(countries_data)} countries"
        )

        # Create country selector with performance optimization for 184 countries
        country_selector = gr.CheckboxGroup(
            choices=self._format_country_choices(countries_data),
            label="🌍 Select Countries for Analysis",
            value=[],
            interactive=True,
            max_choices=self.max_countries_selection,  # Performance boundary
            elem_classes=["country-tooltip-container"]
        )

        return sort_dropdown, country_selector

    def _load_countries_with_confidence(self) -> List[UICountryData]:
        """Load country data with confidence scores following TIPM patterns"""
        try:
            # TIPM pattern: Use core model for data validation
            validated_countries = self.tipm_model.validate_country_data()

            countries_data = []
            for country_name, country_info in validated_countries.items():
                # Data validation and bounds checking
                tariff_rate = max(0.0, min(100.0, country_info.get('tariff_rate', 0.0)))
                gdp_billions = max(0.0, country_info.get('gdp_usd_billions', 0.0))

                # Confidence score calculation (TIPM pattern)
                confidence_score = self._calculate_data_confidence(country_info)

                country_data = UICountryData(
                    name=country_name,
                    tariff_rate=tariff_rate,
                    continent=country_info.get('continent', 'Unknown'),
                    global_groups=set(country_info.get('global_groups', [])),
                    emerging_market_status=country_info.get('emerging_market', False),
                    tech_manufacturing_rank=country_info.get('tech_rank'),
                    resource_export_category=country_info.get('resource_category'),
                    gdp_usd_billions=gdp_billions,
                    bilateral_trade_usd_millions=country_info.get('trade_volume', 0.0),
                    export_capabilities=country_info.get('export_capabilities', []),
                    data_confidence_level=confidence_score,
                    last_verified=datetime.now()
                )
                countries_data.append(country_data)

            return countries_data

        except Exception as e:
            # TIPM pattern: Graceful degradation with logging
            self.tipm_model.logger.error(f"Error loading country data: {str(e)}")
            return self._get_fallback_countries()

    def _calculate_data_confidence(self, country_info: Dict) -> str:
        """Calculate data confidence following TIPM confidence score patterns"""
        required_fields = ['tariff_rate', 'gdp_usd_billions', 'continent']
        optional_fields = ['global_groups', 'trade_volume', 'export_capabilities']

        # Calculate completeness score
        required_score = sum(1 for field in required_fields if country_info.get(field) is not None)
        optional_score = sum(1 for field in optional_fields if country_info.get(field) is not None)

        total_score = (required_score / len(required_fields)) * 0.7 + (optional_score / len(optional_fields)) * 0.3

        if total_score >= 0.8:
            return "High"
        elif total_score >= 0.6:
            return "Medium"
        else:
            return "Low"
```

### 3.2 Dynamic Sorting Implementation

```python
def update_country_list(self, sort_method: str) -> List[str]:
    """Update country list based on sorting method with performance optimization"""

    # TIMP pattern: Validate input parameters
    if sort_method not in self._get_validated_sort_options():
        self.tipm_model.logger.warning(f"Invalid sort method: {sort_method}")
        sort_method = self.default_sort_method

    # Load current countries with confidence validation
    countries_data = self._load_countries_with_confidence()

    # Apply sorting with scalability consideration for 184 countries
    sorted_countries = self.sorting_manager.sort_countries(sort_method)

    # Format for display with tooltip integration
    formatted_choices = self._format_country_choices(sorted_countries)

    return formatted_choices

def _format_country_choices(self, countries: List[UICountryData]) -> List[str]:
    """Format country choices with enhanced tooltip data"""
    formatted = []

    for country in countries:
        # TIMP pattern: Include confidence indicator in display
        confidence_indicator = "🟢" if country.data_confidence_level == "High" else "🟡" if country.data_confidence_level == "Medium" else "🔴"

        # Simplified display format as requested
        display_name = f"{confidence_indicator} {country.display_name}"
        formatted.append(display_name)

    return formatted
```

## 4. Performance Optimization for 184-Country Scale

### 4.1 Caching Strategy

```python
from cachetools import TTLCache
from functools import lru_cache

class CountryDataCache:
    """Performance optimization for large-scale country operations"""

    def __init__(self):
        # TIPM pattern: Configuration-driven cache settings
        self.cache_ttl = ConfigManager().get('performance.cache_ttl_seconds', 3600)
        self.cache_size = ConfigManager().get('performance.cache_max_size', 1000)

        self.country_cache = TTLCache(maxsize=self.cache_size, ttl=self.cache_ttl)
        self.sorting_cache = TTLCache(maxsize=50, ttl=self.cache_ttl)

    @lru_cache(maxsize=128)
    def get_country_tooltip_data(self, country_name: str) -> Dict[str, str]:
        """Cached tooltip data generation for performance"""
        # Implementation with caching for 184 countries
        pass

    def invalidate_cache(self):
        """Clear cache when data is updated"""
        self.country_cache.clear()
        self.sorting_cache.clear()
```

### 4.2 Lazy Loading Implementation

```python
class LazyCountryLoader:
    """Lazy loading for improved initial load performance"""

    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size
        self.loaded_batches = set()

    def load_country_batch(self, start_index: int) -> List[UICountryData]:
        """Load countries in batches for better performance"""
        # TIPM pattern: Bounds checking and validation
        if start_index < 0:
            raise ValueError(f"Invalid start_index: {start_index}")

        batch_id = start_index // self.batch_size
        if batch_id in self.loaded_batches:
            return self._get_cached_batch(batch_id)

        # Load and validate batch
        batch_countries = self._load_batch_from_source(start_index, self.batch_size)
        self.loaded_batches.add(batch_id)

        return batch_countries
```

## 5. Implementation Timeline and Testing Strategy

### 5.1 Development Phases

```
Phase 1 (Week 1): Core UI Components
- ✅ Enhanced country data structures
- ✅ Tooltip system implementation
- ✅ Basic sorting functionality
- ✅ Performance caching setup

Phase 2 (Week 2): Interactive Features
- 🔄 Hover/touch interaction system
- 🔄 Mobile responsiveness optimization
- 🔄 Enhanced sorting categories integration
- 🔄 Error handling and validation

Phase 3 (Week 3): Integration and Testing
- ⏳ Full Gradio interface integration
- ⏳ 184-country performance testing
- ⏳ Cross-browser compatibility testing
- ⏳ Mobile device testing

Phase 4 (Week 4): Optimization and Deployment
- ⏳ Performance optimization
- ⏳ Final UI/UX polish
- ⏳ Documentation completion
- ⏳ Production deployment preparation
```

### 5.2 Testing Strategy Following TIPM Patterns

```python
class UITestSuite:
    """Comprehensive testing for UI enhancements following TIPM testing patterns"""

    def test_country_data_validation(self):
        """Test data validation and bounds checking"""
        # Test tariff rate bounds (0-100%)
        # Test GDP validation (non-negative)
        # Test confidence score calculation

    def test_sorting_performance(self):
        """Test sorting performance with 184 countries"""
        # Benchmark sorting algorithms
        # Validate cache effectiveness
        # Test memory usage

    def test_tooltip_functionality(self):
        """Test tooltip system across devices"""
        # Desktop hover testing
        # Mobile touch testing
        # Content validation

    def test_error_handling(self):
        """Test graceful degradation patterns"""
        # Missing data scenarios
        # API failure handling
        # Network timeout handling
```

## 6. Conclusion

### 6.1 Summary

This TIPM v1.5 implementation plan outlines a comprehensive strategy for enhancing the country selection UI with authoritative data sources, interactive features, and performance optimizations. By adhering to TIPM patterns, we ensure a scalable, maintainable, and user-friendly interface that can handle the complexities of a 184-country database. (Written by Andrew Yeo aka TheGeekyBeng)
