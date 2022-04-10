#!/usr/bin/env python3
import sys
import os

import pika


def callback(ch, method, properties, body):
    """Defining what to do when a message is received"""

    print(f" [x] Received {body}")
    avg_speed = float(body)
    # decoding bytes into string and formatting into JSON
    # body_str = body.decode('utf8').replace("'", '"')
    # body_json = json.loads(body_str)
    color = "Red" if avg_speed >= 20 else "Orange"
    print(f" [x] {color} alert !")


def main():
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='alert_stream')

    channel.basic_consume(queue='alert_stream',
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
