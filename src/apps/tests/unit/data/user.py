from modules.const.users import const  as resp_exc
from common.enums.role import UserRoleEnum

GET_USER_INFO_TEST_DATA = (
    "user_id, test_result",
    (
        ("1", True),
        # не существующий пользователь
        ("090232", resp_exc.USER_NOT_FOUND),
        ("2", True),
    ),
)


CREATE_USERS_PROFILE_TEST_DATA = (
    "test_data",
    (
        {
            "role": UserRoleEnum.CUSTOMER,
            "email": "TestCustomer@gmail.com",
            "password_hash": "1234567890",
            "test_result": resp_exc.EMAIL_CONFLICT,
        },
        {
            "role": UserRoleEnum.CUSTOMER,
            "email": "Guest10@gmail.com",
            "password_hash": "guest_2134_leonov",
            "test_result": True,
        },
        {
            "role": UserRoleEnum.CUSTOMER,
            "email": "Driver10@gmail.com",
            "password_hash": "driver_2134_leonov",
            "test_result": True,
        },
    ),
)