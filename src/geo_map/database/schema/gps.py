from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Index, Integer, Table, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geography
from geo_map.database.schema.base import metadata

GPSLocation = Table(
    "gps_locations",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=False),
    Column("timestamp", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("coordinates", Geography("POINT", srid=4326), nullable=False),
    Column("speed", Float, nullable=True),
    Column("heading", Float, nullable=True),
    Column("accuracy", Float, nullable=True),
    Column("metadata", JSONB, nullable=True),
    CheckConstraint("speed IS NULL OR speed >= 0", name="ck_gps_locations_speed_non_negative"),
    CheckConstraint(
        "heading IS NULL OR (heading >= 0 AND heading <= 360)",
        name="ck_gps_locations_heading_range",
    ),
    CheckConstraint("accuracy IS NULL OR accuracy >= 0", name="ck_gps_locations_accuracy_non_negative"),
    Index("ix_gps_locations_bus_timestamp", "bus_id", "timestamp"),
    Index("ix_gps_locations_trip_timestamp", "trip_id", "timestamp"),
)
