import os
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from telethon import TelegramClient

from .commands.ping import handle_ping
from .filters.spam import handle_spam
from .filters.joined import filter_joined
from .utils.env import load_env_file


def run():
    # configure logs
    logging.basicConfig(
        format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
        level=logging.INFO)

    # optionally load secrets from file
    if 'API_ID' not in os.environ:
        load_env_file('.jani')

    # init sentry
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR) # Send errors as events

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        traces_sample_rate=1.0,
        integrations=[sentry_logging])

    # create telegram client
    client = TelegramClient(
        session='jani',
        api_id=os.environ['API_ID'],
        api_hash=os.environ['API_HASH'])

    client.start(bot_token=os.environ['BOT_TOKEN'])
    client.add_event_handler(handle_ping)
    client.add_event_handler(handle_spam)
    client.add_event_handler(filter_joined)
    client.run_until_disconnected()
