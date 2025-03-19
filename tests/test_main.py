import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.main import app, get_db
from app.models import Base  # Import Base directly from models

# in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    #echo=True
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test data
ENGLISH_PALINDROME = "Able was I ere I saw Elba"
SPANISH_PALINDROME = "Dábale arroz a la zorra el abad"
NOT_PALINDROME = "This is not a palindrome"

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# basic testing of service
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Test" in response.json()

def test_detect_palindrome_english(setup_database):
    user = {
            "text": ENGLISH_PALINDROME,
            "language": "en"
            }
    response = client.post(
        "/detect/",
        json=user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_palindrome"] is True
    assert data["language"] == "en"
    assert "id" in data
    assert "timestamp" in data

def test_detect_palindrome_spanish(setup_database):
    user = {
        "text": SPANISH_PALINDROME,
        "language": "es"
    }
    response = client.post(
        "/detect/",
        json=user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_palindrome"] is True
    assert data["language"] == "es"
    assert "id" in data
    assert "timestamp" in data

def test_detect_non_palindrome(setup_database):
    user = {
        "text": NOT_PALINDROME,
        "language": "en"
    }
    response = client.post(
        "/detect/",
        json=user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_palindrome"] is False


def test_get_detections(setup_database):
    # add test data
    client.post("/detect/", json={"text": ENGLISH_PALINDROME, "language": "en"})
    client.post("/detect/", json={"text": SPANISH_PALINDROME, "language": "es"})

    # test without filters
    response = client.get("/detections")
    assert response.status_code == 200
    data = response.json()
    # we should get 2 results
    assert len(data) == 2

    # test with language filter
    response = client.get("/detections?language=es")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1 # only one
    assert data[0]["language"] == "es"
    assert data[0]["text"] == SPANISH_PALINDROME


def test_get_detection_by_id(setup_database):
    user = {
        "text": ENGLISH_PALINDROME,
        "language": "en"
    }
    response = client.post(
        "/detect/",
        json=user
    )
    detection_id = response.json()["id"]

    # get by ID
    response = client.get(f"/detections/{detection_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == detection_id
    assert data["text"] == ENGLISH_PALINDROME
    assert data["is_palindrome"] is True


def test_get_nonexistent_detection(setup_database):
    # try to get a detection it doesn't exist
    response = client.get("/detections/999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_all_records(setup_database):
    client.post("/detect/", json={"text": ENGLISH_PALINDROME, "language": "en"})
    client.post("/detect/", json={"text": SPANISH_PALINDROME, "language": "es"})
    client.post("/detect/", json={"text": NOT_PALINDROME, "language": "en"})
    client.post("/detect/", json={"text": NOT_PALINDROME, "language": "es"})

    response = client.get("/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

def test_delete_detection(setup_database):
    user = {
        "text": ENGLISH_PALINDROME,
        "language": "en"
    }
    response = client.post(
        "/detect/",
        json=user
    )
    detection_id = response.json()["id"]

    # delete it
    response = client.delete(f"/detections/{detection_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # verify it's not there anymore
    response = client.get(f"/detections/{detection_id}")
    assert response.status_code == 404


def test_delete_nonexistent_detection(setup_database):
    response = client.delete("/detections/999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_date_filtering(setup_database):
    client.post("/detect/", json={"text": ENGLISH_PALINDROME, "language": "en"})
    client.post("/detect/", json={"text": SPANISH_PALINDROME, "language": "es"})

    # get current date/time for testing
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)

    # test date filters. should get results (between yesterday and tomorrow)
    response = client.get(f"/detections?from_date={yesterday}&to_date={tomorrow}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # should get 0 results
    response = client.get(f"/detections?from_date={tomorrow}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_no_database():
    response = client.post("/detect/", json={"text": ENGLISH_PALINDROME, "language": "en"})
    assert response.status_code == 500
    data = response.json()
    assert data["info"] == "A database error occurred."