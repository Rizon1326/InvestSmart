#!/bin/bash

# Business Analysis Platform - Stop Script
# This script stops all running components of the platform

set -e

echo "🛑 Stopping Business Analysis Platform..."
echo "======================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_ROOT="/Users/rizon/Desktop/Therap-Java"

# Function to stop service by PID file
stop_service_by_pid() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}🛑 Stopping $service_name (PID: $pid)...${NC}"
            kill $pid
            sleep 2
            
            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                echo -e "${YELLOW}⚡ Force stopping $service_name...${NC}"
                kill -9 $pid
            fi
            
            echo -e "${GREEN}✅ $service_name stopped${NC}"
        else
            echo -e "${YELLOW}⚠️ $service_name was not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}⚠️ No PID file found for $service_name${NC}"
    fi
}

# Function to stop service by port
stop_service_by_port() {
    local port=$1
    local service_name=$2
    
    local pid=$(lsof -ti:$port 2>/dev/null || echo "")
    if [ -n "$pid" ]; then
        echo -e "${YELLOW}🛑 Stopping $service_name on port $port (PID: $pid)...${NC}"
        kill $pid 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        local still_running=$(lsof -ti:$port 2>/dev/null || echo "")
        if [ -n "$still_running" ]; then
            echo -e "${YELLOW}⚡ Force stopping $service_name...${NC}"
            kill -9 $still_running 2>/dev/null || true
        fi
        
        echo -e "${GREEN}✅ $service_name stopped${NC}"
    else
        echo -e "${YELLOW}⚠️ $service_name was not running on port $port${NC}"
    fi
}

echo -e "${BLUE}🔍 Checking running services...${NC}"

# Stop services by PID files first
stop_service_by_pid "$PROJECT_ROOT/frontend.pid" "React Frontend"
stop_service_by_pid "$PROJECT_ROOT/python.pid" "Python Services"
stop_service_by_pid "$PROJECT_ROOT/backend.pid" "Java Backend"

echo ""
echo -e "${BLUE}🔍 Checking ports for any remaining processes...${NC}"

# Stop any remaining services by port
stop_service_by_port 3000 "Frontend"
stop_service_by_port 5000 "Python Services"  
stop_service_by_port 8080 "Backend"

# Clean up log files (optional)
echo ""
echo -e "${BLUE}🧹 Cleaning up...${NC}"

if [ -f "$PROJECT_ROOT/backend.log" ]; then
    echo -e "${YELLOW}📋 Backend log available at: $PROJECT_ROOT/backend.log${NC}"
fi

if [ -f "$PROJECT_ROOT/python.log" ]; then
    echo -e "${YELLOW}📋 Python log available at: $PROJECT_ROOT/python.log${NC}"
fi

if [ -f "$PROJECT_ROOT/frontend.log" ]; then
    echo -e "${YELLOW}📋 Frontend log available at: $PROJECT_ROOT/frontend.log${NC}"
fi

# Final verification
echo ""
echo -e "${BLUE}🔍 Final verification...${NC}"

ports_to_check=(3000 5000 8080)
all_stopped=true

for port in "${ports_to_check[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}❌ Port $port is still in use${NC}"
        all_stopped=false
    else
        echo -e "${GREEN}✅ Port $port is free${NC}"
    fi
done

echo ""
if [ "$all_stopped" = true ]; then
    echo -e "${GREEN}🎉 All services stopped successfully!${NC}"
    echo -e "${BLUE}📱 To restart the platform, run: ${YELLOW}./start.sh${NC}"
else
    echo -e "${RED}⚠️ Some services may still be running${NC}"
    echo -e "${BLUE}💡 Try running this script again or manually kill processes:${NC}"
    echo -e "   ${YELLOW}lsof -ti:3000,5000,8080 | xargs kill -9${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"