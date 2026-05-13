#!/bin/bash
# Quick start script for Tournament Platform

set -e

echo "========================================="
echo "Tournament Platform - Quick Start Setup"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check requirements
echo -e "${BLUE}Checking requirements...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    echo "Please install Docker from https://www.docker.com"
    exit 1
fi
echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found${NC}"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found: $(docker-compose --version)${NC}"

# Check Python (optional)
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
else
    echo -e "${YELLOW}⚠ Python not found (optional for Docker setup)${NC}"
fi

# Check Node.js (optional)
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found (optional for Docker setup)${NC}"
fi

echo ""
echo -e "${BLUE}Preparing environment...${NC}"

# Create .env if not exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created (please review and update if needed)${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""
echo -e "${BLUE}Building Docker images...${NC}"
docker-compose build

echo ""
echo -e "${BLUE}Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo -e "${BLUE}Running migrations...${NC}"
docker-compose exec -T api-gateway python manage.py migrate
docker-compose exec -T user-service python manage.py migrate
docker-compose exec -T tournament-service python manage.py migrate
docker-compose exec -T submission-service python manage.py migrate

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Show URLs
echo -e "${YELLOW}Available at:${NC}"
echo -e "  ${BLUE}Frontend${NC}:        http://localhost:3000"
echo -e "  ${BLUE}API Gateway${NC}:     http://localhost:8000"
echo -e "  ${BLUE}User Service${NC}:    http://localhost:8001"
echo -e "  ${BLUE}Task Service${NC}:    http://localhost:8002"
echo -e "  ${BLUE}Tournament Service${NC}: http://localhost:8003"
echo ""

# Show useful commands
echo -e "${YELLOW}Useful commands:${NC}"
echo "  docker-compose logs -f              # View all logs"
echo "  docker-compose logs -f user-service # View user service logs"
echo "  docker-compose ps                   # Check container status"
echo "  docker-compose stop                 # Stop all services"
echo "  docker-compose down -v              # Stop and remove services"
echo "  ./run_tests.sh                      # Run tests"
echo ""

echo -e "${YELLOW}Documentation:${NC}"
echo "  Deployment Guide: DEPLOYMENT_GUIDE.md"
echo "  Testing Guide:    TESTING_GUIDE.md"
echo "  Architecture:     ARCHITECTURE.md"
echo ""
