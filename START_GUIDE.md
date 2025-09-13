# 🚀 Complete Setup & Run Guide

Follow these steps to run your Business Analysis Platform locally.

## Prerequisites Check

Before starting, ensure you have:
- ✅ PostgreSQL 12+ installed
- ✅ Java 17+ installed
- ✅ Node.js 16+ installed
- ✅ Python 3.9+ installed (already configured in virtual environment)

## Step 1: Database Setup

### Start PostgreSQL Service
```bash
# On macOS with Homebrew
brew services start postgresql

# Or if using PostgreSQL.app, just start the application
```

### Create Database and Tables
```bash
# Create the database
createdb market_analysis

# Run the schema script
psql -d market_analysis -f /Users/rizon/Desktop/Therap-Java/database/schema.sql
```

### Verify Database Setup
```bash
psql -d market_analysis -c "\dt"  # List tables
```

## Step 2: Backend (Spring Boot) Setup

### Terminal 1 - Java Backend
```bash
cd /Users/rizon/Desktop/Therap-Java/backend

# Build the project
mvn clean install

# Run the Spring Boot application
mvn spring-boot:run
```

**Expected Output:**
```
Started MarketAnalysisApplication in X.XXX seconds
Tomcat started on port(s): 8080 (http)
```

**Test Backend:**
```bash
curl http://localhost:8080/api/market-analysis/health
# Should return: "Market Analysis API is running"
```

## Step 3: Python Services Setup

### Terminal 2 - Python ML Services
```bash
cd /Users/rizon/Desktop/Therap-Java/backend/src/python-services

# Activate virtual environment (already configured)
source /Users/rizon/Desktop/Therap-Java/.venv/bin/activate

# Start the scraping service
python scraping_service.py
```

**Expected Output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Test Python Services:**
```bash
curl http://localhost:5000/health
# Should return: {"status": "healthy", "service": "scraping"}
```

## Step 4: Frontend (React) Setup

### Terminal 3 - React Frontend
```bash
cd /Users/rizon/Desktop/Therap-Java/frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm start
```

**Expected Output:**
```
Compiled successfully!
Local:            http://localhost:3000
```

## Step 5: Access Your Application

### 🎯 Main Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8080/api
- **Python Services**: http://localhost:5000

### 🧪 Quick Test Workflow

1. Open http://localhost:3000 in your browser
2. Fill out the business analysis form:
   - Location: Dhaka
   - Business Interest: Food & Restaurant
   - Capital: 50000-100000 BDT
   - Risk Profile: Balanced
3. Submit and view the analysis results

## Troubleshooting

### Database Issues
```bash
# Check PostgreSQL status
brew services list | grep postgresql

# Reset database if needed
dropdb market_analysis
createdb market_analysis
psql -d market_analysis -f /Users/rizon/Desktop/Therap-Java/database/schema.sql
```

### Backend Issues
```bash
# Check Java version
java -version  # Should be 17+

# Check port availability
lsof -i :8080
```

### Python Services Issues
```bash
# Check virtual environment
which python  # Should point to .venv/bin/python

# Reinstall packages if needed
pip install -r requirements.txt
```

### Frontend Issues
```bash
# Check Node version
node -v  # Should be 16+

# Clear npm cache if needed
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Environment Variables (Optional)

### For Production Use:
Create `.env` files:

**Backend** (`backend/src/main/resources/application.properties`):
```properties
groq.api.key=your_actual_groq_api_key_here
```

**Frontend** (`frontend/.env`):
```
REACT_APP_API_URL=http://localhost:8080/api
REACT_APP_USE_REAL_API=true
```

## 🎉 Success Indicators

- ✅ Database: Tables created successfully
- ✅ Backend: Spring Boot started on port 8080
- ✅ Python: Flask services running on port 5000  
- ✅ Frontend: React app accessible at localhost:3000
- ✅ Integration: Form submission generates analysis results

## Next Steps

Once everything is running:
1. Test the complete workflow by submitting a form
2. Check the database for stored results: `psql -d market_analysis -c "SELECT * FROM user_inputs;"`
3. Monitor logs in all three terminals for any issues
4. Ready for development and testing!