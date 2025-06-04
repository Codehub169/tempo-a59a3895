import pytest
from backend.wws_calculator import (
    calculate_wws_points,
    calculate_max_legal_rent,
    get_wws_details
)
from backend.models import WWSInputData, WWSDetails, WWSBreakdownItem

@pytest.fixture
def sample_input_data_dict() -> dict:
    return {
        "surface_area": 75,  # e.g., 75 m^2 * 1 point/m^2 = 75 points
        "energy_label": "B",  # e.g., B = 20 points
        "woz_value": 300000, # e.g., 300000 / 10000 = 30 points
        "room_count": 3      # e.g., 3 rooms * 5 points/room = 15 points
    }
    # Total expected based on simplified wws_calculator.py: 75+20+30+15 = 140 points

@pytest.fixture
def sample_input_data_model(sample_input_data_dict: dict) -> WWSInputData:
    return WWSInputData(**sample_input_data_dict)

def test_calculate_wws_points(sample_input_data_model: WWSInputData):
    total_points, breakdown = calculate_wws_points(sample_input_data_model)
    
    # Based on the simplified logic in wws_calculator.py
    # surface_area * POINTS_PER_SQ_METER (1) = 75 * 1 = 75
    # ENERGY_LABEL_POINTS['B'] (20)
    # woz_value / WOZ_DIVISOR (10000) = 300000 / 10000 = 30
    # room_count * POINTS_PER_ROOM (5) = 3 * 5 = 15
    # Expected: 75 + 20 + 30 + 15 = 140
    assert total_points == 140
    assert isinstance(breakdown, list)
    assert len(breakdown) == 4 # One item for each category
    for item in breakdown:
        assert isinstance(item, WWSBreakdownItem)
        assert isinstance(item.item, str)
        assert isinstance(item.points, (int, float))
    
    # Check if specific items are present
    assert any(b.item == "Surface Area" and b.points == 75 for b in breakdown)
    assert any(b.item == "Energy Label" and b.points == 20 for b in breakdown)
    assert any(b.item == "WOZ Value" and b.points == 30 for b in breakdown)
    assert any(b.item == "Room Count" and b.points == 15 for b in breakdown)

def test_calculate_max_legal_rent():
    # Max legal rent = points * RENT_FACTOR_PER_POINT (7.5) + BASE_RENT (50)
    points = 140
    expected_rent = (140 * 7.5) + 50 # 1050 + 50 = 1100
    max_rent = calculate_max_legal_rent(points)
    assert max_rent == expected_rent

    points_low = 100
    expected_rent_low = (100 * 7.5) + 50 # 750 + 50 = 800
    max_rent_low = calculate_max_legal_rent(points_low)
    assert max_rent_low == expected_rent_low

def test_get_wws_details(sample_input_data_dict: dict):
    wws_details_obj = get_wws_details(sample_input_data_dict)

    assert isinstance(wws_details_obj, WWSDetails)
    # Expected points: 140 (as calculated in test_calculate_wws_points)
    # Expected rent: 1100 (as calculated in test_calculate_max_legal_rent with 140 points)
    assert wws_details_obj.points == 140
    assert wws_details_obj.max_rent == 1100.0
    assert isinstance(wws_details_obj.breakdown, list)
    assert len(wws_details_obj.breakdown) == 4
    for item in wws_details_obj.breakdown:
        assert isinstance(item, WWSBreakdownItem)

def test_get_wws_details_different_label(sample_input_data_dict: dict):
    data = sample_input_data_dict.copy()
    data["energy_label"] = "A" # A = 30 points
    # Expected points: 75 (surface) + 30 (label A) + 30 (WOZ) + 15 (rooms) = 150
    # Expected rent: (150 * 7.5) + 50 = 1125 + 50 = 1175

    wws_details_obj = get_wws_details(data)
    assert wws_details_obj.points == 150
    assert wws_details_obj.max_rent == 1175.0

def test_get_wws_details_unknown_label(sample_input_data_dict: dict):
    data = sample_input_data_dict.copy()
    data["energy_label"] = "Z" # Unknown label, should default to 0 points in calculator
    # Expected points: 75 (surface) + 0 (label Z) + 30 (WOZ) + 15 (rooms) = 120
    # Expected rent: (120 * 7.5) + 50 = 900 + 50 = 950

    wws_details_obj = get_wws_details(data)
    assert wws_details_obj.points == 120
    assert wws_details_obj.max_rent == 950.0
