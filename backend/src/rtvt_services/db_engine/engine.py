import sqlalchemy
from sqlalchemy.engine import create_engine
from rtvt_services.config.get_creds import DbCreds
from rtvt_services.const import DB_URL


def create_db_engine() -> sqlalchemy.engine:
    """

    :return:
    """
    db_creds = DbCreds()
    url = DB_URL.format(**db_creds.to_dict)

    return create_engine(url=url)

