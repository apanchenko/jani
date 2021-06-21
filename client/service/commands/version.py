import os, logging
from telethon import events

from peano import measured


def handle_version(client) -> None:
    ''' Handle private command /version
    '''
    log = logging.getLogger(__name__)
    git_commit = os.getenv('GIT_COMMIT', 'unspecified')
    __version__ = os.getenv('JANI_VERSION', 'unspecified')
    reply = f'{__version__} commit: {git_commit}'

    @events.register(events.NewMessage(pattern='/version'))
    @measured()
    async def handler(event):
        if not event.is_private:
            return

        await event.respond(reply)

        sender = await event.get_sender()
        log.info(f'/version from 👤{sender.id}')

        raise events.StopPropagation

    client.add_event_handler(handler)