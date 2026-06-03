"""
Database schemas for AAU Bus Tracking System.
Current state: buses, stops, routes, GPS history, trips, stop arrivals.
Google Maps bootstrap: geocoding cache, distance matrix log, prediction comparisons.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TripStatus(str, Enum):
    scheduled = "scheduled"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


# ---------------------------------------------------------------------------
# Core map entities
# ---------------------------------------------------------------------------


class Route(BaseModel):
    id: int
    name: str


class Stop(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    geofence_radius_m: float = Field(default=50.0)
    campus_zone: Optional[str] = None
    route_id: int
    stop_order: int


class Bus(BaseModel):
    id: int
    route_id: Optional[int] = None
    label: Optional[str] = None


# ---------------------------------------------------------------------------
# GPS location history
# ---------------------------------------------------------------------------


class GPSLocation(BaseModel):
    id: UUID
    bus_id: int
    route_id: Optional[int] = None
    trip_id: Optional[UUID] = None
    recorded_at: datetime
    lat: float
    lng: float
    speed_kmh: Optional[float] = None
    heading_deg: Optional[float] = None
    accuracy_m: Optional[float] = None


# ---------------------------------------------------------------------------
# Trips
# ---------------------------------------------------------------------------


class Trip(BaseModel):
    id: UUID
    bus_id: int
    route_id: int
    driver_id: Optional[UUID] = None
    status: TripStatus
    planned_departure: datetime
    actual_departure: Optional[datetime] = None
    planned_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Stop arrivals
# ---------------------------------------------------------------------------


class StopArrival(BaseModel):
    id: UUID
    trip_id: UUID
    stop_id: int
    scheduled_time: Optional[datetime] = None
    actual_time: Optional[datetime] = None
    dwell_time_seconds: Optional[int] = None


# ---------------------------------------------------------------------------
# Google Maps bootstrap — geocoding cache
# Avoids repeat geocoding API calls for the same address or stop name.
# ---------------------------------------------------------------------------


class GeocodingCache(BaseModel):
    id: UUID
    query: str                                # raw address or stop name sent to Google
    google_formatted_address: str             # Google's canonical address string
    google_lat: float
    google_lng: float
    google_geocoded_at: datetime
    google_place_id: Optional[str] = None     # Google place_id for forward lookups


# ---------------------------------------------------------------------------
# Google Maps bootstrap — distance matrix log
# One row per Distance Matrix API call. Stores request context and raw
# Google response so the same data can later become ETA training labels.
# ---------------------------------------------------------------------------


class DistanceMatrixLog(BaseModel):
    id: UUID
    bus_id: int
    route_id: int
    trip_id: Optional[UUID] = None
    origin_lat: float
    origin_lng: float
    destination_stop_id: int
    destination_lat: float
    destination_lng: float
    google_requested_at: datetime

    # Raw Google response fields
    google_duration_seconds: Optional[int] = None    # "duration.value"
    google_distance_m: Optional[float] = None        # "distance.value"
    google_status: str = "OK"                        # element-level status from Google
    google_raw_response: Optional[dict] = None       # full JSON element for debugging

    # Filled after the bus actually reaches the stop
    actual_arrival: Optional[datetime] = None
    google_error_seconds: Optional[int] = None       # actual - google_duration at request time


# ---------------------------------------------------------------------------
# Google Maps bootstrap — prediction comparisons
# Joins DistanceMatrixLog entries with actual arrivals once a trip completes.
# This table becomes the training dataset for the future ETA model.
# ---------------------------------------------------------------------------


class PredictionComparison(BaseModel):
    id: UUID
    distance_matrix_log_id: UUID      # FK to DistanceMatrixLog
    trip_id: UUID
    stop_id: int
    bus_id: int
    route_id: int
    predicted_at: datetime

    # Bus state at prediction time
    bus_lat: float
    bus_lng: float
    bus_speed_kmh: Optional[float] = None
    stops_remaining: Optional[int] = None

    # Google values (copied from DistanceMatrixLog for query convenience)
    google_eta_seconds: Optional[int] = None
    google_distance_m: Optional[float] = None

    # Ground truth — filled after trip completion
    actual_arrival: Optional[datetime] = None
    google_error_seconds: Optional[int] = None       # signed: positive = Google was optimistic