import httpx
from src.utils.config import GOOGLE_MAPS_API_KEY
from src.geo_map.services.buses import PopulateBuses
from src.geo_map.services.stops import PopulateStops

class DistanceMatrix:
    def __init__(self):
        self.d = []
        self.buses_service = PopulateBuses()
        self.stops_services = PopulateStops()
    
    async def distance_metrix(self):
        # """
        # Compute ETA from each bus to each stop using Google Distance Matrix API.
        # """
        buses = await self.buses_service.buses()
        stops = await self.stops_services.populate_stops()
        if not buses or not stops:
            return {"error": "No buses or stops defined"}


        # Prepare origins (buses) and destinations (stops)
        origins = "|".join(f"{bus['location']['lat']},{bus['location']['lng']}" for bus in buses)
        destinations ="|".join(f"{stop["location"]['lat']},{stop["location"]['lng']}" for stop in stops)

        print("\n ++++++++++++++++++++++++++++", destinations)



        if not destinations:
            return {"error": "Stops have no geocoded location yet"}

        # Build the Distance Matrix API URL
        url = (
            "https://maps.googleapis.com/maps/api/distancematrix/json"
            f"?origins={origins}"
            f"&destinations={destinations}"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

        # Map result back to buses → stops
        results = []
        for i, bus in enumerate(buses):
            bus_result = {"bus_id": bus["id"], "etas": []}
            for j, stop in enumerate(stops):
                element = data["rows"][i]["elements"][j]
                if element.get("status") == "OK":
                    bus_result["etas"].append({
                        "stop_id": stop["id"],
                        "distance_meters": element["distance"]["value"],
                        "duration_seconds": element["duration"]["value"],
                        "duration_text": element["duration"]["text"]
                    })
                else:
                    bus_result["etas"].append({
                        "stop_id": stop["id"],
                        "error": element.get("status")
                    })
            results.append(bus_result)
            print("--------"*20)
        print(results)
        return results