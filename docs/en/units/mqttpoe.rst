MQTTPoE Unit
============

.. include:: ../refs/unit.mqttpoe.ref

The ``MQTTPoE Unit`` is an Ethernet communication module specifically designed for MQTT communication. It features supports PoE power and embedded W5500 Ethernet chip, which enables seamless connectivity to Ethernet networks. The module also includes a UART communication interface, allowing for control via AT commands. In addition, it integrates an RJ45 adaptive 10/100M network port for easy network connectivity.

.. NOTE::

    The PoE version has integrated PoE power, with 1.2A@5V (6W) load capability.

Support the following products:

    |MqttPoeUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import MQTTPoEUnit
    import time

    def mqtt_0_SubTopic_event(data):
        global mqttpoe_0
        print(data[0])
        print(data[1])

    mqttpoe_0 = MQTTPoEUnit(port=(18, 17))

    mqttpoe_0.set_client('m5-mqtt-2024', 'mqtt.m5stack.com', 1883, '', '', 120)
    mqttpoe_0.set_subscribe('SubTopic', mqtt_0_SubTopic_event, 0)
    mqttpoe_0.set_connect()

    while True:
        mqttpoe_0.check_msg()
        time.sleep_ms(50)

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |mqttpoe_demo.m5f2|


class MQTTPoEUnit
-----------------

Constructors
------------

.. class:: MQTTPoEUnit(port=(,))

    Create a MQTTPoEUnit object

    The parameters is:
        - ``port`` uart pin tuple, which contains: ``(tx_pin, rx_pin)``.
    
    UIFLOW2:

        |init.png|


Methods
-------

.. method:: MQTTPoEUnit.set_client(client_id, server, port=0, username=None, password=None, keepalive=0)

    :param str client_id: the unique client id string used when connecting to
                          the broker.
    :param str server: the hostname or IP address of the remote broker.
    :param int port: the network port of the server host to connect to.
    :param username: a username for broker authentication.
    :type username: str or None
    :param password: a password for broker authentication.
    :type password: str or None
    :param int keepalive: maximum period in seconds allowed between
                          communications with the broker. If no other messages
                          are being exchanged, this controls the rate at which
                          the client will send ping messages to the broker.

    UIFLOW2:

        |set_client.png|


.. method:: MQTTPoEUnit.set_connect()

    Connect to a server.

    UIFLOW2:

        |set_connect.png|

.. method:: MQTTPoEUnit.set_disconnect()

    Disconnect from a server, release resources.

    UIFLOW2:

        |set_disconnect.png|


.. method:: MQTTPoEUnit.set_publish(topic, msg, qos=0)

    Publish a message.

    :param topic: the topic that the message should be published on.
    :type topic: str or bytes or bytearray
    :param msg: the message to send as a will.
    :type msg: str or bytes or bytearray
    :param int qos: the quality of service level to use

    UIFLOW2:

        |set_publish.png|


.. method:: MQTTPoEUnit.set_subscribe(topic, handler, qos=0)

    Subscribe to a topic.

    :param topic: a string specifying the subscription topic to subscribe to.
    :type topic: str or bytes or bytearray
    :param function handler: called when a message has been received on a topic
                             that the client subscribes to and the message does
                             match an existing topic filter callback.
    :param int qos: the desired quality of service level for the subscription.
                    Defaults to 0.

    .. NOTE:: 1. When using this block, the "MQTT connect" block must be set after this block
              2. The server can only subscribe to four topics at a time

    UIFLOW2:

        |set_subscribe.png|

    An handler showing a message has been received::

        def mqtt_0_SubTopic_event(data):
            print("topic:", data[0])
            print("msg:", data[1])

    On uiflow2, you can get the **topic** and **message** of the current handler
    through |get_topic.png| and |get_msg.png|.


.. method:: MQTTPoEUnit.check_msg() 

    .. important::

        :py:meth:`check_msg()` is "main loop iteration"
        methods, blocking and non-blocking version. They should be called
        periodically in a loop, :py:meth:`check_msg()` if you don't have any
        other foreground tasks to perform (i.e. your app just reacts to
        subscribed MQTT messages).

        Note that you don't need to call :py:meth:`check_msg()` if you only 
        publish messages.

    check for a server message.

    UIFLOW2:

        |check_msg.png|


.. method:: MQTTPoEUnit.check_modem_is_ready()

    To check whether the communication with the MQTT unit has been successful. 

    - Return: ``bool``:  True or False

    UIFLOW2:

        |modem_is_ready.png|


.. method:: MQTTPoEUnit.get_firmware_version()

    Get the current firmware version number. 

    - Return: ``string``   

    UIFLOW2:

        |get_firmware_version.png|


.. method:: MQTTPoEUnit.get_baudrate()

    Get the current baud rate of the module and the default baud rate is 9600. 

    - Return: ``int``:  4800, 9600, 19200, 34800, 115200, 230400

    UIFLOW2:

        |get_baudrate.png|


.. method:: MQTTPoEUnit.get_network_status()

    To check whether the network status is connected or disconnected. 

    - Return: ``int``: 0 ~ 1

    UIFLOW2:

        |get_network_status.png|


.. method:: MQTTPoEUnit.get_network_parameters(param)

    Get the current actual IP address, subnet mask, gateway and DNS server of the module. 
    
    The parameters is:
        - ``param``: IP address = 0, subnet mask = 1, gateway = 2, DNS server = 3.
    
    UIFLOW2:

        |get_network_parameters.png|


.. method:: MQTTPoEUnit.get_mac_address()

    Get the current MAC address of the module and MAC address the format is: XX-XX-XX-XX-XX-XX. 

    - Return: ``string``: "XX-XX-XX-XX-XX-XX"

    UIFLOW2:

        |get_mac_address.png|


.. method:: MQTTPoEUnit.get_static_ip(param)

    Get the current actual IP address, subnet mask and gateway of the module. 
    
    The parameters is:
        - ``param``: IP address = 0, subnet mask = 1, gateway = 2, DNS server = 3.
    
    UIFLOW2:

        |get_static_ip.png|


.. method:: MQTTPoEUnit.get_dhcp_status()

    Get the inquire about enable/disable DHCP status 
    
    - Return: ``int``: 1: Enable, 0: Disable
    
    UIFLOW2:

        |get_dhcp_status.png|

    
.. method:: MQTTPoEUnit.set_dhcp_state(state)

    Set the enable/disable DHCP 
    
    The parameters is:
        - ``state``: Disable = 0, Enable = 1.

    UIFLOW2:

        |set_dhcp_state.png|


.. method:: MQTTPoEUnit.set_static_ip(ip, subnet, gateway)

    Set the static IP address of the MQTT module.
    
    .. NOTE:: When the DHCP function is enabled, the static IP setting will not be enabled.

    The parameters is:
        - ``ip``:  "xxx.xxx.xxx.xxx"
        - ``subnet``:  "xxx.xxx.xxx.xxx"
        - ``gateway``:  "xxx.xxx.xxx.xxx"

    UIFLOW2:

        |set_static_ip.png|
        