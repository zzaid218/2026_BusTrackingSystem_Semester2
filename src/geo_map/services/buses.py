# app/services/cache.py
from typing import List
from fastapi.encoders import jsonable_encoder
from src.helpers.back_fill import buses
from src.geo_map.model import Bus

# Cached geocoded stops

class PopulateBuses:
    def __init__(self):
        self.geocoding_buses: List[Bus] = []

    async def buses(self):
        """
        Fetch static buses and store in memory.
        """
        if self.geocoding_buses: #new
            return jsonable_encoder(self.geocoding_buses) #new

        for bus in buses:
            b = dict(bus)
            self.geocoding_buses.append(b)

        return jsonable_encoder(self.geocoding_buses)
 
