from datetime import datetime

from pydantic import EmailStr, Field, field_validator
from pydantic.json_schema import SkipJsonSchema as HiddenField

from common.enums.role import UserRoleEnum
from common.schemas.base import BaseModel


class UserResponseSchema(BaseModel):
    """Schema of the user response."""
    id: int
    username: str
    email: EmailStr


class CurrentUserSchema(UserResponseSchema):
    """Schema of the current user."""

    role: str


class PersonBaseSchema(BaseModel):
    """Base schema for a person."""

    id: int
    username: str
    email: EmailStr


class PersonSchema(PersonBaseSchema):
    """Schema for a person."""


class RegisterSchema(BaseModel):
    """General schema for registration"""

    role: HiddenField[UserRoleEnum] = Field(default=UserRoleEnum.CUSTOMER)
    username: str
    email: EmailStr
    password_hash: str
    created_at: HiddenField[datetime] = Field(default=datetime.now())
    updated_at: HiddenField[datetime] = Field(default=datetime.now())

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        """Username validation."""
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if not username.isalnum():
            raise ValueError("Username must only contain letters and digits.")
        return username

    @field_validator("password_hash")
    def validate_password(cls, password: str) -> str:  # noqa
        """Password validation."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not password.isalnum():
            raise ValueError("Password must consist of only letters and digits.")
        if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            raise ValueError("Password must contain at least one letter and one digit.")
        return password
