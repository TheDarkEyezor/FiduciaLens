#!/bin/bash

# FiduciaLens Test Runner
# Runs all tests and generates coverage report

set -e

echo "🧪 FiduciaLens Test Suite"
echo "======================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if in backend directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: Please run from backend/ directory${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
if [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found. Run setup.sh first.${NC}"
    exit 1
fi

# Install test dependencies
echo -e "${YELLOW}📥 Installing test dependencies...${NC}"
pip install -q -r requirements-test.txt

echo ""
echo -e "${GREEN}✅ Environment ready${NC}"
echo ""

# Run tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Running Backend API Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_api.py -v --tb=short --color=yes || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Running Smart Contract Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_contract.py -v --tb=short --color=yes || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Generating Coverage Report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing || true

echo ""
echo -e "${GREEN}✅ Tests complete!${NC}"
echo ""
echo "📊 View detailed coverage: open htmlcov/index.html"
echo ""
