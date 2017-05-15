import logging
from datetime import datetime
from queue import Queue
from threading import Thread

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import (Updater)

import settings
from decorators import stop_flood, size_limit, log_message
from exceptions import EncodingException
from shelve_utils import users_history as uh
from urllib_utils import create_gist, get_request_contents
from utils import get_default_description, unix_ts, string_md5

logger = logging.getLogger(__name__)


@log_message
def start(bot, update):
    update.message.reply_text("Hello. I can upload your text and documents to https://gist.github.com.")


@log_message
@stop_flood
@size_limit
def on_text_receive(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    url = create_gist(
        get_default_description(),
        datetime.utcnow().strftime('%Y%d%m%H%M%S'),
        update.message.text
    )
    if url:
        uh.update_user_history(
            update.message.from_user.id,
            date=unix_ts(update.message.date),
            txt_msg_hash=string_md5(update.message.text),
            text_url=url
        )
        update.message.reply_text(url)
    else:
        update.message.reply_text('Error during uploading a gist. Please try again.')


@log_message
@stop_flood
def on_file_receive(bot, update):
    new_file = bot.getFile(update.message.document.file_id)
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    try:
        url = create_gist(
            get_default_description(),
            update.message.document.file_name,
            get_request_contents('GET', new_file.file_path)
        )
    except EncodingException as e:
        update.message.reply_text(str(e))
        return 
    if url:
        new_file = bot.getFile(update.message.document.file_id)
        file_contents = get_request_contents('GET', new_file.file_path)
        uh.update_user_history(
            update.message.from_user.id,
            date=unix_ts(update.message.date),
            file_id=update.message.document.file_id,
            file_contents_hash=string_md5(file_contents),
            file_url=url
        )
        update.message.reply_text(url)
    else:
        update.message.reply_text('Error during uploading a gist. Please try again.')


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    if webhook_url:
        bot = telegram.Bot(settings.TELEGRAM_GIST_BOT_TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(settings.TELEGRAM_GIST_BOT_TOKEN)
        bot = updater.bot
        dp = updater.dispatcher

    # message handlers
    start_msg_handler = CommandHandler('start', start)
    text_handler = MessageHandler(Filters.text, on_text_receive)
    file_handler = MessageHandler(Filters.document, on_file_receive)

    dp.add_handler(start_msg_handler)
    dp.add_handler(text_handler)
    dp.add_handler(file_handler)

    logger.info('Bot started.')

    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
