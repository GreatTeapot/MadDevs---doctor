from typing import Annotated

from fastapi import Depends, Cookie, Header

from api.dependencies.current_user_dep import CurrentUserDep
from api.dependencies.doctor_dep import DoctorOrAdminUserDep
from common.schemas.filters.mixins import DataRangeBaseFilterSchema
from core.constants import REFRESH
from modules.schemas.users.auth_schemas import EmptyUserSchema
from modules.services.patients.service import PatientService
from modules.services.users.auth_serv import AuthService
from modules.services.users.user_serv import UserService
from modules.unit_of_works.patients.patient_uow import PatientUOW
from modules.unit_of_works.users.auth_uow import AuthUOW
from modules.unit_of_works.users.user_uow import UserUOW

# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[EmptyUserSchema, Depends(CurrentUserDep.get_current_user)]
DoctorDep = Annotated[EmptyUserSchema, Depends(DoctorOrAdminUserDep.get_user_with_roles)]
BaseFilterDep = Annotated[DataRangeBaseFilterSchema, Depends(DataRangeBaseFilterSchema)]

# endregion ------------------------------------------------------------------------------

# region --------------------------------- USER ---------------------------------------
UserUOWDep = Annotated[UserUOW, Depends(UserUOW)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- AUTH ---------------------------------------
AuthUOWDep = Annotated[AuthUOW, Depends(AuthUOW)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
# endregion ------------------------------------------------------------------------------

# region ---------------------------------- JWT ---------------------------------------
RefreshDep = Annotated[str, Cookie(alias=REFRESH, include_in_schema=False)]
TokenDep = Annotated[str, Header()]
RolesDep = Annotated[tuple[str, ...], Header()]
HeadersDep = Annotated[str, Header(...)]
# endregion ------------------------------------------------------------------------------

# region ---------------------------------- Patient ---------------------------------------
PatientUOWDep = Annotated[PatientUOW, Depends(PatientUOW)]
PatientServiceDep = Annotated[PatientService, Depends(PatientService)]
