# 📊 Business Analysis Platform

A comprehensive market analysis platform that combines AI-powered insights, ML forecasting, and interactive visualizations to provide business recommendations for the Bangladesh market.

## 🏗 Architecture Overview

```
📦 Business Analysis Platform
├── 🔥 Backend (Java Spring Boot)
│   ├── REST APIs & Business Logic
│   ├── Database Models & Repositories
│   └── Service Layer Integration
├── 🐍 Python Services
│   ├── Web Scraping (Foodpanda, Daraz)
│   ├── ML Forecasting (Prophet, SARIMAX, XGBoost, LightGBM)
│   ├── Groq AI Integration (Llama-3.1-8b-instant)
│   └── Finance Simulation (Monte Carlo)
├── ⚛️ Frontend (React TypeScript)
│   ├── Interactive Forms
│   ├── Data Visualization Charts
│   └── KPI Dashboards
└── 🗄️ Database (PostgreSQL)
    ├── User Data & Analysis Results
    ├── Market Data Storage
    └── Financial Projections
```

## 🚀 Quick Start

### Prerequisites

- Java 17+
- Node.js 16+
- Python 3.9+
- PostgreSQL 12+

### 1. Database Setup

```bash
cd database
psql -U postgres -c "CREATE DATABASE market_analysis;"
psql -U postgres -d market_analysis -f schema.sql
```

### 2. Backend Setup

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

The backend will start on `http://localhost:8080`

### 3. Python Services Setup

```bash
cd backend/src/python-services

# Install dependencies
pip install flask requests beautifulsoup4 selenium pandas numpy
pip install prophet statsmodels xgboost lightgbm scikit-learn

# Start scraping service
python scraping_service.py

# The services will run on http://localhost:5000
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000`

## 📋 Features

### User Input Collection
- **Location**: 64 Bangladesh districts
- **Business Interest**: Food, Retail, Electronics, Beauty, etc.
- **Financial Parameters**: Capital range, target income, risk profile
- **Operational Preferences**: Work type, selling channel, delivery capability

### Market Analysis Pipeline

#### 1. Data Scraping
- **Foodpanda**: Restaurant and food service data
- **Daraz**: E-commerce and retail product data
- Real-time price and demand information

#### 2. AI Analysis (Groq API)
- **Model**: Llama-3.1-8b-instant
- Market opportunity assessment
- Competition analysis
- Risk evaluation
- Business recommendations

#### 3. ML Forecasting
- **Prophet**: Seasonal demand forecasting
- **SARIMAX**: Time series analysis
- **XGBoost/LightGBM**: Demand prediction
- **Ensemble**: Combined model predictions

#### 4. Financial Simulation
- **Deterministic Scenarios**: Best/Expected/Worst case
- **Monte Carlo Analysis**: 1000-iteration probability simulation
- **ROI Calculations**: Revenue, profit, payback analysis
- **Supply Chain Costing**: Logistics, inventory, supplier analysis

### Visualization Dashboard

#### KPI Cards
- Fit Score (0-10 scale)
- Expected Revenue
- ROI Percentage
- Payback Period

#### Interactive Charts
- 📈 **Demand Forecast**: 12-month predictions with confidence intervals
- 💰 **ROI Analysis**: Revenue breakdown and scenario comparison
- ⚖️ **Break-Even Chart**: Unit-based profitability analysis

#### Recommendations Engine
- ✅ **Top Recommendations**: Priority-based action items
- ⚠️ **Risk Mitigation**: Strategies to minimize business risks
- 📈 **Growth Opportunities**: Expansion and optimization suggestions

## 🎯 Key Formulas Implemented

### Business Analysis
```
Fit Score = demand_score × margin_score × feasibility_score
Suggested Price = procurement_cost + margin - competition_adjustment
```

### Financial Metrics
```
Revenue = Price × Quantity
Net Profit = Revenue - (Fixed + Variable + Logistics + Marketing)
ROI = (Annual Profit / Initial Investment) × 100
```

### Supply Chain
```
Total Cost per Unit = Procurement + Storage + Transportation + Handling
Inventory Cost = Average Inventory × Storage Cost per Month
```

## 🔧 Configuration

### Environment Variables

#### Backend (`application.properties`)
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/market_analysis
spring.datasource.username=postgres
spring.datasource.password=password
groq.api.key=your_groq_api_key
python.scraping.service.url=http://localhost:5000
```

#### Frontend (`.env`)
```
REACT_APP_API_URL=http://localhost:8080/api
REACT_APP_USE_REAL_API=true
```

#### Python Services
```
GROQ_API_KEY=your_groq_api_key
```

## 📊 API Endpoints

### Market Analysis
- `POST /api/market-analysis/analyze` - Submit user input for analysis
- `GET /api/market-analysis/result/{id}` - Get analysis results
- `GET /api/market-analysis/health` - Health check

### Python Services
- `POST /scrape` - Market data scraping
- `GET /health` - Service health check

## 🔍 Sample Usage Flow

1. **User Input**: Fill out the comprehensive business analysis form
2. **Data Collection**: System scrapes relevant market data
3. **AI Analysis**: Groq API processes data for insights
4. **ML Forecasting**: Multiple models predict demand trends
5. **Financial Modeling**: Monte Carlo simulation for risk analysis
6. **Visualization**: Interactive dashboard displays results
7. **Recommendations**: Actionable business advice generated

## 🏢 Bangladesh Market Focus

- **Districts**: All 64 districts with location-specific factors
- **Business Types**: Tailored for local market conditions
- **Currency**: All calculations in Bangladeshi Taka (BDT)
- **Seasonal Factors**: Ramadan, Eid, and local seasonal trends
- **Supply Chain**: Local logistics and supplier availability

## 🚧 Development & Testing

### Backend Testing
```bash
mvn test
```

### Frontend Testing
```bash
npm test
```

### Mock Data
The system includes comprehensive mock data for development and testing when external services are unavailable.

## 📈 Future Enhancements

- Real-time market data updates
- Mobile application
- Advanced ML model training
- Multi-language support
- Integration with local payment systems
- Automated report generation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Technology Stack

- **Backend**: Java 17, Spring Boot 3.1, Maven
- **Frontend**: React 18, TypeScript, Material-UI, Recharts
- **Database**: PostgreSQL 12+
- **AI/ML**: Python, Groq API, Prophet, XGBoost, LightGBM
- **Scraping**: BeautifulSoup, Selenium, Requests
- **Deployment**: Docker ready, cloud-native architecture

---

Built with ❤️ for the Bangladesh business community