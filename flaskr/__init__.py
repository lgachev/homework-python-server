# Configurations
from logging.config import dictConfig

from flask import Flask

SERVER_NAME = "python-server"
JAVA_SERVER_ADDRESS = "http://127.0.0.1:8080/rgb"

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(SERVER_NAME)

from flaskr import server
