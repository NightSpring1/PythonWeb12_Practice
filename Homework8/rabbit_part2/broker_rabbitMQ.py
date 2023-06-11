"""
Connector to a rabbitMQ
"""

import pika
def rabbitMQ_connect():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.1.242', port=5672, credentials=credentials))
    channel = connection.channel()
    return channel
