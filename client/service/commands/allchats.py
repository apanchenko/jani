import re
import logging
from telethon import events, Button

from peano import measured
from client.entity.chat import Chat
from ...settings import admin


def handle_allchats(client) -> None:
    ''' Register /allchats handlers
    '''
    command = 'allchats'
    log = logging.getLogger(command)
    page_size = 10


    @events.register(events.NewMessage(pattern='/allchats'))
    @measured()
    async def on_allchats(event) -> None:
        ''' List all chats first page
        '''
        # only accept from private admin 
        if not event.is_private or event.sender_id != admin:
            return

        # show first page chats
        await render_page(event, 0)


    @events.register(events.CallbackQuery(data=re.compile(f'{command}(\d+)')))
    @measured()
    async def on_page(event):
        ''' List all chats starting with offset
        '''
        # get offset from command
        offset = int(event.pattern_match[1])

        # show chats and buttons
        await render_page(event, offset)


    async def render_page(event, offset) -> None:
        ''' Show page of chats and prev/next buttons
        '''
        # clice chats
        chats = Chat.objects[offset:page_size].order_by('deleted_count')

        log.info(f'allchats page: offset {offset}, count {len(chats)}')

        if len(chats) == 0:
            await event.respond('no chat found')
            return

        # prev page button
        buttons = []
        if offset > 0:
            buttons.append(Button.inline(
                text = '⬅️ prev',
                data = command + str(max(offset - page_size, 0))
            ))

        # next page button
        if Chat.objects.count() > offset + page_size:            
            buttons.append(Button.inline(
                text = 'next ➡️',
                data = command + str(offset + page_size)
            ))

        await event.respond(
            message = '\n'.join(f'{c.title}: {c.deleted_count} deleted' for c in chats),
            buttons = None if len(buttons)==0 else buttons
        )

        raise events.StopPropagation


    client.add_event_handler(on_allchats)
    client.add_event_handler(on_page)
