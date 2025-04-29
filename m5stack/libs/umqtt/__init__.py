# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import robust
from micropython import schedule


class MQTTClient(robust.MQTTClient):
    def __init__(
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=False,
        ssl_params={},
    ):
        super().__init__(client_id, server, port, user, password, keepalive, ssl, ssl_params)
        self.set_callback(self._callback)
        self._topics = {}

    def _callback(self, topic, msg):
        if isinstance(topic, bytes):
            handler = self._topics.get(topic.decode())
            if handler is None:
                handler = self._topics.get(topic)
        elif isinstance(topic, str):
            handler = self._topics.get(topic)
            if handler is None:
                handler = self._topics.get(topic.encode())

        if handler is not None:
            schedule(handler, (topic, msg))

    def subscribe(self, topic, handler, qos=0):
        self._topics[topic] = handler
        return super().subscribe(topic, qos)
