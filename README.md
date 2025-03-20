# Palindrome Detection API

A FastAPI-based RESTful API for detecting and managing palindromes in English and Spanish (for now).

[![Test Coverage: 98%](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](https://github.com/username/palindrome-api)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)

## Overview

This API allows you to:
- Detect if a given text is a palindrome in English or Spanish
- Store palindrome detection results in a database
- View detailed information about palindrome detections
- Delete stored detections

The API handles language-specific features (such as Spanish accents) and provides comprehensive filtering capabilities for retrieval operations.

## Features

- **Language Support**: English and Spanish palindrome detection
- **Special Character Handling**: Properly handles punctuation, whitespace, and Spanish accents
- **Database Storage**: Stores all detection attempts for later retrieval
- **Flexible Querying**: Filter by language, date range, and more
- **RESTful Design**: Follows REST API design principles
- **Comprehensive Testing**: 98% test coverage

## API Endpoints

### Root Endpoint
- **GET /** - Basic health check/test endpoint

### Palindrome Detection
- **POST /detect/** - Check if a text is a palindrome
  - Request Body: `{"text": "Your palindrome here", "language": "en"}`
  - Response: Detection result with ID and timestamp

### Retrieval Endpoints
- **GET /detections** - Get all palindrome detections with optional filters
  - Query Parameters:
    - `from_date`: Filter by date (starting from)
    - `to_date`: Filter by date (up to)
    - `language`: Filter by language ("en" or "es")
  
- **GET /detections/{detection_id}** - Get a specific detection by ID
  - Path Parameter: `detection_id` - The ID of the detection to retrieve

- **GET /all** - Get all records (both palindromes and non-palindromes)

### Deletion Endpoint
- **DELETE /detections/{detection_id}** - Delete a specific detection
  - Path Parameter: `detection_id` - The ID of the detection to delete

## Installation

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (optional, for containerized deployment)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/esmitt/palindrome-api.git
   cd palindrome-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   venv\Scripts\activate # on Linux source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your configuration:
   ```
   # Development settings
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///palindrome.db
   
   # Production settings (uncomment when deploying to production)
   # ENVIRONMENT=production
   # DATABASE_URL=postgresql://user:password@db:5432/palindrome
   ```
   > For the purpose of testing, the .env is in the repo

## Running the API

### Local Development

Run the API using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Using Docker

The project includes Docker configurations for easy deployment:

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## Testing

### Running Tests

Execute tests using pytest:

```bash
pytest -vv
```

If you are running the Docker, then:
```bash
docker exec -it palindrome_api bash
pytest -vv
```

### Test Coverage

To check test coverage:

```bash
coverage run -m pytest tests/
coverage report -m
```

Current coverage report (98%):
```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
app\__init__.py                 0      0   100%
app\api\__init__.py             0      0   100%
app\api\endpoints.py           46      0   100%
app\core\__init__.py            0      0   100%
app\core\config.py             14      0   100%
app\core\palindrome.py         27      0   100%
app\db\__init__.py              0      0   100%
app\db\base.py                 26      0   100%
app\db\crud.py                 38      0   100%
app\db\models.py               12      0   100%
app\main.py                    28      7    75%   21-27, 50
app\schemas\__init__.py         0      0   100%
app\schemas\enums.py            4      0   100%
app\schemas\palindrome.py      23      0   100%
tests\__init__.py               0      0   100%
tests\conftest.py               3      0   100%
tests\test_endpoints.py       128      0   100%
tests\test_palindrome.py       23      0   100%
---------------------------------------------------------
TOTAL                         372      7    98%
```

## API Documentation

When the API is running, you can access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Configuration

The application supports two main environments:

### Development
- Debugging enabled
- SQLite database by default
- Automatic reloading of code changes

### Production
- Debugging disabled
- Compatible with PostgreSQL or other production databases
- Optimized for performance

To switch between environments, modify the `ENVIRONMENT` variable in your `.env` file.

## Project Structure

```
palindrome-api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Application configuration
│   │   └── palindrome.py    # Palindrome detection logic
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # Database connection setup
│   │   ├── crud.py          # Database operations
│   │   └── models.py        # Database models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── enums.py         # Enumerations (e.g., Language)
│   │   └── palindrome.py    # Pydantic models/schemas
│   ├── __init__.py
│   └── main.py              # Application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_endpoints.py    # API endpoint tests
│   └── test_palindrome.py   # Palindrome logic tests
├── .env                     # Environment variables
├── docker-compose.yaml      # Docker Compose configuration
├── Dockerfile               # Docker build configuration
├── pytest.ini               # Pytest configuration
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## Palindrome Algorithm

The algorithm for detection of a palindrome text is based on the two-pointer approach.

This allows to get a `O(n)` even for preprocessing and detection.

One possible "regular" option, could be something like:
```python
def is_palindrome(self) -> bool:
    cleaned_text = ''.join(char.lower() for char in self.text if char.isalnum())
    return cleaned_text == cleaned_text[::-1]
```

## TODO List

1. **Database Migration**: Adding Alembic for database migrations.
2. **Authentication**: Add JWT or OAuth2 authentication for production deployments.
3. **Rate Limiting**: Implement rate limiting to prevent API abuse.
4. **Caching**: Add Redis caching for frequently accessed endpoints.
5. **Logging**: Enhance logging for production environments.
6. **CI/CD**: Set up automated testing and deployment pipelines.
7. **Monitoring**: Add monitoring with Prometheus and Grafana.
