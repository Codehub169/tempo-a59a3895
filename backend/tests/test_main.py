from fastapi.testclient import TestClient
from backend.main import app # app should now have WWS data calculated in its mock DB

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Corrected expected message to match main.py
    assert response.json() == {"message": "Welcome to the RentRightNL API. Visit /docs for API documentation."}

def test_read_listings():
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    
    if listings:
        first_listing = next((l for l in listings if l["id"] == 1), None)
        assert first_listing is not None, "Listing with ID 1 not found in mock data"
        
        assert "id" in first_listing
        assert "title" in first_listing
        # Check for WWS fields (using aliases as they appear in API response from response_model_by_alias=True)
        assert "wwsPoints" in first_listing
        assert "maxLegalRent" in first_listing
        assert "wwsBreakdown" in first_listing
        
        # For listing ID 1, check calculated values based on seed_listings.json and wws_calculator.py logic
        # seed_listings.json ID 1: wws_input_data: surface_area: 75, energy_label: "B", woz_value: 450000, room_count: 2
        # Calculation (based on wws_calculator.py logic from summary):
        # Points: 75 (surface: 75 * 1) + 20 (B label) + 135 (WOZ: 450000 * 0.0003) + 5 (rooms: base 5) = 235 points
        # Rent: (235 * 7.50) + 50.00 = 1762.5 + 50 = 1812.50
        
        assert first_listing["wwsPoints"] == 235 
        assert first_listing["maxLegalRent"] == 1812.50
        assert isinstance(first_listing["wwsBreakdown"], list)
        # Expect breakdown items if points are generated from multiple sources
        assert len(first_listing["wwsBreakdown"]) > 0 
        # Example check for a breakdown item (assuming structure and content)
        # This requires knowing the exact output of wws_calculator.py's breakdown formatting
        # e.g., surface_area_item = next((item for item in first_listing["wwsBreakdown"] if "Surface Area" in item["item"]), None)
        # assert surface_area_item is not None
        # assert surface_area_item["points"] == 75

def test_read_listing_existing():
    response = client.get("/api/listings/1")
    assert response.status_code == 200
    listing = response.json()
    assert listing["id"] == 1
    assert listing["title"] == "Charming Canal View Apartment"
    # Verify calculated WWS data for listing 1 (using API aliases)
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
        # Check for a field that should definitely exist from seed_listings.json (using API alias)
        first_listing = next((l for l in listings if l["id"] == 1), None)
        assert first_listing is not None, "Listing with ID 1 not found in mock data for advertised rent check"
        assert "advertisedRent" in first_listing
        assert isinstance(first_listing["advertisedRent"], (int, float))
