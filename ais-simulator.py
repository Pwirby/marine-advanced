#!/usr/bin/env python3
import pika
import json
import random
#from bitarray import bitarray
from enum import Enum


if __name__ == "__main__":

    # simulating a new received signal
    ais_signal = ''
    for i in range(17):
        ais_signal += str(random.randint(0,1))

    # getting a connection to the broker
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring the queue
    channel.queue_declare(queue='ais_stream')

    # send the message, through the exchange ''
    # which simply delivers to the queue having the key as name
    channel.basic_publish(exchange='',
                      routing_key='ais_stream',
                      body=ais_signal)

    print(" [x] AIS message sent for decoding: " + ais_signal)

    # gently close (flush)
    connection.close()
