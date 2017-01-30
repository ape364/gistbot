import os

from flask import Flask, request
from telegram import Update

import bot
import settings

application = Flask(__name__, instance_path=os.environ['OPENSHIFT_REPO_DIR'])
update_queue, bot_instance = bot.setup(webhook_url='https://{}/{}'.format(
    os.environ['OPENSHIFT_GEAR_DNS'],
    settings.TELEGRAM_SECRET_URL
))


@application.route('/')
def not_found():
    """Server won't respond in OpenShift if we don't handle the root path."""
    return ''


@application.route('/' + settings.TELEGRAM_SECRET_URL, methods=['GET', 'POST'])
def webhook():
    if request.json:
        update_queue.put(Update.de_json(request.json, bot_instance))
    return ''


if __name__ == '__main__':
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    application.run(host=ip, port=port)
