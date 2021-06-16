import logging
from typing import List

from pymongo.database import Database


log = logging.getLogger(__name__)


def set_offset(channel:int, offset:int, db:Database) -> None:
    """ Set current message id in channel
    """
    result = db.channel_offset.replace_one({"channel": channel}, {
        'channel': channel,
        'offset': offset
    }, upsert=True)

    log.info(f'set_offset {channel=} {offset=} result {result}')


def get_offset(channel:int, db:Database) -> int:
    """ Get current messasge id in channel
    """
    entity = db.channel_offset.find_one({
        "channel": channel
    })
    log.info(f'get_channel {channel=} result {entity=}')
    return entity['offset']


def update_admins(db:Database, channel:int, admins:List[int]) -> None:
    '''
    Update list of admin by channel

    schema: admin(channel, user)

    1. Remove obsolete admins
    2. Insert new admins

    docs:
        https://docs.mongodb.com/v4.4/core/transactions/
    '''
    col = db['admin']

    # remove obsolete admins
    result = col.delete_many({
        'channel': channel,
        'user': {'$nin': admins}
    })
    log.info(f'deleted {result.deleted_count} admins')

    # insert new admins
    modified_count = 0
    for user in admins:
        doc = {'channel': channel, 'user': user}
        result = col.update_one(doc, {'$set': doc}, upsert=True)
        modified_count += result.modified_count
    log.info(f'modified {modified_count} admins')
