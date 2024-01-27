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
    Enum,
    JSON,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from mlcb_services.db_models.base import Base


class Role(enum.Enum):
    Admin = "Admin"
    User = "User"


class MlcbUsers(Base):
    __tablename__ = 'mlcb_users'

    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    password = Column(Text, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())


class Transcripts(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True, nullable=False)
    body = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())


class MlcbSessions(Base):
    __tablename__ = 'mlcb_sessions'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(MlcbUsers.id), nullable=False)
    participants = Column(ARRAY(String), nullable=False)
    session_passcode = Column(String(100), nullable=True)
    is_call = Column(Boolean, nullable=False, default=False)
    end_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    transcript_id = Column(Integer, ForeignKey(Transcripts.id), nullable=False)
    session_code = Column(String(20), nullable=False)

    users = relationship("MlcbUsers")
    transcripts = relationship("Transcripts")


class UsersSession(Base):
    __tablename__ = 'users_session'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(MlcbUsers.id), nullable=False)
    session_id = Column(Integer, ForeignKey(MlcbSessions.id), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow())
    spoken_lang = Column(String(5), nullable=False)

    users = relationship("MlcbUsers")
    sessions = relationship("MlcbSessions")
