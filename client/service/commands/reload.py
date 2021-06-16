import logging

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from pymongo.database import Database
from peano import measured

from client.entity.channel import update_admins


def register_handle_reload(client, db:Database) -> None:
    """ Register /r handler
    """
    log = logging.getLogger('reload')

    @events.register(events.NewMessage(pattern='/r'))
    @measured()
    async def handler(message) -> None:
        if message.is_private:
            return

        log.info(f'/r from 👤{message.sender_id} {message.chat_id=}')

        admins = []
        async for user in client.iter_participants(message.chat_id, filter=ChannelParticipantsAdmins):
            log.info(f'👤{user.id=} {user.is_self=} {user.bot=}')
            admins.append(user.id)

        update_admins(db, message.chat_id, admins)
            
        await message.respond('Reloaded!')
        raise events.StopPropagation


    client.add_event_handler(handler)
