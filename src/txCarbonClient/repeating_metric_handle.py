class RepeatingMetricHandle(object):
    def __init__(self, looping_call_handle, frequency):
        self._looping_call_handle = looping_call_handle
        self._frequency = frequency

        self._started = False
        self._stopped = False

    def start(self):
        if self._started: return
        self._looping_call_handle.start(self._frequency)
        self._started = True

    def stop(self):
        if self._stopped: return
        self._looping_call_handle.stop()
        self._stopped = True
