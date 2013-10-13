from twisted.application import service
from twisted.application.internet import TCPClient
from twisted.internet import task

from txCarbonClient.carbon_client_factory import CarbonClientFactory
from txCarbonClient.repeating_metric_handle import RepeatingMetricHandle


class CarbonClientService(service.MultiService):
    '''A Twisted service which makes recording metrics with Carbon easy.'''

    def __init__(self, reactor, hostname, port):
        '''Construct a CarbonClientService.

        Args:
            reactor: The Twisted reactor for your application.
            hostname: The hostname of your Carbon server.
            port: The port that the Carbon pickle endpoint is listening on.

        '''
        service.MultiService.__init__(self)
        self._reactor = reactor
        self._hostname = hostname
        self._port = port
        self._client_factory = None
        self._tcp_client = None

        self._repeating_metric_handles = []

    def publish_metric(self, metric_name, metric_value, epoch_seconds=None):
        '''Record a single hit on a given metric.

        Args:
            metric_name: The name of the metric to record with Carbon.
            metric_value: The value to record with Carbon.
            epoch_seconds: Optionally specify the time for the metric hit.

        Returns:
            None

        '''
        if epoch_seconds is None:
            epoch_seconds = self._reactor.seconds()
        self._client_factory.publish_metric(metric_name, metric_value, int(epoch_seconds))

    def register_repeating_metric(self, metric_name, frequency, getter):
        '''Record hits to a metric at a specified interval.

        Args:
            metric_name: The name of the metric to record with Carbon.
            frequency: The frequency with which to poll the getter and record the value with Carbon.
            getter: A function which takes no arguments and returns the value to record with Carbon.

        Returns:
            RepeatingMetricHandle instance. Call .stop() on it to stop recording the metric.

        '''
        l = task.LoopingCall(self._publish_repeating_metric, metric_name, getter)
        repeating_metric_handle = RepeatingMetricHandle(l, frequency)
        self._repeating_metric_handles.append(repeating_metric_handle)
        if self.running:
            repeating_metric_handle.start()
        return repeating_metric_handle

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

    def _publish_repeating_metric(self, metric_name, getter):
        self.publish_metric(metric_name, getter())
