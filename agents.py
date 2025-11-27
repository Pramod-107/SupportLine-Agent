import mesa


class CenterAgent(mesa.Agent):
    """
    An agent representing a Help Center.
    """

    def __init__(self, unique_id, model, name, address, phone, p_type, lat=None, lon=None):
        super().__init__(unique_id, model)
        self.name = name
        self.address = address
        self.phone = phone
        self.p_type = p_type
        self.distance_to_user = 0.0 # Standard Euclidean distance (h)

        # Store coordinates
        self.lat = lat if lat is not None else 0.0
        self.lon = lon if lon is not None else 0.0

    def to_dict(self):
        """Converts agent data to a dictionary for saving."""
        return {
            "unique_id": self.unique_id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "p_type": self.p_type,
            "lat": self.lat,
            "lon": self.lon
        }


class UserAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)