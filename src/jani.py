import os
from telethon import TelegramClient, events

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
        user = await event.get_user()
        added_by = await event.get_added_by()
        logging.info(f'User(id={user.id}, username={user.username}) added by {added_by.id if added_by else added_by}')
        await event.delete()

if __name__ == '__main__':
    bot.run_until_disconnected()