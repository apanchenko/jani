from telethon import events, Button

from peano import measured
from client.entity.admin import Admin


def handle_mychats(client) -> None:
    ''' Register /mychats handler
    '''

    @events.register(events.NewMessage(pattern='/mychats'))
    @measured()
    async def handler(message) -> None:
        ''' List chats where sender is admin
        '''
        if not message.is_private:
            return

        admins = Admin.objects(user=message.sender_id).only('chat')

        await message.respond(
            message = 'Choose a chat from the list below:',
            buttons = [[Button.inline(text=admin.chat.title) for admin in admins]]
        )
        raise events.StopPropagation


    client.add_event_handler(handler)
