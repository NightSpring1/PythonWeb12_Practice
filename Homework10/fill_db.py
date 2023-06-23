import json

from database.db import Session
from database.models import Author, Tag, Quote
from sqlalchemy import select

session = Session()


def fill_db():
    session = Session()
    with open('quotes.json', 'r', encoding='utf-8') as file_quotes:
        quotes = json.load(file_quotes)
    with open('authors.json', 'r', encoding='utf-8') as file_authors:
        authors = json.load(file_authors)

    tags = set()
    for tag_list in quotes:
        tags.update(tag_list['tags'])

    for tag in tags:
        session.add(Tag(name=tag))
    session.commit()

    for author in authors:
        session.add(Author(fullname=author['fullname'],
                           born_date=author['born_date'],
                           born_location=author['born_location'],
                           description=author['description']))
    session.commit()

    for quote in quotes:
        this_author = session.query(Author).filter(Author.fullname == quote['author']).first()
        if not this_author:
            continue
        this_tags = list(session.scalars(select(Tag).where(Tag.name.in_(quote['tags']))))
        session.add(Quote(author_id=this_author.id,
                          tags=this_tags,
                          quote=quote['quote']))
    session.commit()

