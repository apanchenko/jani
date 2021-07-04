import re
import logging
from typing import List, Tuple
from abc import ABCMeta, abstractmethod

from telethon import events, Button
from peano import measured


class Page(metaclass=ABCMeta):
    @property
    @abstractmethod
    def command(self) -> str:
        '''
        '''

    @abstractmethod
    def filter(self, event) -> bool:
        '''
        '''

    @property
    @abstractmethod
    def size(self) -> int:
        ''' Number of objects to show on page
        '''
    
    @property
    @abstractmethod
    def row(self) -> int:
        ''' Number of objects in a row
        '''

    @abstractmethod
    def get_page(self, user:int, offset:int) -> List[Tuple[str, str]]:
        ''' Get objects (text, command) on page
        '''
        # todo: return list of named tuples
        # todo: second value in tuple is item id, create command in common code

    @abstractmethod
    def get_count(self, user:int) -> int:
        ''' Get total object count 
        '''


def create_selector(client, page:Page) -> None: # todo: staticmember
    ''' Register command handlers
    '''
    log = logging.getLogger(page.command)

    @events.register(events.NewMessage(pattern=page.command))
    @measured()
    async def on_command(event) -> None:
        ''' List all chats first page
        '''
        # accept in private only
        if not event.is_private:
            return

        if not page.filter(event):
            return

        # show first page chats
        await render_page(event, 0)


    @events.register(events.CallbackQuery(data=re.compile(f'{page.command}_offset_(\d+)')))
    @measured()
    async def on_page(event):
        ''' Render page by offset
        '''
        # get offset from command
        offset = int(event.pattern_match[1])

        # show chats and buttons
        await render_page(event, offset)


    async def render_page(event, offset) -> None:
        ''' Show page and prev/next buttons
        '''
        log.info(f'render {page.command=}, page {offset=}')

        items = page.get_page(event.sender_id, offset)
        if len(items) == 0:
            await event.respond('no chat found')
            return

        # content buttons
        rows = []
        for i in range(0, len(items), page.row):
            rows.append([Button.inline(text, cmd) for text, cmd in items[i:i + page.row]])

        # prev page button
        arrows = []
        if offset > 0:
            arrows.append(Button.inline(
                text = '⬅️ prev',
                data = f'{page.command}_offset_{max(offset - page, 0)}'
            ))

        # next page button
        next_offset = offset + page.size
        if page.get_count(event.sender_id) > next_offset:
            arrows.append(Button.inline(
                text = 'next ➡️',
                data = f'{page.command}_offset_{next_offset}'
            ))

        rows.append(arrows)

        await event.respond(
            message = 'Choose a chat from the list below:',
            buttons = rows
        )

        raise events.StopPropagation


    client.add_event_handler(on_command)
    client.add_event_handler(on_page)
