#!/usr/bin/env python

from Options import Options
from qpid.messaging import *


class Amqp10BroadcastReceiver:
    block_size = 100
    capacity = 1000

    def __init__(self, options):
        self.options = options
        self.broadcast_address = "broadcast." + self.options.accountName + ".TradeConfirmation; " \
                                 "{ node: { type: queue } , create: never , mode: consume , assert: never }"
        self.message_counter = 0

    def run(self):
        try:
            connection = Connection("amqp:ssl:" + self.options.hostname + ":" + str(self.options.port), protocol="amqp1.0")
            connection.setOption("sasl_mechanisms", "EXTERNAL")
            connection.setOption("transport", "ssl")
            connection.setOption("heartbeat", 60)

            connection.open()
            session = connection.session()
            receiver = session.receiver(self.broadcast_address)
            receiver.capacity = self.capacity

            while True:
                received_message = None

                try:
                    received_message = receiver.fetch(timeout=self.options.timeout)
                except Empty:
                    session.acknowledge(sync=True)
                    print "-I- No message received for ", self.options.timeout, " seconds"
                    break

                self.message_counter += 1
                print "-I- Received message containing: ", received_message.content

                if self.message_counter % self.block_size == 0:
                    session.acknowledge(sync=True)

            print "-I- ", self.message_counter, " messages received"

            receiver.close()
            session.close()
            connection.close()
        except MessagingError, m:
            print "-E- Caught exception: ", m
            raise m


if __name__ == "__main__":
    hostname = "ecag-fixml-simu1.deutsche-boerse.com"
    port = 10170
    accountName = "ABCFR_ABCFRALMMACC1"

    opts = Options(hostname, port, accountName)

    br = Amqp10BroadcastReceiver(opts)
    br.run()
