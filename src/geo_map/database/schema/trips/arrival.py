from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Table, UniqueConstraint, Uuid, text
from src.geo_map.database.schema.base import metadata

StopArrival = Table(
    "stop_arrivals",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=False),
    Column("stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("scheduled_time", DateTime(timezone=True), nullable=True),
    Column("actual_time", DateTime(timezone=True), nullable=True),
    Column("dwell_time_seconds", Integer, nullable=True),
    Column("google_predicted_eta_seconds", Integer, nullable=True),
    UniqueConstraint("trip_id", "stop_id", name="uq_stop_arrivals_trip_stop"),
    CheckConstraint(
        "dwell_time_seconds IS NULL OR dwell_time_seconds >= 0",
        name="ck_stop_arrivals_dwell_time_non_negative",
    ),
    CheckConstraint(
        "google_predicted_eta_seconds IS NULL OR google_predicted_eta_seconds >= 0",
        name="ck_stop_arrivals_google_eta_non_negative",
    ),
)
