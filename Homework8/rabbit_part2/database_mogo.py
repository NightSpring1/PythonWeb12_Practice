"""
mongoDB connector. Credentials should be specified in config.ini
"""
import configparser
from mongoengine import connect, disconnect_all
# ----------------------------------------------------Connect-----------------------------------------------------------

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


def mongo_connect():
    print("mongo connection started")
    disconnect_all()
    url = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
    connect(host=url, ssl=True)
    print("mongo connection: OK")
