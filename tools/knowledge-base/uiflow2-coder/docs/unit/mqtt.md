# MQTT Unit

The `MQTT Unit` is an Ethernet communication module specifically designed for MQTT communication. It features an embedded W5500 Ethernet chip, which enables seamless connectivity to Ethernet networks. The module also includes a UART communication interface, allowing for control via AT commands. In addition, it integrates an RJ45 adaptive 10/100M network port for easy network connectivity.

Support the following products:

    MqttUnit

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from unit import MQTTUnit
import time

def mqtt_0_SubTopic_event(data):
    global mqtt_0
    print(data[0])
    print(data[1])

mqtt_0 = MQTTUnit(port=(18, 17))

mqtt_0.set_client('m5-mqtt-2024', 'mqtt.m5stack.com', 1883, '', '', 120)
mqtt_0.set_subscribe('SubTopic', mqtt_0_SubTopic_event, 0)
mqtt_0.set_connect()

while True:
    mqtt_0.check_msg()
    time.sleep_ms(50)
```

## class MQTTUnit

## Constructors

### `class MQTTUnit(port=(,))`

    Create a MQTTUnit object

    The parameters is:
        - `port` uart pin tuple, which contains: `(tx_pin, rx_pin)`.

## Methods

### `MQTTUnit.set_client(client_id, server, port, username, password, keepalive)`

    - Parameter `client_id` (`str`): the unique client id string used when connecting to
                          the broker.
    - Parameter `server` (`str`): the hostname or IP address of the remote broker.
    - Parameter `port` (`int`): the network port of the server host to connect to.
    - Parameter `username`: a username for broker authentication.
    - Type of `username`: str or None
    - Parameter `password`: a password for broker authentication.
    - Type of `password`: str or None
    - Parameter `keepalive` (`int`): maximum period in seconds allowed between
                          communications with the broker. If no other messages
                          are being exchanged, this controls the rate at which
                          the client will send ping messages to the broker.

### `MQTTUnit.set_connect()`

    Connect to a server.

### `MQTTUnit.set_disconnect()`

    Disconnect from a server, release resources.

### `MQTTUnit.set_publish(topic, msg, qos=0)`

    Publish a message.

    - Parameter `topic`: the topic that the message should be published on.
    - Type of `topic`: str or bytes or bytearray
    - Parameter `msg`: the message to send as a will.
    - Type of `msg`: str or bytes or bytearray
    - Parameter `qos` (`int`): the quality of service level to use

### `MQTTUnit.set_subscribe(topic, handler, qos=0)`

    Subscribe to a topic.

    - Parameter `topic`: a string specifying the subscription topic to subscribe to.
    - Type of `topic`: str or bytes or bytearray
    - Parameter `handler` (`function`): called when a message has been received on a topic
                             that the client subscribes to and the message does
                             match an existing topic filter callback.
    - Parameter `qos` (`int`): the desired quality of service level for the subscription.
                    Defaults to 0.

> Note: 1. When using this block, the "MQTT connect" block must be set after this block
> 2. The server can only subscribe to four topics at a time

    An handler showing a message has been received:
```
def mqtt_0_SubTopic_event(data):
    print("topic:", data[0])
    print("msg:", data[1])
```
    On uiflow2, you can get the **topic** and **message** of the current handler
    through  and .

### `MQTTUnit.check_msg()`

> Important: methods, blocking and non-blocking version. They should be called
> periodically in a loop, :py`check_msg()` if you don't have any
> other foreground tasks to perform (i.e. your app just reacts to
> subscribed MQTT messages).
>
> Note that you don't need to call :py`check_msg()` if you only
> publish messages.
    check for a server message.

### `MQTTUnit.check_modem_is_ready()`

    To check whether the communication with the MQTT unit has been successful.

    - Return: `bool`:  True or False

### `MQTTUnit.get_firmware_version()`

    Get the current firmware version number.

    - Return: `string`

### `MQTTUnit.get_baudrate()`

    Get the current baud rate of the module and the default baud rate is 9600.

    - Return: `int`:  4800, 9600, 19200, 34800, 115200, 230400

### `MQTTUnit.get_network_status()`

    To check whether the network status is connected or disconnected.

    - Return: `int`: 0 ~ 1

### `MQTTUnit.get_network_parameters(param)`

    Get the current actual IP address, subnet mask, gateway and DNS server of the module.

    The parameters is:
        - `param`: IP address = 0, subnet mask = 1, gateway = 2, DNS server = 3.

### `MQTTUnit.get_mac_address()`

    Get the current MAC address of the module and MAC address the format is: XX-XX-XX-XX-XX-XX.

    - Return: `string`: "XX-XX-XX-XX-XX-XX"

### `MQTTUnit.get_static_ip(param)`

    Get the current actual IP address, subnet mask and gateway of the module.

    The parameters is:
        - `param`: IP address = 0, subnet mask = 1, gateway = 2, DNS server = 3.

### `MQTTUnit.get_dhcp_status()`

    Get the inquire about enable/disable DHCP status

    - Return: `int`: 1: Enable, 0: Disable

### `MQTTUnit.set_dhcp_state(state)`

    Set the enable/disable DHCP

    The parameters is:
        - `state`: Disable = 0, Enable = 1.

### `MQTTUnit.set_static_ip(ip, subnet, gateway)`

    Set the static IP address of the MQTT module.

> Note: When the DHCP function is enabled, the static IP setting will not be enabled.
    The parameters is:
        - `ip`:  "xxx.xxx.xxx.xxx"
        - `subnet`:  "xxx.xxx.xxx.xxx"
        - `gateway`:  "xxx.xxx.xxx.xxx"
