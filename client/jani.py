import os
from telethon import TelegramClient, events, errors
from telethon.tl.types import TypeChat, User, MessageActionChatJoinedByLink, PeerChannel

import dotenv
import logging

dotenv.load_dotenv()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
log = logging.getLogger(name='client')

client = TelegramClient('Jani Space Service', os.environ['API_ID'], os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])

def user_str(user: User) -> str:
    if user is None:
        return f'(None)'
    else:
        return f'{type(user).__name__}({user.id}, {user.first_name} {user.last_name})'

def chat_str(chat: TypeChat) -> str:
    return f'{type(chat).__name__}({chat.id}, {chat.username})'

# @client.on(events.NewMessage)
# async def my_event_handler(event):
#     chat = await event.get_chat()
#     log.info(f'chat {chat}')

@client.on(events.ChatAction(func=lambda e: e.user_joined))
async def handler(event):
    # user joined by link inviter by user
    message = event.action_message
    if message is None:
        log.warning(f'action_message is None at {event}')
    elif type(message.action) == MessageActionChatJoinedByLink:
        log.info(f'Channel({message.to_id.channel_id}) User({message.from_id}) joined by link, invited by User({message.action.inviter_id})')
        return

    user = await event.get_user()
    chat = await event.get_chat()

    # user added by another user
    added_by = await event.get_added_by()
    log.info(f'Chat({chat.id}) delete message about joined User({user.id}) added by {user_str(added_by)}')
    if user is None:
        log.warning(event)

    # delete message
    try:
        await event.delete()
    except errors.rpcerrorlist.MessageDeleteForbiddenError:
        log.error(f'{chat_str(chat)} failed delete ({event}) due to MessageDeleteForbiddenError')


if __name__ == '__main__':
    client.run_until_disconnected()