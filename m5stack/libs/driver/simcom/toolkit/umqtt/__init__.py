# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import robust
from micropython import schedule


class MQTTClient(robust.MQTTClient):
    def __init__(
        self,
        modem,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=False,
        ssl_params={},
    ):
        ssl_params1 = ssl_params
        if ssl:
            pass
            key_path = ssl_params1.get("key", None)
            key_value = self._load_file(key_path)
            if key_value:
                ssl_params1["key"] = key_value

            cert_path = ssl_params1.get("cert", None)
            cert_value = self._load_file(cert_path)
            if cert_value:
                ssl_params1["cert"] = cert_value

        super().__init__(
            modem, client_id, server, port, user, password, keepalive, ssl, ssl_params1
        )
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

    @staticmethod
    def _load_file(path):
        if isinstance(path, str) and path.startswith("/flash"):
            try:
                with open(path, "r") as f:
                    return f.read()
            except:
                return None
        else:
            return None
