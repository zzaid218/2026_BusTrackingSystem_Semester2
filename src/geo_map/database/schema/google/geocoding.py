from sqlalchemy import CheckConstraint, Column, DateTime, Float, String, Table, Uuid, text
from geo_map.database.schema.base import metadata

GeocodingCache = Table(
    "geocoding_caches",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("query", String, nullable=False, unique=True),
    Column("google_formatted_address", String, nullable=False),
    Column("google_lat", Float, nullable=False),
    Column("google_lng", Float, nullable=False),
    Column("google_geocoded_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("google_place_id", String, nullable=True),
    CheckConstraint("google_lat >= -90 AND google_lat <= 90", name="ck_geocoding_caches_lat_range"),
    CheckConstraint("google_lng >= -180 AND google_lng <= 180", name="ck_geocoding_caches_lng_range"),
)
