import httpx
from src.utils.config import GOOGLE_MAPS_API_KEY

class DistanceMatrix:
    def __init__(self):
        self.d = []
    
    async def distance_metrix(self, origins: str, destinations: str): #new
        """
        Compute ETA between specified origins and destinations using Google Distance Matrix API.
        """
        url = (
            "https://maps.googleapis.com/maps/api/distancematrix/json"
            f"?origins={origins}"
            f"&destinations={destinations}"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

        results = []
        if "rows" in data and len(data["rows"]) > 0:
            for row in data["rows"]:
                for element in row.get("elements", []):
                    if element.get("status") == "OK":
                        results.append({
                            "distance_meters": element["distance"]["value"],
                            "duration_seconds": element["duration"]["value"]
                        })
        return {"results": results} #new