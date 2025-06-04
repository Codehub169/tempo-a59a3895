from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import json
import os

# --- Pydantic Models --- #

class Amenity(BaseModel):
    name: str
    icon: str

class WWSBreakdownItem(BaseModel):
    item: str
    points: int

class Listing(BaseModel):
    id: int
    title: str
    location: str
    images: List[str] # URLs to images
    advertisedRent: float = Field(..., alias='advertisedRent')
    size: int # in m
    rooms: int
    wwsPoints: int = Field(..., alias='wwsPoints')
    maxLegalRent: float = Field(..., alias='maxLegalRent')
    description: str
    amenities: List[Amenity]
    wwsBreakdown: List[WWSBreakdownItem] = Field(..., alias='wwsBreakdown')

    class Config:
        populate_by_name = True # Allows using alias for field names

# --- FastAPI App Initialization --- #
app = FastAPI(
    title="RentRightNL API",
    description="API for fetching apartment listings with WWS transparency.",
    version="0.1.0"
)

# --- CORS Middleware --- #
# Allows requests from the React frontend (typically on http://localhost:3000 or http://localhost:9000)
origins = [
    "http://localhost:3000",
    "http://localhost:9000",
    # Add any other origins if necessary (e.g., deployed frontend URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Mock Database --- #
# Load mock data from a JSON file or define inline
# This will be replaced by actual database logic later.

_MOCK_LISTINGS_DB: Dict[int, Listing] = {}

def load_mock_data():
    global _MOCK_LISTINGS_DB
    # Path relative to this file's location
    data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'seed_listings.json')
    try:
        with open(data_file_path, 'r') as f:
            raw_data = json.load(f)
            # Convert raw_data (expected to be a list of listing dicts) to Pydantic models
            # and store them in a dictionary keyed by ID for easy lookup.
            for listing_dict in raw_data:
                # Pydantic will handle alias mapping here if aliases are defined in the model
                listing_obj = Listing(**listing_dict)
                _MOCK_LISTINGS_DB[listing_obj.id] = listing_obj
        print(f"Successfully loaded {len(_MOCK_LISTINGS_DB)} listings from {data_file_path}")
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

@app.get("/api/listings", response_model=List[Listing])
async def get_all_listings():
    """Retrieve all available apartment listings."""
    if not _MOCK_LISTINGS_DB:
        # This could happen if seed_listings.json is missing or empty
        # Depending on requirements, could return an error or empty list
        return [] 
    return list(_MOCK_LISTINGS_DB.values())

@app.get("/api/listings/{listing_id}", response_model=Listing)
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

# To run the app (from the project root directory, assuming backend folder is at the same level as startup.sh):
# uvicorn backend.main:app --reload --port 8000
