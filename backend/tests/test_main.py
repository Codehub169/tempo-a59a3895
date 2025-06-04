from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Ensure the mock data is loaded by FastAPI's startup event before tests run
# TestClient handles the lifespan events like startup and shutdown for the app.

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to RentRightNL API"}

def test_read_listings():
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    # Check if there's at least one listing, assuming seed_listings.json is not empty
    # and main.py's load_mock_data works.
    if listings:
        assert "id" in listings[0]
        assert "title" in listings[0]
        # According to main.py summary, WWS fields might be None if not in seed_listings.json
        # and if main.py's load_mock_data doesn't calculate them.
        # Our seed_listings.json does not contain pre-calculated WWS data.
        assert listings[0].get("wws_points") is None 
        assert listings[0].get("max_legal_rent") is None
        assert listings[0].get("wws_breakdown") is None 

def test_read_listing_existing():
    # Assuming listing with ID 1 exists from seed_listings.json loaded by main.py
    response = client.get("/api/listings/1")
    assert response.status_code == 200
    listing = response.json()
    assert listing["id"] == 1
    assert listing["title"] == "Charming Canal View Apartment"
    assert listing.get("wws_points") is None # As per current main.py mock data loading

def test_read_listing_not_existing():
    response = client.get("/api/listings/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Listing with ID 999 not found"}

def test_read_listings_check_advertised_rent():
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    if listings:
        # Check for a field that should definitely exist from seed_listings.json
        assert "advertised_rent" in listings[0]
        assert isinstance(listings[0]["advertised_rent"], (int, float))
