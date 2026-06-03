from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from src.geo_map.route import router, stops_services
from src.utils.config import GOOGLE_MAPS_API_KEY



@asynccontextmanager
async def lifespan(app: FastAPI):
    await stops_services.populate_stops() #new

    yield
 


# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(
    title="Bus Tracking System",
    description="FastAPI backend for buses, stops, and routes",
    version="1.0.0",
    lifespan=lifespan   # ✅ THIS IS THE MISSING PIECE
)

# -------------------------------
# Static & Templates
# -------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



app.include_router(router)

# -------------------------------
# Frontend route
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
        }
    )

