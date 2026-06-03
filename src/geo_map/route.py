from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from typing import List
from src.geo_map.model import Bus, Stop, Route
from src.geo_map.services.buses import PopulateBuses
from src.geo_map.services.stops import PopulateStops
from src.geo_map.services.distance import DistanceMatrix
from src.geo_map.services.geocoding import GeocodingService

router = APIRouter(prefix="/api")
buses_service = PopulateBuses()
stops_services = PopulateStops()
distance_services = DistanceMatrix()
geo_coding_service = GeocodingService()

@router.get("/buses", tags=["Buses"], response_model=List[Bus], response_class=JSONResponse)
async def get_buses():
    content = await buses_service.buses()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/stops",  tags=["Stops"], response_model=List[Stop])
async def get_stops():
    content =  await stops_services.populate_stops()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)



@router.get("/distance/eta",  tags=["Distance Matrix"])
async def get_eta(origins: str = Query(...), destinations: str = Query(...)): #new
    content = await distance_services.distance_metrix(origins, destinations) #new
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/geocode/address",  tags=["Geocoding"])
async def geocode_address(address: str = Query(...)):
    geo = await geo_coding_service.geocode_address(address)
    if not geo:
        return {"error": "Address not found"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=geo)


@router.get("/geocode/reverse", tags=["Geocoding"])
async def reverse_geocode(lat: float = Query(...), lng: float = Query(...)):
    geo = await geo_coding_service.reverse_geocode(lat, lng)
    if not geo:
        return {"error": "Location not found"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=geo)


@router.get("/routes",  tags=["Routes"], response_model=List[Route])
async def get_routes():
    content =  await stops_services.populate_stops()
 
    dynamic_route = {
        "id": 1,
        "name": "Dynamic Route - All Stops",
        "path": [stop["location"] for stop in content]
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=[dynamic_route]) #new
