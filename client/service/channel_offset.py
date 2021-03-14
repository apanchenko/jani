import logging
from pymongo.mongo_client import MongoClient
from dependency_injector.wiring import inject, Provide
from ..container import Container

log = logging.getLogger(__name__)


@inject
def set_offset(
    channel: int,
    offset: int,
    mongo: MongoClient = Provide[Container.mongo_client]) -> None:
    """ Set current message id in channel
    """
    db = mongo['jani']
    result = db.channel_offset.replace_one({"channel": channel}, {
        'channel': channel,
        'offset': offset
    }, upsert=True)

    log.info(f'set_offset {channel=} {offset=} result {result}')


@inject
def get_offset(
    channel: int,
    mongo: MongoClient = Provide[Container.mongo_client]) -> int:
    """ Get current messasge id in channel
    """
    db = mongo['jani']
    entity = db.channel_offset.find_one({
        "channel": channel
    })
    log.info(f'get_channel {channel=} result {entity=}')
    return entity['offset']
