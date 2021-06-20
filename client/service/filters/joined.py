import logging

from telethon import events
from telethon.tl.types import MessageActionChatJoinedByLink

from peano import measured
from ...entity.chat import Chat

log = logging.getLogger('joined')


@events.register(events.ChatAction(func=lambda e: e.user_joined))
@measured()
async def filter_joined(event):

    action_message = event.action_message
    if action_message is None:
        log.info(f'action_message is None: {event}')
        return

    if type(action_message.action) == MessageActionChatJoinedByLink:
        # action_message.action.inviter_id
        log.info(f'👤{action_message.from_id} joined by invite')
        return

    await Chat.delete_event(event)

    # action_message.from_id
    # action_message.id
    # event.added_by
