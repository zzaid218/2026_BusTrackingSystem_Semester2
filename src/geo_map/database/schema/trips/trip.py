from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Index, Integer, Table, Uuid
from src.geo_map.database.schema.base import metadata
from src.geo_map.database.schema.enums import TripStatus

Trip = Table(
    "trips",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("driver_id", Uuid, ForeignKey("users.id"), nullable=True),
    Column("trip_status", Enum(TripStatus, name="tripstatus"), nullable=False),
    Column("scheduled_departure", DateTime(timezone=True), nullable=False),
    Column("actual_departure", DateTime(timezone=True), nullable=True),
    Column("scheduled_arrival", DateTime(timezone=True), nullable=True),
    Column("actual_arrival", DateTime(timezone=True), nullable=True),
    CheckConstraint(
        "scheduled_arrival IS NULL OR scheduled_arrival >= scheduled_departure",
        name="ck_trips_scheduled_arrival_after_departure",
    ),
    CheckConstraint(
        "actual_arrival IS NULL OR actual_departure IS NULL OR actual_arrival >= actual_departure",
        name="ck_trips_actual_arrival_after_departure",
    ),
    Index("ix_trips_bus_status", "bus_id", "trip_status"),
    Index("ix_trips_route_scheduled_departure", "route_id", "scheduled_departure"),
)
