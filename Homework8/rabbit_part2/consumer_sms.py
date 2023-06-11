"""
A stub server which takes a task from rabbitMQ queue and simulates notification to a contact.
"""
import time
from model import Contacts
from broker_rabbitMQ import rabbitMQ_connect
from database_mogo import mongo_connect
from bson import ObjectId


def send_email(ch, method, properties, body):
    contact_id = body.decode()
    record = Contacts.objects.get(id=ObjectId(contact_id))
    if not record.is_notified:
        record.is_notified = True
        print(f" Contact {record.fullname} was notified by SMS")
        record.save()
        time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    mongo_connect()
    channel = rabbitMQ_connect()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='SMS_queue')
    channel.basic_consume(queue='SMS_queue', on_message_callback=send_email)
    channel.start_consuming()
