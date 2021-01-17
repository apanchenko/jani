import logging
from telethon import events

log = logging.getLogger(__name__)

reply = f'''**Jani Bot** help
🧹 Jani will remove messages about user joined chat

Follow these steps:

- Add @JaniBot as admin into your chat
- Give bot a permission to delete messages. No other permissions required

/help - show this message
'''

@events.register(events.NewMessage(pattern='/help'))
async def handle_help(event):
    """
    Handle private command /help
    """
    if not event.is_private:
        return

    await event.respond(reply)

    sender = await event.get_sender()
    log.info(f'/help from 👤{sender.id}')

    raise events.StopPropagation