import datetime
import hashlib

import chardet


def bool2str(b):
    return 'true' if b else 'false'


def formatted_utc_time(dt_format='%Y%d%m%H%M%S'):
    return datetime.datetime.utcnow().strftime(dt_format)


def get_http_headers(content_type='application/json', user_agent='Gist-Uploader-Bot'):
    return {'Content-Type': content_type,
            'User-Agent': user_agent}


def get_default_description():
    return 'Created from http://t.me/github_gist_bot'


def unix_ts(date):
    return int(date.strftime('%s'))


def string_md5(s):
    return hashlib.md5(s.encode()).hexdigest() if isinstance(s, str) else hashlib.md5(s).hexdigest()


def decode_bytes(data):
    return data if isinstance(data, str) else data.decode(chardet.detect(data).get('encoding'))
