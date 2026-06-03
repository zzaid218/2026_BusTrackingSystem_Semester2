# Bug Resolution Report

This report summarizes the bugs resolved in the Bus Tracking System codebase. Snippets show a line-level comparison with $\pm 1$ line of context around the changes.

---

## 1. `/api/routes` response shape
* **Problem description**: `/api/routes` is declared as `List[Route]`, but returns one route object. Frontend treats response as an array and calls `forEach`, so browser can throw `TypeError: data.forEach is not a function`.
* **What it can cause**: Causes browser-side JavaScript execution failure (`TypeError: data.forEach is not a function`), preventing the routes from being drawn on the map interface.
* **Old code part** ([route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py)):
  ```python
      #old
      }
  
      return JSONResponse(status_code=status.HTTP_200_OK, content=dynamic_route)
  ```
* **New code part** ([route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py)):
  ```python
      #new
      }
  
      return JSONResponse(status_code=status.HTTP_200_OK, content=[dynamic_route]) #new
  ```

---

## 2. Distance Matrix endpoint shape
* **Problem description**: Frontend expects `data.results`. Backend builds a bus-grouped list with `bus_id` and `etas`. Same feature has two response contracts.
* **What it can cause**: It causes a frontend crash with `TypeError: Cannot read properties of undefined` when trying to access `data.results.length` and subsequent elements. Additionally, the backend was ignoring specific frontend query parameters `origins` and `destinations` sent by the client.
* **Old code part** ([distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) & [route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py)):
  * In [route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py):
    ```python
    #old
    @router.get("/distance/eta",  tags=["Distance Matrix"])
    async def get_eta():
        content = await distance_services.distance_metrix()
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Imports):
    ```python
    #old
    import httpx
    from src.geo_map.services.buses import PopulateBuses
    from src.geo_map.services.stops import PopulateStops
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Class Init & Signature):
    ```python
    #old
    class DistanceMatrix:
        def __init__(self):
            self.d = []
            self.buses_service = PopulateBuses()
            self.stops_services = PopulateStops()
        
        async def distance_metrix(self):
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Return Statement):
    ```python
    #old
            print(results)
            return results
    ```
* **New code part** ([distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) & [route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py)):
  * In [route.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/route.py):
    ```python
    #new
    @router.get("/distance/eta",  tags=["Distance Matrix"])
    async def get_eta(origins: str = Query(...), destinations: str = Query(...)): #new
        content = await distance_services.distance_metrix(origins, destinations) #new
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Imports):
    ```python
    #new
    import httpx
    from src.utils.config import GOOGLE_MAPS_API_KEY
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Class Init & Signature):
    ```python
    #new
    class DistanceMatrix:
        def __init__(self):
            self.d = []
        
        async def distance_metrix(self, origins: str, destinations: str): #new
    ```
  * In [distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py) (Return Statement):
    ```python
    #new
            return {"results": results} #new
    ```

---

## 3. `loadBuses` variable scope
* **Problem description**: `busObj` is created only when bus is new. Existing bus path updates marker, then later code still references `busObj`, which can cause `ReferenceError: busObj is not defined`.
* **What it can cause**: Causes frontend execution crash (`ReferenceError: busObj is not defined`) whenever a bus updates its position, preventing real-time markers from updating correctly.
* **Old code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  ```javascript
  //old
    data.forEach(async bus => {
      if (this.buses.has(bus.id)) {
        this.buses.get(bus.id).update(bus.location);
      } else {
        const busObj = new Bus(bus, this.map);
        this.buses.set(bus.id, busObj);
      }
  ```
* **New code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  ```javascript
  //new
    data.forEach(async bus => {
      let busObj; //new
      if (this.buses.has(bus.id)) {
        busObj = this.buses.get(bus.id); //new
        busObj.update(bus.location);
      } else {
        busObj = new Bus(bus, this.map); //new
        this.buses.set(bus.id, busObj);
      }
  ```

---

## 4. `fetchETA` null path
* **Problem description**: `fetchETA` can return `null`, but caller immediately reads `eta.etaSeconds`. If ETA call fails or response shape does not match, frontend can throw when building bus info window.
* **What it can cause**: Causes a frontend script crash with `TypeError: Cannot read properties of null (reading 'etaSeconds')` if the backend call fails or fails to return a valid route estimate.
* **Old code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  ```javascript
  //old
        const eta = await fetchETA(bus.location, this.stops[0].position);
        busObj.infoWindow.setContent(`<strong>Bus ${bus.id}</strong><br>ETA to ${this.stops[0].name}: ${Math.round(eta.etaSeconds/60)} min`);
      }
  ```
* **New code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  ```javascript
  //new
        const eta = await fetchETA(bus.location, this.stops[0].position);
        if (eta) { //new
          busObj.infoWindow.setContent(`<strong>Bus ${bus.id}</strong><br>ETA to ${this.stops[0].name}: ${Math.round(eta.etaSeconds/60)} min`);
        }
      }
  ```

---

## 5. Stop cache grows on repeated calls
* **Problem description**: `PopulateStops.populate_stops()` appends to `geocoding_stops` every call. `/api/stops` and `/api/routes` both call it, so repeated requests can duplicate stop records in memory.
* **What it can cause**: Causes unbounded memory growth (memory leak) on the backend and sends duplicated lists of stops to the client, leading to UI performance degradation and redundant markers on the Google Map.
* **Old code part** ([stops.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/stops.py)):
  ```python
  #old
      async def populate_stops(self):
          """
          Geocode all stops once and store in memory.
          """
  
          for stop in stops:
  ```
* **New code part** ([stops.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/stops.py)):
  ```python
  #new
      async def populate_stops(self):
          """
          Geocode all stops once and store in memory.
          """
          if self.geocoding_stops: #new
              return jsonable_encoder(self.geocoding_stops) #new
  
          for stop in stops:
  ```

---

## 6. Bus cache grows on repeated calls
* **Problem description**: `PopulateBuses.buses()` appends static bus data to `geocoding_buses` every call. Repeated `/api/buses` calls can duplicate bus records in memory.
* **What it can cause**: Same as stop cache growth, this leaks memory over time and sends duplicate bus markers to the map frontend.
* **Old code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #old
      async def buses(self):
          """
          Fetch static buses and store in memory.
          """
          for bus in buses:
  ```
* **New code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #new
      async def buses(self):
          """
          Fetch static buses and store in memory.
          """
          if self.geocoding_buses: #new
              return jsonable_encoder(self.geocoding_buses) #new
  
          for bus in buses:
  ```

---

## 7. `PopulateBuses` docstring mismatch
* **Problem description**: Docstring says it geocodes stops. Actual behavior copies static bus data from `back_fill.py`.
* **What it can cause**: Developer confusion and decreased code readability/maintainability.
* **Old code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #old
      async def buses(self):
          """
          Geocode all stops once and store in memory.
          """
  ```
* **New code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #new
      async def buses(self):
          """
          Fetch static buses and store in memory.
          """
  ```

---

## 8. `PopulateBuses` unused geocoding dependency
* **Problem description**: `PopulateBuses` creates a `GeocodingService`, but bus population does not use geocoding.
* **What it can cause**: Unnecessary allocation of `GeocodingService` objects, cluttering memory and imports.
* **Old code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #old
  from src.geo_map.services.geocoding import GeocodingService
  from src.helpers.back_fill import buses
  ```
  and:
  ```python
  #old
  class PopulateBuses:
      def __init__(self):
          self.geocoding = GeocodingService()
          self.geocoding_buses: List[Bus] = []
  ```
* **New code part** ([buses.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/buses.py)):
  ```python
  #new
  from src.helpers.back_fill import buses
  ```
  and:
  ```python
  #new
  class PopulateBuses:
      def __init__(self):
          self.geocoding_buses: List[Bus] = [] #new
  ```

---

## 9. Startup geocoding is separate from route service cache
* **Problem description**: `main.py` geocodes stops in lifespan using one `PopulateStops` instance. API routes use another global `PopulateStops` instance, so startup work is not reused by `/api/stops` or `/api/routes`.
* **What it can cause**: Slow initial API response times because the application performs expensive API-based geocoding calculations repeatedly during runtime requests instead of leveraging the boot-up cache.
* **Old code part** ([main.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/main.py)):
  ```python
  #old
  from src.geo_map.services.stops import PopulateStops
  from src.geo_map.route import router
  ```
  and:
  ```python
  #old
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # Populate geocoded stops once at startup
      service = PopulateStops()
      await service.populate_stops()
  
      yield
  ```
* **New code part** ([main.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/main.py)):
  ```python
  #new
  from src.geo_map.route import router, stops_services
  ```
  and:
  ```python
  #new
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      await stops_services.populate_stops() #new
  
      yield
  ```

---

## 10. Debug prints in service path
* **Problem description**: Distance Matrix service prints destinations and results during request handling. This mixes runtime API behavior with console debug output.
* **What it can cause**: Pollutes standard output and system log files during normal operation, making logs harder to parse.
* **Old code part** ([distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py)):
  ```python
  #old
          origins = "|".join(f"{bus['location']['lat']},{bus['location']['lng']}" for bus in buses)
          destinations ="|".join(f"{stop["location"]['lat']},{stop["location"]['lng']}" for stop in stops)
  
          print("\n ++++++++++++++++++++++++++++", destinations)
  
  
  
          if not destinations:
  ```
  and:
  ```python
  #old
                  results.append(bus_result)
                  print("--------"*20)
              print(results)
              return results
  ```
* **New code part** ([distance.py](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/src/geo_map/services/distance.py)):
  * #new: Debug prints have been completely deleted from the file body.

---

## 11. Map center mismatch
* **Problem description**: HTML map starts with New York coordinates. JavaScript later recenters to AAU coordinates. This creates duplicate center source and possible first-load mismatch.
* **What it can cause**: Visual glitch on page load where the map briefly renders New York before jumping to AAU coordinates in Jordan.
* **Old code part** ([index.html](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/templates/index.html)):
  ```html
  <!--old-->
            <gmp-map zoom="16" map-id="DEMO_MAP_ID"
                  center="40.749933,-73.98633">
  ```
* **New code part** ([index.html](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/templates/index.html)):
  ```html
  <!--new-->
    <!-- Google Map component -->
          <gmp-map zoom="16" map-id="DEMO_MAP_ID"
                center="31.9450,35.9287"> <!--new-->
  ```

---

## 12. Frontend has old commented implementation
* **Problem description**: `static/index.js` keeps an older commented `loadBuses` implementation. Active and inactive versions sit together, which makes current behavior harder to read.
* **What it can cause**: Harder to read and maintain the javascript codebase.
* **Old code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  ```javascript
  //old
  //   async loadBuses() {
  //     const response = await fetch("/api/buses");
  //     const data = await response.json();
  //     data.forEach(async bus => {
  //       if (this.buses.has(bus.id)) {
  //         this.buses.get(bus.id).update(bus.location);
  //      } else {
  //         const busObj = new Bus(bus, this.map);
  //        // Optional: get address from backend
  //         const addr = await fetch(`/api/geocode/reverse?lat=${bus.location.lat}&lng=${bus.location.lng}`).then(r => r.json());
  //         busObj.infoWindow.setContent(`<strong>Bus ${bus.id}</strong><br>${addr.formatted_address}`);
  //        this.buses.set(bus.id, busObj);
  //       }
  //    });
  //  }
  ```
* **New code part** ([index.js](file:///home/cybersecurity/Desktop/practical/2026_BusTrackingSystem_Semester2/static/index.js)):
  * #new: This commented code block has been completely removed.
