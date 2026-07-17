# LoRa

LoRa is used to control the built-in long-range wireless communication module inside the host device. Below is the detailed LoRa support for the host:

     Controllers      LoRa    |
     UnitC6L          S     |
     Nesso N1         S     |

## MicroPython Example

#### Sender

This example sends data every second.

```python
import os, sys, io
import M5
from M5 import *
from hardware import LoRa
import time

title0 = None
label_tx = None
lora = None
last_time = None
count = None
tx = None

def setup():
    global title0, label_tx, lora, last_time, count, tx
    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Tx", 3, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12)
    label_tx = Widgets.Label("label0", 2, 23, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)
    lora = LoRa(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    last_time = time.ticks_ms()
    count = 0

def loop():
    global title0, label_tx, lora, last_time, count, tx
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        tx = str("M5 ") + str(count)
        count = (count if isinstance(count, (int, float)) else 0) + 1
        lora.send(tx, None)
        label_tx.setText(str(tx))

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

#### Receiver

This example receives and displays data.

```python
import os, sys, io
import M5
from M5 import *
from hardware import LoRa

title0 = None
label_rx = None
lora = None
lora_data = None
snr = None
rssi = None

def lora_receive_event(received_data):
    global title0, label_rx, lora, lora_data, snr, rssi
    lora_data = received_data
    label_rx.setText(str(lora_data.decode()))
    snr = (lora_data.snr) / 4
    rssi = lora_data.rssi
    print((str((str("SNR: ") + str(snr))) + str((str(" RSSI： ") + str(rssi)))))

def setup():
    global title0, label_rx, lora, lora_data, snr, rssi
    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Rx", 3, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12)
    label_rx = Widgets.Label("label0", 2, 23, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)
    lora = LoRa(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    lora.set_irq_callback(lora_receive_event)
    lora.start_recv()

def loop():
    global title0, label_rx, lora, lora_data, snr, rssi
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

#### Important: IRQ when using interrupt receive

> Note: When receiving data with the interrupt method (`set_irq_callback` and
> `start_recv()`), the firmware automatically clears the LoRa IRQ flag
> after interrupt handling.
>
> In this case, polling `irq_triggered()` may always return `False`
> because the flag has already been cleared. This is not a receive failure.
>
> Please use synchronous receive mode (`recv()`) for testing.
## **API**

#### class LoRa

### `class hardware.LoRa(freq_khz = 868000, \`
                        bw = "250", \
                        sf = 8, \
                        coding_rate = 8, \
                        reamble_len = 12, \
                        syncword = 0x12, \
                        output_power = 10)

    Create an LoRa object.

    - Parameter `freq_khz` (`int`): LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
    - Parameter `bw` (`str`): Bandwidth, options include:

        - `"7.8"`: 7.8 KHz
        - `"10.4"`: 10.4 KHz
        - `"15.6"`: 15.6 KHz
        - `"20.8"`: 20.8 KHz
        - `"31.25"`: 31.25 KHz
        - `"41.7"`: 41.7 KHz
        - `"62.5"`: 62.5 KHz
        - `"125"`: 125 KHz
        - `"250"`: 250 KHz
        - `"500"`: 500 KHz
    - Parameter `sf` (`int`): Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    - Parameter `coding_rate` (`int`): Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    - Parameter `preamble_len` (`int`): Length of the preamble sequence in symbols, range from 0 to 255.
    - Parameter `syncword` (`int`): Sync word to mark the start of the data frame, default is 0x12.
    - Parameter `output_power` (`int`): Output power in dBm, range from -9 to 22.

```python
from hardware import LoRa

lora_0 = LoRa(868000, '250', 8, 8, 12, 0x12, 10)
```
### `set_freq(freq_khz)`

        Set frequency in kHz.

        - Parameter `freq_khz` (`int`): Frequency in kHz (850000 ~ 930000), default is 868000.

```python
lora_0.set_freq(freq_khz)
```
### `set_sf(sf)`

        Set spreading factor (SF).

        - Parameter `sf` (`int`): Spreading factor (7 ~ 12)

```python
lora_0.set_sf(sf)
```
### `set_bw(bw)`

        Set bandwidth.

        - Parameter `bw` (`str`): Bandwidth in kHz as string. Must be one of:
                       '7.8', '10.4', '15.6', '20.8', '31.25', '41.7',
                       '62.5', '125', '250', '500'.

```python
lora_0.set_bw(bw)
```
### `set_coding_rate(coding_rate)`

        Set coding rate.

        - Parameter `coding_rate` (`int`): Coding rate (5 ~ 8)

```python
lora_0.set_coding_rate(coding_rate)
```
### `set_syncword(syncword)`

        Set syncword.

        - Parameter `syncword` (`int`): Sync word (0 ~ 0xFF)

```python
lora_0.set_syncword(syncword)
```
### `set_preamble_len(preamble_len)`

        Set preamble length.

        - Parameter `preamble_len` (`int`): Preamble length, range: 0~255.

```python
lora_0.set_preamble_len(preamble_len)
```
### `set_output_power(output_power)`

        Set output power in dBm.

        - Parameter `output_power` (`int`): Output power in dBm (-9 ~ 22)

```python
lora_0.set_output_power(output_power)
```
### `set_irq_callback(callback)`

        Set the interrupt callback function to be executed on IRQ.

        - Parameter `callback`: The callback function to be invoked when the interrupt is triggered.
                          The callback should not take any arguments and should return nothing.

        Call `start_recv()` to begin receiving data.

```python
lora_0.set_irq_callback()
```
### `start_recv()`

        Start receive data.

        This method initiates the process to begin receiving data.

```python
lora_0.start_recv()
```
### `recv(self, timeout_ms, rx_length, rx_packet)`

        Receive data.

        - Parameter `timeout_ms` (`int`): Timeout in milliseconds (optional). Default is None.
        - Parameter `rx_length` (`int`): Length of the data to be read. Default is 0xFF.
        - Parameter `rx_packet` (`RxPacket`): An instance of `RxPacket` (optional) to reuse.
        - Returns: Received packet instance
        - Return type: RxPacket

        Attempt to receive a LoRa packet. Returns `None` if timeout occurs, or returns the received packet instance.

```python
data = lora_0.recv()
```
### `send(buf, tx_at_ms=None)`

        Send data.

        - Parameter ` list  tuple  int  bytearray packet` (`str`): The data to be sent.
        - Parameter `tx_at_ms` (`int`): The timestamp in milliseconds when to send the data (optional). Default is None.
        - Returns: Returns a timestamp (result of `time.ticks_ms()`) indicating when the data packet was sent.
        - Return type: int

        Send a data packet and return the timestamp after the packet is sent.

```python
lora_0.send()
```
### `standby()`

        Set module to standby mode.

        Puts the LoRa module into standby mode, consuming less power.

```python
lora_0.standby()
```
### `sleep()`

        Put the module to sleep mode.

        Reduces the power consumption by putting the module into deep sleep mode.

```python
lora_0.sleep()
```
### `irq_triggered()`

        Check IRQ trigger.

        - Returns: Returns `True` if an interrupt service routine (ISR) has been
                  triggered since the last send or receive started. In **interrupt
                  receive** mode the IRQ is usually cleared inside the driver when
                  the callback runs, so this method may stay `False`. Use
                  synchronous `recv()` to test reception (see the note above).
        - Return type: bool

```python
lora_0.irq_triggered()
```
Refer to `lora_rxpacket` for more details about RxPacket.
