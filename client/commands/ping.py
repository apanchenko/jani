import os, logging

from telethon import events

from ..settings import admin

log = logging.getLogger(__name__)
reply = f'pong from {os.getenv("JANI_HOST", "?")}'

@events.register(events.NewMessage(pattern='/ping'))
async def handle_ping(event):
    """
    Handle private command /ping
    """
    if not event.is_private:
        return

    sender = await event.get_sender() # event.sender_id
    if sender.id != admin:
        return

    await event.respond(reply)

    log.info(f'/ping from 👤{sender.id}')

    raise events.StopPropagation