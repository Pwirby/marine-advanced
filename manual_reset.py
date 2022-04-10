#!/usr/bin/env python3
import sys
import os


def main():
    import pika
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='reset_stream')
    
    # send the message, through the exchange ''
    # which simply delivers to the queue having the key as name
    channel.basic_publish(exchange='',
                      routing_key='reset_stream',
                      body='')

    print(" [x] Reset signal sent to boat counter.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
