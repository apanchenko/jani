import os
from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageActionChatJoinedByLink

import dotenv
import logging

dotenv.load_dotenv()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
log = logging.getLogger(name='client')

client = TelegramClient('Jani Space Service', os.environ['API_ID'], os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])

def user_str(user):
    if user:
        return f'({user.id})'
    else:
        return f'(None)'

@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        # log message to delete
        user = await event.get_user()

        # user joined by link inviter by user
        message = event.action_message
        if type(message.action) == MessageActionChatJoinedByLink:
            log.info(f'user {user_str(user)} joined by link, invited by ({message.action.inviter_id})')
            return

        # user added by another user
        added_by = await event.get_added_by()
        log.info(f'delete message about joined user {user_str(user)} added by {user_str(added_by)}')

        # delete message
        try:
            await event.delete()
        except errors.rpcerrorlist.MessageDeleteForbiddenError:
            log.error(f'Failed delete ({event}) due to MessageDeleteForbiddenError')


if __name__ == '__main__':
    client.run_until_disconnected()