import random

class CommunityAgent:
    def __init__(self):
        self.agent_type = 'community'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        base_lat, base_lon = 12.9784, 77.6408 # Indiranagar
        for i in range(10):
            lat = base_lat + random.uniform(-0.04, 0.04)
            lon = base_lon + random.uniform(-0.04, 0.04)
            center = {
                "id": f"comm_{i}",
                "name": f"Community Center {i+1}",
                "address": f"{300 + i} 100ft Road, Bangalore",
                "phone": "8121203705",
                "email": f"help{i+1}@community.org",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "distance": 0.0,
                "status": random.choice(["Active", "Inactive", "Busy"])
            }
            centers.append(center)
        return centers