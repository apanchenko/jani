import os
from telethon import TelegramClient, events, errors

import dotenv
import logging

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = TelegramClient('Jani Space Service', os.environ['API_ID'], os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])


# @bot.on(events.NewMessage)
# async def echo_all(event):
#     logging.info(f'Message: {event}')

@bot.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        # log message to delete
        user = await event.get_user()
        added_by = await event.get_added_by()
        if added_by:
            logging.info(f'User(id={user.id}, username={user.username}) added by {added_by.id}')
        else:
            logging.info(f'User(id={user.id}, username={user.username})')
        # delete message
        try:
            await event.delete()
        except errors.rpcerrorlist.MessageDeleteForbiddenError:
            logging.error(f'Failed delete ({event}) due to MessageDeleteForbiddenError')

if __name__ == '__main__':
    bot.run_until_disconnected()