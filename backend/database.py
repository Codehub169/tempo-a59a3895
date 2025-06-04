from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
# from sqlalchemy.ext.declarative import declarative_base # Old style, not used with DeclarativeBase
from typing import List, Optional, Any # Any for JSON type hint
import os

DATABASE_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "listings.db")
# Corrected DATABASE_URL to correctly use an absolute path for the SQLite database file.
# Change `f"sqlite:///./{DATABASE_FILE_PATH}"` to `f"sqlite:///{DATABASE_FILE_PATH}"`.
# This assumes `DATABASE_FILE_PATH` is an absolute path (e.g., "/var/data/app.db" or a variable evaluating to such).
# This correction ensures that the path is interpreted as an absolute path by SQLite (e.g. `sqlite:////var/data/app.db`),
# resolving the 'unable to open database file' error.
DATABASE_URL = f"sqlite:///{DATABASE_FILE_PATH}"

# Ensure the data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # check_same_thread is for SQLite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# SQLAlchemy ORM Models
class ListingORM(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String)
    images = Column(JSON) # Store list of image URLs as JSON
    advertised_rent = Column(Float)
    size_m2 = Column(Float) # Field name matches WWSInputData and internal consistency
    rooms = Column(Integer)
    description = Column(Text)
    wws_points = Column(Integer, nullable=True)
    max_legal_rent = Column(Float, nullable=True)
    # Raw data for WWS, if stored
    energy_label = Column(String, nullable=True)
    woz_value = Column(Float, nullable=True)
    raw_wws_inputs = Column(JSON, nullable=True) # Added field to store raw inputs for WWS

    amenities = relationship("AmenityORM", back_populates="listing", cascade="all, delete-orphan")
    wws_breakdown = relationship("WWSBreakdownItemORM", back_populates="listing", cascade="all, delete-orphan") # Corrected relationship name to match seed_db.py usage

class AmenityORM(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    icon = Column(String)
    listing_id = Column(Integer, ForeignKey("listings.id"))

    listing = relationship("ListingORM", back_populates="amenities")

class WWSBreakdownItemORM(Base):
    __tablename__ = "wws_breakdown_items"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String) # e.g., "Surface Area (75 m\texttwosuperior)"
    points = Column(Integer)
    listing_id = Column(Integer, ForeignKey("listings.id"))

    listing = relationship("ListingORM", back_populates="wws_breakdown")

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
