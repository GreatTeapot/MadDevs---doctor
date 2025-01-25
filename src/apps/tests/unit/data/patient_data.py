create_patient_data = [
    {
        "date_of_birth": "2000-01-01",
        "diagnoses": ["Diagnosis A", "Diagnosis B"],
        "expected_status": 201,
    },
    {
        "date_of_birth": "2025-04-04",  # Invalid future date
        "diagnoses": None,
        "expected_status": 422,
    },
]

update_patient_data = [
    {
        "patient_id": 1,
        "date_of_birth": "1995-05-05",
        "diagnoses": ["Updated Diagnosis"],
        "expected_status": 200,
    },
]

