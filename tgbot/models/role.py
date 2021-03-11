from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    COURIER = "courier"
    USER = "user"
