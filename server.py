import requests
from flask import Flask, request
from requests import ConnectionError
from werkzeug.exceptions import UnprocessableEntity

# Configurations
SERVER_NAME = "python-server"
JAVA_SERVER_ADDRESS = "http://127.0.0.1:8080/rgb"
# Error messages
ERROR_MESSAGE_DRAMATIC = "The Horror! "
ERROR_MESSAGE_MISSING_SESSION_ID = "Missing session id."
ERROR_MESSAGE_MISSING_TIMESTAMP = "Missing timestamp."
ERROR_MESSAGE_MISSING_TEMPLATE = "Missing one or more css templates."
ERROR_MESSAGE_MISSING_TEXT = "Missing one or more RGB values."
ERROR_MESSAGE_MISSING_VALUES = "Missing one or more RGB values."
ERROR_MESSAGE_VALUE_OUT_OF_RANGE = "The RGB values should be integers between 0 and 255."
ERROR_MESSAGE_JAVA_IS_DOWN = "The java server is sad and not answering any calls :("
# Return Messages
RETURN_MESSAGE_POSITIVE = "Java server is up and happily running!"

app = Flask(SERVER_NAME)


@app.post('/rgb')
def rgb():
    css_builder_service(request.json)
    return RETURN_MESSAGE_POSITIVE


def css_builder_service(json):
    validate_request(json)
    session_id = json['sessionId']
    timestamp = timestamp = json['timestamp']
    css_background_color_template = json['cssBackgroundColorTemplate']
    css_text_color_template = json['cssTextColorTemplate']
    red = json['red']
    green = json['green']
    blue = json['blue']
    css_background_color = format_css(css_background_color_template, red, green, blue)
    call_java(session_id, timestamp, css_background_color, css_text_color_template)


def validate_request(json):
    try:
        session_id = json['sessionId']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_SESSION_ID)
    try:
        timestamp = json['timestamp']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_TIMESTAMP)
    try:
        css_background_color_template = json['cssBackgroundColorTemplate']
        css_text_color_template = json['cssTextColorTemplate']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_TEMPLATE)
    try:
        text = json['text']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_TEXT)
    try:
        red = json['red']
        green = json['green']
        blue = json['blue']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_VALUES)
    if (not isinstance(red, int) or
            not isinstance(green, int) or
            not isinstance(blue, int) or
            red < 0 or red > 255 or
            green < 0 or green > 255 or
            blue < 0 or blue > 255):
        raise UnprocessableEntity(ERROR_MESSAGE_VALUE_OUT_OF_RANGE)


def format_css(css_template: str, red, green, blue):
    result = css_template
    result = result.replace("{red}", str(red))
    result = result.replace("{green}", str(green))
    result = result.replace("{blue}", str(blue))
    return result


def call_java(session_id, timestamp, css_background_color, css_text_color_template):
    requests.post(JAVA_SERVER_ADDRESS, json={
        "sessionId": session_id,
        "timestamp": timestamp,
        "cssBackgroundColor": css_background_color,
        "cssTextColorTemplate": css_text_color_template
    })


@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(e: UnprocessableEntity):
    return ERROR_MESSAGE_DRAMATIC + e.description, 422


@app.errorhandler(ConnectionError)
def handle_service_unavailable(e: ConnectionError):
    return ERROR_MESSAGE_JAVA_IS_DOWN, 503
