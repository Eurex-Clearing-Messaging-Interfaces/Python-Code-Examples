#! /usr/bin/python

from Options import Options
from qpid_messaging import *

class RequestResponse:
    def __init__(self, options):
        self.options = options
        self.request_address = "request." + self.options.accountName + "/request; " \
                               "{ node: { type: topic }, create: never }"
        self.reply_adress = "response/response." + self.options.accountName + ".response_queue_1; " \
                            "{ create: receiver, node: { type: topic } }"
        self.response_address = "response." + self.options.accountName + ".response_queue_1; {create: receiver, " \
                                "assert: never, node: { type: queue, x-declare: { auto-delete: true, exclusive: false, " \
                                "arguments: {'qpid.policy_type': ring, 'qpid.max_count': 1000, 'qpid.max_size': 1000000}}, " \
                                "x-bindings: [{exchange: 'response', queue: 'response." + self.options.accountName + ".response_queue_1', " \
                                "key: 'response." + self.options.accountName + ".response_queue_1'}]}}";
        self.message_counter = 0

    def run(self):
        try:
            connection = Connection("amqp:ssl:" + self.options.hostname + ":" + str(self.options.port))
            connection.setOption("sasl_mechanisms", "EXTERNAL")
            connection.setOption("transport", "ssl")
            connection.setOption("heartbeat", 60)
            connection.open()
            session = connection.session()
            receiver = session.receiver(self.response_address)
            sender = session.sender(self.request_address)

            message = Message("<FIXML>...</FIXML>", durable=False, reply_to=self.reply_adress)
            sender.send(message, sync=True);

            try:
                message = receiver.fetch(timeout=self.options.timeout)
                session.acknowledge(sync=False)

                print "-I- Response received with content: ", message.content
                self.message_counter = 1
            except Empty:
                print "-I- No response received for ", self.options.timeout, " seconds"

            session.sync(timeout=None)

            sender.close()
            receiver.close()
            session.close()
            connection.close()
        except MessagingError, m:
            print "-E- Caught exception: ", m

if __name__ == "__main__":
    hostname = "ecag-fixml-simu1.deutsche-boerse.com"
    port = 10170
    accountName = "ABCFR_ABCFRALMMACC1"

    opts = Options(hostname, port, accountName)

    rr = RequestResponse(opts)
    rr.run()
