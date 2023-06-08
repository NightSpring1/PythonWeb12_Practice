import json
import configparser
from mongoengine import connect, Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField

# ----------------------------------------------------Connect-----------------------------------------------------------

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)


# ----------------------------------------------------Models------------------------------------------------------------
class Authors(Document):
    name = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()


# ----------------------------------------------------Write-------------------------------------------------------------

if __name__ == '__main__':
    with open("authors.json", 'r', encoding='utf-8') as fr:
        authors = json.load(fr)
    with open("quotes.json", 'r', encoding='utf-8') as fr:
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
