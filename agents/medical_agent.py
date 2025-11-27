import random

class MedicalAgent:
    def __init__(self):
        self.agent_type = 'medical'
        self.centers = self.generate_mock_centers()

    def generate_mock_centers(self):
        centers = []
        base_lat, base_lon = 13.0031, 77.5643 # Malleshwaram
        for i in range(10):
            lat = base_lat + random.uniform(-0.04, 0.04)
            lon = base_lon + random.uniform(-0.04, 0.04)
            center = {
                "id": f"med_{i}",
                "name": f"Medical Clinic {i+1}",
                "address": f"{400 + i} Margosa Rd, Bangalore",
                "phone": "8121203705",
                "email": f"clinic{i+1}@medical.com",
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "distance": 0.0,
                "status": random.choice(["Open", "Closed", "On Call"])
            }
            centers.append(center)
        return centers