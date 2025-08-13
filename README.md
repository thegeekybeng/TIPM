# TIPM - Tariff Impact Propagation Model

## 🎯 Project Overview

TIPM (Tariff Impact Propagation Model) is a comprehensive, AI-powered economic analysis platform that provides intelligent insights into the multi-faceted impacts of trade policies and tariffs. The system combines advanced machine learning models with autonomous data crawling to deliver accurate, real-time economic impact assessments.

## 🚀 Key Features

### **ML Model Excellence** ✅
- **Hybrid ML Architecture**: Multi-class classification + Neural Networks
- **Core Models**: XGBoost, LightGBM, Random Forest, LSTM networks
- **Ensemble Methods**: Voting, Stacking, Dynamic weight optimization
- **Explainability**: SHAP integration for policy insights
- **Model Management**: Centralized MLModelManager with lifecycle management

### **Data Intelligence & Autonomy** ✅
- **RAG-Powered Data Crawler**: Autonomous data discovery using Retrieval-Augmented Generation
- **ML Validation**: Multi-layer data quality assessment with anomaly detection
- **Vector Database**: ChromaDB integration with semantic embeddings
- **Specialized Crawlers**: World Bank, US Census, UN Comtrade APIs
- **Real-time Processing**: Live data crawling and validation

### **Platform Modernization** ✅
- **React Frontend**: Modern web interface with Tailwind CSS
- **Component Architecture**: Modular, reusable UI components
- **Responsive Design**: Mobile-first approach with Framer Motion
- **Professional UI**: Beautiful, intuitive user experience

## 🏗️ Architecture

```
TIPM/
├── 🧠 ML Models (tipm/ml_models/)
│   ├── Classifiers (XGBoost, LightGBM, Random Forest)
│   ├── Neural Networks (LSTM, Attention Mechanisms)
│   ├── Ensemble Methods (Voting, Stacking)
│   └── Model Manager (Training, Prediction, Lifecycle)
├── 🕷️ Data Crawler (data_crawler/)
│   ├── RAG Engine (Vector Search, Embeddings)
│   ├── Specialized Crawlers (APIs, Web Scraping)
│   ├── ML Validator (Quality Assessment, Anomaly Detection)
│   └── Autonomous Discovery (Source Recommendation)
├── 🎨 Frontend (src/)
│   ├── React Components (TypeScript)
│   ├── Tailwind CSS (Modern Styling)
│   └── Interactive Dashboards
└── ⚙️ Configuration & Utils
    ├── Settings Management
    ├── Data Processing
    └── Testing Framework
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Virtual environment recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TIPM
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv tipm_env
   source tipm_env/bin/activate  # On Windows: tipm_env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd src
   npm install
   npm run dev
   ```

4. **Run tests**
   ```bash
   python test_current_functionality.py
   ```

5. **Run demo**
   ```bash
   python demo_ml_models.py
   ```

## 📊 Demo & Testing

### **Current Functionality Test**
```bash
python test_current_functionality.py
```
This script verifies all implemented components and provides a status report.

### **Full ML Demo**
```bash
python demo_ml_models.py
```
This comprehensive demo showcases:
- ML model training and prediction
- Data crawler autonomous operation
- Real-time data validation
- Policy insights generation

## 🔧 Configuration

### **Data Sources**
Configure data sources in `data_crawler/config/sources.json`:
```json
{
  "sources": [
    {
      "id": "world_bank_gdp",
      "name": "World Bank GDP Data",
      "url": "https://api.worldbank.org/v2/country",
      "source_type": "api"
    }
  ]
}
```

### **ML Model Settings**
Adjust model parameters in `tipm/config/settings.py`:
```python
@dataclass
class MLConfig:
    model_type: str = "ensemble"
    training_epochs: int = 100
    batch_size: int = 32
    learning_rate: float = 0.001
```

## 📈 Performance Metrics

- **ML Model Accuracy**: Target >90%
- **Data Freshness**: Real-time crawling (<24 hours)
- **Validation Quality**: Multi-layer assessment system
- **System Reliability**: Robust error handling and fallbacks

## 🔮 Future Roadmap

See [PROJECT_FUTURE_ROADMAP.md](PROJECT_FUTURE_ROADMAP.md) for comprehensive development plans including:

1. **Advanced ML Capabilities**: Causal inference, reinforcement learning
2. **Real-Time Streaming**: Live data feeds and instant analysis
3. **Enterprise Features**: Authentication, collaboration, API endpoints
4. **Global Expansion**: Multi-language support, regional data sources
5. **Scalability**: Microservices architecture, cloud deployment

## 🛠️ Development

### **Project Structure**
```
TIPM/
├── tipm/                    # Core TIPM functionality
│   ├── ml_models/          # Machine learning models
│   ├── config/             # Configuration management
│   └── utils/              # Utility functions
├── data_crawler/           # Autonomous data discovery
│   ├── core/               # RAG engine and crawler logic
│   ├── crawlers/           # Specialized data crawlers
│   ├── validators/         # Data quality validation
│   └── config/             # Data source configuration
├── src/                    # React frontend
│   ├── components/         # UI components
│   └── pages/              # Application pages
├── tests/                  # Test suite
├── data/                   # Sample data and datasets
└── docs/                   # Documentation
```

### **Adding New ML Models**
1. Create model class in `tipm/ml_models/`
2. Implement required methods (train, predict, evaluate)
3. Add to MLModelManager
4. Update configuration and tests

### **Adding New Data Sources**
1. Create crawler class in `data_crawler/crawlers/`
2. Add source configuration to `sources.json`
3. Implement validation rules
4. Test with sample data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Economic Data Sources**: World Bank, US Census, UN Comtrade
- **ML Libraries**: scikit-learn, PyTorch, XGBoost, LightGBM
- **Frontend**: React, Tailwind CSS, Framer Motion
- **Data Processing**: Pandas, NumPy, ChromaDB

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Review the documentation
- Check the test results
- Run the demo scripts

---

**TIPM**: Transforming economic analysis through intelligent automation and machine learning.

*Built with ❤️ for economic research and policy analysis.*
