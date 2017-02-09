import settings
from settings import MSG_FREQ_LIMIT_IN_SECONDS
from shelve_utils import users_history as uh
from urllib_utils import get_request_contents
from utils import string_md5, unix_ts


def size_limit(f):
    def wrapped_f(bot, update, *args, **kwargs):
        if update.message.document:
            size = bot.getFile(update.message.document.file_id).file_size
            msg_type = 'File size'
        else:
            size = len(update.message.text)
            msg_type = 'Message length'

        min_limit, max_limit = settings.FILESIZE_LIMIT_MIN_IN_BYTES, settings.FILESIZE_LIMIT_MAX_IN_BYTES

        if min_limit < size < max_limit:
            f(bot, update, *args, **kwargs)
        else:
            update.message.reply_text(
                '{} must be greater than {} and less than {} bytes'.format(msg_type, min_limit, max_limit)
            )

    return wrapped_f


def stop_flood(f):
    def wrapped_f(bot, update, *args, **kwargs):
        def msg_freq_check(upd):
            msg_ts = unix_ts(upd.message.date)
            uid = upd.message.from_user.id
            if MSG_FREQ_LIMIT_IN_SECONDS > msg_ts - uh.get_last_message_ts(uid):
                seconds_remaining = uh.get_last_message_ts(uid) + MSG_FREQ_LIMIT_IN_SECONDS - msg_ts
                return 'Too many requests. Please try again in {} seconds'.format(seconds_remaining)

        def txt_msg_dup_check(upd):
            uid = upd.message.from_user.id
            if string_md5(upd.message.text) == uh.get_last_text_message_hash(upd.message.from_user.id):
                gist_url = uh.get_last_gist_from_text_url(uid)
                return 'Your message is duplicating previous. Here it is {}'.format(gist_url)

        def file_msg_dup_check(upd):
            if not upd.message.document:
                return

            file_id = upd.message.document.file_id
            checked_file = bot.getFile(file_id)
            uid = upd.message.from_user.id
            checked_file_contents = get_request_contents('GET', checked_file.file_path)

            if any([file_id == uh.get_last_file_id(uid),
                    string_md5(checked_file_contents) == uh.get_last_file_contents_hash(uid)]):
                gist_url = uh.get_last_gist_from_file_url(uid)
                return 'Your document is duplicating previous. Here it is {}'.format(gist_url)

        flooding = False

        if uh.is_known_user(update.message.from_user.id):
            for check in [msg_freq_check, txt_msg_dup_check, file_msg_dup_check]:
                error_message = check(update)
                if error_message:
                    update.message.reply_text(error_message)
                    flooding = True
                    break

        if flooding:
            return

        if update.message.document:
            new_file = bot.getFile(update.message.document.file_id)
            file_contents = get_request_contents('GET', new_file.file_path)
            uh.update_user_history(
                update.message.from_user.id,
                date=unix_ts(update.message.date),
                file_id=update.message.document.file_id,
                file_contents_hash=string_md5(file_contents)
            )
        else:
            uh.update_user_history(
                update.message.from_user.id,
                date=unix_ts(update.message.date),
                txt_msg_hash=string_md5(update.message.text)
            )

        f(bot, update, *args, **kwargs)

    return wrapped_f
