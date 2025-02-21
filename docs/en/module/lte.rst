COMX LTE Module
===============

.. sku: M031-A

.. include:: ../refs/module.lte.ref

LTEModule Class provides a set of methods to control the LTE module. Through the
chat script of AT commands, the module is set to PPP mode and then the data is
sent to the Internet through the serial port.

Support the following products:

    |COMX LTE|


UiFlow2 Example
---------------

HTTP GET over LTE
^^^^^^^^^^^^^^^^^

Open the |core2_lte_http_example.m5f2| project in UiFlow2.

This example demonstrates how to use PPP dial-up on the LTE module and then use
the `requests2` library to send an HTTP GET request.

UiFlow2 Code Block:

    |example_http.png|

Example output:

    None


Chat script
^^^^^^^^^^^

Open the |core2_lte_chat_example.m5f2| project in UiFlow2.

Set the LTE module to PPP mode through a custom AT command chat script.

UiFlow2 Code Block:

    |example_chat.png|

Example output:

    None

MicroPython Example
-------------------

HTTP GET over LTE
^^^^^^^^^^^^^^^^^

This example demonstrates how to use PPP dial-up on the LTE module and then use
the `requests2` library to send an HTTP GET request.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/lte/core2_lte_http_example.py
        :language: python
        :linenos:

Example output:

    None

Chat script
^^^^^^^^^^^

Set the LTE module to PPP mode through a custom AT command chat script.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/lte/core2_lte_chat_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

LTEModule
^^^^^^^^^

.. autoclass:: module.lte.LTEModule
    :members:

    .. py:method:: active([is_active])

        Activate (“up”) or deactivate (“down”) the network interface, if a
        boolean argument is passed. Otherwise, query current state if no
        argument is provided.

        :param bool is_active: If True, the LTE module is enabled, if False, the LTE module is disabled.

        :return: Returns the activation status of the LTE module.
        :rtype: bool

        UiFlow2 Code Block:

            |active.png|

        MicroPython Code Block:

            .. code-block:: python

                comlte_0.active(True)
                comlte_0.active(False)
                comlte_0.active()


    .. py:method:: connect(authmode=AUTH_NONE, username="", password="")

        Initiate a PPP connection with the given parameters.

        :param int authmode: Authentication Mode, either LTEModule.AUTH_NONE, LTEModule.AUTH_PAP, or LTEModule.AUTH_CHAP.
        :param str username: An optional user name to use with the authentication mode.
        :param str password: An optional password to use with the authentication mode.

        :return: None

        UiFlow2 Code Block:

            |connect.png|

        MicroPython Code Block:

            .. code-block:: python

                comlte_0.connect(authmode=AUTH_NONE, username="", password="")
                comlte_0.connect()


    .. py:method:: isconnected()

        Returns True if the PPP link is connected and up. Returns False otherwise.

        :return: True if the PPP link is connected and up, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |isconnected.png|

        MicroPython Code Block:

            .. code-block:: python

                comlte_0.isconnected()

    .. py:method:: ifconfig()

        Get IP-level network interface parameters: IP address, subnet mask,
        gateway and DNS server. This method returns a 4-tuple with the above
        information.

        :return: A 4-tuple with IP address, subnet mask, gateway and DNS server.

        UiFlow2 Code Block:

            |get_localip.png|

            |get_subnet.png|

            |get_gateway.png|

            |get_dns.png|

        MicroPython Code Block:

            .. code-block:: python

                comlte_0.ifconfig()
                comlte_0.ifconfig()[0] # IP address
                comlte_0.ifconfig()[1] # network
                comlte_0.ifconfig()[2] # gateway
                comlte_0.ifconfig()[3] # DNS server
