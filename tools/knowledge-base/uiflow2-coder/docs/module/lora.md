
# Lora Module

The LoRa433_V1.1 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 433MHz frequency and utilizes the Ra-02 module (SX1278 chip) solution.

Support the following products:

LoraModule

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from module import LoraModule
lora = LoraModule(pin_irq=35, pin_rst=13) # basic
lora = LoraModule(pin_irq=35, pin_rst=25) # core2
lora = LoraModule(pin_irq=10, pin_rst=5) # cores3
lora.send("Hello, LoRa!")

print(lora.recv())

def callback(received_data):
    global lora
    print(received_data)
    lora.start_recv()
lora.set_irq_callback(callback)
lora.start_recv()
```

## class LoraModule

## Constructors

### `class LoraModule(pin_cs, pin_irq, pin_rst, freq_band, sf, bw, coding_rate, preamble_len, output_power)`

    Initialize the LoRa module.

    - Parameter `pin_cs` (`int`): Chip select pin
    - Parameter `pin_irq` (`int`): Interrupt pin
    - Parameter `pin_rst` (`int`): Reset pin
    - Parameter `freq_band`: LoRa RF frequency in kHz.
    - Parameter `sf` (`int`): Spreading factor, Higher spreading factors allow reception of weaker signals but have slower data rate.
    - Parameter `bw` (`str`): Bandwidth value in kHz. Must be exactly one of BANDWIDTHS
    - Parameter `coding_rate` (`int`): Forward Error Correction (FEC) coding rate is expressed as a ratio, &#x60;4/N&#x60;.
    - Parameter `preamble_len` (`int`): Length of the preamble sequence, in units of symbols.
    - Parameter `output_power` (`int`): Output power in dBm.

## Methods

### `LoraModule.send(packet, tx_at_ms)`

    Send a data packet.

    - Parameter `packet`: The data packet to send.
    - Parameter `tx_at_ms`: Time to transmit the packet in milliseconds. For precise timing of sent packets, there is an optional &#x60;tx_at_ms&#x60; argument which is a timestamp (as a &#x60;time.ticks_ms()&#x60; value). If set, the packet will be sent as close as possible to this timestamp and the function will block until that time arrives

### `LoraModule.recv(timeout_ms, rx_length, rx_packet)`

    Receive a data packet.

    - Parameter `timeout_ms`: Optional, sets a receive timeout in milliseconds. If None (default value), then the function will block indefinitely until a packet is received.
    - Parameter `rx_length` (`int`): Necessary to set if &#x60;implicit_header&#x60; is set to &#x60;True&#x60; (see above). This is the length of the packet to receive. Ignored in the default LoRa explicit header mode, where the received radio header includes the length.
    - Parameter `rx_packet` (`RxPacket`): Optional, this can be an &#x60;RxPacket&#x60; object previously received from the modem. If the newly received packet has the same length, this object is reused and returned to save an allocation. If the newly received packet has a different length, a new &#x60;RxPacket&#x60; object is allocated and returned instead.

### `LoraModule.start_recv()`

    Start receiving data once, trigger an interrupt when data is received.

### `LoraModule.set_irq_callback(callback)`

    Set the IRQ callback function.

    - Parameter `callback`: The callback function. The function should accept one argument, which is the received data.

### `LoraModule.standby()`

    Set the modem to standby mode.

### `LoraModule.sleep()`

    Set the modem to sleep mode.

### `LoraModule.irq_triggered()`

    Check if the IRQ has been triggered.

## Constants

### `LoraModule.LORA_433`
### `LoraModule.LORA_868`

    Select the LoRa frequency band.

### `LoraModule.BANDWIDTHS`

    Valid bandwidth
