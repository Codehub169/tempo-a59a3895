from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import json
import os

# Import models from .models and .wws_calculator
from .models import Listing as PydanticListing, Amenity as PydanticAmenity, WWSInputData, WWSDetails, WWSBreakdownItem as PydanticWWSBreakdownItem # Corrected imports
from .wws_calculator import get_wws_details # Corrected: WWSDetails and WWSBreakdownItem not imported from here

# --- FastAPI App Initialization --- #
app = FastAPI(
    title="RentRightNL API",
    description="API for fetching apartment listings with WWS transparency.",
    version="0.1.0"
)

# --- CORS Middleware --- #
origins = [
    "http://localhost:3000",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mock Database --- #
_MOCK_LISTINGS_DB: Dict[int, PydanticListing] = {}

def load_mock_data():
    global _MOCK_LISTINGS_DB
    data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'seed_listings.json')
    try:
        with open(data_file_path, 'r', encoding='utf-8') as f:
            raw_listings_data = json.load(f)
            for listing_data_from_json in raw_listings_data:
                listing_payload = listing_data_from_json.copy()

                wws_input_data_raw = listing_payload.pop('wws_input_data', {})
                
                adapted_wws_input_dict = {
                    "size_m2": wws_input_data_raw.get("surface_area"),
                    "rooms": wws_input_data_raw.get("room_count"),
                    "energy_label": wws_input_data_raw.get("energy_label"),
                    "woz_value": wws_input_data_raw.get("woz_value"),
                }
                
                wws_points_val: Optional[int] = None
                max_legal_rent_val: Optional[float] = None
                wws_breakdown_val: List[PydanticWWSBreakdownItem] = []

                if adapted_wws_input_dict["size_m2"] is not None: 
                    try:
                        # WWSInputData expects Pythonic names (e.g. size_m2)
                        validated_wws_input = WWSInputData(**adapted_wws_input_dict)
                        # get_wws_details also expects a dict with Pythonic names
                        wws_details_result: WWSDetails = get_wws_details(validated_wws_input.model_dump())
                        wws_points_val = wws_details_result.points
                        max_legal_rent_val = wws_details_result.max_rent
                        # wws_details_result.breakdown contains PydanticWWSBreakdownItem instances
                        wws_breakdown_val = wws_details_result.breakdown 
                    except Exception as e_calc:
                        print(f"Warning: Could not calculate WWS for listing ID {listing_data_from_json['id']}: {e_calc}")
                else:
                    print(f"Warning: Missing 'surface_area' (size_m2) for WWS calculation for listing ID {listing_data_from_json['id']}. Skipping WWS calculation.")

                listing_payload_for_model = {
                    **listing_payload, 
                    "wws_points": wws_points_val,
                    "max_legal_rent": max_legal_rent_val,
                    "wws_breakdown": wws_breakdown_val,
                    "amenities": [PydanticAmenity(**a) for a in listing_payload.get('amenities', [])]
                }
                
                # PydanticListing (models.Listing) uses aliases for some fields (e.g. size for size_m2)
                # It expects Pythonic names for construction if populate_by_name=True is set in Config, 
                # or aliased names if not. seed_listings.json uses 'advertised_rent' and 'size'.
                # models.ListingBase has aliases: advertised_rent (alias advertisedRent), size_m2 (alias size).
                # The payload already contains 'advertised_rent' and 'size' with these keys, which is fine for pydantic.
                listing_obj = PydanticListing(**listing_payload_for_model)
                _MOCK_LISTINGS_DB[listing_obj.id] = listing_obj
        print(f"Successfully loaded and processed {len(_MOCK_LISTINGS_DB)} listings into in-memory DB.")
    except FileNotFoundError:
        print(f"Warning: Mock data file not found at {data_file_path}. API will return empty data.")
        _MOCK_LISTINGS_DB = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {data_file_path}.")
        _MOCK_LISTINGS_DB = {}
    except Exception as e:
        print(f"An unexpected error occurred while loading mock data: {e}")
        _MOCK_LISTINGS_DB = {}

@app.on_event("startup")
async def startup_event():
    load_mock_data()

# --- API Endpoints --- #

@app.get("/api/listings", response_model=List[PydanticListing], response_model_by_alias=True)
async def get_all_listings():
    """Retrieve all available apartment listings."""
    if not _MOCK_LISTINGS_DB:
        return [] 
    return list(_MOCK_LISTINGS_DB.values())

@app.get("/api/listings/{listing_id}", response_model=PydanticListing, response_model_by_alias=True)
async def get_listing_by_id(listing_id: int):
    """Retrieve a specific apartment listing by its ID."""
    listing = _MOCK_LISTINGS_DB.get(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

# --- Root Endpoint (Optional) --- #
@app.get("/")
async def read_root():
    return {"message": "Welcome to the RentRightNL API. Visit /docs for API documentation."}
