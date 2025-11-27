import solara
import model
import os

# --- GLOBAL APPLICATION STATE ---
model_instance = model.SupportModel()

# --- THEME CONFIGURATION ---
HOME_BG_URL = "home.jpeg" 
OTHER_BG_URL = "home.jpeg"

# Colors
TEXT_PRIMARY = "#1e3a8a"
TEXT_SECONDARY = "#475569"
ACCENT_COLOR = "#00b4d8"
GLASS_WHITE = "rgba(255, 255, 255, 0.9)"

# --- ICON MAPPING ---
# We now use direct filenames. Solara will serve these automatically.
ICON_MAPPING = {
    "Police": "police.jpg",
    "Hospital": "hospital.jpg",
    "Cyber Crime": "cybercrime.jpg",
    "Consultation": "consultation.jpg",
    "Pharmacy": "pharmacy.jpg",
    "Fire/Emergency": "fire.jpg",
}

# --- GLOBAL NAVIGATION STATE ---
current_page = solara.reactive("home")
show_emergency_menu = solara.reactive(False)

# --- USER FLOW STATE ---
user_view_step = solara.reactive(1)
selected_category = solara.reactive("Police")
user_location_input = solara.reactive("Indiranagar")
user_current_coords = solara.reactive(model.BANGALORE_LOCATIONS["Indiranagar"])
target_center = solara.reactive(None)
nearest_found = solara.reactive(False)
show_route = solara.reactive(False)

# --- MANAGER FLOW STATE ---
mgr_name = solara.reactive("New Center")
mgr_type = solara.reactive("Police")
mgr_phone = solara.reactive("8121203705")
mgr_area = solara.reactive("Indiranagar")
show_registration_success = solara.reactive(False)

# --- CONSTANTS FROM MODEL ---
BANGALORE_LOCATIONS = model.BANGALORE_LOCATIONS
BBOX = model.BBOX

# --- UTILITY FUNCTIONS ---
def get_coordinates(location_name: str) -> tuple[float, float]:
    coords = BANGALORE_LOCATIONS.get(location_name)
    if coords is not None:
        return coords
    return BANGALORE_LOCATIONS["Majestic"]

user_current_coords.set(get_coordinates(user_location_input.value))