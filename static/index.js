class Bus {
  constructor(bus, map) {
    this.id = bus.id;
    this.position = bus.location;
    this.map = map;

    this.marker = new google.maps.Marker({
      position: this.position,
      map: this.map,
      icon: {
        url: "https://maps.google.com/mapfiles/ms/icons/bus.png",
        scaledSize: new google.maps.Size(40, 40)
      }
    });

    this.infoWindow = new google.maps.InfoWindow({
      content: `<strong>Bus ${this.id}</strong>`
    });

    this.marker.addListener("click", () => {
      this.infoWindow.open(this.map, this.marker);
    });
  }

  update(location) {
    this.position = location;
    this.marker.setPosition(location);
  }
}





class Stop {
  constructor(stop, map) {
    this.name = stop.name;
    this.position = stop.location;
    this.map = map;

    this.marker = new google.maps.Marker({
      position: this.position,
      map: this.map,
      icon: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
    });

    this.infoWindow = new google.maps.InfoWindow({
      content: `<strong>${this.name}</strong>`
    });

    this.marker.addListener("click", () => {
      this.infoWindow.open(this.map, this.marker);
    });
  }
}
 



class Route {
  constructor(route, map) {
    this.polyline = new google.maps.Polyline({
      path: route.path,
      map: map,
      geodesic: true,
    strokeOpacity: 0.8,
      strokeWeight: 4
    });

    this.polyline.addListener("click", () => {
  new google.maps.InfoWindow({
    content: `<strong>${route.name}</strong>`,
    position: route.path[0]
  }).open(map);
});



  }
}


/* ========= Main Map App ========= */
class MapApp {
  constructor() {
    this.defaultLocation = { lat: 31.9450, lng: 35.9287 }; // AAU
    this.map = null;
    this.buses = new Map();   // id → Bus
    this.stops = [];
    this.routes = [];
    this.routePath = [];
    this.directionsPolyline = null;

  }

  async init() {
    await customElements.whenDefined("gmp-map");

    const gmpMap = document.querySelector("gmp-map");
    this.map = gmpMap.innerMap;

    this.map.setCenter(this.defaultLocation);
    this.map.setZoom(15);


    await this.loadStops();
    await this.loadRoutes();
  
    await this.loadBuses();

  await this.showDirections("Amman", "Zarqa");
   }

  /* ===== API CALLS ===== */
 
 

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
 

 async loadBuses() {
  const response = await fetch("/api/buses");
  const data = await response.json();

  data.forEach(async bus => {
    if (this.buses.has(bus.id)) {
      this.buses.get(bus.id).update(bus.location);
    } else {
      const busObj = new Bus(bus, this.map);
      this.buses.set(bus.id, busObj);
    }

    // Example: show ETA to first stop
    if (this.stops.length > 0) {
      const eta = await fetchETA(bus.location, this.stops[0].position);
      busObj.infoWindow.setContent(`<strong>Bus ${bus.id}</strong><br>ETA to ${this.stops[0].name}: ${Math.round(eta.etaSeconds/60)} min`);
    }
  });
}

 

async loadStops() {
  const response = await fetch("/api/stops");
  const data = await response.json();

  this.stops = []; // clear old stops if refreshing
  data.forEach(stop => {
    if (stop.location) {
      this.stops.push(new Stop(stop, this.map));
    } else {
      console.warn(`Stop ${stop.name} has no location!`);
    }
  });
}



  async loadRoutes() {
    // Fetch routes from backend
    const response = await fetch("/api/routes");
    const data = await response.json();

    this.routes = []; // clear old routes
    data.forEach(route => {
      // If route.path is empty, try building it from stops
      if (!route.path || route.path.length === 0) {
        route.path = this.stops.map(stop => stop.position);
      }
      this.routePath = route.path; // ✅ store for buses
      this.routes.push(new Route(route, this.map));
    });
  } 

  async showDirections(origin, destination) {
    if (!this.map) {
      console.warn("Map is not ready for directions rendering.");
      return;
    }

    const data = await getDirections(origin, destination);

    if (!data.routes || data.routes.length === 0) {
      console.warn("No directions route returned from API.");
      return;
    }

    const route = data.routes[0];

    if (!route.overview_polyline || !route.overview_polyline.points) {
      console.warn("Directions route did not include an overview polyline.");
      return;
    }

    const { encoding } = google.maps.geometry ?? await google.maps.importLibrary("geometry");
    const path = encoding.decodePath(route.overview_polyline.points);

    if (this.directionsPolyline) {
      this.directionsPolyline.setMap(null);
    }

    this.directionsPolyline = new google.maps.Polyline({
      path,
      map: this.map,
      geodesic: true,
      strokeColor: "#1a73e8",
      strokeOpacity: 0.9,
      strokeWeight: 5
    });

    console.log(`Distance: ${route.legs?.[0]?.distance?.text ?? "N/A"}`);
    console.log(`Duration: ${route.legs?.[0]?.duration?.text ?? "N/A"}`);
  }
  
}
 



async function fetchETA(busLocation, stopLocation) {
  const origins = `${busLocation.lat},${busLocation.lng}`;
  const destinations = `${stopLocation.lat},${stopLocation.lng}`;
  
  const res = await fetch(`/api/distance/eta?origins=${origins}&destinations=${destinations}`);
  const data = await res.json();
  
  if (data.results.length > 0) {
    const etaSeconds = data.results[0].duration_seconds;
    const distanceMeters = data.results[0].distance_meters;
    console.log(`Distance: ${distanceMeters}m, ETA: ${etaSeconds/60} min`);
    return { distanceMeters, etaSeconds };
  }
  return null;
}


/* ========= Run App ========= */

document.addEventListener("DOMContentLoaded", () => {
  const app = new MapApp();
  app.init();
});

async function getDirections(origin, destination) {
    const response = await fetch(
        `/api/directions?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`
    );

    return await response.json();
}