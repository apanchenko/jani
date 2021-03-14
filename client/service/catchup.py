import logging
from .channel_offset import get_offset
from telethon import TelegramClient, functions, types
import datetime as dt

log = logging.getLogger(__name__)

#   {
#     "channel": -1001163629262,
#     "offset": 7162
#   }

async def catchup(client: TelegramClient) -> None:
    """ Catchup all channels after restart
    """
    channel = -1001163629262
    offset = get_offset(channel)

    # result = await client(functions.messages.SearchRequest(
    #     peer=-1001163629262,
    #     q='',
    #     filter=types.InputMessagesFilterPhotos(),
    #     min_date=None,
    #     max_date=None,
    #     offset_id=0,
    #     add_offset=0,
    #     limit=100,
    #     max_id=0,
    #     min_id=offset,
    #     hash=0,
    #     from_id=None,
    #     top_msg_id=0
    # ))

    # result = await client(functions.messages.GetHistoryRequest(
    #     peer = channel,
    #     limit = 1,
    #     offset_date = 0,
    #     offset_id = 0,
    #     min_id = offset,
    #     max_id = 0,
    #     add_offset = 0,
    #     hash = 0
    # ))
    # log.info(f'catchup {type(result)=}, {result}')


    # async for message in client.iter_messages(entity=-1001163629262, limit=20, min_id=offset):
    #     log.info(f'catchup {type(message)=}, {message.text}')

    # num = 0
    # while num < 10:
    #     num += 1
    #     message = await client.get_messages(channel, ids=offset + num) 
    #     log.info(f'catchup {type(message)=}, {message.text}')

    result = None
    try:
        result = await client.get_messages(channel, ids=[offset, offset+1, offset+2])
    except ValueError:
        log.exception('failed get messages')
        return

    log.info(f'catchup {type(result)=}, {result}')
