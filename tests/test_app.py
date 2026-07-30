from fastapi.testclient import TestClient

from src.app import app


def test_unregister_participant_removes_user_from_activity():
    client = TestClient(app)

    initial_response = client.get("/activities")
    assert initial_response.status_code == 200
    initial_activities = initial_response.json()
    assert "michael@mergington.edu" in initial_activities["Chess Club"]["participants"]

    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    assert "michael@mergington.edu" not in updated_activities["Chess Club"]["participants"]
