from sqlalchemy import Column, Enum, String, Table, Uuid, text

from geo_map.database.schema.base import metadata
from geo_map.database.schema.enums import UserRole

User = Table(
    "users",
    metadata,
    Column("id", Uuid, primary_key=True, server_default=text("gen_random_uuid()")),
    Column("email", String, nullable=True, unique=True),
    Column("display_name", String, nullable=False),
    Column("role", Enum(UserRole, name="userrole"), nullable=False),
)
