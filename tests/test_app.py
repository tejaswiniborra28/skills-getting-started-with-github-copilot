import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = {}
    for name, details in activities.items():
        original_state[name] = {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": list(details["participants"]),
        }

    yield

    for name, details in original_state.items():
        activities[name] = {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": list(details["participants"]),
        }


client = TestClient(app)


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert second_response.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant_removes_them_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
