from mongoengine import Document, IntField, ReferenceField

from .chat import Chat


class Admin(Document):
    user = IntField(primary_key=True)
    chat = ReferenceField(Chat)

