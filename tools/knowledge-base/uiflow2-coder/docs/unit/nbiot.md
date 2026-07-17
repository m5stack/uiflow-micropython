# NB-IoT Unit

The `NB-IOT Unit` is a wireless communication module suitable for global wide Cat-NB frequency band . It has a built-in SIM7020G communication module, uses serial communication (AT instruction set control).

Support the following products:

    Unit NBIoT       Unit NBIoT-CN

> Note: Please ensure that the device supports the NB-IoT frequency bands in your area before use.
> Note: Please ensure that the firmware version of SIM7020 is greater than or equal to **1752B12SIM7020C**.
>
>  can be used to check the firmware version.
## MicroPython Example

#### NBIoT HTTP Example

This example shows how to send HTTP request using the NBIoT Unit.

click **Send** button to send HTTP request. Response data will be printed in the textarea.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import NBIOTUnit

page0 = None
label0 = None
label1 = None
button0 = None
textarea0 = None
textarea1 = None
nbiot_0_http_req = None
nbiot_0 = None

def button0_short_clicked_event(event_struct):
    global page0, label0, label1, button0, textarea0, textarea1, nbiot_0_http_req, nbiot_0
    nbiot_0_http_req = nbiot_0.post(
        "http://httpbin.org/post",
        json={"message": "Hello from M5Stack!", "status": "active"},
        headers={
            "Content-Type": "application/json",
            "Custom-Header": "MyHeaderValue",
        },
    )
    textarea1.set_text(str(nbiot_0_http_req.text))

def button0_event_handler(event_struct):
    global page0, label0, label1, button0, textarea0, textarea1, nbiot_0_http_req, nbiot_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def setup():
    global page0, label0, label1, button0, textarea0, textarea1, nbiot_0_http_req, nbiot_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="http://httpbin.org/post",
        placeholder="Placeholder...",
        x=46,
        y=10,
        w=195,
        h=21,
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
        y=68,
        w=300,
        h=162,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "url:",
        x=10,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Response",
        x=10,
        y=44,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="Send",
        x=251,
        y=10,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    textarea0.set_one_line(True)
    page0.screen_load()
    nbiot_0 = NBIOTUnit(1, port=(18, 17), verbose=False)
    nbiot_0.connect(apn="cmnbiot")
    while not (nbiot_0.isconnected()):
        pass

def loop():
    global page0, label0, label1, button0, textarea0, textarea1, nbiot_0_http_req, nbiot_0
    M5.update()

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

    Output of received NBIoT message data on screen.

#### MQTT Example

This example shows how to send MQTT message using the NBIoT Unit.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import NBIOTUnit

page0 = None
label0 = None
nbiot_0_mqtt = None
nbiot_0 = None

def nbiot_0__testtopic_a_event(data):
    global page0, label0, nbiot_0_mqtt, nbiot_0
    label0.set_text(str(data[1]))

def setup():
    global page0, label0, nbiot_0_mqtt, nbiot_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=130,
        y=105,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    nbiot_0 = NBIOTUnit(1, port=(18, 17), verbose=False)
    nbiot_0.connect(apn="cmnbiot")
    while not (nbiot_0.isconnected()):
        pass
    nbiot_0_mqtt = nbiot_0.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    nbiot_0_mqtt.connect(clean_session=False)
    nbiot_0_mqtt.subscribe("testtopic/a", nbiot_0__testtopic_a_event, qos=0)

def loop():
    global page0, label0, nbiot_0_mqtt, nbiot_0
    M5.update()
    nbiot_0_mqtt.check_msg()

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

    Output of received NBIoT message data on screen.

## **API**

## `NBIOTUnit`
Create an NBIOTUnit object.

- Parameter `uart_or_id`: The UART object or UART ID.
- Type of `uart_or_id`: machine.UART | int
- Parameter `port`: A list or tuple containing the RX and TX pin numbers. Required if uart_or_id is an ID.
- Type of `port`: list | tuple
- Parameter `verbose` (`bool`): Whether to print debug information.

```python
from unit import NBIOTUnit
import machine

# Using UART ID and pins (rx, tx)
nbiot = NBIOTUnit(1, (16, 17))

# Or using UART object
uart = machine.UART(1, tx=17, rx=16)
nbiot = NBIOTUnit(uart)
```

### `connect(apn="cmnbiot")`

        Connect to the NB-IoT network.

        - Parameter `apn` (`str`): The APN of the NB-IoT network. Default is "cmnbiot".

```python
nbiot.connect("cmnbiot")
```
### `isconnected()`

        Check if the NB-IoT unit is connected to the network.

        - Returns: True if connected, False otherwise.
        - Return type: bool

```python
if nbiot.isconnected():
    print("NB-IoT unit is connected")
else:
    print("NB-IoT unit is not connected")
```
### `active(en)`

        Activate or deactivate the NB-IoT unit. Deactivating will enter low power consumption mode.

        - Parameter `en` (`bool`): True to activate, False to deactivate.

