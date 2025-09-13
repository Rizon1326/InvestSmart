#!/bin/bash

# Business Analysis Platform - Complete Startup Script
# This script starts all components of the platform

set -e  # Exit on any error

echo "🚀 Starting Business Analysis Platform..."
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="/Users/rizon/Desktop/Therap-Java"

# Function to check if service is running
check_service() {
    local port=$1
    local service_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${GREEN}✅ $service_name is running on port $port${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name is not running on port $port${NC}"
        return 1
    fi
}

# Function to wait for service to start
wait_for_service() {
    local port=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}⏳ Waiting for $service_name to start on port $port...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}❌ $service_name failed to start within $((max_attempts * 2)) seconds${NC}"
    return 1
}

# Step 1: Check Prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Java
if command -v java &> /dev/null; then
    java_version=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$java_version" -ge 17 ]; then
        echo -e "${GREEN}✅ Java $java_version found${NC}"
    else
        echo -e "${RED}❌ Java 17+ required, found Java $java_version${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Java not found${NC}"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    node_version=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -ge 16 ]; then
        echo -e "${GREEN}✅ Node.js v$(node -v) found${NC}"
    else
        echo -e "${RED}❌ Node.js 16+ required, found v$(node -v)${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Node.js not found${NC}"
    exit 1
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL found${NC}"
else
    echo -e "${RED}❌ PostgreSQL not found${NC}"
    exit 1
fi

# Check Python virtual environment
if [ -f "$PROJECT_ROOT/.venv/bin/python" ]; then
    echo -e "${GREEN}✅ Python virtual environment found${NC}"
else
    echo -e "${RED}❌ Python virtual environment not found${NC}"
    exit 1
fi

echo ""

# Step 2: Setup Database
echo -e "${BLUE}🗄️ Setting up database...${NC}"

# Check if database exists
if psql -lqt | cut -d \| -f 1 | grep -qw market_analysis; then
    echo -e "${GREEN}✅ Database 'market_analysis' already exists${NC}"
else
    echo -e "${YELLOW}📊 Creating database 'market_analysis'...${NC}"
    createdb market_analysis
    echo -e "${GREEN}✅ Database created${NC}"
fi

# Run schema
echo -e "${YELLOW}📋 Running database schema...${NC}"
if psql -d market_analysis -f "$PROJECT_ROOT/database/schema.sql" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database schema applied${NC}"
else
    echo -e "${YELLOW}⚠️ Schema may already exist (this is normal)${NC}"
fi

echo ""

# Step 3: Start Backend
echo -e "${BLUE}🔥 Starting Java Spring Boot backend...${NC}"
cd "$PROJECT_ROOT/backend"

# Check if backend is already running
if check_service 8080 "Backend"; then
    echo -e "${YELLOW}⚠️ Backend already running, skipping startup${NC}"
else
    echo -e "${YELLOW}🔧 Building and starting backend...${NC}"
    
    # Start backend in background
    nohup mvn spring-boot:run > "$PROJECT_ROOT/backend.log" 2>&1 &
    backend_pid=$!
    echo $backend_pid > "$PROJECT_ROOT/backend.pid"
    
    # Wait for backend to start
    if wait_for_service 8080 "Backend"; then
        echo -e "${GREEN}✅ Backend started successfully (PID: $backend_pid)${NC}"
    else
        echo -e "${RED}❌ Backend failed to start${NC}"
        exit 1
    fi
fi

echo ""

# Step 4: Start Python Services
echo -e "${BLUE}🐍 Starting Python ML services...${NC}"
cd "$PROJECT_ROOT/backend/src/python-services"

# Check if Python services are already running
if check_service 5000 "Python Services"; then
    echo -e "${YELLOW}⚠️ Python services already running, skipping startup${NC}"
else
    echo -e "${YELLOW}🔧 Starting Python services...${NC}"
    
    # Start Python services in background
    nohup "$PROJECT_ROOT/.venv/bin/python" scraping_service.py > "$PROJECT_ROOT/python.log" 2>&1 &
    python_pid=$!
    echo $python_pid > "$PROJECT_ROOT/python.pid"
    
    # Wait for Python services to start
    if wait_for_service 5000 "Python Services"; then
        echo -e "${GREEN}✅ Python services started successfully (PID: $python_pid)${NC}"
    else
        echo -e "${RED}❌ Python services failed to start${NC}"
        exit 1
    fi
fi

echo ""

# Step 5: Start Frontend
echo -e "${BLUE}⚛️ Starting React frontend...${NC}"
cd "$PROJECT_ROOT/frontend"

# Check if frontend is already running
if check_service 3000 "Frontend"; then
    echo -e "${YELLOW}⚠️ Frontend already running, skipping startup${NC}"
else
    echo -e "${YELLOW}🔧 Starting frontend...${NC}"
    
    # Start frontend in background
    nohup npm start > "$PROJECT_ROOT/frontend.log" 2>&1 &
    frontend_pid=$!
    echo $frontend_pid > "$PROJECT_ROOT/frontend.pid"
    
    # Wait for frontend to start
    if wait_for_service 3000 "Frontend"; then
        echo -e "${GREEN}✅ Frontend started successfully (PID: $frontend_pid)${NC}"
    else
        echo -e "${RED}❌ Frontend failed to start${NC}"
        exit 1
    fi
fi

echo ""

# Final status check
echo -e "${BLUE}🎯 Final Status Check...${NC}"
echo "======================================"

check_service 8080 "Java Backend"
check_service 5000 "Python Services" 
check_service 3000 "React Frontend"

echo ""
echo -e "${GREEN}🎉 Business Analysis Platform is ready!${NC}"
echo "======================================"
echo -e "${BLUE}📱 Application URLs:${NC}"
echo -e "   Frontend:        ${GREEN}http://localhost:3000${NC}"
echo -e "   Backend API:     ${GREEN}http://localhost:8080/api${NC}"
echo -e "   Python Services: ${GREEN}http://localhost:5000${NC}"
echo ""
echo -e "${BLUE}📋 Commands to test:${NC}"
echo -e "   Backend health:  ${YELLOW}curl http://localhost:8080/api/market-analysis/health${NC}"
echo -e "   Python health:   ${YELLOW}curl http://localhost:5000/health${NC}"
echo ""
echo -e "${BLUE}📊 Log files:${NC}"
echo -e "   Backend:  ${YELLOW}$PROJECT_ROOT/backend.log${NC}"
echo -e "   Python:   ${YELLOW}$PROJECT_ROOT/python.log${NC}"
echo -e "   Frontend: ${YELLOW}$PROJECT_ROOT/frontend.log${NC}"
echo ""
echo -e "${BLUE}🛑 To stop all services:${NC}"
echo -e "   Run: ${YELLOW}$PROJECT_ROOT/stop.sh${NC}"

# Open browser automatically (optional)
if command -v open &> /dev/null; then
    echo ""
    echo -e "${YELLOW}🌐 Opening browser...${NC}"
    sleep 3
    open http://localhost:3000
fi