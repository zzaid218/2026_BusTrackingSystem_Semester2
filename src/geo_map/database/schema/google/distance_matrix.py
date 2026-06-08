from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Table, Uuid, text
from src.geo_map.database.schema.base import metadata

DistanceMatrixLog = Table(
    "distance_matrix_logs",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=True),
    Column("origin_lat", Float, nullable=False),
    Column("origin_lng", Float, nullable=False),
    Column("destination_stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("destination_lat", Float, nullable=False),
    Column("destination_lng", Float, nullable=False),
    Column("google_requested_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("google_duration_seconds", Integer, nullable=True),
    Column("google_distance_m", Float, nullable=True),
    Column("google_status", String, default="OK", nullable=False),
    Column("google_raw_response", JSON, nullable=True),
    Column("actual_arrival", DateTime(timezone=True), nullable=True),
    Column("google_error_seconds", Integer, nullable=True),
    CheckConstraint(
        "google_duration_seconds IS NULL OR google_duration_seconds >= 0",
        name="ck_distance_matrix_logs_duration_non_negative",
    ),
    CheckConstraint(
        "google_distance_m IS NULL OR google_distance_m >= 0",
        name="ck_distance_matrix_logs_distance_non_negative",
    ),
)
