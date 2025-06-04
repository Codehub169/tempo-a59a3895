import json
import os
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, create_db_and_tables, ListingORM, AmenityORM, WWSBreakdownItemORM
from .models import WWSInputData, WWSDetails, WWSBreakdownItem # Corrected: WWSDetails and WWSBreakdownItem are from .models
from .wws_calculator import get_wws_details # Corrected: WWSDetails is not imported from here

# Determine the correct path to the JSON file relative to this script
# This script is in backend/, data is in backend/data/
SEED_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'seed_listings.json')

def seed_database():
    print("Creating database tables...")
    create_db_and_tables() # Ensures tables are created via database.py logic
    print("Database tables created (if they didn't exist).")

    db: Session = SessionLocal()

    try:
        # Clear existing data order carefully due to foreign key constraints
        print("Clearing existing data...")
        db.query(AmenityORM).delete()
        db.query(WWSBreakdownItemORM).delete()
        db.query(ListingORM).delete()
        db.commit()
        print("Existing data cleared.")

        print(f"Loading seed data from: {SEED_DATA_PATH}")
        with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
            listings_data = json.load(f)
        print(f"Loaded {len(listings_data)} listings from JSON.")

        for listing_data in listings_data:
            print(f"Processing listing ID: {listing_data['id']}")
            
            raw_wws_inputs = listing_data['wws_input_data']
            
            # Adapt raw_wws_inputs from JSON to WWSInputData model structure
            adapted_wws_input_dict = {
                "size_m2": raw_wws_inputs.get("surface_area"),
                "rooms": raw_wws_inputs.get("room_count"),
                "energy_label": raw_wws_inputs.get("energy_label"),
                "woz_value": raw_wws_inputs.get("woz_value"),
            }
            # Validate with Pydantic model before passing to calculator
            # This ensures data types are correct before calculator uses them.
            validated_wws_input = WWSInputData(**adapted_wws_input_dict)

            # Pass the dictionary representation of validated inputs to the calculator
            # get_wws_details expects a dict and will parse it internally with WWSInputData
            wws_results: WWSDetails = get_wws_details(validated_wws_input.model_dump()) 

            db_listing = ListingORM(
                id=listing_data['id'],
                title=listing_data['title'],
                location=listing_data['location'],
                images=listing_data['images'], # Stored as JSON
                advertised_rent=listing_data['advertised_rent'],
                size_m2=listing_data['size'], # JSON 'size' maps to ORM 'size_m2'
                rooms=listing_data['rooms'],
                description=listing_data['description'],
                wws_points=wws_results.points,
                max_legal_rent=wws_results.max_rent,
                raw_wws_inputs=raw_wws_inputs, # Stored as JSON
                energy_label=validated_wws_input.energy_label, 
                woz_value=validated_wws_input.woz_value 
            )

            for amenity_data in listing_data.get('amenities', []):
                db_amenity = AmenityORM(
                    name=amenity_data['name'],
                    icon=amenity_data['icon'],
                    listing_id=db_listing.id
                )
                db_listing.amenities.append(db_amenity)
            
            if wws_results.breakdown:
                # wws_results.breakdown contains Pydantic WWSBreakdownItem models
                for item_data_pydantic in wws_results.breakdown: 
                    db_breakdown_item = WWSBreakdownItemORM(
                        item=item_data_pydantic.item,
                        points=item_data_pydantic.points,
                        listing_id=db_listing.id
                    )
                    db_listing.wws_breakdown.append(db_breakdown_item)
            
            db.add(db_listing)
        
        db.commit()
        print(f"Successfully seeded {len(listings_data)} listings into the database.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding process...")
    seed_database()
    print("Database seeding process finished.")
