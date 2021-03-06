#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import threading
from time import sleep

from proton import SSLDomain
from proton.handlers import MessagingHandler
from proton.reactor import Container

from Options import Options

class Receiver(MessagingHandler):
    def __init__(self, opts):
        super(Receiver, self).__init__(prefetch=1000, auto_accept=False, peer_close_is_error=True)
        self.options = opts
        self.address = "amqps://" + self.options.hostname + ":" + str(self.options.port)
        self.broadcast_address = "broadcast." + self.options.accountName + ".TradeConfirmation"
        self.message_counter = 0

    def on_start(self, event):
        self.container = event.container

        ssl = SSLDomain(SSLDomain.MODE_CLIENT)
        ssl.set_credentials(str(self.options.accountPublicKey), str(self.options.accountPrivateKey), str(""))
        ssl.set_trusted_ca_db(str(self.options.brokerPublicKey))
        ssl.set_peer_authentication(SSLDomain.VERIFY_PEER_NAME, trusted_CAs=str(self.options.brokerPublicKey))

        conn = event.container.connect(self.address, ssl_domain=ssl, heartbeat=60000, allowed_mechs=str("EXTERNAL"))
        event.container.create_receiver(conn, self.broadcast_address)

    def on_message(self, event):
        print("-I- Received broadcast message: " + event.message.body)
        self.message_counter += 1
        self.accept(event.delivery)

    def on_stop(self, event):
        event.connection.close()

class BroadcastReceiver:
    def __init__(self, options):
        self.options = options
        self.message_counter = 0

    def run(self):
        receiver = Receiver(self.options)
        reactor = Container(receiver)

        thread = threading.Thread(target=reactor.run)
        thread.daemon = True
        thread.start()

        sleep(self.options.timeout)

        self.message_counter = receiver.message_counter
        print("-I- Received in total " + str(self.message_counter) + " messages")

if __name__ == "__main__":
    hostname = "ecag-fixml-simu1.deutsche-boerse.com"
    port = 10170
    accountName = "ABCFR_ABCFRALMMACC1"
    accountPrivateKey = "ABCFR_ABCFRALMMACC1.pem"
    accountPublicKey = "ABCFR_ABCFRALMMACC1.crt"
    brokerPublicKey = "ecag-fixml-simu1.deutsche-boerse.com.crt"
    timeout = 10

    opts = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey, timeout)
    br = BroadcastReceiver(opts)
    br.run()

