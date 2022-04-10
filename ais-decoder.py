#!/usr/bin/env python3
import sys
import os

import pika
import json

from enum import Enum


class BoatType(Enum):
    TANKER = 0
    CARGO = 1
    PASSENGER = 2
    FISHING = 3


class Port(Enum):
    BREST = 0
    VALENCIA = 1
    PALERMO = 2
    BRIGHTON = 3
    AMSTERDAM = 4
    ODESSA = 5
    PORTO = 6
    HELSINKY = 7


class BoatSignal:

    def __init__(self, signal):

        id_signal = signal[0:7]
        self.boat_id = int(id_signal, 2)
        print("ID:" + str(self.boat_id))

        type_signal = signal[7:9]
        self.boat_type = BoatType(int(type_signal, 2)).name
        print("type:" + str(self.boat_type))

        # TO BE COMPLETED
        speed_signal = signal[9:14]
        self.boat_speed = int(speed_signal, 2)
        print("speed:" + str(self.boat_speed))

        dest_signal = signal[14:17]
        self.boat_dest = Port(int(dest_signal, 2)).name
        print("destination:" + str(self.boat_dest))

    def getBoatId(self):
        return self.boat_id

    def getType(self):
        return self.boat_type

    # TO BE MODIFIED
    def getSpeed(self):
        return self.boat_speed

    # TO BE MODIFIED
    def getDest(self):
        return self.boat_dest

    def toDict(self):
        d = {}
        d["boat_id"] = self.getBoatId()
        d["boat_type"] = self.getType()
        d["boat_destination"] = self.getDest()
        d["boat_speed"] = self.getSpeed()

        return d


def callback(ch, method, properties, body):
    """Defining what to do when a message is received"""

    print(" [x] Received signal %r" % body)
    # decoding signal into a human readable boat signal
    bs = BoatSignal(body)

    # publishing the message to following queues
    ch.basic_publish(exchange='boat_data',
                     routing_key='',
                     body=str(bs.toDict()))


def main():
    # credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    # parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='ais_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='ais_stream',
                          auto_ack=True,
                          on_message_callback=callback)

    channel.exchange_declare(exchange='boat_data',
                             exchange_type='fanout')

    # wait for messages
    print(' [*] Waiting for AIS signals. To exit press CTRL+C')
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
