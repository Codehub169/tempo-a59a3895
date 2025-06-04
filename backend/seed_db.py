import json
import os
from sqlalchemy.orm import Session

# Import DATABASE_FILE_PATH from database.py
from .database import SessionLocal, engine, create_db_and_tables, ListingORM, AmenityORM, WWSBreakdownItemORM, DATABASE_FILE_PATH
from .models import WWSInputData, WWSDetails, WWSBreakdownItem # Corrected: WWSDetails and WWSBreakdownItem are from .models
from .wws_calculator import get_wws_details # Corrected: WWSDetails is not imported from here

# Determine the correct path to the JSON file relative to this script
# This script is in backend/, data is in backend/data/
SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'seed_listings.json')

def seed_database():
    # Remove existing database file to ensure a clean start if it exists
    # DATABASE_FILE_PATH is an absolute path defined in database.py
    if os.path.exists(DATABASE_FILE_PATH):
        print(f"Found existing database file at {DATABASE_FILE_PATH}. Removing it to ensure fresh seeding.")
        try:
            os.remove(DATABASE_FILE_PATH)
            print("Old database file removed.")
        except OSError as e:
            # If removal fails, print a warning. The subsequent create_db_and_tables might still fail if the file is problematic and locked.
            print(f"Warning: Could not remove existing database file {DATABASE_FILE_PATH}: {e}. Seeding might fail if the file is invalid or locked.")

    print("Creating database tables...")
    create_db_and_tables() # Ensures tables are created via database.py logic (idempotent)
    print("Database tables created (if they didn't exist).")

    db: Session = SessionLocal()

    try:
        # Clearing data from tables is still a good practice after ensuring schema,
        # even if the file was removed, to handle cases where removal failed.
        # Delete order: dependent tables first, then principal table.
        print("Clearing existing data from tables (if any)...")
        db.query(AmenityORM).delete()
        db.query(WWSBreakdownItemORM).delete()
        db.query(ListingORM).delete()
        db.commit()
        print("Existing data cleared from tables.")

        print(f"Loading seed data from: {SEED_DATA_PATH}")
        with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
            listings_data = json.load(f)
        print(f"Loaded {len(listings_data)} listings from JSON.")

        for listing_data in listings_data:
            print(f"Processing listing ID: {listing_data['id']}")
            
            # Assuming 'wws_input_data' key is always present in each listing in seed_listings.json.
            # If it could be missing, listing_data.get('wws_input_data', {}) would be safer.
            raw_wws_inputs = listing_data['wws_input_data']
            
            adapted_wws_input_dict = {
                "size_m2": raw_wws_inputs.get("surface_area"),
                "rooms": raw_wws_inputs.get("room_count"),
                "energy_label": raw_wws_inputs.get("energy_label"),
                "woz_value": raw_wws_inputs.get("woz_value"),
            }
            
            # WWSInputData will raise pydantic.ValidationError if required fields (size_m2, rooms)
            # are None (e.g. "surface_area" missing in raw_wws_inputs) or of incorrect type.
            # This error is not caught per-item, so it will stop the entire seeding process (fail-fast approach).
            # This is acceptable for a seeder to enforce seed data quality.
            validated_wws_input = WWSInputData(**adapted_wws_input_dict)
            
            # get_wws_details expects a dictionary. validated_wws_input.model_dump() provides this.
            # get_wws_details has internal error handling for parsing its input_data_dict;
            # it returns a WWSDetails object with 0 points/rent if parsing fails.
            wws_results: WWSDetails = get_wws_details(validated_wws_input.model_dump()) 

            db_listing = ListingORM(
                id=listing_data['id'],
                title=listing_data['title'],
                location=listing_data['location'],
                images=listing_data['images'], # Stored as JSON by SQLAlchemy
                advertised_rent=listing_data['advertised_rent'],
                size_m2=listing_data['size'], # JSON 'size' maps to ORM 'size_m2'
                rooms=listing_data['rooms'],
                description=listing_data['description'],
                wws_points=wws_results.points,
                max_legal_rent=wws_results.max_rent,
                raw_wws_inputs=raw_wws_inputs, # Store the original raw inputs as JSON
                energy_label=validated_wws_input.energy_label, # Store from validated input
                woz_value=validated_wws_input.woz_value    # Store from validated input
            )

            # Process amenities, using .get for safety if 'amenities' key might be missing
            for amenity_data in listing_data.get('amenities', []):
                db_amenity = AmenityORM(
                    name=amenity_data['name'],
                    icon=amenity_data['icon'],
                    listing_id=db_listing.id # Foreign key; SQLAlchemy also infers from relationship append
                )
                db_listing.amenities.append(db_amenity) # Add to relationship collection
            
            # Process WWS breakdown items if available
            if wws_results.breakdown: # wws_results.breakdown can be None or an empty list
                for item_data_pydantic in wws_results.breakdown: # item_data_pydantic is a WWSBreakdownItem Pydantic model
                    db_breakdown_item = WWSBreakdownItemORM(
                        item=item_data_pydantic.item,
                        points=item_data_pydantic.points,
                        listing_id=db_listing.id # Foreign key
                    )
                    db_listing.wws_breakdown.append(db_breakdown_item) # Add to relationship collection
            
            db.add(db_listing) # Add the main listing object (and its cascaded children) to the session
        
        db.commit() # Commit all changes for all listings at once after the loop
        print(f"Successfully seeded {len(listings_data)} listings into the database.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback() # Rollback in case of any error during the process
    finally:
        db.close() # Always close the session to free resources

if __name__ == "__main__":
    print("Starting database seeding process...")
    seed_database()
    print("Database seeding process finished.")
