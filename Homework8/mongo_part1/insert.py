"""
A simple script to insert authors and quotes data in JSON format into mongoDB.
Before using script, DB connection credentials should be specified in config.ini
All fields should be filled, every quote should have valid Author.
Contains documents` models which could be used externally.

Authors .json format:
[{  "fullname": "<name>",
    "born_date": "<date>",
    "born_location": "<location>",
    "description": "<description>"},]

Quotes .json format:
[{  "tags": [<tag1>,<tag2>],
    "author": "<author>",
    "quote": "<quote>"},]
"""

import json
import configparser
from mongoengine import connect, disconnect_all, Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


# ----------------------------------------------------Connect-----------------------------------------------------------
def mongo_connect():
    """
    Establish mongoDB connection with credentials provided in config.ini.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    disconnect_all()
    url = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
    connect(host=url, ssl=True)


# ----------------------------------------------------Models------------------------------------------------------------
class Authors(Document):
    """
    ODM Authors model for mongoDB.
    """
    name = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    """
    ODM Quotes model for mongoDB.
    """
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()


# ----------------------------------------------------Write-------------------------------------------------------------

def json_to_db(authors_json: str, quotes_json: str) -> None:
    """
    Writes Authors and Quotes data from .json to mongoDB. Connection should be
    established before calling this function. JSON structure should correspond
    to Authors and Quotes model. All Quotes should have a valid Author, otherwise
    exception will be raised.
    """
    with open(authors_json, 'r', encoding='utf-8') as fr:
        authors = json.load(fr)
    with open(quotes_json, 'r', encoding='utf-8') as fr:
        quotes = json.load(fr)

    for author in authors:
        Authors(name=author['fullname'],
                born_date=author['born_date'],
                born_location=author['born_location'],
                description=author['description']).save()

    for quote in quotes:
        author = Authors.objects.get(name=quote['author'])
        Quotes(tags=quote['tags'],
               author=author,
               quote=quote['quote']).save()


if __name__ == '__main__':
    mongo_connect()
    json_to_db("authors.json", "quotes.json")
