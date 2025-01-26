from typing import Optional, Union

import pytest
from fastapi import HTTPException

from common.enums.role import UserRoleEnum
from modules.exceptions.users import exception as exceptions
from modules.schemas.users.user_schemas import RegisterSchema
from modules.services.users.user_serv import UserService
from tests.unit.data import user as data_array
from tests.unit.fixtures.user import ProfileTestUOW


@pytest.mark.parametrize(*data_array.CREATE_USERS_PROFILE_TEST_DATA)
async def test_create_users_profile(
    profile_uow: ProfileTestUOW,
    profile_service: UserService,
    test_data: dict[str, Union[str, bool, Optional[int], UserRoleEnum]],
) -> None:
    """Тест для регистрации пользователя."""
    test_result = test_data.pop("test_result")
    filters = RegisterSchema(**test_data)

    list_exceptions = (
        exceptions.EmailAlreadyExistsException,
    )

    if isinstance(test_result, str):
        with pytest.raises(HTTPException) as exc:
            await profile_service.create(profile_uow, filters)
        assert exc.type in list_exceptions
        assert exc.value.detail == test_result
    else:
        result = await profile_service.create(profile_uow, filters)
        assert bool(result) == test_result