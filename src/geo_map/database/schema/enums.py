from enum import Enum


class TripStatus(str, Enum):
    scheduled = "scheduled"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class BusStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    offline = "offline"


class UserRole(str, Enum):
    student = "student"
    driver = "driver"
    admin = "admin"
