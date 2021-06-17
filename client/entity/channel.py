import logging
from typing import List

from pymongo.database import Database


log = logging.getLogger('🧑‍⚖️')


def update_admins(db:Database, channel_id:int, channel_title:str, admins:List[int]) -> None:
    '''
    Update list of admin by channel

    schema: admin(channel, user)

    1. Remove obsolete admins
    2. Insert new admins

    docs:
        https://docs.mongodb.com/v4.4/core/transactions/
    '''
    col = db['admin']
    channel_collection = db['channel']

    # update channel info
    channel_collection.update_one(
        {'id':channel_id},
        {'$set': {'id':channel_id, 'title':channel_title}},
        upsert = True
    )

    # remove obsolete admins
    result = col.delete_many({
        'channel': channel_id,
        'user': {'$nin': admins}
    })
    log.info(f'deleted {result.deleted_count} admins')

    # insert new admins
    modified_count = 0
    for user in admins:
        doc = {'channel': channel_id, 'user': user}
        result = col.update_one(doc, {'$set': doc}, upsert=True)
        modified_count += result.modified_count
    log.info(f'modified {modified_count} admins')


def get_channels(db:Database, admin:int) -> List[str]:
    '''
    Get list of channels by admin
    '''
    col = db['admin']
    channel_collection = db['channel']

    # get channel ids by admin user
    channels_ids = []
    for admin_entity in col.find({'user': admin}, {'_id':0, 'channel':1}):
        channels_ids.append(admin_entity['channel'])

    # get channel titles
    titles = []
    for channel_entity in channel_collection.find({'id':{'$in':channels_ids}}):
        titles.append(channel_entity['title'])

    return titles