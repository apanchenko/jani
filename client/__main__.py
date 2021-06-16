""" Entry point
"""
import os
import logging

import sentry_sdk, peano
from sentry_sdk.integrations.logging import LoggingIntegration
from telethon import TelegramClient
import pymongo

from .service.commands.help    import handle_help
from .service.commands.ping    import handle_ping
from .service.commands.reload  import register_handle_reload
from .service.commands.version import handle_version
from .service.filters.spam     import handle_spam
from .service.filters.joined   import filter_joined
from .service.message.private  import handle_private_message
from .util.env import load_env_file


if __name__ == '__main__':

    logging.basicConfig(
        level  = "INFO",
        format = "%(asctime)s %(name)-8s %(message)s"
    )
    log = logging.getLogger()

    mongo_client = pymongo.MongoClient('mongo', 27017)
    db = mongo_client['jani']

    # optionally load secrets from file
    if 'API_ID' not in os.environ:
        load_env_file('.jani')

    log.info(f'run on {os.getenv("JANI_HOST")}, git commit: {os.getenv("GIT_COMMIT")}')

    # init sentry
    if os.getenv('JANI_SENTRY_ENABLED') == 'True':
        sentry_logging = LoggingIntegration(
            level = logging.INFO,        # Capture info and above as breadcrumbs
            event_level = logging.ERROR  # Send errors as events
        )
        sentry_sdk.init(
            dsn = os.environ['SENTRY_DSN'],
            traces_sample_rate = 1.0,
            integrations = [sentry_logging]
        )

    peano.init(
        url = os.getenv("JORDAN_INFLUXDB_URL"),
        organ = os.getenv("JORDAN_INFLUXDB_ORG"),
        token = os.getenv("JORDAN_INFLUXDB_TOKEN"),
        bucket = os.getenv("JORDAN_INFLUXDB_BUCKET")
    )

    # create telegram client
    with TelegramClient(
        session   = 'jani',
        api_id    = os.environ['API_ID'],
        api_hash  = os.environ['API_HASH']).start(
        bot_token = os.environ['BOT_TOKEN']) as client:

        client.add_event_handler(handle_help)
        client.add_event_handler(handle_ping)
        register_handle_reload(client, db)
        client.add_event_handler(handle_version)
        client.add_event_handler(handle_spam)
        client.add_event_handler(filter_joined)
        client.add_event_handler(handle_private_message)

        client.loop.create_task(client.catch_up())

        client.run_until_disconnected()
