import hashlib

import chardet


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
    if isinstance(data, str):
        return data
    encoding = chardet.detect(data).get('encoding')
    if not encoding:
        return
    return data.decode(encoding)
