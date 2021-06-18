from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins
from peano import measured

from client.entity.chat import Chat
from client.entity.admin import Admin


def register_mychannels(client) -> None:
    ''' Register /mychannels handler
    '''

    @events.register(events.NewMessage(pattern='/mychannels'))
    @measured()
    async def handler(message) -> None:
        ''' List channels where sender is admin
        '''
        if not message.is_private:
            return

        admins = Admin.objects(user=message.sender_id).only('chat')

        await message.respond(
            message = 'Choose a channel from the list below:',
            buttons = [[Button.inline(text=admin.chat.title) for admin in admins]]
        )
        raise events.StopPropagation


    client.add_event_handler(handler)
