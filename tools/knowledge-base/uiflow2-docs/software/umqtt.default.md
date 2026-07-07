<!-- .. py:currentmodule:: umqtt -->

# umqtt.default

<!-- .. include:: ../refs/software.umqtt.default.ref -->

`umqtt.default` rewrites the :py:meth:`subscribe` method and supports ca file.

## UiFlow2 Example

#### MQTT basic

Open the |cores3_mqtt_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to connect to an MQTT broker.

UiFlow2 Code Block:

Example output:

    None

#### MQTT over SSL

Open the |cores3_mqtt_over_ssl_example.m5f2| project in UiFlow2.

This example demonstrates how to connect to an MQTT broker over SSL.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### MQTT basic

This example demonstrates how to connect to an MQTT broker.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from umqtt import MQTTClient

page0 = None
label0 = None
button0 = None
textarea0 = None
label1 = None
textarea1 = None
label2 = None
keyboard0 = None
mqtt_client = None

def button0_short_clicked_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    mqtt_client.publish("testtopic/test", textarea0.get_text(), qos=0)

def mqtt_testtopic_test_event(data):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    textarea1.set_text(str(data[1]))

def textarea0_focused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)

def textarea0_defocused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)

def button0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def textarea0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return

def setup():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=52,
        y=32,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea1",
        placeholder="Placeholder...",
        x=10,
        y=132,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "pubish topic: testtopic/test",
        x=10,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="publish",
        x=217,
        y=32,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "subscribe topic: testtopic/test",
        x=11,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "msg:",
        x=10,
        y=32,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.set_flag(lv.obj.FLAG.SCROLLABLE, True)
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)
    page0.screen_load()
    mqtt_client = MQTTClient(
        "uiflow", "broker.emqx.io", port=1883, user="test", password="test", keepalive=0
    )
    mqtt_client.connect(clean_session=True)
    mqtt_client.subscribe("testtopic/test", mqtt_testtopic_test_event, qos=0)

def loop():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    M5.update()
    mqtt_client.check_msg()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

#### MQTT over SSL

This example demonstrates how to connect to an MQTT broker over SSL.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from umqtt import MQTTClient

page0 = None
label0 = None
button0 = None
textarea0 = None
label1 = None
textarea1 = None
label2 = None
keyboard0 = None
mqtt_client = None

def button0_short_clicked_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    mqtt_client.publish("testtopic/test", textarea0.get_text(), qos=0)

def mqtt_testtopic_test_event(data):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    textarea1.set_text(str(data[1]))

def textarea0_focused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)

def textarea0_defocused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)

def button0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def textarea0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return

def setup():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=52,
        y=32,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea1",
        placeholder="Placeholder...",
        x=10,
        y=132,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "pubish topic: testtopic/test",
        x=10,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="publish",
        x=217,
        y=32,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "subscribe topic: testtopic/test",
        x=11,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "msg:",
        x=10,
        y=32,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.set_flag(lv.obj.FLAG.SCROLLABLE, True)
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)
    page0.screen_load()
    mqtt_client = MQTTClient(
        "uiflow",
        "y90166f4.ala.cn-hangzhou.emqxsl.cn",
        port=8883,
        user="test",
        password="test",
        keepalive=0,
        ssl=True,
        ssl_params={
            "cafile": "/flash/certificate/emqxsl-ca.crt",
            "server_hostname": "y90166f4.ala.cn-hangzhou.emqxsl.cn",
        },
    )
    mqtt_client.connect(clean_session=True)
    mqtt_client.subscribe("testtopic/test", mqtt_testtopic_test_event, qos=0)

def loop():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    M5.update()
    mqtt_client.check_msg()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### MQTTClient

