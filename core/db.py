from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(current_app)
from .models import *  # NOQA
