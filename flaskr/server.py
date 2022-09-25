import requests
from flask import Flask, request
from werkzeug.exceptions import UnprocessableEntity

# Configurations
SERVER_NAME = "python-server"
JAVA_SERVER_ADDRESS = "http://127.0.0.1:8080/rgb"
# Error messages
ERROR_MESSAGE_DRAMATIC = "The Horror! "
ERROR_MESSAGE_MISSING_SESSION_ID = "Missing session id."
ERROR_MESSAGE_MISSING_TIMESTAMP = "Missing timestamp."
ERROR_MESSAGE_MISSING_TEMPLATE = "Missing background color css template."
ERROR_MESSAGE_MISSING_RGB_VALUES_IN_TEMPLATE = "Missing one or more RGB values in the template."
ERROR_MESSAGE_MISSING_RGB_VALUES = "Missing one or more RGB values."
ERROR_MESSAGE_RGB_VALUE_OUT_OF_RANGE = "The RGB values should be integers between 0 and 255."
ERROR_MESSAGE_JAVA_IS_DOWN = "The java server is sad and not answering any calls :("
# Return Messages
RETURN_MESSAGE_POSITIVE = "Java server is up and happily running!"

app = Flask(SERVER_NAME)


@app.post('/rgb')
def rgb():
    css_builder_service(request.json)
    return RETURN_MESSAGE_POSITIVE


def css_builder_service(request_json):
    _validate_request(request_json)
    css_background_color = _format_css(request_json["cssBackgroundColorTemplate"],
                                       request_json["red"],
                                       request_json["green"],
                                       request_json["blue"])

    response_json = request_json.copy()
    del request_json["cssBackgroundColorTemplate"]
    del response_json["red"]
    del response_json["green"]
    del response_json["blue"]
    response_json["cssBackgroundColor"] = css_background_color

    requests.post(JAVA_SERVER_ADDRESS, json=response_json)


def _validate_request(json):
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
        if "{red}" not in css_background_color_template \
                or "{green}" not in css_background_color_template \
                or "{blue}" not in css_background_color_template:
            raise UnprocessableEntity(ERROR_MESSAGE_MISSING_RGB_VALUES_IN_TEMPLATE)
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_TEMPLATE)
    try:
        red = json['red']
        green = json['green']
        blue = json['blue']
    except KeyError:
        raise UnprocessableEntity(ERROR_MESSAGE_MISSING_RGB_VALUES)
    if (not isinstance(red, int) or
            not isinstance(green, int) or
            not isinstance(blue, int) or
            red < 0 or red > 255 or
            green < 0 or green > 255 or
            blue < 0 or blue > 255):
        raise UnprocessableEntity(ERROR_MESSAGE_RGB_VALUE_OUT_OF_RANGE)


def _format_css(css_template: str, red, green, blue):
    result = css_template
    result = result.replace("{red}", str(red))
    result = result.replace("{green}", str(green))
    result = result.replace("{blue}", str(blue))
    return result


@app.errorhandler(UnprocessableEntity)
def _handle_unprocessable_entity(e: UnprocessableEntity):
    return ERROR_MESSAGE_DRAMATIC + e.description, 422


@app.errorhandler(requests.ConnectionError)
def _handle_service_unavailable(e: requests.ConnectionError):
    return ERROR_MESSAGE_JAVA_IS_DOWN, 503
