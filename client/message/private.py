import logging
from telethon import events

from ..utils.jordan import measured
from ..settings import admin

log = logging.getLogger(__name__)

@measured()
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
    if (msg.gif is not None or
        msg.file is not None or
        msg.photo is not None or
        msg.audio is not None or
        msg.voice is not None or
        msg.video is not None or
        msg.contact is not None or
        msg.document is not None or
        'https://' in msg.text or
        'http://' in msg.text
    ):
        await msg.reply('Do not send me this, please.')
        return

    # resend admin's reply to origin message sender
    if msg.sender_id == admin and msg.is_reply:
        origin = await msg.get_reply_message()
        if origin and origin.forward:
            user_id = origin.forward.sender_id
            if user_id is None:
                # reply to admin that original sender is unknown
                await msg.reply("cannot reply: sender is unknown")
            else:
                # send text from admin to original sender
                log.info(f'reply "{msg.text}" from admin to {user_id}')
                await msg.client.send_message(user_id, msg.text)
        return

    # forward incoming message to admin 
    log.info(f'forward "{msg.text}" from {msg.sender_id} to admin')
    await msg.forward_to(admin)
