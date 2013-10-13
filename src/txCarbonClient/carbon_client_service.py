from twisted.application import service
from twisted.application.internet import TCPClient
from twisted.internet import task

from txCarbonClient.carbon_client_factory import CarbonClientFactory
from txCarbonClient.repeating_metric_handle import RepeatingMetricHandle


class CarbonClientService(service.MultiService):
    def __init__(self, reactor, hostname, port):
        service.MultiService.__init__(self)
        self._reactor = reactor
        self._hostname = hostname
        self._port = port
        self._client_factory = None
        self._tcp_client = None

        self._repeating_metric_handles = []

    def startService(self):
        self._client_factory = CarbonClientFactory()
        self._tcp_client = TCPClient(self._hostname, self._port, self._client_factory, reactor=self._reactor)
        self._tcp_client.setServiceParent(self)
        for repeating_metric_handle in self._repeating_metric_handles:
            repeating_metric_handle.start()
        service.MultiService.startService(self)

    def stopService(self):
        for repeating_metric_handle in self._repeating_metric_handles:
            repeating_metric_handle.stop()
        return service.MultiService.stopService(self)

    def publish_metric(self, metric_name, metric_value):
        epoch_seconds = int(self._reactor.seconds())
        self._client_factory.publish_metric(metric_name, metric_value, epoch_seconds)

    def register_repeating_metric(self, metric_name, frequency, getter):
        l = task.LoopingCall(self._publish_repeating_metric, metric_name, getter)
        repeating_metric_handle = RepeatingMetricHandle(l, frequency)
        self._repeating_metric_handles.append(repeating_metric_handle)
        if self.running:
            repeating_metric_handle.start()
        return repeating_metric_handle

    def _publish_repeating_metric(self, metric_name, getter):
        self.publish_metric(metric_name, getter())
