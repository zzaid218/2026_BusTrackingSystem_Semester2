from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, Uuid
from geo_map.database.schema.base import metadata

StopArrival = Table(
    "stop_arrivals",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=False),
    Column("stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("scheduled_time", DateTime, nullable=True),
    Column("actual_time", DateTime, nullable=True),
    Column("dwell_time", Integer, nullable=True),
    Column("google_predicted_eta", Integer, nullable=True),
)
