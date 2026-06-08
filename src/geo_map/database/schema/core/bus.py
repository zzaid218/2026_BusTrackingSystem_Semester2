from sqlalchemy import CheckConstraint, Column, Enum, Integer, String, Table, text
from geo_map.database.schema.base import metadata
from geo_map.database.schema.enums import BusStatus

Bus = Table(
    "buses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String, nullable=False, unique=True),
    Column("capacity", Integer, nullable=False, server_default=text("0")),
    Column(
        "status",
        Enum(BusStatus, name="busstatus"),
        nullable=False,
        server_default=BusStatus.inactive.value,
    ),
    CheckConstraint("capacity >= 0", name="ck_buses_capacity_non_negative"),
)
