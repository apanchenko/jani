"""
Filter spam messages in controlled channels
"""
from telethon import events
from telethon.events import StopPropagation

from peano import measured
from ...entity.chat import Chat
from ...settings import whitelist


@events.register(events.NewMessage())
@measured()
async def handle_spam(event):

    if not event.is_channel:
        return

    if event.sender_id in whitelist:
        return

    if 'https://' in event.text or 'http://' in event.text:
        await Chat.delete_event(event)
        raise StopPropagation