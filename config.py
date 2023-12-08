import os
from os import environ, path

BASE_DIR = path.abspath(path.dirname(__file__))


# config class
class Config(object):
    """set Flask configuration variables from .env file."""
    DEBUG = environ.get("DEBUG")
    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

 