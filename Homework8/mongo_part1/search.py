from mongoengine import connect
from main import Authors, Quotes
import time
from functools import wraps
import logging
from prettytable import PrettyTable
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="192.168.1.242", port=6379, password=None)
cache = RedisLRU(client)

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


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


@time_it
def mongo_connect():
    url = "mongodb+srv://name:pwd@cluster0.vpozurp.mongodb.net/mydatabase?retryWrites=true&w=majority"
    connect(host=url, ssl=True)


@cache
@time_it
def search_by_name(name: str) -> set:
    quotes = set()
    authors = Authors.objects.filter(name__icontains=name)
    for author in authors:
        quotes.update(Quotes.objects.filter(author=author.id))
    return quotes


@cache
@time_it
def search_by_tag(tags: tuple[str]) -> set:
    quotes = set()
    for tag in tags:
        quotes.update(Quotes.objects(tags__icontains=tag))
    return quotes


def print_quotes(quotes: set) -> None:
    table = PrettyTable()
    table.field_names = ["Author", "Quote", "Tags"]

    for quote in quotes:
        table.add_row([quote.author.name, quote.quote, ", ".join(quote.tags)], divider=True)
    print(table)


if __name__ == "__main__":
    mongo_connect()
    time.sleep(0.1)

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
