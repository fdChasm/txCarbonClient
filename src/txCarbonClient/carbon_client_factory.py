from twisted.internet.protocol import ReconnectingClientFactory

from txCarbonClient.carbon_client_protocol import CarbonClientProtocol


class CarbonClientFactory(ReconnectingClientFactory):
    def __init__(self):
        self._protocol_instance = None
        self._metrics_to_publish = []

    def buildProtocol(self, addr):
        self.resetDelay()
        self._protocol_instance = CarbonClientProtocol(self)
        return self._protocol_instance

    def publish_metric(self, metric_name, metric_value, epoch_seconds):
        self._metrics_to_publish.append((metric_name, (epoch_seconds, metric_value)))
        if self._protocol_instance is not None:
            self._protocol_instance.check_queued_metrics_to_send()

    def clientConnectionLost(self, connector, unused_reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)
        self._protocol_instance = None

    def get_metric_tuples(self):
        metric_tuples = self._metrics_to_publish
        self._metrics_to_publish = []
        return metric_tuples
