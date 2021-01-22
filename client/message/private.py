import logging
from telethon import events

from ..settings import admin

log = logging.getLogger(__name__)


@events.register(events.NewMessage(outgoing=False))
async def handle_private_message(msg) -> None:
    """
    Forward private messages to admin
    """
    if not msg.is_private:
        return

    # filter out commands
    if msg.text[:1] == "/":
        return

    if msg.file or msg.photo or msg.document or msg.audio or msg.voice or msg.video or msg.gif or msg.contact:
        await msg.reply('Do not send me this, please.')
        return

    await msg.forward_to(admin)
