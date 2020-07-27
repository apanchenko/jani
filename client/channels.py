import os
from typing import Dict, Optional

from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest


class Channels:
    _titles: Dict[int, str] = {}

    def __init__(self):
        pass

    async def describe(self, client: TelegramClient, id: int) -> Optional[str]:
        if id in self._titles:
            return self._titles[id]

        entity = await client.get_input_entity(PeerChannel(id))
        result = await client(GetFullChannelRequest(entity))
        if hasattr(result, 'chats') and len(result.chats) > 0:
            chat = result.chats[0]
            self._titles[id] = f"{type(chat).__name__}🆔{id} '{chat.title}'"

        return self._titles.get(id)
