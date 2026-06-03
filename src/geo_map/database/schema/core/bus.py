from sqlalchemy import Table, Column, Integer, String, ForeignKey
from geo_map.database.schema.base import metadata

Bus = Table(
    "buses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=True),
    Column("label", String, nullable=True),
)
