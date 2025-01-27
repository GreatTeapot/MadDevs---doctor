from common.enums.role import UserRoleEnum

register_data = [
    {
        "username": "testuser2",
        "email": "test@gmail.com",
        "password_hash": "pass12345",
        "expected_status": 200,
        "role": UserRoleEnum.DOCTOR
    },
    {
        "username": "us#@",  # Invalid username
        "email": "invalid_email@example.com",
        "password_hash": "123",
        "expected_status": 422,
    },
]

profile_data = [
    {
        "expected_status": 200,
    },
]
