import logging
import os
from typing import Generator

from sqlalchemy.orm import sessionmaker
from rtvt_services.db_engine.engine import create_db_engine, ssh_db_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("session making (session.py)")

SSH = os.getenv('SSH')

Session = sessionmaker()


def get_session() -> Generator:
    if not SSH:
        logger.info('session not using ssh')
        engine = create_db_engine()
        Session.configure(bind=engine)
        session = Session()
        logger.info('successfully establishing session factory !ssh')
        try:
            yield session
        finally:
            session.close()
    else:
        logger.info('session using ssh')
        with ssh_db_engine() as engine:
            logger.info('Got ssh engine')
            Session.configure(bind=engine)
            session = Session()
            logger.info('successfully establishing ssh session factory')
            try:
                yield session
            finally:
                session.close()
