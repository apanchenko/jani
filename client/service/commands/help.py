from telethon import events
from telethon.errors.rpcerrorlist import UserIsBlockedError

from peano import measured


def handle_help(client) -> None:
    '''
    Handle private command /help
    '''
    reply = f'''**Jani Bot** help
    🧹 Jani will remove messages about user joined chat

    Follow these steps:

    - Add @JaniBot as admin into your chat
    - Give bot a permission to delete messages. No other permissions required

    /help - show this message
    '''

    @events.register(events.NewMessage(pattern='/help'))
    @measured()
    async def handler(message):
        if not message.is_private:
            return

        try:
            await message.respond(reply)
        except UserIsBlockedError:
            pass

        raise events.StopPropagation

    client.add_event_handler(handler)