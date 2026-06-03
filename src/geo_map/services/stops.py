# app/services/cache.py
from typing import List
from src.geo_map.services.geocoding import GeocodingService
from src.helpers.back_fill import stops
from src.geo_map.model import Stop, Location
from fastapi.encoders import jsonable_encoder

# Cached geocoded stops

class PopulateStops:
    def __init__(self):
        self.geocoding = GeocodingService()
        self.geocoding_stops: List[Stop] = []

    async def populate_stops(self):
        """
        Geocode all stops once and store in memory.
        """
        if self.geocoding_stops: #new
            return jsonable_encoder(self.geocoding_stops) #new

        for stop in stops:
            geo = await self.geocoding.geocode_address(stop["name"])
            if geo:
                location = Location(
                    lat=geo["lat"],
                    lng= geo["lng"]
                )
                stop_obj = Stop(
                    id= stop["id"],
                    name= stop["name"],
                    location=location

                )
                self.geocoding_stops.append(stop_obj)
        return jsonable_encoder(self.geocoding_stops)
 
