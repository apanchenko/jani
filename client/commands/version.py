import os, logging
from telethon import events

log = logging.getLogger(__name__)
git_commit = os.getenv('GIT_COMMIT', 'unspecified')
__version__ = os.getenv('JANI_VERSION', 'unspecified')
reply = f'{__version__} commit: {git_commit}'

@events.register(events.NewMessage(pattern='/version'))
async def handle_version(event):
    """
    Handle private command /version
    """
    if not event.is_private:
        return

    await event.respond(reply)

    sender = await event.get_sender()
    log.info(f'/version from 👤{sender.id}')

    raise events.StopPropagation