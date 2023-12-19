from contextlib import contextmanager
import sshtunnel
import sqlalchemy

from sqlalchemy.engine import create_engine
from rtvt_services.config.get_creds import DbCreds, SshCreds
from rtvt_services.util.constant import DB_URL, SSH_DB_URL


def create_db_engine(ssh_port=None) -> sqlalchemy.engine:
    """

    :return:
    """
    db_creds = DbCreds()
    if not ssh_port:
        url = DB_URL.format(**db_creds.to_dict)
    else:
        url = SSH_DB_URL.format(**db_creds.to_dict, SHH_TUNNEL=ssh_port)
        print(url)
    return create_engine(url=url)


@contextmanager
def ssh_db_engine():
    """

    :return:
    """
    ssh_creds = SshCreds()
    with sshtunnel.SSHTunnelForwarder(
            (ssh_creds.ssh_hostname, int(ssh_creds.ssh_port)),
            ssh_password=ssh_creds.ssh_password,
            ssh_username=ssh_creds.ssh_username,
            # ssh_pkey='',
            remote_bind_address=(ssh_creds.ssh_hostname, 5432),
    ) as server:
        try:
            server.start()
            engine = create_db_engine(f'0.0.0.0:{server.local_bind_port}')
            yield engine
        finally:
            server.stop()
