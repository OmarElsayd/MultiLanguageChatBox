# Author: Omar Elsayd
from datetime import datetime
import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum
)
from sqlalchemy.orm import relationship
from rtvt_services.db_models.base import Base


class Role(enum.Enum):
    Admin = "Admin"
    User = "User"


class RtvtUsers(Base):
    __tablename__ = 'rtvt_users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())


class RtvtSessions(Base):
    __tablename__ = 'rtvt_sessions'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(RtvtUsers.id), nullable=False)
    transcript = Column(Text, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    users = relationship(RtvtUsers)
