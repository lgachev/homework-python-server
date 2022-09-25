import pytest
import requests
from werkzeug.exceptions import UnprocessableEntity

from flaskr import server
from flaskr.server import app


@pytest.fixture()
def application():
    app.config.update({
        "TESTING": True
    })

    yield app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def valid_json():
    return {
        "sessionId": -1,
        "timestamp": -1,
        "cssBackgroundColorTemplate": "rgb({red}, {green}, {blue})",
        "red": 1,
        "green": 2,
        "blue": 3,
        "cssTextColorTemplate": "",
        "text": ""
    }


# Test REST API
def test_correct_request(client, valid_json, requests_mock):
    requests_mock.post(server.JAVA_SERVER_ADDRESS)
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 200
    assert server.RETURN_MESSAGE_POSITIVE in response.text


def test_missing_java(client, valid_json, requests_mock):
    requests_mock.post(server.JAVA_SERVER_ADDRESS, exc=requests.ConnectionError)
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 503
    assert server.ERROR_MESSAGE_JAVA_IS_DOWN in response.text


def test_java_rethrow_422(client, valid_json, requests_mock):
    java_error = "Java validator fail."
    requests_mock.post(server.JAVA_SERVER_ADDRESS, exc=UnprocessableEntity(java_error))
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert java_error in response.text


# Test validations
def test_missing_session_id(client, valid_json):
    valid_json.pop("sessionId")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_SESSION_ID in response.text


def test_missing_timestamp(client, valid_json):
    valid_json.pop("timestamp")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_TIMESTAMP in response.text


def test_missing_template(client, valid_json):
    valid_json.pop("cssBackgroundColorTemplate")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_TEMPLATE in response.text


def test_missing_rgb_template(client, valid_json):
    valid_json["cssBackgroundColorTemplate"] = "rgb({red}, {green})"
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_RGB_VALUES_IN_TEMPLATE in response.text


def test_red_value_out_of_range(client, valid_json):
    valid_json["red"] = -1
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_RGB_VALUE_OUT_OF_RANGE in response.text


def test_red_missing_value(client, valid_json):
    valid_json.pop("red")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_RGB_VALUES in response.text


def test_green_value_out_of_range(client, valid_json):
    valid_json["green"] = -1
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_RGB_VALUE_OUT_OF_RANGE in response.text


def test_green_missing_value(client, valid_json):
    valid_json.pop("green")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_RGB_VALUES in response.text


def test_blue_value_out_of_range(client, valid_json):
    valid_json["blue"] = -1
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_RGB_VALUE_OUT_OF_RANGE in response.text


def test_blue_missing_value(client, valid_json):
    valid_json.pop("blue")
    response = client.post("/rgb", content_type="application/json", json=valid_json)
    assert response.status_code == 422
    assert server.ERROR_MESSAGE_MISSING_RGB_VALUES in response.text


# Test css formatter
def test_css_formatter(valid_json):
    css = server._format_css(valid_json["cssBackgroundColorTemplate"],
                             valid_json["red"],
                             valid_json["green"],
                             valid_json["blue"])
    assert css == "rgb(1, 2, 3)"
