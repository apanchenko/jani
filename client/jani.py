import os
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from telethon import TelegramClient

from .commands.ping import handle_ping
from .commands.version import handle_version
from .commands.help import handle_help
from .filters.spam import handle_spam
from .filters.joined import filter_joined
from .message.private import handle_private_message
from .utils.env import load_env_file
from .utils.monitor import monitor


def run():
    # configure logs
    logging.basicConfig(
        format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
        level=logging.INFO)
    log = logging.getLogger(__name__)

    # optionally load secrets from file
    if 'API_ID' not in os.environ:
        load_env_file('.jani')

    log.info(f'run on {os.getenv("JANI_HOST")}, git commit: {os.getenv("GIT_COMMIT")}')

    # init sentry
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR) # Send errors as events

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        traces_sample_rate=1.0,
        integrations=[sentry_logging])

    monitor.init(
        url = os.getenv("INFLUXDB_V2_URL"),
        org = os.getenv("INFLUXDB_V2_ORG"),
        token = os.getenv("INFLUXDB_V2_TOKEN"),
        bucket = os.getenv("INFLUXDB_BUCKET")
    )

    # create telegram client
    with TelegramClient(
        session   = 'jani',
        api_id    = os.environ['API_ID'],
        api_hash  = os.environ['API_HASH']).start(
        bot_token = os.environ['BOT_TOKEN']) as client:

        #loop.create_task(show_channels(client, log))

        client.add_event_handler(handle_ping)
        client.add_event_handler(handle_version)
        client.add_event_handler(handle_help)
        client.add_event_handler(handle_spam)
        client.add_event_handler(filter_joined)
        client.add_event_handler(handle_private_message)
        client.run_until_disconnected()
