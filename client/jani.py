import os
import logging

from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageActionChatJoinedByLink, UpdateNewMessage

from channels import Channels
from utils.env import load_env_file
from commands.ping import handle_ping
from filters.spam import handle_spam


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)

log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)
log.info(f'Create tg client')

# optionally load secrets from file
if 'API_ID' not in os.environ:
    load_env_file('.jani')

client = TelegramClient('Jani Space Service', os.environ['API_ID'], os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
channels = Channels()



@client.on(events.ChatAction(func=lambda e: e.user_joined))# or e.user_added))
async def handler(event):

    if type(event) == UpdateNewMessage:
        return

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
    client.add_event_handler(handle_ping)
    client.add_event_handler(handle_spam)
    client.add_event_handler(handler)
    client.run_until_disconnected()