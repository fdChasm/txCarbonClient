txCarbonClient
==============

A simple Twisted client for reporting metrics to Carbon.


installation
--------------

```shell
pip install txCarbonClient
```

Or get the latest development version.

```shell
pip install git+git://github.com/fdChasm/txCarbonClient.git
```


use
--------------

Simply add create an instance of the CarbonClientService and add it to your
Twisted application service hierarchy.

```python

from twisted.application import service
from twisted.internet import reactor

from txCarbonClient import CarbonClientService


carbon_client_service = CarbonClientService(reactor, 'localhost', 2004)

application = service.Application("Testing")

carbon_client_service.setServiceParent(application)

```

Then you can record metric hits easily in your application.

```python

carbon_client_service.publish_metric('metric.test.irregular', .75)

carbon_client_service.publish_metric('metric.test.irregular', .75, epoch_seconds=time.time())

```

You can also setup a metric to record the result of a getter on a regular basis.

```python

value = 0

def test_metric_sin_getter():
    global value
    value += 0.1
    return (math.sin(value) * 0.5) + 0.5

carbon_client_service.register_repeating_metric('metric.test.sin', 1, test_metric_sin_getter)

```
