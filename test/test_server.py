import pytest

from server import app


@pytest.fixture()
def application():
    app.config.update({
        "TESTING": True
    })

    yield app


@pytest.fixture()
def client():
    return app.test_client()


def test_correct_request(client):
    response = client.post("/rgb", content_type="application/json", json={
        "sessionId": -1,
        "red": 1,
        "green": 2,
        "blue": 3
    })
    assert response.status_code == 200


def test_value_out_of_range(client):
    response = client.post("/rgb", content_type="application/json", json={
        "sessionId": -1,
        "red": -1,
        "green": 2,
        "blue": 3
    })
    assert response.status_code == 422


def test_missing_value(client):
    response = client.post("/rgb", content_type="application/json", json={
        "sessionId": -1,
        "green": 2,
        "blue": 3
    })
    assert response.status_code == 422

# TODO test missing session id

# TODO test missing timestamp

# TODO test missing templates

# TODO test missing text

# TODO test css_builder_service

# TODO test call to java server
