import random

class MixedAgent:
    def __init__(self):
        self.agent_type = 'mixed'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        base_lat, base_lon = 12.9250, 77.5468 # Banashankari
        for i in range(10):
            lat = base_lat + random.uniform(-0.05, 0.05)
            lon = base_lon + random.uniform(-0.05, 0.05)
            center = {
                "id": f"mix_{i}",
                "name": f"General Aid {i+1}",
                "address": f"{600 + i} Outer Ring Rd, Bangalore",
                "phone": "8121203705",
                "email": f"help{i+1}@mixed.org",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "distance": 0.0,
                "status": random.choice(["Open", "Closed", "Busy"])
            }
            centers.append(center)
        return centers