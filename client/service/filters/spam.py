""" Filter spam messages in controlled chats
"""
from telethon import events
from telethon.events import StopPropagation

from peano import measured
from ...entity.chat import Chat
from ...settings import whitelist


def filter_spam(client) -> None:
    ''' Delete spam messages
    '''
    @events.register(events.NewMessage())
    @measured()
    async def handler(event):
        if not event.is_channel:
            return

        if event.sender_id in whitelist:
            return

        if 'https://' in event.text or 'http://' in event.text:
            await Chat.delete_event(event)
            raise StopPropagation

    client.add_event_handler(handler)