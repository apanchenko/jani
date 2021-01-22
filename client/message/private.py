import logging
from telethon import events

from ..settings import admin

log = logging.getLogger(__name__)


@events.register(events.NewMessage(outgoing=False))
async def handle_private_message(message) -> None:
    """
    Forward private messages to admin
    """
    if not message.is_private:
        return

    # filter out commands
    if message.text[:1] == "/":
        return

    if message.contact:
        await message.reply('Do not send me contacts, please.')
        return

    await message.forward_to(admin)
