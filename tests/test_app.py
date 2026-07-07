import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    app_module.activities = copy.deepcopy(original)
    yield
    app_module.activities = copy.deepcopy(original)


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email(client):
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
