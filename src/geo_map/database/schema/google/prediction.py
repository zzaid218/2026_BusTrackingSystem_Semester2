from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, Table, Uuid, text
from src.geo_map.database.schema.base import metadata

PredictionComparison = Table(
    "prediction_comparisons",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("distance_matrix_log_id", Uuid, ForeignKey("distance_matrix_logs.id"), nullable=False),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=False),
    Column("stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("timestamp", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("bus_lat", Float, nullable=False),
    Column("bus_lng", Float, nullable=False),
    Column("bus_speed_kmh", Float, nullable=True),
    Column("stops_remaining", Integer, nullable=True),
    Column("google_eta_seconds", Integer, nullable=True),
    Column("google_distance_m", Float, nullable=True),
    Column("actual_arrival", DateTime(timezone=True), nullable=True),
    Column("google_error_seconds", Integer, nullable=True),
    CheckConstraint("bus_lat >= -90 AND bus_lat <= 90", name="ck_prediction_comparisons_bus_lat_range"),
    CheckConstraint("bus_lng >= -180 AND bus_lng <= 180", name="ck_prediction_comparisons_bus_lng_range"),
    CheckConstraint(
        "bus_speed_kmh IS NULL OR bus_speed_kmh >= 0",
        name="ck_prediction_comparisons_speed_non_negative",
    ),
    CheckConstraint(
        "stops_remaining IS NULL OR stops_remaining >= 0",
        name="ck_prediction_comparisons_stops_remaining_non_negative",
    ),
    CheckConstraint(
        "google_eta_seconds IS NULL OR google_eta_seconds >= 0",
        name="ck_prediction_comparisons_google_eta_non_negative",
    ),
    CheckConstraint(
        "google_distance_m IS NULL OR google_distance_m >= 0",
        name="ck_prediction_comparisons_distance_non_negative",
    ),
)
