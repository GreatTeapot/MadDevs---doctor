login_data = [
    {"credentials": "validuser", "password": "ValidPass123", "expected_status": 200},
    {"credentials": "invalid_user", "password": "ValidPass123", "expected_status": 401},
    {"credentials": "validuser", "password": "WrongPass%", "expected_status": 401},
]

logout_data = [
    {"expected_message": "You have successfully logged out.", "expected_status": 200},
]
