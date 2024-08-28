:mod:`requests2` --- Network Request Module
===========================================

.. include:: ../refs/software.requests2.ref

.. module:: requests2
    :synopsis: Network Request Module

requests2 is based on urequests and supports Streaming Uploads and x-www-form-urlencoded.

The main functionality and function of the ``requests2`` module.


Micropython Example:

    .. literalinclude:: ../../../examples/softwave/http/cores3_http_get_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_http_get_example.m5f2|


Function
--------

.. function:: requests2.request(method, url, data=None, json=None, headers={}) -> Response

    Send a network request, it will block the response data returned to the network, parameters:

    :param str method: method of establishing a network request. e.g. ``HEAD``,``GET``,``POST``,``PUT``,``PATCH``, ``DELETE``.
    :param str url: URL of the network request.
    :param data: (optional), a dictionary, tuple list [(key, value)] (will be form coded), byte or class file object sent in the request body.
    :param json: (optional), json data sent in the request body.
    :param dict headers: (optional), HTTP header dictionary to be sent with the request.


.. function:: requests2.head(url, **kw) -> Response

    Send a ``HEAD`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.


.. function:: requests2.get(url, **kw) -> Response

    Send a ``GET`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

        |get.png|


.. function:: requests2.post(url, **kw) -> Response

    Send a ``POST`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

        |post.png|

.. function:: requests2.put(url, **kw) -> Response

    Send a ``PUT`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

        |put.png|

.. function:: requests2.patch(url, **kw) -> Response

    Send a ``PATCH`` request, the return type is the response of the request, parameters:

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

        |patch.png|


.. function:: requests2.delete(url, **kw) -> Response

    Send a ``DELETE`` request, the return type is the response of the request, parameters：

    :param str url: URL of the network request.
    :param kw: request optional parameters.

    UIFLOW2:

        |delete.png|


class Response
--------------

Methods
-------

.. attribute:: Response.headers

    :type: dict

    Return the response header.

    UIFLOW2:

        |headers.png|


.. attribute:: Response.status_code

    :type: int

    Return the status code of the response.

    UIFLOW2:

        |status_code.png|


.. method:: Response.close() -> None

    Close the connection and release resources.

    UIFLOW2:

        |close.png|


.. property:: Response.content

    :type: dict

    Return the content of the response, in bytes.

    UIFLOW2:

        |content.png|


.. property:: Response.text

    :type: str

    Return the content of the response, in str.

    UIFLOW2:

        |text.png|


.. method:: Response.json() -> dict

    Return the content of the response, in dict.

    UIFLOW2:

        |json.png|

