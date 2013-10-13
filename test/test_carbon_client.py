import math

from twisted.application import service
from twisted.internet import reactor

from txCarbonClient import CarbonClientService


carbon_client_service = CarbonClientService(reactor, 'localhost', 2004)

value = 0

def test_metric_getter():
    global value
    value += 0.1
    return (math.sin(value) * 0.5) + 0.5

carbon_client_service.register_repeating_metric('metric.test.sin', 1, test_metric_getter)

application = service.Application("Testing")

carbon_client_service.setServiceParent(application)
