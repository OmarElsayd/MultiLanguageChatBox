from typing import Generator

from sqlalchemy.orm import sessionmaker
from rtvt_services.db_engine.engine import create_db_engine

engine = create_db_engine()
Session = sessionmaker(bind=engine)


def get_session() -> Generator:
    session = Session()
    try:
        yield session
    finally:
        session.close()
