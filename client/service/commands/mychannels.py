import logging

from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins
from pymongo.database import Database
from peano import measured

from client.entity.channel import get_channels


def register_mychannels(client, db:Database) -> None:
    """ Register /mychannels handler
    """
    log = logging.getLogger('/mychannels')

    @events.register(events.NewMessage(pattern='/mychannels'))
    @measured()
    async def handler(message) -> None:
        ''' List channels where sender is admin
        '''
        if not message.is_private:
            return

        channels = get_channels(db, message.sender_id)
        log.info(f'👤{message.sender_id}: {channels}')

        await message.respond(
            message = 'Choose a channel from the list below:',
            buttons = [[Button.inline(text=ch) for ch in channels]]
        )
        raise events.StopPropagation


    client.add_event_handler(handler)
