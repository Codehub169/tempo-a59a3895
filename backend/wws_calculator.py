from typing import List, Tuple, Dict, Any, Optional
from pydantic import ValidationError # For specific Pydantic error handling
from .models import WWSBreakdownItem, WWSInputData, WWSDetails # Added WWSDetails

# This is a simplified placeholder for the Woningwaarderingsstelsel (WWS) calculation.
# A real implementation would require detailed rules and point tables from the Dutch government.

# Example point assignments (highly simplified)
POINTS_PER_SQ_METER = 1
ENERGY_LABEL_POINTS = {
    "A++": 40,
    "A+": 35,
    "A": 30,
    "B": 20,
    "C": 10,
    "D": 5,
}
WOZ_VALUE_FACTOR = 0.0003 # Example: 1 point per ~3333 EUR of WOZ value. For 300k, this is 90 points.
BASE_POINTS_ROOMS = 5 # Base points for having rooms, not per room.

# Example mapping of points to max legal rent (highly simplified)
# In reality, this is a table updated annually by the government.
# Rent = Points * Factor + Base (example linear model)
RENT_FACTOR_PER_POINT = 7.50
RENT_BASE = 50.00

def calculate_wws_points(data: WWSInputData) -> Tuple[int, List[WWSBreakdownItem]]:
    """
    Calculates WWS points based on input data.
    Returns total points and a breakdown of points per category.
    """
    total_points = 0
    breakdown: List[WWSBreakdownItem] = []

    # 1. Surface Area
    surface_points = int(data.size_m2 * POINTS_PER_SQ_METER)
    total_points += surface_points
    breakdown.append(WWSBreakdownItem(item=f"Surface Area ({data.size_m2} m\texttwosuperior)", points=surface_points))

    # 2. Energy Label
    if data.energy_label and data.energy_label.upper() in ENERGY_LABEL_POINTS:
        label_points = ENERGY_LABEL_POINTS[data.energy_label.upper()]
        total_points += label_points
        breakdown.append(WWSBreakdownItem(item=f"Energy Label ({data.energy_label.upper()})", points=label_points))
    else:
        breakdown.append(WWSBreakdownItem(item="Energy Label (Not specified or invalid)", points=0))

    # 3. WOZ Value
    if data.woz_value and data.woz_value > 0:
        woz_points = int(data.woz_value * WOZ_VALUE_FACTOR)
        total_points += woz_points
        breakdown.append(WWSBreakdownItem(item=f"WOZ Value (\texteuro{data.woz_value:,.0f})", points=woz_points))
    else:
        breakdown.append(WWSBreakdownItem(item="WOZ Value (Not specified)", points=0))
    
    # 4. Rooms (very basic)
    # A real calculation would consider heating, size of rooms etc.
    room_points = BASE_POINTS_ROOMS if data.rooms > 0 else 0
    total_points += room_points
    breakdown.append(WWSBreakdownItem(item=f"Number of Rooms ({data.rooms})", points=room_points))

    # Add other categories here: kitchen, bathroom, outdoor space, etc.
    # For example:
    # kitchen_points = ...
    # total_points += kitchen_points
    # breakdown.append(WWSBreakdownItem(item="Kitchen Quality", points=kitchen_points))

    return total_points, breakdown

def calculate_max_legal_rent(points: int) -> float:
    """
    Calculates the maximum legal rent based on WWS points.
    """
    if points <= 0:
        return 0.0
    max_rent = (points * RENT_FACTOR_PER_POINT) + RENT_BASE
    return round(max_rent, 2)

def get_wws_details(input_data_dict: Dict[str, Any]) -> WWSDetails:
    """
    Provides a full WWS assessment: total points, max legal rent, and breakdown.
    Takes a dictionary that can be parsed by WWSInputData.
    Returns a WWSDetails Pydantic model instance.
    """
    # Validate and parse input data
    try:
        wws_input_data = WWSInputData(**input_data_dict)
    except ValidationError as ve: # Specific Pydantic validation error
        print(f"Error parsing WWS input data (Validation Error): {ve}")
        # Return a WWSDetails object with error indication
        return WWSDetails(points=0, max_rent=0.0, breakdown=[WWSBreakdownItem(item=f"Error in input data: {ve.errors()}", points=0)])
    except Exception as e: # Other unexpected errors
        print(f"Error parsing WWS input data (General Error): {e}")
        return WWSDetails(points=0, max_rent=0.0, breakdown=[WWSBreakdownItem(item="General error in input data processing", points=0)])

    points, breakdown_list = calculate_wws_points(wws_input_data)
    max_rent_val = calculate_max_legal_rent(points)
    return WWSDetails(points=points, max_rent=max_rent_val, breakdown=breakdown_list)

# Example Usage (for testing)
if __name__ == '__main__':
    sample_data = {
        "size_m2": 75.0,
        "rooms": 3,
        "energy_label": "A",
        "woz_value": 300000.0
    }
    wws_details_obj = get_wws_details(sample_data)
    print(f"Total WWS Points: {wws_details_obj.points}")
    print(f"Maximum Legal Rent: \texteuro{wws_details_obj.max_rent:.2f}")
    print("Breakdown:")
    for item in wws_details_obj.breakdown:
        print(f"- {item.item}: {item.points} pts")

    error_sample_data = {
        "size_m2": "not_a_float", # Invalid data type
        "rooms": 3
    }
    wws_details_error_obj = get_wws_details(error_sample_data)
    print("\n--- Error Case ---")
    print(f"Total WWS Points: {wws_details_error_obj.points}")
    print(f"Maximum Legal Rent: \texteuro{wws_details_error_obj.max_rent:.2f}")
    print("Breakdown:")
    for item in wws_details_error_obj.breakdown:
        print(f"- {item.item}: {item.points} pts")
