import mesa
import math
import random
import json
import os
from agents import CenterAgent # Simple Agent structure maintained

# File to store the data persistently
DATA_FILE = "centers.json"

BANGALORE_LOCATIONS = {
    "Majestic": (12.9767, 77.5713), "Indiranagar": (12.9784, 77.6408),
    "Koramangala": (12.9352, 77.6245), "Whitefield": (12.9698, 77.7500),
    "Jayanagar": (12.9308, 77.5838), "M G Road": (12.9766, 77.5993),
    "Hebbal": (13.0359, 77.5970), "Electronic City": (12.8452, 77.6602),
    "Malleshwaram": (13.0031, 77.5643), "Yeshwanthpur": (13.0238, 77.5529),
    "Domlur": (12.9609, 77.6387), "Basavanagudi": (12.9421, 77.5754),
    "HSR Layout": (12.9116, 77.6388)
}

BBOX = {"min_lat": 12.85, "max_lat": 13.12, "min_lon": 77.45, "max_lon": 77.75}


class SupportModel(mesa.Model):
    def __init__(self):
        super().__init__()
        self.space = mesa.space.ContinuousSpace(20, 20, False)
        self.schedule = mesa.time.RandomActivation(self)

        # LOAD DATA FROM FILE
        self.load_data()
        
    def _latlon_to_grid(self, lat, lon):
        """Converts real-world (lat, lon) to internal MESA grid (x, y)."""
        x = ((lon - BBOX["min_lon"]) / (BBOX["max_lon"] - BBOX["min_lon"])) * 20
        y = ((lat - BBOX["min_lat"]) / (BBOX["max_lat"] - BBOX["min_lat"])) * 20
        x = max(0, min(x, 20))
        y = max(0, min(y, 20))
        return x, y

    def load_data(self):
        """Load agents from JSON file or initialize defaults."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    if data:
                        # Check if loaded data adheres to the new distribution pattern for simplicity
                        # If not, it will be overwritten by defaults below, which is the safer path here.
                        # We only check if CenterAgents exist.
                        if not any(item['p_type'] in ["Police", "Hospital", "Cyber Crime", "Consultation", "Pharmacy", "Fire/Emergency"] for item in data):
                            print("Loaded data was incomplete. Re-initializing new structured defaults.")
                            self._initialize_default_centers()
                        else:
                            for item in data:
                                self._restore_agent(item)
                            print("Data loaded successfully.")

                    else:
                        print("JSON file was empty. Initializing new structured defaults.")
                        self._initialize_default_centers()
            except Exception as e:
                print(f"Error loading data: {e}. Re-initializing new structured defaults.")
                self._initialize_default_centers()
        else:
            print("Data file not found. Initializing new structured defaults.")
            self._initialize_default_centers()

    def save_data(self):
        """Save all current CenterAgents to JSON file."""
        data = []
        for agent in self.schedule.agents:
            if isinstance(agent, CenterAgent):
                data.append(agent.to_dict())

        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def _restore_agent(self, data):
        """Recreates an agent from the saved dictionary."""
        required_keys = ['unique_id', 'name', 'address', 'phone', 'p_type', 'lat', 'lon']
        if not all(key in data for key in required_keys):
            return

        x, y = self._latlon_to_grid(data['lat'], data['lon'])
        agent = CenterAgent(
            data['unique_id'], self,
            data['name'], data['address'],
            data['phone'], data['p_type'],
            data['lat'], data['lon']
        )
        self.space.place_agent(agent, (x, y))
        self.schedule.add(agent)

    def _initialize_default_centers(self):
        """Initializes 6 agents for 6 categories across 4 specified locations."""
        self.schedule.agents.clear()
        
        # 6 Primary Agent Categories
        categories = ["Police", "Hospital", "Cyber Crime", "Consultation", "Pharmacy", "Fire/Emergency"]
        # 4 Primary Distribution Locations
        locations = ["Majestic", "Indiranagar", "Koramangala", "Domlur"]

        # Counter for agent numbering
        agent_count = 1
        
        # Create 6 agents for EACH category
        for category in categories:
            for i in range(6):
                # Distribute agents evenly across 4 locations (6/4 = 1.5, so we cycle through 4 locations)
                location_name = locations[i % len(locations)]
                
                # Use a specific name for easy verification
                name = f"{category} Center {agent_count}"
                address = f"{location_name} Area"
                phone = "8121203705"
                
                # Add the agent
                self.add_agent(
                    category=category, 
                    name=name, 
                    address=address, 
                    phone=phone, 
                    location_name=location_name, 
                    save=False
                )
                agent_count += 1
                
        # Save all 36 (6 * 6) agents once created
        self.save_data()
        print(f"Initialized {len(self.schedule.agents)} agents across 6 types and 4 locations.")


    def add_agent(self, category, name, address, phone, location_name, save=True):
        """Adds a new agent and saves to file."""
        lat, lon = BANGALORE_LOCATIONS.get(location_name, BANGALORE_LOCATIONS["Majestic"])

        # Jitter added to prevent exact overlap in the MESA space
        lat += random.uniform(-0.002, 0.002)
        lon += random.uniform(-0.002, 0.002)

        x, y = self._latlon_to_grid(lat, lon)

        uid = f"{category}_{random.randint(10000, 99999)}"
        while any(a.unique_id == uid for a in self.schedule.agents):
            uid = f"{category}_{random.randint(10000, 99999)}"
            
        agent = CenterAgent(uid, self, name, address, phone, category, lat, lon)

        self.space.place_agent(agent, (x, y))
        self.schedule.add(agent)

        if save:
            self.save_data()


    def get_centers(self, category):
        """Returns all agents matching the specified category."""
        return [a for a in self.schedule.agents if isinstance(a, CenterAgent) and a.p_type == category]

    def calculate_metrics(self, user_lat, user_lon, category):
        """
        Calculates the grid distance to all centers in the category, scales it to 
        an arbitrary 'km' metric, and sorts the results. (Simple heuristic)
        """
        ux, uy = self._latlon_to_grid(user_lat, user_lon)
        centers = self.get_centers(category)
        results = []
        for c in centers:
            # Grid distance (Euclidean distance)
            dist_grid = self.space.get_distance((ux, uy), c.pos)
            # Scale factor 1.5 is arbitrary for a 20x20 grid 
            c.distance_to_user = round(dist_grid * 1.5, 2) 
            results.append(c)
        results.sort(key=lambda x: x.distance_to_user)
        return results

    def find_nearest_using_heuristic(self, user_lat, user_lon, category):
        """
        Finds the nearest center based on simple Euclidean distance in the MESA grid.
        (Simple greedy heuristic)
        """
        centers = self.get_centers(category)
        if not centers:
            return None
        ux, uy = self._latlon_to_grid(user_lat, user_lon)

        best_agent = None
        min_distance = float('inf')

        for agent in centers:
            # Distance is the Euclidean distance (the simple heuristic)
            distance = self.space.get_distance((ux, uy), agent.pos)
            
            if distance < min_distance:
                min_distance = distance
                best_agent = agent

        return best_agent

    def get_grid_coords(self, lat, lon):
        """Public getter for grid coordinates."""
        return self._latlon_to_grid(lat, lon)