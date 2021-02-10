import logging

from telethon import events, errors
from telethon.tl.types import MessageActionChatJoinedByLink

from ..channels import get_from
from ..utils.measure import measured
from ..settings import whitelist

log = logging.getLogger(__name__)

@measured()
@events.register(events.ChatAction(func=lambda e: e.user_joined))
async def filter_joined(event):
    desc = await get_from(event)

    action_message = event.action_message
    if action_message is None:
        log.info(f'{desc} action_message is None: {event}')
        return

    # cannot delete due to MessageDeleteForbiddenError
    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatJoinedByLink(inviter_id=x), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatJoinedByLink(inviter_id=x), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    if type(action_message.action) == MessageActionChatJoinedByLink:
        log.info(f'{desc} 👤{action_message.from_id} joined 🆔{action_message.id} by link invited by 👤{action_message.action.inviter_id}')
        return

    # delete
    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    try:
        await event.delete()
        log.info(f'{desc} 👤{action_message.from_id} delete message 🆔{action_message.id} about joined added by 👤{event.added_by}')

    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    except errors.rpcerrorlist.MessageDeleteForbiddenError:
        log.debug(f'{desc} 👤{action_message.from_id} failed delete {event} due to MessageDeleteForbiddenError')
