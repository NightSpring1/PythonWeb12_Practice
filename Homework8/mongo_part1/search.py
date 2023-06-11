"""
A simple CLI search engine to search Quotes by author name or tag(s).
Connections to mongoDB and redis should be established compulsory.
Input commands should be entered carefully, since input validation
is not implemented.
Usage:
     name:<author> - Searches for quotes with given name
     (ex. name:Albert Einstein; name:alb)

     tag:<tag1>,<tag2> - Searches for quotes with a given tag(s)
     (ex. tag:live,value; tag:vi,va)

     exit - Terminate script
"""

import logging
import redis
import time

from insert import Authors, Quotes, mongo_connect
from functools import wraps
from prettytable import PrettyTable
from redis_lru import RedisLRU

client = redis.StrictRedis(host="192.168.1.242", port=6379, password=None)
cache = RedisLRU(client)

# logger initialize
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


# Decorator function to measure functions execution time
def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'Function {func.__name__} started')
        start = time.time()
        results = func(*args, **kwargs)
        finish = time.time()
        logger.debug(f'Function {func.__name__} executed in {finish - start:.4f} seconds.')
        return results
    return wrapper


@cache
@time_it
def search_by_name(name: str) -> set[Quotes]:
    """
    Searches in database for quotes by authors whose names contain the specified string.
    Returns a set of Quotes objects or empty set if no matches were found.
    """
    quotes = set()
    authors = Authors.objects.filter(name__icontains=name)
    for author in authors:
        quotes.update(Quotes.objects.filter(author=author.id))
    return quotes


@cache
@time_it
def search_by_tag(tags: tuple[str]) -> set[Quotes]:
    """
    Searches for quotes whose tags contain the specified string(s).
    Single string should be given as tuple.
    Returns a set of Quotes objects or empty set if no matches were found.
    """
    quotes = set()
    for tag in tags:
        quotes.update(Quotes.objects(tags__icontains=tag))
    return quotes


def print_quotes(quotes: set[Quotes]) -> None:
    """
    Prints a formatted table with given set of Quotes objects.
    """
    table = PrettyTable()
    table.field_names = ["Author", "Quote", "Tags"]

    for quote in quotes:
        table.add_row([quote.author.name, quote.quote, ", ".join(quote.tags)], divider=True)
    print(table)


def run() -> None:
    while True:
        prompt = input('Enter command: ')
        command, entry = prompt.split(':')
        if command == 'name':
            result = search_by_name(entry)
        elif command == 'tag':
            entry = tuple(entry.split(','))
            result = search_by_tag(entry)
        elif prompt == 'exit':
            break
        else:
            continue

        time.sleep(0.1)
        print_quotes(result)


if __name__ == "__main__":
    mongo_connect()
    time.sleep(0.1)
    run()
