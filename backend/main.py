from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# FileResponse removed as it's not used
from typing import List, Dict, Any, Optional # Any kept for flexibility, though not explicitly used in this file
import json
import os
import logging # Added for better logging practice

# Import models from .models and .wws_calculator
from .models import Listing as PydanticListing, Amenity as PydanticAmenity, WWSInputData, WWSDetails, WWSBreakdownItem as PydanticWWSBreakdownItem
from .wws_calculator import get_wws_details

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization --- #
app = FastAPI(
    title="RentRightNL API",
    description="API for fetching apartment listings with WWS transparency.",
    version="0.1.0"
)

# --- CORS Middleware --- #
# For production, restrict origins to the actual frontend domain
origins = [
    "http://localhost:3000", # For React dev server
    "http://localhost:9000", # For served app from backend
    # Add production frontend URL here, e.g., "https://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"], # Restrict to GET if only GET is needed for these endpoints
    allow_headers=["Content-Type"], # Be specific about allowed headers if possible
)

# --- Mock Database --- #
_MOCK_LISTINGS_DB: Dict[int, PydanticListing] = {}

def load_mock_data():
    global _MOCK_LISTINGS_DB
    # Use absolute path for data file to be robust
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(base_dir, 'data', 'seed_listings.json')
    
    try:
        with open(data_file_path, 'r', encoding='utf-8') as f:
            raw_listings_data = json.load(f)
            processed_listings_count = 0
            for listing_data_from_json in raw_listings_data:
                listing_payload = listing_data_from_json.copy()
                listing_id = listing_data_from_json.get('id', 'UNKNOWN')

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

                if adapted_wws_input_dict["size_m2"] is not None and adapted_wws_input_dict["rooms"] is not None:
                    try:
                        validated_wws_input = WWSInputData(**adapted_wws_input_dict)
                        wws_details_result: WWSDetails = get_wws_details(validated_wws_input.model_dump())
                        wws_points_val = wws_details_result.points
                        max_legal_rent_val = wws_details_result.max_rent
                        wws_breakdown_val = wws_details_result.breakdown
                    except Exception as e_calc:
                        logger.warning(f"Could not calculate WWS for listing ID {listing_id}: {e_calc}", exc_info=True)
                else:
                    logger.warning(f"Missing 'surface_area' or 'rooms' for WWS calculation for listing ID {listing_id}. Skipping WWS calculation.")

                listing_payload_for_model = {
                    **listing_payload,
                    "wws_points": wws_points_val,
                    "max_legal_rent": max_legal_rent_val,
                    "wws_breakdown": wws_breakdown_val,
                    "amenities": [PydanticAmenity(**a) for a in listing_payload.get('amenities', [])]
                }
                
                try:
                    listing_obj = PydanticListing(**listing_payload_for_model)
                    _MOCK_LISTINGS_DB[listing_obj.id] = listing_obj
                    processed_listings_count += 1
                except Exception as e_model:
                     logger.error(f"Failed to create PydanticListing for ID {listing_id}: {e_model}", exc_info=True)

            logger.info(f"Successfully loaded and processed {processed_listings_count} listings into in-memory DB.")
            if processed_listings_count != len(raw_listings_data):
                logger.warning(f"Attempted to load {len(raw_listings_data)} listings, but only {processed_listings_count} were successfully processed.")

    except FileNotFoundError:
        logger.error(f"Mock data file not found at {data_file_path}. API will return empty data.")
        _MOCK_LISTINGS_DB = {}
    except json.JSONDecodeError:
        logger.error(f"Could not decode JSON from {data_file_path}. Ensure it is valid JSON.", exc_info=True)
        _MOCK_LISTINGS_DB = {}
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading mock data: {e}", exc_info=True)
        _MOCK_LISTINGS_DB = {}

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: loading mock data...")
    load_mock_data()
    logger.info("Mock data loading complete.")

# --- API Endpoints (Define before SPA mount) --- #

@app.get("/api/", response_model_by_alias=True)
async def read_api_root():
    return {"message": "Welcome to the RentRightNL API. Visit /docs for API documentation."}

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

# --- Serve Static React App (Define this last) --- #
# Path to the React build directory, relative to this file (backend/main.py)
# ProjectRoot/backend/main.py -> ProjectRoot/build
STATIC_FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build"))

if os.path.exists(STATIC_FILES_DIR) and os.path.isdir(STATIC_FILES_DIR):
    logger.info(f"Serving static files from: {STATIC_FILES_DIR}")
    app.mount("/", StaticFiles(directory=STATIC_FILES_DIR, html=True), name="spa")
else:
    logger.warning(f"Frontend build directory not found at {STATIC_FILES_DIR}. Frontend will not be served.")
    @app.get("/")
    async def missing_frontend_fallback():
        raise HTTPException(
            status_code=503,
            detail=f"Frontend not found. Please build the frontend. Expected at: {STATIC_FILES_DIR}"
        )
