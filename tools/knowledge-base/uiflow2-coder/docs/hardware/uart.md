# UART

UART implements the standard UART/USART duplex serial communications protocol. At the physical level it consists of 2 lines: RX and TX. The unit of communication is a character (not to be confused with a string character) which can be 8 or 9 bits wide.

## MicroPython Example

#### Echo

This example demonstrates how to utilize UART interfaces by echoing back to the
sender any data received on configured UART.

```python
import os, sys, io
import M5
from M5 import *
from hardware import UART
import time

label0 = None
uart1 = None

i = None

def setup():
    global label0, uart1, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 102, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart1 = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)
    i = 0

def loop():
    global label0, uart1, i
    M5.update()
    uart1.write(i)
    if uart1.any():
        label0.setText(str(uart1.read()))
    i = (i if isinstance(i, (int, float)) else 0) + 1
    time.sleep(1)

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

## **API**

#### class UART

### `class UART(id, baudrate=9600, bits=8, parity=None, stop=1, *, ...)`

    Construct a UART object of the given id.

    For more parameters, please refer to init.

```python
from hadrware import UART

uart1 = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)
```
### `UART.init(baudrate=9600, bits=8, parity=None, stop=1, *, ...)`

        Initialise the UART bus with the given parameters.

        - Parameter `baudrate` (`int`): the clock rate.
        - Parameter `bits` (`int`): the number of bits per character, 7, 8 or 9.
        - Parameter `parity`: the parity, `None`, 0 (even) or 1 (odd).
        - Type of `parity`: None or int
        - Parameter `stop` (`int`): the number of stop bits, 1 or 2.
        - Keyword `tx`: the TX pin to use.
        - Type of `tx`: Pin or int
        - Keyword `rx`: the RX pin to use.
        - Type of `rx`: Pin or int
        - Keyword `rts`: the RTS (output) pin to use for hardware receive flow control.
        - Type of `rts`: Pin or int
        - Keyword `cts`: the CTS (input) pin to use for hardware transmit flow control.
        - Type of `cts`: Pin or int
        - Keyword `txbuf` (`int`): the length in characters of the TX buffer.
        - Keyword `rxbuf` (`int`): the length in characters of the RX buffer.
        - Keyword `timeout` (`int`): the time to wait for the first character (in ms).
        - Keyword `timeout_char` (`int`): the time to wait between characters (in ms).
        - Keyword `invert` (`int`): which lines to invert.

            - `0` will not invert lines (idle state of both lines is logic high).

            - `UART.INV_TX` will invert TX line (idle state of TX line now logic low).

            - `UART.INV_RX` will invert RX line (idle state of RX line now logic low).

            - `UART.INV_TX | UART.INV_RX` will invert both lines (idle state at logic low).

        - Keyword `flow` (`int`): which hardware flow control signals to use. The value is a bitmask.

            - `0` will ignore hardware flow control signals.

            - `UART.RTS` will enable receive flow control by using the RTS output pin to signal if the receive FIFO has sufficient space to accept more data.

            - `UART.CTS` will enable transmit flow control by pausing transmission when the CTS input pin signals that the receiver is running low on buffer space.

            - `UART.RTS | UART.CTS` will enable both, for full hardware flow control.

        - Keyword `mode` (`int`): the mode of the UART. The value is a bitmask.

            - `UART.MODE_UART` specifies regular UART mode.

            - `UART.MODE_RS485_HALF_DUPLEX` specifies half duplex RS485 UART mode control by RTS pin.

            - `UART.MODE_IRDA` specifies IRDA UART mode.

            - `UART.MODE_RS485_COLLISION_DETECT` specifies RS485 collision detection UART mode (used for test purposes).

            - `UART.MODE_RS485_APP_CTRL` specifies application control RS485 UART mode (used for test purposes).

> Note: It is possible to call `init()` multiple times on the same object in
> order to reconfigure  UART on the fly. That allows using single UART
> peripheral to serve different devices attached to different GPIO pins.
> Only one device can be served at a time in that case.
> Also do not call `deinit()` as it will prevent calling `init()`
> again.

```python
uart1.init(baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)
```
### `UART.deinit()`

        Turn off the UART bus.

> Note: You will not be able to call `init()` on the object after `deinit()`.
> A new instance needs to be created in that case.

```python
uart1.deinit()
```
### `UART.any()`

        Returns an integer counting the number of characters that can be read without
        blocking.  It will return 0 if there are no characters available and a positive
        number if there are characters.  The method may return 1 even if there is more
        than one character available for reading.

        - Returns: the number of characters available for reading.
        - Return type: int

        For more sophisticated querying of available characters use select.poll:
```
poll = select.poll()
poll.register(uart, select.POLLIN)
poll.poll(timeout)
```

```python
print(uart1.any())
```
### `UART.read([nbytes])`

        Read characters.  If `nbytes` is specified then read at most that many bytes,
        otherwise read as much data as possible. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        - Returns: a bytes object containing the bytes read in.  Returns `None` on timeout.
        - Return type: bytes or None

```python
print(uart1.read())
```
### `UART.readinto(buf[, nbytes])`

        Read bytes into the `buf`.  If `nbytes` is specified then read at most
        that many bytes.  Otherwise, read at most `len(buf)` bytes. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        - Returns: number of bytes read and stored into `buf` or `None` on timeout.
        - Return type: int or None

```python
buf = bytearray(10)
uart1.readinto(buf)
```
### `UART.readline()`

        Read a line, ending in a newline character. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        - Returns: the line read or `None` on timeout.
        - Return type: str or None

```python
print(uart1.readline())
```
### `UART.write(buf)`

        Write the buffer of bytes to the bus.

        - Parameter `buf`: the buffer of bytes to write.
        - Type of `buf`: bytes or bytearray or str

        - Returns: number of bytes written or `None` on timeout.
        - Return type: int or None

```python
uart1.write('1234!')
```
### `UART.sendbreak()`

        Send a break condition on the bus. This drives the bus low for a duration
        longer than required for a normal transmission of a character.

```python
uart1.sendbreak()
```
### `UART.flush()`

        Waits until all data has been sent. In case of a timeout, an exception is raised. The timeout
        duration depends on the tx buffer size and the baud rate. Unless flow control is enabled, a timeout
        should not occur.

> Note: For the rp2, esp8266 and nrf ports the call returns while the last byte is sent.
> If required, a one character wait time has to be added in the calling script.

```python
uart1.flush()
```
### `UART.txdone()`

        Tells whether all data has been sent or no data transfer is happening. In this case,
        it returns `True`. If a data transmission is ongoing it returns `False`.

> Note: For the rp2, esp8266 and nrf ports the call may return `True` even if the last byte
> of a transfer is still being sent. If required, a one character wait time has to be
> added in the calling script.

```python
print(uart1.txdone())
```
### `UART.irq(handler=None, trigger=0, hard=False)`

        Configure an interrupt handler to be called when a UART event occurs.

        - Parameter `handler` (`func`): an optional function to be called when the interrupt event triggers.  The handler must take exactly one argument which is the `UART` instance.

        - Parameter `trigger` (`int`): configures the event(s) which can generate an interrupt. Possible values are a mask of one or more of the following:

            - `UART.IRQ_RXIDLE` interrupt after receiving at least one character and then the RX line goes idle.

            - `UART.IRQ_RX` interrupt after each received character.

            - `UART.IRQ_TXIDLE` interrupt after or while the last character(s) of a message are or have been sent.

            - `UART.IRQ_BREAK` interrupt when a break state is detected at RX

        - Parameter `hard` (`bool`): if true a hardware interrupt is used.  This reduces the delay between the pin change and the handler being called. Hard interrupt handlers may not allocate memory; see `isr_rules`.

        - Returns: Returns an irq object.

        Due to limitations of the hardware not all trigger events are available on all ports.

            Port / Trigger IRQ_RXIDLE IRQ_RX IRQ_TXIDLE IRQ_BREAK
            CC3200                      yes
            ESP32            yes        yes                yes
            MIMXRT           yes                yes
            NRF                         yes     yes
            RENESAS-RA       yes        yes
            RP2              yes                yes        yes
            SAMD             yes        yes     yes
            STM32            yes        yes

> Note: - The ESP32 port does not support the option hard=True.
>
> - The rp2 port's UART.IRQ_TXIDLE is only triggered when the message
>   is longer than 5 characters and the trigger happens when still 5 characters
>   are to be sent.
>
> - The rp2 port's UART.IRQ_BREAK needs receiving valid characters for triggering
>   again.
>
> - The SAMD port's UART.IRQ_TXIDLE is triggered while the last character is sent.
>
> - On STM32F4xx MCU's, using the trigger UART.IRQ_RXIDLE the handler will be called once
>   after the first character and then after the end of the message, when the line is
>   idle.
        Availability: cc3200, esp32, mimxrt, nrf, renesas-ra, rp2, samd, stm32.

### `UART.RTS`
### `UART.CTS`

        Flow control options.

### `UART.MODE_UART`
### `UART.MODE_RS485_HALF_DUPLEX`
### `UART.MODE_IRDA`
### `UART.MODE_RS485_COLLISION_DETECT`
### `UART.MODE_RS485_APP_CTRL`

        UART mode options.

### `UART.IRQ_RXIDLE`
### `UART.IRQ_RX`
### `UART.IRQ_TXIDLE`
### `UART.IRQ_BREAK`

        IRQ trigger sources.