```python
nbiot.active(True)
```
### `status([param])`

        Get the status of the NB-IoT unit.

        Following are commonly supported parameters.

        Parameter         Description
        rssi              signal strength
        pin               SIM Card status
        station           station registration status

        - Parameter `param` (`str`): Optional parameter to specify the status type.
        - Returns: Status information.
        - Return type: str | tuple

```python
# get signal strength
print(nbiot.status("rssi"))

# get SIM Card status
print(nbiot.status("pin"))

# get station registration status
print(nbiot.status("station"))
```
### `ifconfig`

        Get IP-level network interface parameters: IP address, subnet mask, gateway and DNS server.

        - Returns: A tuple with the network interface parameters.
        - Return type: tuple

```python
# Get IP address
print(nbiot.ifconfig()[0])
# Get subnet mask
print(nbiot.ifconfig()[1])
# Get gateway
print(nbiot.ifconfig()[2])
# Get DNS server
print(nbiot.ifconfig()[3])
```
### `config('param')`
                   config(param=value)

        Get or set the configuration parameters of the NB-IoT unit.

        Following are commonly supported parameters.

        Parameter         permissions       Description
        apn               R                 Access Point Name
        mode              R                 Network mode(only supported NB-IoT)
        band              R/W               Frequency Band
        ccid              R                 SIM Card CCID
        imei              R                 Device IMEI
        imsi              R                 SIM Card IMSI
        mfr               R                 Manufacturer
        model             R                 Module Model
        version           R                 Firmware Version

        - Parameter `param` (`str`): The configuration parameter to get or set.
        - Parameter `value`: The value to set for the configuration parameter.
        - Returns: The value of the configuration parameter when getting.
        - Return type: None  str  int | tuple

```python
# Get apn
print(nbiot.config('apn'))

# Get network mode
nbiot.config('mode')

# Get Frequency Band
nbiot.config('band')

# Set Frequency Band
nbiot.config(band=(1, 3, 5, 8))

# Get CCID
nbiot.config('ccid')

# Get IMEI
nbiot.config('imei')

# Get IMSI
nbiot.config('imsi')

# Get Manufacturer
nbiot.config('mfr')

# Get Module Model
nbiot.config('model')

# Get Firmware Version
nbiot.config('version')
```
### `request(method, url, data=None, json=None, headers={}, stream=None, auth=None, timeout=None, parse_headers=True)`
                   head(url, **kw)
                   get(url, **kw)
                   post(url, **kw)
                   put(url, **kw)
                   patch(url, **kw)
                   delete(url, **kw)

        Send an HTTP request.

        - Parameter `method` (`str`): HTTP method to use (e.g. "GET", "POST").
        - Parameter `url` (`str`): URL to send the request to.
        - Parameter `data`: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
        - Parameter `json`: (optional) A JSON serializable Python object to send in the body of the Request.
        - Parameter `headers` (`dict`): (optional) Dictionary of HTTP Headers to send with the Request.
        - Parameter `stream` (`bool`): (optional) if False, the response content will be immediately downloaded.
        - Parameter `auth` (`tuple`): (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        - Parameter `timeout` (`float`): (optional) How many seconds to wait for the server to send data before giving up.
        - Parameter `parse_headers` (`bool`): (optional) Whether to parse response headers.

        - Returns: A Response object.

> Note: See `requests2` for more details.

```python
# GET request
response = nbiot.get("http://httpbin.org/get")
print(response.status_code)
print(response.text)
response.close()

# POST request with JSON data
response = nbiot.post("http://httpbin.org/post", json={"key": "value"})
print(response.json())
response.close()
```
### `MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={})`

        Create an MQTT client.

        - Parameter `client_id` (`str`): The unique client ID string.
        - Parameter `server` (`str`): The hostname or IP address of the remote broker.
        - Parameter `port` (`int`): Network port of the server host to connect to. Default is 0.
        - Parameter `user` (`str`): User name for authentication.
        - Parameter `password` (`str`): Password for authentication.
        - Parameter `keepalive` (`int`): Maximum period in seconds allowed between communications with the broker. Default is 0.
        - Parameter `ssl` (`bool`): Whether to use SSL/TLS support. Default is False.
        - Parameter `ssl_params` (`dict`): SSL/TLS parameters.

        - Returns: An MQTTClient object.

> Note: See `MQTTClient <umqtt.MQTTClient>` for more details.

```python
mqtt = nbiot.MQTTClient("client_id", "mqtt.m5stack.com", port=1883, user="user", password="password")
mqtt.connect()
mqtt.publish("topic", "message")
mqtt.subscribe("topic", lambda topic, msg: print(topic, msg))
mqtt.check_msg()
```