<!-- .. class:: MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={}) -->

    Create an MQTTClient object.

    :param str client_id: the unique client id string used when connecting to
                          the broker.
    :param str server: the hostname or IP address of the remote broker.
    :param int port: the network port of the server host to connect to.
    :param user: a username for broker authentication.
    :type user: str or None
    :param password: a password for broker authentication.
    :type password: str or None
    :param int keepalive: maximum period in seconds allowed between
                          communications with the broker. If no other messages
                          are being exchanged, this controls the rate at which
                          the client will send ping messages to the broker.
    :param bool ssl: Whether to use ssl.
    :param dict ssl_params: Some parameters required to initiate an ssl connection.
    :return: MQTTClient object
    :rtype: MQTTClient

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from umqtt import MQTTClient

            mqtt_client = MQTTClient(
                'uf2',
                'y90166f4.ala.cn-hangzhou.emqxsl.cn',
                port=8883,
                user='test',
                password='test',
                keepalive=0,
                ssl=True,
                ssl_params={
                    "server_hostname":'y90166f4.ala.cn-hangzhou.emqxsl.cn',
                    "key": "/flash/certificate/emqxsl-ca.crt", # 私钥文件，双向认证的时候使用
                    "cert": "/flash/certificate/emqxsl-ca.crt", # 客户端证书文件，双向认证的时候使用
                    "cafile": "/flash/certificate/emqxsl-ca.crt", # CA证书，单向认证的时候使用
                }
            )

<!-- .. method:: MQTTClient.connect(clean_session=True) -> bool -->

        Connect to a server. Returns True if this connection uses persisten
        session stored on a server (this will be always False if clean_session=True
        argument is used (default)).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.connect(clean_session=True)

<!-- .. method:: MQTTClient.disconnect() -> None -->

        Disconnect from a server, release resources.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.disconnect()

<!-- .. method:: MQTTClient.reconnect() -> None -->

        Disconnect from a server, release resources.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.reconnect()

<!-- .. method:: MQTTClient.ping() -> None -->

        Ping server (response is processed automatically by :py:meth:`wait_msg()`).

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.ping()

<!-- .. method:: MQTTClient.publish(topic, msg, retain=False, qos=0) -> None -->

        Publish a message.

        :param topic: the topic that the message should be published on.
        :type topic: str or bytes or bytearray
        :param msg: the message to send as a will.
        :type msg: str or bytes or bytearray
        :param bool retain: if set to True, the will message will be set as
                            the "last will"/retained message for the topic.
        :param int qos: the quality of service level to use

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.publish(topic, msg, retain=False, qos=0)

<!-- .. method:: MQTTClient.subscribe(topic, handler, qos=0) -> None -->

        Subscribe to a topic.

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str or bytes or bytearray
        :param function handler: called when a message has been received on a topic
                                that the client subscribes to and the message does
                                match an existing topic filter callback.
        :param int qos: the desired quality of service level for the subscription.
                        Defaults to 0.

        UiFlow2 Code Block:

        An handler showing a message has been received::

            def on_sub_cb(data):
                print("topic:", data[0])
                print("msg:", data[1])

        On uiflow2, you can get the **topic** and **message** of the current handler
        through  and .

<!-- .. method:: MQTTClient.unsubscribe(topic) -> None -->

        Unsubscribe from a topic.

        :param topic: a string specifying the subscription topic to unsubscribe from.
        :type topic: str or bytes or bytearray

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.unsubscribe(topic)

<!-- .. method:: MQTTClient.set_last_will(topic, msg, retain=False, qos=0) -> None -->

<!-- .. important:: -->

            Should be called before :py:meth:`connect()`.

        Set MQTT "last will" message.

        :param topic: the topic that the will message should be published on.
        :type topic: str or bytes or bytearray
        :param msg: the message to send as a will. If not given, or set to None a
                    zero length message will be used as the will.
        :type msg: str or bytes or bytearray
        :param bool retain: if set to True, the will message will be set as
                            the "last will"/retained message for the topic.
        :param int qos: the quality of service level to use for the will.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.set_last_will()

<!-- .. method:: MQTTClient.wait_msg() -> None -->

<!-- .. important:: -->

            :py:meth:`wait_msg()` and :py:meth:`check_msg()` are "main loop iteration"
            methods, blocking and non-blocking version. They should be called
            periodically in a loop, :py:meth:`wait_msg()` if you don't have any
            other foreground tasks to perform (i.e. your app just reacts to
            subscribed MQTT messages), :py:meth:`check_msg()` if you process other
            foreground tasks too.

            Note that you don't need to call :py:meth:`wait_msg()` /
            :py:meth:`check_msg()` if you only publish messages, never subscribe
            to them.

        Wait for a server message.

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.wait_msg()

<!-- .. method:: MQTTClient.check_msg(attempts=2) -> None -->

        Check if there's pending message from server. If yes, process the same way
        as :py:meth:`wait_msg()`, if not, return immediately.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mqtt_client.check_msg()
