import datetime


def bool2str(b):
    return 'true' if b else 'false'


def formatted_utc_time(dt_format='%Y%d%m%H%M%S'):
    return datetime.datetime.utcnow().strftime(dt_format)


def get_http_headers():
    return {'Content-Type': 'application/json',
            'User-Agent': 'Gist-Uploader-Bot'}


def get_default_description():
    return 'Created from http://t.me/github_gist_bot'