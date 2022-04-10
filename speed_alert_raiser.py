#!/usr/bin/env python
import sys
import os

import pika
import json

agg_speed = 0
nb_signals = 0


def callback(ch, method, properties, body):
    """Defining what to do when a message is received"""

    global agg_speed
    global nb_signals
    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    agg_speed = agg_speed + body_json["boat_speed"]
    nb_signals = nb_signals + 1
    avg_speed = agg_speed/nb_signals
    print(" [x] Avg speed: " + str(avg_speed))

    # TO BE COMPLETED
    if avg_speed >= 10 and nb_signals % 5 == 0:
        ch.basic_publish(exchange='',
                         routing_key='alert_stream',
                         body=str(avg_speed))


def main():
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='alert_stream')

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
