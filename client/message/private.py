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

    # allow text only
    if msg.file or msg.photo or msg.document or msg.audio or msg.voice or msg.video or msg.gif or msg.contact:
        await msg.reply('Do not send me this, please.')
        return

    # resend admin's reply to origin message sender
    if msg.sender_id == admin and msg.is_reply:
        origin = await msg.get_reply_message()
        if origin and origin.forward:
            log.info(f'reply "{msg.text}" from admin to {origin.forward.sender_id}')
            await msg.client.send_message(origin.forward.sender_id, msg.text)
        return

    # forward incoming message to admin 
    log.info(f'forward "{msg.text}" from {msg.sender_id} to admin')
    await msg.forward_to(admin)
