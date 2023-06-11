import time
from model import Contacts
from broker_rabbitMQ import rabbitMQ_connect
from database_mogo import mongo_connect
from bson import ObjectId


def send_sms(ch, method, properties, body):
    contact_id = body.decode()
    record = Contacts.objects.get(id=ObjectId(contact_id))
    if not record.is_notified:
        record.is_notified = True
        print(f" Contact {record.fullname} was notified by Email")
        record.save()
        time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    mongo_connect()
    channel = rabbitMQ_connect()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='Email_queue')
    channel.basic_consume(queue='Email_queue', on_message_callback=send_sms)
    channel.start_consuming()
