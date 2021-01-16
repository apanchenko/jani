import logging

from telethon import events
from telethon.events import StopPropagation

from .. import __version__

log = logging.getLogger(__name__)

@events.register(events.NewMessage(pattern='/version'))
async def handle_version(event):
    """
    Handle private message /version
    """
    if not event.is_private:
        return

    await event.respond(__version__)

    sender = await event.get_sender()
    log.info(f'/version from 👤{sender.id}')

    raise StopPropagation