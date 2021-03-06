import json
import shelve
from contextlib import contextmanager

import settings


@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()


class ShelveHelper:
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def _get_keys():
        return {'date', 'txt_msg_hash', 'file_contents_hash', 'file_id', 'text_url', 'file_url'}

    def _get_value(self, user_id):
        with closing(shelve.open(self.filepath)) as db:
            data = db.get(str(user_id))
            return json.loads(data) if data else dict()

    def _set_value(self, user_id, data):
        with closing(shelve.open(self.filepath)) as db:
            db[str(user_id)] = json.dumps(data)

    def is_known_user(self, user_id):
        with closing(shelve.open(self.filepath)) as db:
            return str(user_id) in db

    def get_last_message_ts(self, user_id):
        return int(self._get_value(user_id).get('date'))

    def get_last_text_message_hash(self, user_id):
        return self._get_value(user_id).get('txt_msg_hash')

    def get_last_file_contents_hash(self, user_id):
        return self._get_value(user_id).get('file_contents_hash')

    def get_last_file_id(self, user_id):
        return self._get_value(user_id).get('file_id')

    def get_last_gist_from_text_url(self, user_id):
        return self._get_value(user_id).get('text_url')

    def get_last_gist_from_file_url(self, user_id):
        return self._get_value(user_id).get('file_url')

    def update_user_history(self, user_id, **kwargs):
        d = dict.fromkeys(self._get_keys())
        for k in self._get_keys():
            if k in kwargs:
                d[k] = kwargs[k]
            else:
                d[k] = self._get_value(user_id).get(str(k))
        self._set_value(user_id, d)


users_history = ShelveHelper(settings.SHELVE_FILENAME)
