import requests

API_URL = "http://localhost:8000"

def test_predict_endpoint():
    payload = {
        "age": 22,
        "student_income": 500,
        "parent_income": 2000,
        "academic_year": 2024,
        "region": "Île-de-France",
        "residence_type": "Urban",
        "gender": "Male",
        "grade_math": 14,
        "grade_programming": 15,
        "grade_algorithms": 13,
        "grade_databases": 14,
        "grade_software_engineering": 16
    }
    response = requests.post(f"{API_URL}/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "probability" in result

def test_healthcheck():
    response = requests.get(f"{API_URL}/docs")
    assert response.status_code == 200
