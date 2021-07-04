import re
import logging
from typing import List, Tuple

from telethon import events
from peano import measured

from client.entity.chat import Chat
from ..selector import Page, create_selector
from ...settings import admin


class AllChatsPage(Page):
    @property
    def command(self) -> str:
        '''
        '''
        return '/allchats'

    def filter(self, event) -> bool:
        '''
        '''
        # only accept from private admin 
        return event.sender_id == admin

    @property
    def size(self) -> int:
        ''' Number of objects to show on page
        '''
        return 10
    
    @property
    def row(self) -> int:
        ''' Number of objects in a row
        '''
        return 1

    def get_page(self, user:int, offset:int) -> List[Tuple[str, str]]:
        ''' Get objects on page
        '''
        chats = Chat.objects[offset:offset + self.size].order_by('-deleted_count')
        return [(c.title, f'{self.command}{c.id}') for c in chats]

    def get_count(self, user:int) -> int:
        ''' Get total object count 
        '''
        return Chat.objects.count()



def handle_allchats(client) -> None:
    ''' Register /allchats handlers
    '''
    page = AllChatsPage()
    create_selector(client, page)
    log = logging.getLogger(page.command)


    @events.register(events.CallbackQuery(data=re.compile(f'{page.command}(-?\d+)')))
    @measured()
    async def on_allchats_id(event):
        ''' Render page by offset
        '''
        # get chat id
        chat_id = int(event.pattern_match[1])
        log.info(f'on_allchats_id {chat_id}')

        chat = Chat.objects.get(id = chat_id)

        await event.respond(f'{chat.title}: deleted {chat.deleted_count}')
        raise events.StopPropagation

    client.add_event_handler(on_allchats_id)