import os, logging

from telethon import events

from ...settings import admin
from peano import measured

log = logging.getLogger('ping')
reply = f'pong from {os.getenv("JANI_HOST", "?")}'

@events.register(events.NewMessage(pattern='/ping'))
@measured()
async def handle_ping(message) -> None:
    """
    Handle private command /ping
    """
    if not message.is_private:
        return

    if message.sender_id != admin:
        return

    await message.respond(reply)

    log.info(f'/ping from 👤{message.sender_id}')

    raise events.StopPropagation