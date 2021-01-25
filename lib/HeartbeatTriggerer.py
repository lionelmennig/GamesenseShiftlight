from threading import Thread
from queue import Queue
import time
from gamesense_shiftlight.lib import requests
import json

class HeartbeatTriggerer(Thread):
    def __init__(self, keepaliveTimeout, urlToKeepalive, eventHeartbeat, headers):
        Thread.__init__(self)
        self.keepaliveTimeout = keepaliveTimeout
        self.urlToKeepalive = urlToKeepalive
        self.eventHeartbeat = eventHeartbeat
        self.headers = headers

    def run(self):
        while True:
            time.sleep(self.keepaliveTimeout)
            requests.post(self.urlToKeepalive, data = json.dumps(self.eventHeartbeat), headers = self.headers)
