import json

import urllib3
from urllib3.exceptions import InsecureRequestWarning

import settings
from utils import get_http_headers, decode_bytes


def create_gist(description, filename, content, public=True):
    decoded_content = decode_bytes(content)
    if not decoded_content:
        return
    encoded_body = {
        "description": description,
        "public": 'true' if public else 'false',
        "files": {
            filename: {
                "content": decoded_content
            }
        }
    }

    r = get_request_contents('POST', settings.GITHUB_API_URL, get_http_headers(), encoded_body)
    return json.loads(r.decode('utf-8')).get('html_url')


def get_request_contents(method, url, headers=None, body=None):
    http = urllib3.PoolManager()
    urllib3.disable_warnings(InsecureRequestWarning)
    return http.request(method=method, url=url, headers=headers, body=json.dumps(body)).data
