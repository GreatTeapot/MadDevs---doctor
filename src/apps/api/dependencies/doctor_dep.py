from fastapi import Depends

from api.dependencies.current_user_dep import CurrentUserDep, oauth2_scheme
from common.enums.role import UserRoleEnum
from modules.exceptions.users.exception import UserRolesForbiddenException
from modules.schemas.users.auth_schemas import UserInfoSchema


class DoctorOrAdminUserDep(CurrentUserDep):
    """Dependency for doctor or admin users."""

    allowed_roles = [UserRoleEnum.DOCTOR, UserRoleEnum.ADMIN]

    @classmethod
    async def get_user_with_roles(
        cls,
        token: str = Depends(oauth2_scheme),
    ) :
        """Retrieve the current doctor or admin user."""
        user = await cls.get_current_user(token=token)
        if user.role not in cls.allowed_roles:
            raise UserRolesForbiddenException()
        return user
