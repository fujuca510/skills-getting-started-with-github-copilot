#!/bin/bash
# Test runner script for the High School Management System API

echo "Running FastAPI tests..."
echo "========================="

# Activate virtual environment if it exists, otherwise use system Python
if [ -f ".venv/bin/python" ]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

# Run tests with coverage
$PYTHON_CMD -m pytest tests/ --cov=src --cov-report=term-missing -v

echo ""
echo "Test run complete!"