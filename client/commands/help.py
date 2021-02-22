import logging
from telethon import events

from peano import measured


log = logging.getLogger(__name__)

reply = f'''**Jani Bot** help
🧹 Jani will remove messages about user joined chat

Follow these steps:

- Add @JaniBot as admin into your chat
- Give bot a permission to delete messages. No other permissions required

/help - show this message
'''

@measured()
@events.register(events.NewMessage(pattern='/help'))
async def handle_help(message):
    """
    Handle private command /help
    """
    if not message.is_private:
        return

    await message.respond(reply)
    raise events.StopPropagation