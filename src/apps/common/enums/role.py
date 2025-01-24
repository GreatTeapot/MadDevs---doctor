from enum import Enum

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    CUSTOMER = "customer"

    def __str__(self) -> str:
        return self.value