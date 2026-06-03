from sqlalchemy import Table, Column, String, Float, DateTime, Uuid
from geo_map.database.schema.base import metadata

GeocodingCache = Table(
    "geocoding_caches",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("query", String, nullable=False),
    Column("google_formatted_address", String, nullable=False),
    Column("google_lat", Float, nullable=False),
    Column("google_lng", Float, nullable=False),
    Column("google_geocoded_at", DateTime, nullable=False),
    Column("google_place_id", String, nullable=True),
)
