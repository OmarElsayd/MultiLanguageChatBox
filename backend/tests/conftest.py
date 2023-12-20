import os

import pytest

PYTEST_ENV_DICT = {
    'DB_HOST': 'localhost',
    'DB_PASS': 'pytest',
    'DB_PORT': '5432',
    'DB_USER': 'postgres',
    'DB_NAME': 'pytest',
    'ssh_username': 'pytest',
    'ssh_password': 'pytest',
    'ssh_hostname': '127.0.0.1',
    'ssh_port': '22',
    'JWT_SECRET_KEY': 'Pytest',
    'JWT_REFRESH_SECRET_KEY': 'Pytest',
    'SSH': 'True'
}


@pytest.fixture(scope='session')
def db_test_env():
    for key, value in PYTEST_ENV_DICT.items():
        os.environ[key] = value
    return PYTEST_ENV_DICT

