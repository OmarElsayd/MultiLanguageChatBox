import os

DB_ENV_LIST = ["DB_HOST", "DB_PASS", "DB_PORT", "DB_NAME", "DB_USER"]
SSH_ENV_LIST = ['ssh_password', 'ssh_username', 'ssh_hostname', 'ssh_port']

SSH_DB_URL = 'postgresql://{DB_USER}:{DB_PASS}@{SHH_TUNNEL}/{DB_NAME}'
DB_URL = 'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

REQ_LIB_PATH = 'requirements.txt'

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 45
ALGORITHM = "HS256"

DB_SCHEMA = os.getenv('SCHEMA')
