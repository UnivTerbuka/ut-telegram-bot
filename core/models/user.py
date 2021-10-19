from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, String, func
from sqlalchemy_utils import JSONType
from core.db import Base


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    username: str = Column(String, nullable=True)

    # Data
    token: str = Column(String, nullable=True)
    data: dict = Column(JSONType)

    # Debug time
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: datetime = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Flags
    started: bool = Column(Boolean, nullable=False, default=False)
    banned: bool = Column(Boolean, nullable=False, default=False)

    # Permanent settings
    admin: bool = Column(Boolean, nullable=False, default=False)
    notifications_enabled: bool = Column(Boolean, nullable=False, default=True)

    # Chat logic
    expected_input: str = Column(String)

    def __init__(self, user_id: int, name: str, data: dict = None, admin=False):
        self.id = user_id
        self.name = name
        self.data = data or {}
        self.admin = admin

    def __repr__(self):
        """Print as string."""
        return f"User with Id: {self.id}, name: {self.name}"

    def delete(self):
        """Delete the user."""
        self.started = False
        self.username = "GDPR removed user"
        self.name = "GDPR removed user"
        self.locale = "English"
        self.european_date_format = False
        self.notifications_enabled = False
