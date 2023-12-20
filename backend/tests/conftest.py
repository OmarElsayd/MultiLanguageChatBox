import os

import pytest

from rtvt_services.db_engine.engine import create_db_engine
from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.base import Base

PYTEST_ENV_DICT = {
    'DB_HOST': 'localhost',
    'DB_PASS': 'test_password',
    'DB_PORT': '5432',
    'DB_USER': 'test_user',
    'DB_NAME': 'test_db',
    'ssh_username': 'pytest',
    'ssh_password': 'pytest',
    'ssh_hostname': '127.0.0.1',
    'ssh_port': '22',
    'JWT_SECRET_KEY': 'Pytest',
    'JWT_REFRESH_SECRET_KEY': 'Pytest',
    'DB_SCHEMA': 'pytest'
}


@pytest.fixture(scope='session')
def db_test_env():
    for key, value in PYTEST_ENV_DICT.items():
        os.environ[key] = value
    return PYTEST_ENV_DICT


@pytest.fixture(scope="session")
def setup_test_db():
    pytest_engine = create_db_engine()
    Base.metadata.create_all(bind=pytest_engine)

    pytest_session = get_session()
    session = next(pytest_session)  # pylint: disable=R1708
    yield session

    session.rollback()
    Base.metadata.drop_all(bind=pytest_engine)
    session.close()
