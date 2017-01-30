import json
import logging

import telegram
import urllib3
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import (Updater)
from urllib3.exceptions import InsecureRequestWarning

import settings
from utils import bool2str, formatted_utc_time, get_http_headers, get_default_description

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def create_gist(description, filename, content, public=True):
    encoded_body = {
        "description": description,
        "public": bool2str(public),
        "files": {
            filename: {
                "content": content
            }
        }
    }

    r = get_request_contents('POST', settings.GITHUB_API_URL, get_http_headers(), encoded_body)
    return json.loads(r).get('html_url', 'Error during uploading a gist.')


def get_request_contents(method, url, headers=None, body=None):
    http = urllib3.PoolManager()
    urllib3.disable_warnings(InsecureRequestWarning)
    return http.request(method=method, url=url, headers=headers, body=json.dumps(body)).data


def start(bot, update):
    update.message.reply_text("Hello. I can upload your text and documents to https://gist.github.com.")


def on_text_receive(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(create_gist(get_default_description(),
                                          formatted_utc_time(),
                                          update.message.text))


def on_file_receive(bot, update):
    filename = update.message.document.file_name
    new_file = bot.getFile(update.message.document.file_id)
    if new_file.file_size > settings.FILESIZE_LIMIT_IN_BYTES:
        update.message.reply_text('File size is too big. Limit is %d bytes' % settings.FILESIZE_LIMIT_IN_BYTES)
        return

    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(create_gist(get_default_description(),
                                          filename,
                                          get_request_contents('GET', new_file.file_path).decode('utf-8')))


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # message handlers
    text_handler = MessageHandler(Filters.text, on_text_receive)
    file_handler = MessageHandler(Filters.document, on_file_receive)

    dp.add_handler(text_handler)
    dp.add_handler(file_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info('Bot started.')

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
