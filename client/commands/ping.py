import logging

from telethon import events
from telethon.events import StopPropagation

log = logging.getLogger(name='client')


@events.register(events.NewMessage(pattern='/ping'))
async def handle_ping(event):
    """
    Handle private message /ping with reply pong
    """
    if not event.is_private:
        return
    sender = await event.get_sender() # event.sender_id
    log.info(f'/ping from 👤{sender.id}')

    await event.respond('pong')

    raise StopPropagation