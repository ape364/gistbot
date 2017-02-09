import os

TELEGRAM_SECRET_URL = os.environ['TELEGRAM_SECRET_URL']
TELEGRAM_GIST_BOT_TOKEN = os.environ['TELEGRAM_GIST_BOT_TOKEN']

MSG_FREQ_LIMIT_IN_SECONDS = 5
FILESIZE_LIMIT_MIN_IN_BYTES = 16
FILESIZE_LIMIT_MAX_IN_BYTES = 1024 * 16

GITHUB_API_URL = 'https://api.github.com/gists'
SHELVE_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shelve.db')

REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR')
DOMAIN_NAME = os.environ.get('OPENSHIFT_GEAR_DNS')
SERVER_IP = os.environ.get('OPENSHIFT_PYTHON_IP')
SERVER_PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', '0'))
