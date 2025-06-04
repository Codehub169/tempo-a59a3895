from fastapi.testclient import TestClient
from backend.main import app # app should now have WWS data calculated in its mock DB
import os
import shutil
import pytest

# Create a dummy build directory and index.html for SPA serving tests
# This is a simplified way to ensure TestClient can find an index.html
# In a more complex setup, you might use pytest fixtures and temporary directories.

# Determine project root to correctly place the dummy 'build' directory
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEST_STATIC_FILES_DIR = os.path.join(PROJECT_ROOT_DIR, "build")
TEST_INDEX_HTML_PATH = os.path.join(TEST_STATIC_FILES_DIR, "index.html")

@pytest.fixture(scope="session", autouse=True)
def setup_dummy_spa():
    # Create dummy build directory and index.html before tests run
    if not os.path.exists(TEST_STATIC_FILES_DIR):
        os.makedirs(TEST_STATIC_FILES_DIR, exist_ok=True)
    if not os.path.exists(TEST_INDEX_HTML_PATH):
        with open(TEST_INDEX_HTML_PATH, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Test SPA</title></head><body>Test App</body></html>")
    yield
    # Teardown: remove dummy build directory after all tests in the session
    if os.path.exists(TEST_STATIC_FILES_DIR):
        shutil.rmtree(TEST_STATIC_FILES_DIR)

client = TestClient(app)

def test_read_api_root():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RentRightNL API. Visit /docs for API documentation."}

def test_serve_spa_at_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"].lower()
    assert "Test SPA" in response.text # Check content from dummy index.html

def test_read_listings():
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    
    if listings:
        # Assuming listing with ID 1 exists from seed_listings.json
        first_listing = next((l for l in listings if l.get("id") == 1), None)
        assert first_listing is not None, "Listing with ID 1 not found in mock data"
        
        assert "id" in first_listing
        assert "title" in first_listing
        assert "wwsPoints" in first_listing
        assert "maxLegalRent" in first_listing
        assert "wwsBreakdown" in first_listing
        
        # For listing ID 1, check calculated values based on seed_listings.json and wws_calculator.py logic
        # seed_listings.json ID 1: wws_input_data: {surface_area: 75, energy_label: "B", woz_value: 450000, room_count: 2}
        # Calculation:
        # Points: 75 (surface: 75*1) + 20 (B label) + 135 (WOZ: 450000*0.0003) + 5 (rooms: base 5) = 235 points
        # Rent: (235 * 7.50) + 50.00 = 1762.5 + 50 = 1812.50
        assert first_listing["wwsPoints"] == 235 
        assert first_listing["maxLegalRent"] == 1812.50
        assert isinstance(first_listing["wwsBreakdown"], list)
        assert len(first_listing["wwsBreakdown"]) > 0 

def test_read_listing_existing():
    response = client.get("/api/listings/1")
    assert response.status_code == 200
    listing = response.json()
    assert listing["id"] == 1
    assert listing["title"] == "Charming Canal View Apartment"
    assert listing["wwsPoints"] == 235
    assert listing["maxLegalRent"] == 1812.50
    assert isinstance(listing["wwsBreakdown"], list)
    assert len(listing["wwsBreakdown"]) > 0

def test_read_listing_not_existing():
    response = client.get("/api/listings/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Listing not found"}

def test_read_listings_check_advertised_rent():
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    if listings:
        first_listing = next((l for l in listings if l.get("id") == 1), None)
        assert first_listing is not None, "Listing with ID 1 not found for advertised rent check"
        assert "advertisedRent" in first_listing
        assert isinstance(first_listing["advertisedRent"], (int, float))
