from datetime import date, datetime
from typing import Optional, List

from pydantic import  Field, field_validator
from pydantic.json_schema import SkipJsonSchema as HiddenField

from common.schemas.base import BaseModel


class PatientBaseSchema(BaseModel):
    """Base schema for a patient."""

    id: int
    date_of_birth: date
    diagnoses: Optional[List[str]] = Field(default=None)


class PatientResponseSchema(PatientBaseSchema):
    """Schema for a patient response."""
    pass


class CreatePatientSchema(BaseModel):
    """Schema for creating a patient."""

    date_of_birth: date
    diagnoses: Optional[List[str]] = Field(default=None)
    created_at: HiddenField[datetime] = Field(default=datetime.now())
    updated_at: HiddenField[datetime] = Field(default=datetime.now())


    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, dob: date) -> date:
        """Validate that date of birth is not in the future."""
        from datetime import date as today_date
        if dob > today_date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return dob


class PatientUpdateSchema(CreatePatientSchema):
    """Schema for updating a patient."""

