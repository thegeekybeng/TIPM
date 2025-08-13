# TIPM Data Crawler Module

## Overview

The TIPM Data Crawler is an intelligent, autonomous data collection system that uses **RAG (Retrieval-Augmented Generation)** capabilities to discover, validate, and integrate new data sources for economic and trade analysis. This module operates independently from the main TIPM system and continuously enhances the data quality and coverage.

## 🚀 Key Features

### **Intelligent Data Discovery**
- **RAG-Powered Source Discovery**: Uses vector embeddings and semantic search to find new relevant data sources
- **Gap Analysis**: Automatically identifies missing data categories and suggests new sources
- **Natural Language Queries**: Discover sources using plain English descriptions

### **Multi-Source Crawling**
- **Specialized Crawlers**: Dedicated crawlers for different data source types (APIs, web scraping, databases)
- **Rate Limiting**: Respectful crawling with configurable delays and retry logic
- **Error Handling**: Robust error handling with automatic retries and fallback mechanisms

### **ML-Powered Validation**
- **Data Quality Assessment**: Multi-dimensional validation (completeness, accuracy, consistency, timeliness)
- **Anomaly Detection**: Statistical and pattern-based anomaly detection
- **Business Logic Validation**: Domain-specific rule validation for economic data

### **Autonomous Operation**
- **Scheduled Updates**: Automatic crawling based on source update frequencies
- **Quality Scoring**: Continuous quality assessment and source reliability tracking
- **Integration Decisions**: ML-based recommendations for data integration

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TIPM Data Crawler                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   RAG Engine   │  │  ML Validator   │  │   Crawler   │ │
│  │                │  │                 │  │  Manager    │ │
│  │ • Vector Store │  │ • Anomaly      │  │ • Source    │ │
│  │ • Embeddings   │  │   Detection     │  │   Routing   │ │
│  │ • Discovery    │  │ • Quality      │  │ • Scheduling│ │
│  └─────────────────┘  │   Scoring      │  │ • Monitoring│ │
│                       └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ World Bank     │  │   US Census     │  │ UN Comtrade │ │
│  │   Crawler      │  │    Crawler      │  │   Crawler   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Web Scraping   │  │   Database      │  │   File      │ │
│  │   Crawler      │  │    Crawler      │  │   Crawler   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Sources Supported

### **Economic Data**
- **World Bank**: GDP, development indicators, global economic data
- **FRED**: Federal Reserve economic indicators
- **OECD**: Economic cooperation and development data
- **IMF**: World Economic Outlook and forecasts
- **Eurostat**: European Union economic statistics

### **Trade Data**
- **US Census**: International trade statistics
- **UN Comtrade**: Global trade commodity data
- **WTO**: Trade policy and statistics
- **BIS**: Financial and banking statistics

### **Research Data**
- **NBER**: Economic research and indicators
- **Academic Sources**: University research databases
- **Policy Institutes**: Think tank data and reports

## 🛠️ Installation

### **Prerequisites**
```bash
# Python 3.8+ required
python --version

# Install required packages
pip install -r requirements.txt
```

### **Dependencies**
```bash
# Core ML and data science
pip install numpy pandas scikit-learn

# Vector database and embeddings
pip install chromadb sentence-transformers

# Async HTTP client
pip install aiohttp

# Data validation
pip install pydantic great-expectations
```

### **Quick Start**
```bash
# Clone the repository
git clone <repository-url>
cd TIPM/data_crawler

# Install dependencies
pip install -e .

# Run initial setup
python -m data_crawler.main --status
```

## 🚀 Usage

### **Command Line Interface**

#### **Run Full Crawl Cycle**
```bash
# Crawl all active data sources
python -m data_crawler.main --cycle

# Verbose output with detailed logging
python -m data_crawler.main --cycle --verbose
```

#### **Crawl Specific Source**
```bash
# Crawl World Bank data
python -m data_crawler.main --crawl world_bank_gdp

# Crawl US Census trade data
python -m data_crawler.main --crawl us_census_trade
```

#### **Discover New Sources**
```bash
# Discover sources for tariff data
python -m data_crawler.main --discover "tariff data and trade policy"

# Discover financial market data sources
python -m data_crawler.main --discover "financial markets exchange rates"
```

#### **Monitor Status**
```bash
# Show current crawler status
python -m data_crawler.main --status

# List all configured sources
python -m data_crawler.main --list-sources

# Save current configuration
python -m data_crawler.main --save-config
```

### **Programmatic Usage**

