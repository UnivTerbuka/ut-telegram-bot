from core.db import db
from sqlalchemy import Column, Integer, Boolean, DateTime, String, func


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    token = Column(String, nullable=True)

    # Debug time
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime,
                        server_default=func.now(),
                        onupdate=func.now(),
                        nullable=False)

    # Permanent settings
    admin = Column(Boolean, nullable=False, default=False)
    locale = Column(String, default="English")
    notifications_enabled = Column(Boolean, nullable=False, default=True)
