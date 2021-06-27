import logging
from mongoengine import Document, StringField, IntField, DoesNotExist
from telethon import errors

from .event_deleted import EventDeleted

log = logging.getLogger('chat')


class Chat(Document):
    '''
    :id:            telegram chat id: event.chat_id
    :title:         telegram chat title
    :deleted_count: total number of deleted messages
    '''
    id            = IntField(primary_key=True)
    title         = StringField(max_length=255, required=True)
    deleted_count = IntField(default=0)


    @classmethod
    async def delete_event(cls, event) -> bool:
        ''' Delete event from chat
        '''
        try:
            await event.delete()
        except errors.rpcerrorlist.MessageDeleteForbiddenError:
            log.debug(f'failed delete due to MessageDeleteForbiddenError: {event}')
            return

        # increment total deleted count
        try:
            chat = cls.objects(id=event.chat_id).get()
        except DoesNotExist:
            tchat = await event.get_chat()
            chat = Chat(
                id    = tchat.id,
                title = tchat.title
            )
        chat.deleted_count += 1
        chat.save()

        # create event deleted
        EventDeleted(chat=event.chat_id).save()
