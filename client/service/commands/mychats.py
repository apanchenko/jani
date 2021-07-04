import re
import logging
from typing import List, Tuple

from telethon import events, Button
from peano import measured

from client.entity.admin import Admin
from client.entity.chat import Chat
from ..selector import Page, create_selector


class MyChatsPage(Page):
    @property
    def command(self) -> str:
        '''
        '''
        return '/mychats'

    def filter(self, event) -> bool:
        '''
        '''
        return True

    @property
    def size(self) -> int:
        ''' Number of objects to show on page
        '''
        return 5
    
    @property
    def row(self) -> int:
        ''' Number of objects in a row
        '''
        return 3

    def get_page(self, user:int, offset:int) -> List[Tuple[str, str]]:
        ''' Get objects on page
        '''
        return [(a.chat.title, f'{self.command}{a.chat.id}') for a in Admin.objects(user=user)[offset:offset+self.size].only('chat')]

    def get_count(self, user:int) -> int:
        ''' Get total object count 
        '''
        return Admin.objects(user=user).count()


def handle_mychats(client) -> None:
    ''' Register /mychats handlers
    '''
    page = MyChatsPage()
    create_selector(client, page)
    log = logging.getLogger(page.command)

    @events.register(events.CallbackQuery(data=re.compile(f'{page.command}(-?\d+)')))
    @measured()
    async def on_mychats_id(event):
        ''' Render selected chat
        '''
        # get chat id
        chat_id = int(event.pattern_match[1])
        log.info(f'on_mychats_id {chat_id}')

        chat = Chat.objects.get(id = chat_id)

        await event.respond(f'{chat.title}: deleted {chat.deleted_count}')
        raise events.StopPropagation

    client.add_event_handler(on_mychats_id)
