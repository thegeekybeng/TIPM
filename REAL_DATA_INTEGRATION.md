# 🌐 Real Data Integration Guide

## Overview
TIPM now integrates with **real, authoritative data sources** instead of using synthetic or estimated data. This ensures data credibility and accuracy for tariff impact analysis.

## 🏛️ **Authoritative Data Sources**

### 1. 🇺🇸 **U.S. International Trade Commission (USITC)**
- **What**: Official U.S. tariff database with HTS codes
- **Data**: Real-time tariff rates by sector and country
- **API**: `https://data.usitc.gov/api`
- **Confidence**: 95% (official U.S. government data)

### 2. 🌍 **UN Comtrade Database**
- **What**: United Nations trade statistics
- **Data**: Bilateral trade flows, sector-specific volumes
- **API**: `https://comtradeapi.un.org/data/v1`
- **Confidence**: 90% (international standard)

### 3. 🏛️ **World Trade Organization (WTO)**
- **What**: Global tariff schedules and trade policies
- **Data**: Most-favored-nation rates, trade notifications
- **API**: `https://tariffdata.wto.org/api`
- **Confidence**: 90% (international trade authority)

### 4. 📊 **World Bank Economic Indicators**
- **What**: Economic development and trade metrics
- **Data**: GDP, trade balance, economic indicators
- **API**: `https://api.worldbank.org/v2`
- **Confidence**: 85% (development economics authority)

## 🚀 **Installation & Setup**

### 1. Install Dependencies
```bash
pip install -r requirements_real_data.txt
```

### 2. Verify Installation
```python
from tipm.real_data_connectors import RealDataManager
real_data = RealDataManager()
print("✅ Real data connectors installed successfully")
```

## 🔧 **Usage Examples**

### Basic Data Retrieval
```python
from tipm.real_data_connectors import RealDataManager

# Initialize manager
real_data = RealDataManager()

# Get comprehensive data for a country
china_data = real_data.get_comprehensive_data("China")

# Extract specific data types
tariffs = china_data.get('tariff_data', [])
trade_flows = china_data.get('trade_data', [])
economic_indicators = china_data.get('economic_indicators', {})

print(f"China: {len(tariffs)} tariff records, {len(trade_flows)} trade records")
```

### Sector-Specific Analysis
```python
# Get semiconductor tariff data for China
semiconductor_data = real_data.get_comprehensive_data("China", "Semiconductors")

if semiconductor_data.get('sources') != ['FALLBACK']:
    print("✅ Using real-time data from APIs")
    for tariff in semiconductor_data.get('tariff_data', []):
        print(f"Semiconductor tariff: {tariff.tariff_rate}% (Source: {tariff.source})")
else:
    print("⚠️ Using fallback data - APIs unavailable")
```

## 📊 **Data Structure**

### TariffData
```python
@dataclass
class TariffData:
    country: str           # Country name
    sector: str            # Economic sector
    tariff_rate: float     # Tariff percentage
    hts_code: str          # Harmonized Tariff Schedule code
    effective_date: str    # When tariff took effect
    source: str            # Data source (USITC, WTO, etc.)
    confidence: float      # Data confidence level (0.0-1.0)
```

### TradeData
```python
@dataclass
class TradeData:
    country: str           # Country name
    sector: str            # Economic sector
    trade_volume_usd: float # Trade volume in USD
    trade_balance: float   # Trade balance (positive = surplus)
    year: int              # Data year
    source: str            # Data source (UN Comtrade, etc.)
```

## 🔄 **Fallback Strategy**

The system uses a **3-tier fallback strategy**:

1. **Primary**: Real-time APIs (USITC, UN Comtrade, WTO, World Bank)
2. **Secondary**: Local CSV data (`data/trump_tariffs_by_country.csv`)
3. **Fallback**: Synthetic data generation (clearly marked)

### Fallback Detection
```python
data = real_data.get_comprehensive_data("Country")
if data.get('sources') == ['FALLBACK']:
    print("⚠️ Using fallback data - real APIs unavailable")
else:
    print(f"✅ Using real data from: {data.get('sources')}")
```

## 🧪 **Testing & Validation**

### 1. Test Real Data Integration
Use the **"🌐 Test Real Data Integration"** button in the TIPM interface to:
- Verify API connectivity
- Test data retrieval for multiple countries
- Check data source coverage
- Validate fallback mechanisms

### 2. Debug Country Loading
Use the **"🔍 Debug Country Loading"** button to:
- Check data loading status
- Verify country count
- Monitor sector coverage
- Validate data structure

## 📈 **Performance & Caching**

### Caching Strategy
- **Cache TTL**: 1 hour (3600 seconds)
- **Cache Key**: `{country}_{sector}`
- **Memory Management**: Automatic cleanup of expired entries

### Rate Limiting
- **USITC**: 100 requests/hour
- **UN Comtrade**: 1000 requests/day
- **WTO**: 500 requests/hour
- **World Bank**: 1000 requests/hour

## 🚨 **Error Handling**

### Common Issues & Solutions

#### 1. Import Error
```python
try:
    from tipm.real_data_connectors import RealDataManager
except ImportError:
    print("❌ Install real data connectors: pip install -r requirements_real_data.txt")
```

#### 2. API Unavailable
```python
try:
    data = real_data.get_comprehensive_data("Country")
    if data.get('sources') == ['FALLBACK']:
        print("⚠️ APIs unavailable, using fallback data")
except Exception as e:
    print(f"❌ API error: {e}")
```

#### 3. Network Timeout
```python
# All API calls have 30-second timeout
# Automatic retry with exponential backoff
```

## 🔒 **Data Privacy & Security**

- **No sensitive data**: Only public trade and tariff information
- **User-Agent**: Identifies TIPM as research tool
- **Rate limiting**: Respects API usage policies
- **Local caching**: Reduces external API calls

## 📚 **API Documentation Links**

- **USITC**: [https://data.usitc.gov/api/docs](https://data.usitc.gov/api/docs)
- **UN Comtrade**: [https://comtradeapi.un.org/data/v1/docs](https://comtradeapi.un.org/data/v1/docs)
- **WTO**: [https://tariffdata.wto.org/api/docs](https://tariffdata.wto.org/api/docs)
- **World Bank**: [https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview](https://datahelpdesk.worldbank.org/knowledgebase/articles/889386-developer-information-overview)

## 🎯 **Next Steps**

1. **Install dependencies**: `pip install -r requirements_real_data.txt`
2. **Test integration**: Use the test button in TIPM interface
3. **Monitor performance**: Check API response times and success rates
4. **Validate data**: Compare with official government sources
5. **Scale usage**: Monitor rate limits and optimize caching

## 📞 **Support**

For issues with real data integration:
1. Check the debug output in TIPM interface
2. Verify API endpoints are accessible
3. Check network connectivity and firewall settings
4. Review rate limiting and API quotas

---

**Status**: ✅ **Real data integration implemented and ready for use**
**Last Updated**: Current session
**Version**: TIPM v2.0 with Real Data
