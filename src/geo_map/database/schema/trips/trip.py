from sqlalchemy import Table, Column, Integer, DateTime, Enum, ForeignKey, Uuid
from geo_map.database.schema.base import metadata
from geo_map.database.schema.enums import TripStatus

Trip = Table(
    "trips",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("driver_id", Uuid, nullable=True),
    Column("trip_status", Enum(TripStatus, name="tripstatus"), nullable=False),
    Column("scheduled_departure", DateTime, nullable=False),
    Column("actual_departure", DateTime, nullable=True),
    Column("scheduled_arrival", DateTime, nullable=True),
    Column("actual_arrival", DateTime, nullable=True),
)
