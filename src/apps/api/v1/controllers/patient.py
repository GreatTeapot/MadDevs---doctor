from fastapi import APIRouter

from api.dependencies.dependencies import PatientUOWDep, PatientServiceDep, BaseFilterDep, DoctorDep
from common.schemas.pages.mixins import PageViewSchema
from modules.schemas.patients.schemas import CreatePatientSchema, PatientBaseSchema, PatientUpdateSchema
from modules.responses.patients import response

patient = APIRouter(prefix="/api/v1/patient", tags=["Patient"])


@patient.post("/",
              summary="Create a new patient",
              responses=response.PATIENT_CREATE_RESPONSES)
async def create_patient(uow: PatientUOWDep,
                         service: PatientServiceDep,
                         model:CreatePatientSchema,
                         doctor_dep: DoctorDep) -> int:
    """Controller for creating a new patient"""
    patient_data = await service.create(uow, model)
    return patient_data


@patient.get("/",
             summary="Get all patients",
             responses=response.PATIENT_GET_RESPONSES)
async def get_all_patients(uow: PatientUOWDep,
                           service: PatientServiceDep,
                           filters: BaseFilterDep,
                           doctor_dep: DoctorDep) -> PageViewSchema[PatientBaseSchema]:
    """Controller for getting all patients"""
    patient_list = await service.get_all_patients(uow, filters)
    return patient_list


@patient.get("/{patient_id}",
             summary="Get a patient",
             responses=response.PATIENT_GET_RESPONSES)
async def get_patient(uow: PatientUOWDep,
                      service: PatientServiceDep,
                      patient_id: int,
                      doctor_dep: DoctorDep) -> PatientBaseSchema:
    """Controller for getting a patient"""
    patient_data = await service.get_patient(uow, patient_id)
    return patient_data


@patient.put("/{patient_id}",
             summary="Update a patient",
             responses=response.PATIENT_EDIT_RESPONSES)
async def update_patient(uow: PatientUOWDep,
                         service: PatientServiceDep,
                         patient_id: int,
                         model: PatientUpdateSchema,
                         doctor_dep: DoctorDep ) -> bool:
    """Controller for updating a patient"""
    patient_data = await service.update_patient(uow, patient_id, model )
    return patient_data



