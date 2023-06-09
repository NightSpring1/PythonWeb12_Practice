from model import Contacts
from database_mogo import mongo_connect
from broker_rabbitMQ import rabbitMQ_connect


if __name__ == "__main__":
    mongo_connect()
    channel = rabbitMQ_connect()

    channel.queue_declare(queue='SMS_queue')
    channel.queue_declare(queue='Email_queue')

    # Create fake contacts
    contacts = Contacts.objects()

    for contact in contacts:
        if contact.prioritize_email:
            channel.basic_publish(exchange='', routing_key='Email_queue', body=str(contact.id).encode())
        else:
            channel.basic_publish(exchange='', routing_key='SMS_queue', body=str(contact.id).encode())

    channel.close()
