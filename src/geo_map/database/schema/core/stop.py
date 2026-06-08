from sqlalchemy import CheckConstraint, Column, Float, Integer, String, Table
from geoalchemy2 import Geometry
from geo_map.database.schema.base import metadata

Stop = Table(
    "stops",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("stop_name", String, nullable=False),
    Column("location", Geometry("POINT", srid=4326), nullable=False),
    Column("geofence_radius", Float, default=50.0, nullable=False),
    Column("campus_zone", String, nullable=True),
    CheckConstraint("geofence_radius > 0", name="ck_stops_geofence_radius_positive"),
)
