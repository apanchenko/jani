"""
Filter spam messages in controlled channels
"""
import logging

from telethon import events, errors
from telethon.events import StopPropagation

from ...util.channels import get_from
from ...settings import whitelist
from peano import measured
from ..channel_offset import set_offset

log = logging.getLogger(__name__)

@events.register(events.NewMessage())
@measured()
async def handle_spam(event):

    if not event.is_channel:
        return

    #set_offset(event.chat_id, event.id)

    sender = event.sender_id
    try:
        if sender in whitelist:
            message = 'pass message from manager'
            
        elif 'https://' in event.text or 'http://' in event.text:
            await event.delete()
            message = 'delete link spam'

        else:
            # unhandled event
            return

    except errors.rpcerrorlist.MessageDeleteForbiddenError:
        log.warning(f'failed delete spam due to MessageDeleteForbiddenError: {event}')
        return

    # log and stop propagating event
    desc = await get_from(event)
    log.info(f'{desc} 👤{sender} {message} 🆔{event.message.id}: {event.text}')
    raise StopPropagation