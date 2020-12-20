import os
from typing import Dict, Optional
import logging

from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import User, Channel, Chat

log = logging.getLogger(name='channels')
log.setLevel(level=logging.INFO)

async def get_from(event) -> str:
    """
    Describe event chat/channel
    TODO: chat_id may be not set (https://docs.telethon.dev/en/latest/modules/custom.html#telethon.tl.custom.chatgetter.ChatGetter.chat_id)
    """
    chat = await event.get_chat()

    name = ''
    if isinstance(chat, (Chat, Channel)):
        name = chat.title

    elif isinstance(chat, User):
        name = chat.username

    return f"📣{type(chat).__name__}🆔{event.chat_id} '{name}'"


class Channels:
    _titles: Dict[int, str] = {}

    def __init__(self):
        pass

    async def describe(self, client: TelegramClient, id: int) -> Optional[str]:
        if id in self._titles:
            return self._titles[id]

        try:
            entity = await client.get_input_entity(PeerChannel(id))
        except:
            # ValueError: Could not find the input entity for <telethon.tl.types.PeerChannel object at 0x7f03496580a0>. Please read https://docs.telethon.dev/en/latest/concepts/entities.html to find out more details.
            log.warning(f'‼️ Failed get_input_entity({id})')
            return None

        result = await client(GetFullChannelRequest(entity))
        if hasattr(result, 'chats') and len(result.chats) > 0:
            chat = result.chats[0]
            self._titles[id] = f"{type(chat).__name__}🆔{id} '{chat.title}'"

        return self._titles.get(id)
