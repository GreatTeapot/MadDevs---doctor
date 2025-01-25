register_data = [
    {
        "username": "testuser",
        "email": "test_user@example.com",
        "password_hash": "ValidPass123",
        "expected_status": 201,
    },
    {
        "username": "us#@",  # Invalid username
        "email": "invalid_email@example.com",
        "password_hash": "123",
        "expected_status": 422,
    },
]

profile_data = [
    {"expected_status": 200},
]
