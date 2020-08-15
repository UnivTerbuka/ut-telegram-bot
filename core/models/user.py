from core.db import db
from sqlalchemy import Column, Integer, Boolean, String


class User(db.Model):
    id = Column(Integer, primary_key=True)
    is_bot = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
