import os

from dataclasses import dataclass
from rtvt_services.const import DB_ENV_LIST


@dataclass
class DbCreds:
    """
    Class to fetch env creds from env
    """
    def __init__(self):
        for env_key in DB_ENV_LIST:
            setattr(self, env_key, os.getenv(env_key))

    @property
    def to_dict(self):
        return vars(self)
