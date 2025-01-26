from datetime import datetime
from typing import TypeAlias, Union

from common.schemas.filters.mixins import DataRangeBaseFilterSchema
from common.schemas.pages.mixins import PageViewSchema
from common.services.mixins import PaginatedPageService
from models.patient import Patient
from modules.exceptions.patients.exception import PatientNotFoundException
from modules.schemas.patients.schemas import CreatePatientSchema, PatientBaseSchema, PatientUpdateSchema
from modules.unit_of_works.patients.patient_uow import PatientUOW

EditData: TypeAlias = dict[str, Union[str, bool, datetime, int, None]]


class PatientService(PaginatedPageService):
    """service for working with patients"""

    @staticmethod
    def __convert_record(record: Patient) -> PatientBaseSchema:
        """Convert a record into a pydantic model"""
        return PatientBaseSchema(
            id=record.id,
            date_of_birth=record.date_of_birth,
            diagnoses=record.diagnoses,
        )

    @classmethod
    async def create(cls,
                     uow: PatientUOW,
                     schema: CreatePatientSchema) -> int:
        """create a new patient"""
        patient_data = schema.model_dump()
        result = await cls.add(uow, patient_data)
        return result

    @classmethod
    async def get_patient(cls,
                          uow: PatientUOW,
                          patient_id: int) -> PatientBaseSchema:
        """get a patient"""
        current_patient = await cls.get(uow, patient_id)
        if current_patient is None:
            raise PatientNotFoundException()
        return current_patient

    @classmethod
    async def update_patient(cls,
                             uow: PatientUOW,
                             patient_id: int,
                             schema: PatientUpdateSchema) -> bool:
        """update the patient"""
        patient_data = schema.model_dump()
        result = await cls.edit(uow, patient_data, patient_id)
        return result

    @classmethod
    async def delete_patient(cls,
                             uow: PatientUOW,
                             patient_id: int) -> bool:
        """Set patient status to deleted"""
        result = await cls.delete(uow, patient_id)
        return bool(result)

    @classmethod
    async def get_all_patients(cls, uow: PatientUOW,
                               filters: DataRangeBaseFilterSchema) -> PageViewSchema:
        """get all patients by filters"""
        async with uow:
            count_records, records = await uow.repo.get_all(filters)
            if filters is None:
                list_records = []
            else:
                list_records = [
                    cls.__convert_record(record) for record in cls._gen_records(records)
                ]
            response = cls._get_response(
                count_records, PatientBaseSchema, list_records, filters
            )
            return response
