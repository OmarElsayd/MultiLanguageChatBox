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

API_V1_ROOT_PATH = "/api/v1"

SUPPORTED_LANGS = [
  "en",
  "es",
  "fr",
  "de",
  "zh",
  "ja",
  "ko",
  "ru",
  "ar",
  "hi",
  "pt",
  "it",
  "nl",
  "sv",
  "fi",
  "tr",
  "pl",
  "vi",
  "th",
  "id",
  "ms",
  "fa",
  "he",
  "el",
  "cs",
  "hu",
  "ro",
  "da",
  "no",
  "sk",
  "sl",
  "bg",
  "hr",
  "sr",
  "et",
  "lv",
  "lt"
]

MAX_LENGTH_PER_STR = 1000
