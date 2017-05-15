import os

TELEGRAM_SECRET_URL = os.environ['TELEGRAM_SECRET_URL']
TELEGRAM_GIST_BOT_TOKEN = os.environ['TELEGRAM_GIST_BOT_TOKEN']

MESSAGE_INTERVAL = 5  # seconds
MESSAGE_LEN_LIMIT_MIN = 16  # bytes
MESSAGE_LEN_LIMIT_MAX = 1024 * 4  # bytes

GITHUB_API_URL = 'https://api.github.com/gists'

DATA_FILEPATH = os.environ.get('OPENSHIFT_DATA_DIR')
LOG_FILENAME = os.path.join(DATA_FILEPATH, 'bot.log')
SHELVE_FILENAME = os.path.join(DATA_FILEPATH, 'shelve.db')
ACCESS_LOG_DB_PATH = os.path.join(DATA_FILEPATH, 'blitz-db/')

REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR')
DOMAIN_NAME = os.environ.get('OPENSHIFT_GEAR_DNS')
SERVER_IP = os.environ.get('OPENSHIFT_PYTHON_IP')
SERVER_PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', '0'))
