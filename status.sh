#!/bin/bash

# Business Analysis Platform - Status Check Script
# This script checks the status of all platform components

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Business Analysis Platform - Status Check${NC}"
echo "============================================="

# Function to check service status
check_service_status() {
    local port=$1
    local service_name=$2
    local url=$3
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $service_name${NC} - Running on port $port"
        
        # Test HTTP endpoint if provided
        if [ -n "$url" ]; then
            if curl -s "$url" > /dev/null 2>&1; then
                echo -e "   ${GREEN}🌐 HTTP endpoint responding${NC}"
            else
                echo -e "   ${YELLOW}⚠️ HTTP endpoint not responding${NC}"
            fi
        fi
    else
        echo -e "${RED}❌ $service_name${NC} - Not running on port $port"
    fi
}

# Check Database
echo -e "${BLUE}🗄️ Database Status:${NC}"
if command -v psql &> /dev/null; then
    if psql -lqt | cut -d \| -f 1 | grep -qw market_analysis; then
        echo -e "${GREEN}✅ PostgreSQL Database${NC} - 'market_analysis' exists"
        
        # Check table count
        table_count=$(psql -d market_analysis -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs)
        if [ "$table_count" -gt 0 ]; then
            echo -e "   ${GREEN}📋 $table_count tables found${NC}"
        else
            echo -e "   ${YELLOW}⚠️ No tables found${NC}"
        fi
    else
        echo -e "${RED}❌ PostgreSQL Database${NC} - 'market_analysis' not found"
    fi
else
    echo -e "${RED}❌ PostgreSQL${NC} - Command not found"
fi

echo ""

# Check Backend
echo -e "${BLUE}🔥 Backend Status:${NC}"
check_service_status 8080 "Java Spring Boot" "http://localhost:8080/api/market-analysis/health"

echo ""

# Check Python Services
echo -e "${BLUE}🐍 Python Services Status:${NC}"
check_service_status 5000 "Flask ML Services" "http://localhost:5000/health"

echo ""

# Check Frontend
echo -e "${BLUE}⚛️ Frontend Status:${NC}"
check_service_status 3000 "React Application" "http://localhost:3000"

echo ""

# Check Python Environment
echo -e "${BLUE}🐍 Python Environment:${NC}"
if [ -f "/Users/rizon/Desktop/Therap-Java/.venv/bin/python" ]; then
    python_version=$(/Users/rizon/Desktop/Therap-Java/.venv/bin/python --version 2>&1)
    echo -e "${GREEN}✅ Virtual Environment${NC} - $python_version"
    
    # Check key packages
    if /Users/rizon/Desktop/Therap-Java/.venv/bin/python -c "import flask, pandas, prophet, sklearn" 2>/dev/null; then
        echo -e "   ${GREEN}📦 ML packages installed${NC}"
    else
        echo -e "   ${YELLOW}⚠️ Some ML packages missing${NC}"
    fi
else
    echo -e "${RED}❌ Virtual Environment${NC} - Not found"
fi

echo ""

# Summary
echo -e "${BLUE}📱 Application URLs:${NC}"
echo "   Frontend:        http://localhost:3000"
echo "   Backend API:     http://localhost:8080/api"
echo "   Python Services: http://localhost:5000"

echo ""
echo -e "${BLUE}🛠️ Quick Commands:${NC}"
echo "   Start all:       ./start.sh"
echo "   Stop all:        ./stop.sh"
echo "   Check status:    ./status.sh"

echo ""
echo "============================================="