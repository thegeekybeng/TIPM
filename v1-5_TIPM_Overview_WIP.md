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
    data_sources: Dict[str, str]        # Field -> Official source mapping
    last_updated: datetime              # Data vintage tracking
    confidence_level: str               # High/Medium/Low based on source quality
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

## 3. Dependencies

### Required Python Packages

```python
# Core dependencies
requests>=2.31.0           # Government API integration
pycountry>=22.3.1         # ISO country codes
pandas-datareader>=0.10.0  # World Bank/FRED data
cachetools>=5.3.0         # API caching
aiohttp>=3.8.0            # Async HTTP client
asyncio>=3.4.3            # Async operations

# Additional imports
from typing import Set, Dict, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging              # Data validation logging
```

## 4. UI Enhancement Strategy

### 4.1 Enhanced Country Data Structure for UI

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

        except Exception as e:
            logging.error(f"Error generating tooltip for {self.name}: {str(e)}")
            return {"error": "Tooltip data unavailable"}
```

### 4.2 Enhanced Sorting Implementation

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
            sort_methods = {
                "Alphabetical": lambda c: c.name.lower(),
                "By Continent": lambda c: (c.continent, c.name.lower()),
                "By Global Groups": lambda c: (len(c.global_groups), c.name.lower()),
                "By Emerging Markets": lambda c: (c.emerging_market_status, c.name.lower()),
                "By Tech Manufacturing Exporters": lambda c: (c.tech_manufacturing_rank or 999, c.name.lower()),
                "By Resource Exporters (Mining)": lambda c: (c.resource_export_category == "Mining", c.name.lower()),
                "By Resource Exporters (Agriculture)": lambda c: (c.resource_export_category == "Agriculture", c.name.lower())
            }

            if sort_method not in sort_methods:
                logging.warning(f"Unknown sort method: {sort_method}, defaulting to Alphabetical")
                sort_method = "Alphabetical"

            sorted_countries = sorted(
                self.countries,
                key=sort_methods[sort_method],
                reverse=sort_method in ["By Global Groups", "By Emerging Markets", "By Resource Exporters (Mining)", "By Resource Exporters (Agriculture)"]
            )

            # Cache result for performance
            self.sorting_cache[cache_key] = sorted_countries
            return sorted_countries

        except Exception as e:
            logging.error(f"Error sorting countries: {str(e)}")
            return self.countries  # Return unsorted as fallback
```

## 5. Performance Optimization

### 5.1 Caching Strategy

```python
from cachetools import TTLCache
from functools import lru_cache

class CountryDataCache:
    """Performance optimization for large-scale country operations"""

    def __init__(self):
        self.cache_ttl = 3600  # 1 hour TTL
        self.cache_size = 1000

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

## 6. Testing Strategy

### 6.1 Test Suite Following TIPM Patterns

```python
class UITestSuite:
    """Comprehensive testing for UI enhancements following TIPM testing patterns"""

    def test_country_data_validation(self):
        """Test data validation and bounds checking"""
        # Test tariff rate bounds (0-100%)
        # Test GDP validation (non-negative)
        # Test confidence score calculation
        pass

    def test_sorting_performance(self):
        """Test sorting performance with 184 countries"""
        # Benchmark sorting algorithms
        # Validate cache effectiveness
        # Test memory usage
        pass

    def test_tooltip_functionality(self):
        """Test tooltip system across devices"""
        # Desktop hover testing
        # Mobile touch testing
        # Content validation
        pass

    def test_error_handling(self):
        """Test graceful degradation patterns"""
        # Missing data scenarios
        # API failure handling
        # Network timeout handling
        pass
```

## 7. Development Timeline

### Implementation Phases

- **Phase 1 (Week 1)**: Core Database Expansion

  - ✅ Enhanced country data structures
  - ✅ Data source integration planning
  - 🔄 API integration setup
  - 🔄 Validation framework

- **Phase 2 (Week 2)**: Category Classification

  - ⏳ Emerging market classification
  - ⏳ Tech manufacturing rankings
  - ⏳ Resource exporter classification
  - ⏳ Data validation

- **Phase 3 (Week 3)**: UI Enhancement

  - ⏳ Enhanced sorting implementation
  - ⏳ Tooltip system development
  - ⏳ Performance optimization
  - ⏳ Mobile responsiveness

- **Phase 4 (Week 4)**: Testing & Deployment
  - ⏳ Comprehensive testing
  - ⏳ Performance benchmarking
  - ⏳ Documentation completion
  - ⏳ Production deployment

## Next Steps

1. **Review and approve** this cleaned-up implementation strategy
2. **Begin Phase 1** implementation with core database expansion
3. **Validate data sources** accessibility and terms of use
4. **Set up development environment** with required dependencies

---

_TIPM v1.5 Planning Document - Cleaned and Organized_
_Author: Andrew Yeo (TheGeekyBeng)_
