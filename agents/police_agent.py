import random

class PoliceAgent:
    def __init__(self):
        self.agent_type = 'police'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        for i in range(6):
            # Generating Grid Coordinates (0-20) instead of Lat/Lon
            center = {
                "id": f"pol_{i}",
                "name": f"Police Station {i+1}",
                "address": f"Sector {i+1}, Main Road",
                "phone": "8121203705", # Updated to your preferred number
                "type": "police",
                "pos": (random.randint(0, 19), random.randint(0, 19)), # (X, Y)
                "status": random.choice(["Open", "Busy"])
            }
            centers.append(center)
        return centers