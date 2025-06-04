from pydantic import BaseModel, Field
from typing import List, Optional

# Pydantic models for API requests and responses
# These models define the structure of data exchanged with the frontend

class Amenity(BaseModel):
    name: str
    icon: str

class WWSBreakdownItem(BaseModel):
    item: str
    points: int

class ListingBase(BaseModel):
    title: str
    location: str
    images: List[str] = []
    advertised_rent: float = Field(..., alias="advertisedRent")
    size_m2: float = Field(..., alias="size") # Renamed from 'size' to 'size_m2' for clarity, alias for frontend 'size'
    rooms: int
    description: str
    # Raw data for WWS calculation - these would ideally be stored and used by the calculator
    energy_label: Optional[str] = None
    woz_value: Optional[float] = None
    # ... other raw WWS input fields could be added here

class ListingCreate(ListingBase):
    # Fields required to create a new listing
    # WWS points and max legal rent might be calculated upon creation
    pass

class Listing(ListingBase):
    id: int
    wws_points: Optional[int] = Field(None, alias="wwsPoints")
    max_legal_rent: Optional[float] = Field(None, alias="maxLegalRent")
    amenities: List[Amenity] = []
    wws_breakdown: List[WWSBreakdownItem] = Field([], alias="wwsBreakdown")

    class Config:
        from_attributes = True # Enables ORM mode (Pydantic V2)
        populate_by_name = True # Allows using alias for field population

# Model for WWS Calculation input data, separate from Listing model if needed for calculator utility
class WWSInputData(BaseModel):
    size_m2: float
    rooms: int
    energy_label: Optional[str] = None # e.g., "A", "B", "C"
    woz_value: Optional[float] = None # WOZ value in EUR
    # Example of more detailed inputs for WWS calculation:
    # kitchen_luxury_level: Optional[int] = Field(1, ge=1, le=5) # 1-5 scale
    # bathroom_luxury_level: Optional[int] = Field(1, ge=1, le=5) # 1-5 scale
    # has_balcony: Optional[bool] = False
    # balcony_size_m2: Optional[float] = 0.0

class WWSDetails(BaseModel):
    points: int
    max_rent: float
    breakdown: List[WWSBreakdownItem]
