#!/usr/bin/env python

import unittest

from proton_binding.Options import Options
from proton_binding.BroadcastReceiver import BroadcastReceiver
from pure_python.RequestResponse import RequestResponse

from utils.Responder import Responder
from utils.Broadcaster import Broadcaster


class ProtonTests(unittest.TestCase):
    def setUp(self):
        hostname = "ecag-fixml-dev1"
        port = 35671
        accountName = "ABCFR_ABCFRALMMACC1"
        accountPrivateKey = "./tests/resources/ABCFR_ABCFRALMMACC1.pem"
        accountPublicKey = "./tests/resources/ABCFR_ABCFRALMMACC1.crt"
        brokerPublicKey = "./tests/resources/ecag-fixml-dev1.crt"
        self.options = Options(hostname, port, accountName, accountPublicKey, accountPrivateKey, brokerPublicKey)

    def test_broadcastReceiver(self):
        broadcaster = Broadcaster(self.options.hostname, 35672, "admin", "admin", "broadcast", "broadcast.ABCFR.TradeConfirmation", 1)
        broadcaster.run()

        br = BroadcastReceiver(self.options)
        br.run()

        self.assertGreaterEqual(br.message_counter, 1)

#    def test_requestResponse(self):
#        responder = Responder(self.options.hostname, 35672, "admin", "admin", "request_be.ABCFR_ABCFRALMMACC1", 5)
        #responder.start()
        #
        #rr = RequestResponse(self.options)
        #rr.run()
        #
        #self.assertGreaterEqual(rr.message_counter, 1)

if __name__ == '__main__':
    unittest.main()