#### **Initialize Crawler**
```python
import asyncio
from data_crawler.core import DataCrawlerRAG

async def main():
    # Initialize the crawler
    crawler = DataCrawlerRAG(
        vector_db_path="data_crawler/vector_store",
        config_path="data_crawler/config/sources.json"
    )
    
    # Run a crawl cycle
    results = await crawler.run_full_crawl_cycle()
    print(f"Crawled {results['successful_crawls']} sources successfully")
    
    # Discover new sources
    new_sources = await crawler.discover_new_sources("economic indicators")
    print(f"Discovered {len(new_sources)} new sources")

# Run the crawler
asyncio.run(main())
```

#### **Add Custom Data Source**
```python
from data_crawler.models import DataSource, DataSourceType

# Create a new data source
new_source = DataSource(
    id="custom_economic_data",
    name="Custom Economic Database",
    description="Custom economic indicators and forecasts",
    source_type=DataSourceType.API,
    url="https://api.customdata.org",
    tags=["economics", "custom", "forecasts"],
    categories=["macroeconomic", "custom"],
    country_coverage=["all"],
    time_coverage="2010-2024",
    update_frequency="weekly"
)

# Add to crawler
crawler.add_data_source(new_source)
```

## 🔧 Configuration

### **Data Source Configuration**
The system uses a JSON configuration file (`data_crawler/config/sources.json`) to define data sources:

```json
{
  "id": "world_bank_gdp",
  "name": "World Bank GDP Data",
  "description": "Global GDP and economic indicators",
  "source_type": "api",
  "url": "https://api.worldbank.org/v2/country",
  "update_frequency": "daily",
  "tags": ["economics", "gdp", "world_bank"],
  "categories": ["macroeconomic", "development"],
  "country_coverage": ["all"],
  "time_coverage": "1960-2024"
}
```

### **System Settings**
```json
{
  "settings": {
    "default_update_frequency": "daily",
    "max_concurrent_crawls": 5,
    "retry_attempts": 3,
    "timeout_seconds": 30,
    "rate_limit_delay": 1.0,
    "validation_threshold": 0.7,
    "anomaly_detection_enabled": true
  }
}
```

## 📈 Data Quality Metrics

### **Validation Scores**
- **Completeness**: Data field coverage and record counts
- **Accuracy**: Statistical validity and outlier detection
- **Consistency**: Data structure and format consistency
- **Timeliness**: Data freshness and update frequency

### **ML Validation**
- **Anomaly Detection**: Statistical outlier identification
- **Business Logic**: Domain-specific rule validation
- **Pattern Analysis**: Data structure pattern validation

### **Quality Levels**
- **Excellent (90-100%)**: Ready for immediate integration
- **Good (75-89%)**: Minor issues, integration recommended
- **Fair (60-74%)**: Some issues, review required
- **Poor (40-59%)**: Significant issues, manual review needed
- **Unacceptable (<40%)**: Major issues, integration not recommended

## 🔍 RAG Capabilities

### **Vector Database**
- **ChromaDB**: Persistent vector storage for embeddings
- **Source Metadata**: Vectorized descriptions and tags
- **Data Content**: Vectorized crawled data for similarity search

### **Embedding Model**
- **Sentence Transformers**: `all-MiniLM-L6-v2` for text vectorization
- **Semantic Search**: Find similar data sources and content
- **Discovery**: Identify gaps and suggest new sources

### **Intelligent Routing**
- **Source Classification**: Automatic crawler selection
- **Pattern Recognition**: Learn from successful crawls
- **Adaptive Scheduling**: Optimize update frequencies

## 📊 Monitoring and Logging

### **Log Files**
- **Main Log**: `data_crawler.log` - All system activities
- **Crawl Logs**: Individual source crawl results
- **Validation Logs**: Data quality assessment results

### **Status Monitoring**
```bash
# Real-time status
python -m data_crawler.main --status

# Health check
python -m data_crawler.main --list-sources
```

### **Performance Metrics**
- **Crawl Duration**: Time per source and total cycle time
- **Success Rates**: Crawl and validation success percentages
- **Data Volume**: Records processed and data sizes
- **Error Tracking**: Failed attempts and error patterns

## 🔒 Security and Privacy

### **API Key Management**
- **Environment Variables**: Secure storage of API credentials
- **Access Control**: Rate limiting and request throttling
- **Audit Logging**: Track all data access and modifications

### **Data Privacy**
- **No PII Storage**: Personal data is not collected or stored
- **Aggregated Data**: Only statistical and aggregated information
- **Source Attribution**: Clear attribution for all data sources

## 🚧 Error Handling

### **Retry Logic**
- **Exponential Backoff**: Progressive delay between retries
- **Circuit Breaker**: Stop requests to failing sources
- **Fallback Sources**: Alternative data sources when primary fails

