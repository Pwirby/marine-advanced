#!/usr/bin/env python3
from itertools import count
import sys
import os

import json
import pika


def reset_counter():
    return {"TANKER": 0,
            "CARGO": 0,
            "PASSENGER": 0,
            "FISHING": 0}

counter = reset_counter()


def reset(ch, method, properties, body):
    """Reset the counter of each boat types"""
    global counter
    counter = reset_counter()
    print(f" [x] Counters has been reset:\n{counter}")


def callback(ch, method, properties, body):
    """Defining what to do when a message is received"""

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    boat_type = str(body_json["boat_type"])
    counter[boat_type] += 1
    print(f" [x] Number of each type of boat:\n{counter}")


def main():
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='reset_stream')
    channel.basic_consume(queue='reset_stream',
                          on_message_callback=reset,
                          auto_ack=True)

    # declaring its own input queue and bind it to the boat_data exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='boat_data',
                       queue=result.method.queue)

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)
    # wait for messages
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
