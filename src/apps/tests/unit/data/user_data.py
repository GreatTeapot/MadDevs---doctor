register_data = [
    {
        "username": "testuser1",
        "email": "testuser@example.com",
        "password_hash": "validpass123",
        "expected_status": 200,
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
