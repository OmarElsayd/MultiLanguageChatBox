import os
API_V1_BASE_ROOT = '/mlcb/api/v1'

DB_ENV_LIST = ["DB_HOST", "DB_PASS", "DB_PORT", "DB_NAME", "DB_USER"]
SSH_ENV_LIST = ['ssh_password', 'ssh_username', 'ssh_hostname', 'ssh_port']

SSH_DB_URL = 'postgresql://{DB_USER}:{DB_PASS}@{SHH_TUNNEL}/{DB_NAME}'
DB_URL = 'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

REQ_LIB_PATH = 'requirements.txt'

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 45
NUM_SESSION_CODE_CHAR = 6

ALGORITHM = "HS256"

DB_SCHEMA = os.getenv('SCHEMA')

# SUPPORTED_LANGS = [
#   "en",
#   "es",
#   "fr",
#   "de",
#   "zh",
#   "ja",
#   "ko",
#   "ru",
#   "ar",
#   "hi",
#   "pt",
#   "it",
#   "nl",
#   "sv",
#   "fi",
#   "tr",
#   "pl",
#   "vi",
#   "th",
#   "id",
#   "ms",
#   "fa",
#   "he",
#   "el",
#   "cs",
#   "hu",
#   "ro",
#   "da",
#   "no",
#   "sk",
#   "sl",
#   "bg",
#   "hr",
#   "sr",
#   "et",
#   "lv",
#   "lt"
# ]

SUPPORTED_LANGS = [
    "en-US",
    "es-ES",
    "fr-FR",
    "de-DE",
    "zh-CN",
    "ja-JP",
    "ko-KR",
    "ru-RU",
    "ar-EG",
    "hi-IN",
    "pt-PT",
    "it-IT",
    "nl-NL",
    "sv-SE",
    "fi-FI",
    "tr-TR",
    "pl-PL",
    "vi-VN",
    "th-TH",
    "id-ID",
    "ms-MY",
    "fa-IR",
    "he-IL",
    "el-GR",
    "cs-CZ",
    "hu-HU",
    "ro-RO",
    "da-DK",
    "no-NO",
    "sk-SK",
    "sl-SI",
    "bg-BG",
    "hr-HR",
    "sr-RS",
    "et-EE",
    "lv-LV",
    "lt-LT"
]

MAX_LENGTH_PER_STR = 1000

# ws broadcast types
WS_MESSAGE = 'message'
WS_ERROR = 'error'

TRANSCRIPTS_BODY = {
  "body": {
    "user1": {
      "REPLACE_WITH_USER1_USERNAME": {
        "transcript_text": [],
        "source_lang": ""
      }
    },
    "user2": {
      "REPLACE_WITH_USER2_USERNAME": {
        "transcript_text": [],
        "source_lang": ""
      }
    }
  },
  "info": {
    "user1": "",
    "user2": "",
    "user1_lang": "",
    "user2_lang": ""
  }
}

EMAIL_CONFIRMATION_SUBJECT = "Your Confirmation Code for Multi Language Chat Box"
EMAIL_CONFIRMATION_TEMPLET = """
Hello {FIRST_NAME},

Thank you for your recent request. To proceed, please use the confirmation code provided below:

{CONFIRMATION_CODE}

This code is valid for the next 10 min. 

If you did not request this code, please ignore this email or contact our support team.

Best regards,
Multi Language Chat Box

Founder and Maintainer: Omar Elsayd
omar_2546@hotmail.com

"""

CHAT_INVITATION_SUBJECT = "Multi Language Chat Box! You have been invited"
CHAT_INVITATION_TEMPLATE = """
Hello {INVITEE_NAME},

{INVITER_NAME} has invited you to join a chat session on Multi Language Chat Box.

To join the chat, please user the session code below:

{CHAT_CODE}

Date & Time of Chat Session: {DATE_TIME}

If you're unable to attend or have questions, feel free to contact {INVITER_NAME} at {INVITER_EMAIL}.

Looking forward to your participation!

Best regards,
Multi Language Chat Box Team

Note: If you did not expect this invitation, please disregard this email or contact our support team for assistance.

Your Chat Platform Link: 
Support Team Email: omar_2546@hotmail.com

"""
