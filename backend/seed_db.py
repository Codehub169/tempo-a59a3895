import json
import os
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine, create_db_and_tables, ListingORM, AmenityORM, WWSBreakdownItemORM
from backend.models import WWSInputData, WWSDetails # Assuming WWSDetails is the return type of get_wws_details
from backend.wws_calculator import get_wws_details

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
        with open(SEED_DATA_PATH, 'r') as f:
            listings_data = json.load(f)
        print(f"Loaded {len(listings_data)} listings from JSON.")

        for listing_data in listings_data:
            print(f"Processing listing ID: {listing_data['id']}")
            # Validate and parse wws_input_data
            # The get_wws_details function in wws_calculator.py expects a dict, not a Pydantic model instance
            raw_wws_inputs = listing_data['wws_input_data']
            
            # Call WWS calculator
            # Ensure get_wws_details returns an object with points, max_rent, and breakdown attributes
            wws_results: WWSDetails = get_wws_details(raw_wws_inputs)

            db_listing = ListingORM(
                id=listing_data['id'],
                title=listing_data['title'],
                location=listing_data['location'],
                images=listing_data['images'], # Stored as JSON
                advertised_rent=listing_data['advertised_rent'],
                size=listing_data['size'],
                rooms=listing_data['rooms'],
                description=listing_data['description'],
                wws_points=wws_results.points,
                max_legal_rent=wws_results.max_rent,
                raw_wws_inputs=raw_wws_inputs # Stored as JSON
            )

            for amenity_data in listing_data.get('amenities', []):
                db_amenity = AmenityORM(
                    name=amenity_data['name'],
                    icon=amenity_data['icon'],
                    listing_id=db_listing.id
                )
                db_listing.amenities.append(db_amenity)
            
            if wws_results.breakdown:
                for item_data in wws_results.breakdown:
                    db_breakdown_item = WWSBreakdownItemORM(
                        item=item_data.item,
                        points=item_data.points,
                        listing_id=db_listing.id
                    )
                    db_listing.wws_breakdown_items.append(db_breakdown_item)
            
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
