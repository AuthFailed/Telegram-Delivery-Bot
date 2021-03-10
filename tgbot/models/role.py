from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SUPPORT = "support"
    USER = "user"
