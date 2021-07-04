import logging

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from peano import measured
from mongoengine import DoesNotExist

from client.entity.chat import Chat
from client.entity.admin import Admin


def handle_reload(client) -> None:
    """ Register /r handler
    """
    log = logging.getLogger('reload')

    @events.register(events.NewMessage(pattern='/r'))
    @measured()
    async def handler(message) -> None:
        if message.is_private:
            return

        log.info(f'/r from 👤{message.sender_id} {message.chat_id=}')

        tchat = await message.get_chat()

        # get or create chat entity
        try:
            chat = Chat.objects.get(id=message.chat_id)
        except DoesNotExist:
            chat = Chat(id=message.chat_id, title=tchat.title)
        chat.save()

        # list admins
        admins = []
        async for user in client.iter_participants(message.chat_id, filter=ChannelParticipantsAdmins):
            log.info(f'👤{user.id=} {user.is_self=} {user.bot=}')
            admins.append(user.id)

        # remove obsolete admins
        Admin.objects(chat=message.chat_id, user__nin=admins).delete()
        
        # insert new admins
        for user in admins:
            Admin(user=user, chat=chat).save()
            
        await message.respond('Reloaded!')
        raise events.StopPropagation


    client.add_event_handler(handler)
