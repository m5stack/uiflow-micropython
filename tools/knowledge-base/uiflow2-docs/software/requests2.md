# :mod:`requests2` --- Network Request Module

<!-- .. include:: ../refs/software.requests2.ref -->

<!-- .. module:: requests2 -->
    :synopsis: Network Request Module

requests2 is based on urequests and supports Streaming Uploads and x-www-form-urlencoded.

The main functionality and function of the ``requests2`` module.

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import requests2

label0 = None
http_req = None

def setup():
    global label0, http_req

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 6, 6, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    http_req = requests2.get(
        "https://httpbin.org/get", headers={"Content-Type": "application/json"}
    )
    label0.setText(str(http_req.text))

def loop():
    global label0, http_req
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_http_get_example.m5f2|

## Function

<!-- .. function:: requests2.request(method, url, data=None, json=None, headers={}) -> Response -->

    Send a network request, it will block the response data returned to the network, parameters:

    :param str method: method of establishing a network request. e.g. ``HEAD``,``GET``,``POST``,``PUT``,``PATCH``, ``DELETE``.
    :param str url: URL of the network request.
    :param data: (optional), a dictionary, tuple list [(key, value)] (will be form coded), byte or class file object sent in the request body.
    :param json: (optional), json data sent in the request body.
    :param dict headers: (optional), HTTP header dictionary to be sent with the request.

<!-- .. function:: requests2.head(url, **kw) -> Response -->

    Send a ``HEAD`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

<!-- .. function:: requests2.get(url, **kw) -> Response -->

    Send a ``GET`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

<!-- .. function:: requests2.post(url, **kw) -> Response -->

    Send a ``POST`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

<!-- .. function:: requests2.put(url, **kw) -> Response -->

    Send a ``PUT`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

<!-- .. function:: requests2.patch(url, **kw) -> Response -->

    Send a ``PATCH`` request, the return type is the response of the request, parameters:

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

<!-- .. function:: requests2.delete(url, **kw) -> Response -->

    Send a ``DELETE`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

## class Response

## Methods

<!-- .. attribute:: Response.headers -->

    :type: dict

    Return the response header.

    UIFLOW2:

<!-- .. attribute:: Response.status_code -->

    :type: int

    Return the status code of the response.

    UIFLOW2:

<!-- .. method:: Response.close() -> None -->

    Close the connection and release resources.

    UIFLOW2:

<!-- .. property:: Response.content -->

    :type: dict

    Return the content of the response, in bytes.

    UIFLOW2:

<!-- .. property:: Response.text -->

    :type: str

    Return the content of the response, in str.

    UIFLOW2:

<!-- .. method:: Response.json() -> dict -->

    Return the content of the response, in dict.

    UIFLOW2:
