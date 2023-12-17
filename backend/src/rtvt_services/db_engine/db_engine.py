import sqlalchemy
from sqlalchemy.engine import create_engine
from rtvt_services.config.get_creds import DbCreds
from rtvt_services.const import db_url


def create_db_engine() -> sqlalchemy.engine:
    """

    :return:
    """
    db_creds = DbCreds()
    url = db_url.format(**db_creds.to_dict())
    print(url)
    return create_engine(url)


print(create_db_engine())