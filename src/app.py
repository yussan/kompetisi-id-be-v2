#!flask/bin/python

from flask import Flask
from config import Config

def create_app(config=Config):
    # create flask app, return flask app
    app = Flask(__name__)

    # load configuration
    app.config.from_object(config)

    return app