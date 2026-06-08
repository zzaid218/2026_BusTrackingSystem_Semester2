from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from src.geo_map.database.schema.base import metadata

RouteStop = Table(
    "route_stops",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("stop_id", Integer, ForeignKey("stops.id"), nullable=False),
    Column("stop_order", Integer, nullable=False),
    UniqueConstraint("route_id", "stop_id", name="uq_route_stops_route_stop"),
    UniqueConstraint("route_id", "stop_order", name="uq_route_stops_route_order"),
)
