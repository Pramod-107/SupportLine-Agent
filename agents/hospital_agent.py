import random

class HospitalAgent:
    def __init__(self):
        self.agent_type = 'hospital'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        base_lat, base_lon = 12.9352, 77.6245 # Koramangala
        for i in range(10):
            lat = base_lat + random.uniform(-0.05, 0.05)
            lon = base_lon + random.uniform(-0.05, 0.05)
            center = {
                "id": f"hosp_{i}",
                "name": f"City Hospital {i+1}",
                "address": f"{200 + i} Hosur Rd, Bangalore",
                "phone": "8121203705",
                "email": f"info{i+1}@cityhospital.com",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "distance": 0.0,
                "status": random.choice(["Available", "Full", "On Call"])
            }
            centers.append(center)
        return centers