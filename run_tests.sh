#!/bin/bash
# Script to run tests for all services

set -e

echo "========================================="
echo "Running Tests for Tournament Platform"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test user-service
echo -e "${YELLOW}Testing User Service...${NC}"
cd services/user-service
python -m pytest --cov=apps --cov-report=term-missing -v || echo -e "${RED}User Service tests failed${NC}"
cd ../..
echo ""

# Test tournament-service
echo -e "${YELLOW}Testing Tournament Service...${NC}"
cd services/tournament-service
python -m pytest --cov=apps --cov-report=term-missing -v || echo -e "${RED}Tournament Service tests failed${NC}"
cd ../..
echo ""

# Test submission-service
echo -e "${YELLOW}Testing Submission Service...${NC}"
cd services/submission-service
python -m pytest --cov=apps --cov-report=term-missing -v || echo -e "${RED}Submission Service tests failed${NC}"
cd ../..
echo ""

# Test api-gateway
echo -e "${YELLOW}Testing API Gateway...${NC}"
cd api-gateway
python -m pytest --cov=apps --cov-report=term-missing -v || echo -e "${RED}API Gateway tests failed${NC}"
cd ..
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${GREEN}=========================================${NC}"
