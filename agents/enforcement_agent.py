import random

class EnforcementAgent:
    def __init__(self):
        self.agent_type = 'enforcement'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        base_lat, base_lon = 12.9698, 77.7500 # Whitefield
        for i in range(10):
            lat = base_lat + random.uniform(-0.06, 0.06)
            lon = base_lon + random.uniform(-0.06, 0.06)
            center = {
                "id": f"enf_{i}",
                "name": f"Enforcement Squad {i+1}",
                "address": f"{500 + i} ITPL Main Rd, Bangalore",
                "phone": "8121203705",
                "email": f"squad{i+1}@force.gov",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "distance": 0.0,
                "status": random.choice(["Patrolling", "Stationed", "Off Duty"])
            }
            centers.append(center)
        return centers