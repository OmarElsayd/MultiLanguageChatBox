import logging
from contextlib import contextmanager
import socket
import sshtunnel
import sqlalchemy

from sqlalchemy.engine import create_engine
from mlcb_services.config.get_creds import DbCreds, SshCreds
from mlcb_services.util.constant import DB_URL, SSH_DB_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("engine.py")


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('1.1.1.1', 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except socket.error as error:
        logger.error(f"Error getting local IP address: {error}")
        return None


def create_db_engine(ssh_port=None) -> sqlalchemy.engine:
    """

    :return:
    """
    db_creds = DbCreds()
    if not ssh_port:
        logger.info('bypass ssh db connection')
        url = DB_URL.format(**db_creds.to_dict)
    else:
        logger.info('using ssh db connection')
        url = SSH_DB_URL.format(**db_creds.to_dict, SHH_TUNNEL=ssh_port)
    return create_engine(url=url)


@contextmanager
def ssh_db_engine():
    """

    :return:
    """
    ssh_creds = SshCreds()
    logger.info('fetched ssh creds')
    with sshtunnel.SSHTunnelForwarder(
            (ssh_creds.ssh_hostname, int(ssh_creds.ssh_port)),
            ssh_password=ssh_creds.ssh_password,
            ssh_username=ssh_creds.ssh_username,
            # ssh_pkey='',
            remote_bind_address=(ssh_creds.ssh_hostname, 5432),
    ) as server:
        try:
            server.start()
            logger.info('SSH Tunnel started')
            local_ip = get_local_ip()
            engine = create_db_engine(f'{local_ip}:{server.local_bind_port}')
            logger.info('SSH engine started')
            yield engine
        except Exception as ssh_error:  # pylint: disable=W0718
            logger.error(ssh_error)
        finally:
            server.stop()
