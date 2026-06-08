from sqlalchemy import Table, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from src.geo_map.database.schema.base import metadata

Route = Table(
    "routes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("route_name", String, nullable=False),
    Column("geometry", Geometry("LINESTRING", srid=4326), nullable=True),
    Column("schedule_template", JSONB, nullable=True),
    UniqueConstraint("route_name", name="uq_routes_route_name"),
)
