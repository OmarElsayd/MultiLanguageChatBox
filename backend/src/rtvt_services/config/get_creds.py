import os

from dataclasses import dataclass
from rtvt_services.util.constant import DB_ENV_LIST, SSH_ENV_LIST


def set_env_attr(_obj, env_list):
    for env_key in env_list:
        setattr(_obj, env_key, os.getenv(env_key))


@dataclass
class DbCreds:
    """
    Data Class to fetch env creds from env
    """
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    def __init__(self):
        set_env_attr(self, DB_ENV_LIST)

    @property
    def to_dict(self):
        return vars(self)


@dataclass
class SshCreds:
    """
    Data Class to fetch ssh creds from env
    """
    ssh_hostname: str
    ssh_port: int
    ssh_username: str
    ssh_password: str

    def __init__(self):
        set_env_attr(self, SSH_ENV_LIST)

    @property
    def to_dict(self):
        return vars(self)
