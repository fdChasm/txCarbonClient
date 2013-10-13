import struct

from twisted.internet import protocol

import cPickle as pickle


class CarbonClientProtocol(protocol.Protocol):
    def __init__(self, factory):
        self._factory = factory

    def connectionMade(self):
        protocol.Protocol.connectionMade(self)
        self.check_queued_metrics_to_send()

    def check_queued_metrics_to_send(self):
        metric_tuples = self._factory.get_metric_tuples()
        self._write_metric_tuples(metric_tuples)

    def _write_metric_tuples(self, metric_tuples):
        payload = pickle.dumps(metric_tuples)
        header = struct.pack("!L", len(payload))
        self.transport.write(header + payload)
