# pylint: disable=W0613
import os
import pytest
from sqlalchemy.engine import create_engine
from mlcb_services.config.get_creds import DbCreds, SshCreds
from mlcb_services.db_engine.engine import create_db_engine
from mlcb_services.util.constant import DB_URL


@pytest.mark.parametrize("test_creds_class", [DbCreds, SshCreds])
def test_fetch_db_and_ssh_creds(test_creds_class, db_test_env):
    creds = test_creds_class().to_dict
    for key, value in creds.items():
        assert value == os.getenv(key)


def test_db_engine(db_test_env):
    url = DB_URL.format(**db_test_env)
    pytest_engine = create_engine(url=url)
    assert_engine = create_db_engine()

    assert pytest_engine.url == assert_engine.url
