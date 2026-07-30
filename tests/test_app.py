import copy
import importlib

import pytest
from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")


@pytest.fixture(autouse=True)
def restore_activities():
    original_state = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))


def test_get_activities_returns_activity_catalog():
    client = TestClient(app_module.app)

    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_new_participant_to_activity():
    client = TestClient(app_module.app)
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant():
    client = TestClient(app_module.app)

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_user_from_activity():
    client = TestClient(app_module.app)

    response = client.delete("/activities/Chess Club/participants/daniel@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
