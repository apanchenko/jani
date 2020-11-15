import os
from telethon import TelegramClient, events, errors
from telethon.tl.types import TypeChat, User, MessageActionChatJoinedByLink, MessageActionChatAddUser, PeerChannel, InputMessagesFilterUrl
from telethon.tl.functions.channels import GetFullChannelRequest

import dotenv
import logging
import re

from channels import Channels
from settings import whitelist


dotenv.load_dotenv()

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)

log = logging.getLogger(name='client')
log.setLevel(level=logging.INFO)
log.info(f'Create tg client')

client = TelegramClient('Jani Space Service', os.environ['API_ID'], os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
channels = Channels()


@client.on(events.NewMessage())
async def handle_spam(event):
    # NewMessage.Event(
    #     original_update=UpdateNewChannelMessage(
    #         message=Message(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), message='xxx', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, from_id=x, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[MessageEntityUrl(offset=0, length=55)], views=None, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]),
    #         pts=24638,
    #         pts_count=1),
    #     pattern_match=None,
    #     message=Message(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), message='xxx', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, from_id=x, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[MessageEntityUrl(offset=0, length=55)], views=None, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]))
    sender = event.sender_id
    if sender in whitelist:
        return
        
    if 'https://' in event.text or 'http://' in event.text:
        channel = await channels.describe(client, event.chat_id)
        try:
            await event.delete()
            log.info(f'{channel} 👤{sender} delete spam 🆔{event.message.id}: {event.text}')
        except errors.rpcerrorlist.MessageDeleteForbiddenError:
            log.debug(f'{channel} 👤{sender} failed delete spam {event} due to MessageDeleteForbiddenError')

    if re.search("k\s*y\s*c", event.text, re.IGNORECASE):
        channel = await channels.describe(client, event.chat_id)
        try:
            await event.delete()
            log.info(f'{channel} 👤{sender} delete spam 🆔{event.message.id}: {event.text}')
        except errors.rpcerrorlist.MessageDeleteForbiddenError:
            log.debug(f'{channel} 👤{sender} failed delete spam {event} due to MessageDeleteForbiddenError')

@client.on(events.ChatAction(func=lambda e: e.user_joined))# or e.user_added))
async def handler(event):
    channel = await channels.describe(client, event.chat_id)
    action_message = event.action_message
    if action_message is None:
        log.info(f'{channel} action_message is None: {event}')
        return

    # cannot delete due to MessageDeleteForbiddenError
    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatJoinedByLink(inviter_id=x), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatJoinedByLink(inviter_id=x), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    if type(action_message.action) == MessageActionChatJoinedByLink:
        log.info(f'{channel} 👤{action_message.from_id} joined 🆔{action_message.id} by link invited by 👤{action_message.action.inviter_id}')
        return

    # delete
    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    try:
        channel = await channels.describe(client, event.chat_id)
        await event.delete()
        log.info(f'{channel} 👤{action_message.from_id} delete message 🆔{action_message.id} about joined added by 👤{event.added_by}')

    # ChatAction.Event(                  action_message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None),
    #   original_update=UpdateNewChannelMessage(message=MessageService(id=x, to_id=PeerChannel(channel_id=x), date=datetime.datetime(x), action=MessageActionChatAddUser(users=[x]), out=False, mentioned=False, media_unread=False, silent=False, post=False, legacy=False, from_id=x, reply_to_msg_id=None), pts=x, pts_count=1),
    #   new_pin=False, new_photo=False, photo=None, user_added=False, user_joined=True, user_left=False, user_kicked=False, unpin=None, created=False, new_title=None)
    except errors.rpcerrorlist.MessageDeleteForbiddenError:
        log.debug(f'{channel} 👤{action_message.from_id} failed delete {event} due to MessageDeleteForbiddenError')

def run():
    client.run_until_disconnected()