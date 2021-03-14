from telethon.tl.types import User, Channel, Chat

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