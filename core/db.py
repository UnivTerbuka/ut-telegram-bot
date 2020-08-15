from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(current_app)
migrate = Migrate(current_app, db)
