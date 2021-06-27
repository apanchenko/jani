from datetime import datetime as dt

from mongoengine import Document, IntField, DateTimeField


class EventDeleted(Document):
    created = DateTimeField(default=dt.utcnow)
    chat = IntField()
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 3600*24}
        ]
    }