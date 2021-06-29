import re
import logging
from typing import List

from telethon import events, Button
from peano import measured

from client.entity.admin import Admin
from client.entity.chat import Chat


def handle_mychats(client) -> None:
    ''' Register /mychats handlers
    '''
    command = '/mychats'
    log = logging.getLogger(command)
    page = 5
    row = 3

    def get_page(user:int, offset:int) -> List[str]:
        ''' Slice objects
        '''
        #return [admin.chat.title for admin in Admin.objects(user=user)[offset:size].only('chat')]
        return [f'b{offset+i}' for i in range(page)]


    def get_count(user:int) -> int:
        ''' Total count objects
        '''
        return 25#Admin.objects(user=user).count()


    @events.register(events.NewMessage(pattern=command))
    @measured()
    async def on_mychats(event) -> None:
        ''' List all chats first page
        '''
        # accept private message only
        if not event.is_private:
            return

        # show first page chats
        await render_page(event, 0)


    @events.register(events.CallbackQuery(data=re.compile(f'{command}(\d+)')))
    @measured()
    async def on_page(event):
        ''' List chats starting with offset
        '''
        # get offset from command
        offset = int(event.pattern_match[1])

        # show chats and buttons
        await render_page(event, offset)


    async def render_page(event, offset) -> None:
        ''' Show page and prev/next buttons
        '''
        log.info(f'render_page {offset=}')

        items = get_page(event.sender_id, offset)
        if len(items) == 0:
            await event.respond('no chat found')
            return

        # content buttons
        rows = [list(map(Button.inline, items[i:i+row])) for i in range(0, len(items), row)]

        # prev page button
        arrows = []
        if offset > 0:
            arrows.append(Button.inline(
                text = '⬅️ prev',
                data = command + str(max(offset - page, 0))
            ))

        # next page button
        if get_count(event.sender_id) > offset + page:
            arrows.append(Button.inline(
                text = 'next ➡️',
                data = command + str(offset + page)
            ))

        rows.append(arrows)

        await event.respond(
            message = 'Choose a chat from the list below:',
            buttons = rows
        )

        raise events.StopPropagation


    client.add_event_handler(on_mychats)
    client.add_event_handler(on_page)
