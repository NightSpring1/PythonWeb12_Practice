"""
Contacts model for mongoengine
"""
from mongoengine import Document, connect
from mongoengine.fields import StringField, EmailField, BooleanField


connect(host="mongodb://127.0.0.1:27017/my_db")


class Contacts(Document):
    fullname = StringField()
    email = EmailField()
    phone = StringField()
    is_notified = BooleanField()
    prioritize_email = BooleanField()
