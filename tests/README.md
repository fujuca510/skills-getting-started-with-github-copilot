# Tests for High School Management System API

This directory contains comprehensive pytest tests for the FastAPI application.

## Test Structure

- `test_app.py` - Main test file containing all API endpoint tests
- `conftest.py` - Shared pytest configuration and path setup
- `__init__.py` - Makes the directory a Python package

## Test Categories

### 1. Root Endpoint Tests (`TestRootEndpoint`)
- Tests the root `/` endpoint redirect functionality

### 2. Activities Listing Tests (`TestGetActivities`)
- Tests the `GET /activities` endpoint
- Verifies data structure and content

### 3. Signup Tests (`TestSignupEndpoint`)
- Tests the `POST /activities/{activity_name}/signup` endpoint
- Covers success cases, error conditions, and edge cases
- Tests capacity limits and duplicate signup prevention

### 4. Unregister Tests (`TestUnregisterEndpoint`)
- Tests the `DELETE /activities/{activity_name}/unregister` endpoint
- Covers success cases and error conditions
- Tests participant removal functionality

### 5. Edge Cases (`TestEdgeCases`)
- Tests email validation
- Tests missing parameters
- Tests invalid input formats

### 6. Data Integrity Tests (`TestDataIntegrity`)
- Tests multiple operations in sequence
- Verifies state management and data consistency
- Tests capacity tracking accuracy

## Running Tests

### Method 1: Using the test runner script
```bash
./run_tests.sh
```

### Method 2: Using pytest directly
```bash
# Basic test run
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing -v

# Run specific test class
python -m pytest tests/test_app.py::TestSignupEndpoint -v

# Run specific test
python -m pytest tests/test_app.py::TestSignupEndpoint::test_signup_success -v
```

## Test Coverage

The test suite achieves **100% code coverage** of the FastAPI application, ensuring all code paths are tested.

## Test Dependencies

- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `httpx` - HTTP client for FastAPI testing (via TestClient)

## Fixtures

- `client` - FastAPI TestClient instance for making HTTP requests
- `fresh_activities` - Resets the activities database to a clean state before each test

## Test Data

Tests use a simplified set of activities:
- Chess Club (with existing participants)
- Programming Class (with existing participants)  
- Basketball Team (empty, for testing signups)

This provides a good mix of scenarios for comprehensive testing.