from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geography
from geo_map.database.schema.base import metadata

GPSLocation = Table(
    "gps_locations",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=True),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=True),
    Column("timestamp", DateTime(timezone=True), nullable=False),
    Column("coordinates", Geography("POINT", srid=4326), nullable=False),
    Column("speed", Float, nullable=True),
    Column("heading", Float, nullable=True),
    Column("accuracy", Float, nullable=True),
    Column("metadata", JSONB, nullable=True),
)
