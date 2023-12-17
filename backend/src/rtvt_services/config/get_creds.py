import os

from dataclasses import dataclass
from rtvt_services.const import db_env_list


@dataclass
class DbCreds:
    def __init__(self):
        for env_key in db_env_list:
            setattr(self, env_key, os.getenv(env_key))

    def to_dict(self):
        return vars(self)


