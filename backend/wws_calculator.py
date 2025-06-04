from typing import List, Tuple, Dict, Any, Optional
from .models import WWSBreakdownItem, WWSInputData

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
WOZ_VALUE_FACTOR = 0.0003 # Example: 1 point per ~3333 EUR of WOZ value
BASE_POINTS_ROOMS = 5 # Base points for having rooms

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
    breakdown.append(WWSBreakdownItem(item=f"Surface Area ({data.size_m2} m²)", points=surface_points))

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
        breakdown.append(WWSBreakdownItem(item=f"WOZ Value (€{data.woz_value:,.0f})", points=woz_points))
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

def get_wws_details(input_data_dict: Dict[str, Any]) -> Tuple[int, float, List[WWSBreakdownItem]]:
    """
    Provides a full WWS assessment: total points, max legal rent, and breakdown.
    Takes a dictionary that can be parsed by WWSInputData.
    """
    # Validate and parse input data
    try:
        wws_input_data = WWSInputData(**input_data_dict)
    except Exception as e: # Broad exception for Pydantic validation errors
        # In a real app, handle this more gracefully or raise specific errors
        print(f"Error parsing WWS input data: {e}")
        return 0, 0.0, [WWSBreakdownItem(item="Error in input data", points=0)]

    points, breakdown = calculate_wws_points(wws_input_data)
    max_rent = calculate_max_legal_rent(points)
    return points, max_rent, breakdown

# Example Usage (for testing)
if __name__ == '__main__':
    sample_data = {
        "size_m2": 75.0,
        "rooms": 3,
        "energy_label": "A",
        "woz_value": 300000.0
    }
    points, max_rent, breakdown = get_wws_details(sample_data)
    print(f"Total WWS Points: {points}")
    print(f"Maximum Legal Rent: €{max_rent:.2f}")
    print("Breakdown:")
    for item in breakdown:
        print(f"- {item.item}: {item.points} pts")
