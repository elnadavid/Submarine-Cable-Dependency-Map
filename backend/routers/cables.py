import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Load mock data once when the server starts
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mock_cables.json")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


# ─────────────────────────────────────────────
#  ENDPOINT 1: GET /api/cables
#  Returns the full list of all submarine cables
# ─────────────────────────────────────────────
@router.get("/cables")
def get_all_cables():
    """
    Returns every cable with its path coordinates, owners, and landing points.
    The frontend uses this to draw lines on the map.
    """
    data = load_data()
    return {"cables": data["cables"]}


# ─────────────────────────────────────────────
#  ENDPOINT 2: GET /api/cables/{cable_id}
#  Returns details for one specific cable
# ─────────────────────────────────────────────
@router.get("/cables/{cable_id}")
def get_cable_by_id(cable_id: str):
    """
    Returns details for a single cable.
    Example: GET /api/cables/dunant
    """
    data = load_data()
    for cable in data["cables"]:
        if cable["id"] == cable_id:
            return cable
    raise HTTPException(status_code=404, detail=f"Cable '{cable_id}' not found")


# ─────────────────────────────────────────────
#  ENDPOINT 3: GET /api/landing-stations
#  Returns all coastal landing point locations
# ─────────────────────────────────────────────
@router.get("/landing-stations")
def get_landing_stations():
    """
    Returns all landing stations with their lat/lng coordinates.
    The frontend uses this to place markers on the map.
    """
    data = load_data()
    return {"landing_stations": data["landing_stations"]}


# ─────────────────────────────────────────────
#  ENDPOINT 4: GET /api/country/{country_name}
#  Returns the dependency profile for one country
# ─────────────────────────────────────────────
@router.get("/country/{country_name}")
def get_country_dependency(country_name: str):
    """
    Returns which cables serve a country and its redundancy score.
    Redundancy score = number of independent cables. 
    A score of 1 means the country goes offline if that cable is cut.
    """
    data = load_data()

    # Find matching landing station
    station = None
    for s in data["landing_stations"]:
        if s["country"].lower() == country_name.lower():
            station = s
            break

    if not station:
        raise HTTPException(status_code=404, detail=f"Country '{country_name}' not found")

    # Get full details for each cable serving this country
    cable_ids = station["cables"]
    serving_cables = []
    for cable in data["cables"]:
        if cable["id"] in cable_ids:
            serving_cables.append({
                "id": cable["id"],
                "name": cable["name"],
                "owners": cable["owners"],
                "length_km": cable["length_km"],
                "ready_for_service": cable["ready_for_service"]
            })

    redundancy_score = len(serving_cables)
    risk_level = "HIGH" if redundancy_score == 1 else "MEDIUM" if redundancy_score == 2 else "LOW"

    return {
        "country": station["country"],
        "lat": station["lat"],
        "lng": station["lng"],
        "redundancy_score": redundancy_score,
        "risk_level": risk_level,
        "serving_cables": serving_cables
    }
