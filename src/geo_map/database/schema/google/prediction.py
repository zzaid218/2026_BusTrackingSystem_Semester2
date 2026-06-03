from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey, Uuid
from geo_map.database.schema.base import metadata

PredictionComparison = Table(
    "prediction_comparisons",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("distance_matrix_log_id", Uuid, ForeignKey("distance_matrix_logs.id"), nullable=False),
    Column("trip_id", Uuid, ForeignKey("trips.id"), nullable=False),
    Column("stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("bus_id", Integer, ForeignKey("buses.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("bus_lat", Float, nullable=False),
    Column("bus_lng", Float, nullable=False),
    Column("bus_speed_kmh", Float, nullable=True),
    Column("stops_remaining", Integer, nullable=True),
    Column("google_eta", Integer, nullable=True),
    Column("google_distance_m", Float, nullable=True),
    Column("actual_arrival", DateTime, nullable=True),
    Column("google_error", Integer, nullable=True),
)