### **Error Categories**
- **Network Errors**: Connection timeouts and HTTP errors
- **Data Errors**: Malformed responses and validation failures
- **Rate Limiting**: API quota exceeded and throttling
- **Authentication**: Invalid credentials and access denied

## 🔄 Integration with TIPM

### **Data Flow**
1. **Crawler** discovers and collects data from sources
2. **Validator** assesses data quality using ML models
3. **RAG Engine** stores embeddings and metadata
4. **Integration Layer** feeds validated data to main TIPM system

### **API Endpoints**
```python
# Get crawl status
GET /api/crawler/status

# Trigger manual crawl
POST /api/crawler/crawl/{source_id}

# Get validation results
GET /api/crawler/validation/{source_id}

# Discover new sources
POST /api/crawler/discover
```

## 🧪 Testing

### **Unit Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_crawlers.py
python -m pytest tests/test_validators.py
```

### **Integration Tests**
```bash
# Test with real APIs (requires API keys)
python -m pytest tests/test_integration.py --api-keys

# Test with mock data
python -m pytest tests/test_integration.py --mock
```

### **Performance Tests**
```bash
# Load testing
python -m pytest tests/test_performance.py --benchmark

# Memory profiling
python -m pytest tests/test_performance.py --profile
```

## 📚 API Reference

### **Core Classes**

#### **DataCrawlerRAG**
Main orchestrator class for the crawler system.

```python
class DataCrawlerRAG:
    async def run_full_crawl_cycle() -> Dict[str, Any]
    async def crawl_data_source(source_id: str) -> CrawlResult
    async def discover_new_sources(query: str) -> List[DataSource]
    async def validate_crawl_result(crawl_result: CrawlResult) -> ValidationResult
    def get_crawl_status() -> Dict[str, Any]
```

#### **BaseCrawler**
Base class for all specialized crawlers.

```python
class BaseCrawler:
    async def crawl(source: DataSource) -> Any
    async def _make_request(url: str, **kwargs) -> Dict[str, Any]
    def _validate_response(data: Any, expected_fields: List[str]) -> bool
```

#### **DataQualityValidator**
Multi-dimensional data quality assessment.

```python
class DataQualityValidator:
    async def validate_data(processed_data: Dict, raw_data: Any) -> Dict[str, float]
    def _validate_completeness(data: Dict, raw: Any) -> float
    def _validate_accuracy(data: Dict, raw: Any) -> float
    def _validate_consistency(data: Dict, raw: Any) -> float
    def _validate_timeliness(data: Dict, raw: Any) -> float
```

#### **MLAnomalyDetector**
ML-powered anomaly detection and validation.

```python
class MLAnomalyDetector:
    async def detect_anomalies(processed_data: Dict) -> Dict[str, float]
    def _detect_statistical_anomalies(data: Dict) -> float
    def _detect_business_logic_anomalies(data: Dict) -> float
    def _detect_pattern_anomalies(data: Dict) -> float
```

## 🤝 Contributing

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd TIPM/data_crawler

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### **Code Style**
- **Black**: Code formatting
- **Flake8**: Linting and style checking
- **MyPy**: Type checking
- **Pre-commit**: Automated quality checks

### **Adding New Crawlers**
1. **Extend BaseCrawler**: Implement the `crawl` method
2. **Add Validation**: Implement source-specific validation logic
3. **Update Factory**: Add crawler to the factory function
4. **Write Tests**: Comprehensive test coverage
5. **Document**: Update README and API docs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Documentation**
- **API Reference**: Comprehensive API documentation
- **Examples**: Code examples and use cases
- **Tutorials**: Step-by-step guides

### **Community**
- **Issues**: GitHub issue tracker
- **Discussions**: GitHub discussions
- **Wiki**: Community-maintained documentation

### **Contact**
- **Email**: tipm-dev@example.com
- **Slack**: #tipm-data-crawler
- **Office Hours**: Weekly community calls

## 🔮 Roadmap

### **Phase 1 (Current)**
- ✅ Core crawler infrastructure
- ✅ Basic validation system
- ✅ RAG-powered discovery
- ✅ Multi-source support

### **Phase 2 (Q2 2025)**
- 🔄 Advanced ML validation
- 🔄 Real-time streaming
- 🔄 Automated source discovery
- 🔄 Performance optimization

### **Phase 3 (Q3 2025)**
- 📋 Federated learning
- 📋 Advanced anomaly detection
- 📋 Predictive data quality
- 📋 Integration with external ML platforms

### **Phase 4 (Q4 2025)**
- 📋 Autonomous operation
- 📋 Self-healing capabilities
- 📋 Advanced RAG features
- 📋 Enterprise features

---

**Built with ❤️ by the TIPM Development Team**

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/tipm/data-crawler).*
