# Stamp UWB

Stamp UWB is a QM33120 ultra-wideband transceiver. The `StampUWB` class
selects the pin mapping for the current Stamp host and provides the PHY, frame,
status, and timestamp operations. The PHY channel is fixed to channel 9, and
only one active
`StampUWB` instance is supported.

Support the following products:

    Stamp UWB

Supported hosts:

- StampS3Mini
- StampC6
- StampC5

## DS-TWR Ranging Principle

The simple examples use a three-message double-sided two-way ranging exchange:

1. The Tag transmits a Poll frame and records the Poll TX timestamp `T1`.
   The Anchor receives it and records the Poll RX timestamp `T2`.
2. The Anchor transmits a Response frame and records the Response TX timestamp
   `T3`. The Tag receives it and records the Response RX timestamp `T4`.
3. The Tag schedules a delayed Final frame, records its TX timestamp `T5`,
   and includes `T1`, `T4`, and `T5` in the frame. The Anchor receives
   the Final frame and records timestamp `T6`.

The examples use the following compact frame format. Multi-byte values are
little-endian, and the sequence number associates the three frames:

- Poll: `[0x01, sequence]`
- Response: `[0x02, sequence]`
- Final: `[0x03, sequence, T1, T4, T5]`, where each timestamp occupies the
  low 32 bits of a device timestamp

The Anchor calculates the time of flight while handling 32-bit timestamp
wraparound:

```text
round_a = T4 - T1
round_b = T6 - T3
delay_a = T5 - T4
delay_b = T3 - T2
tof = (round_a * round_b - delay_a * delay_b) \
      / (round_a + round_b + delay_a + delay_b)
distance = abs(tof * DWT_TIME_UNITS * 299702547)
```
`DWT_TIME_UNITS` is `1 / (499200000 * 128)` seconds. The Anchor prints the
calculated distance locally. This simplified protocol does not send the
distance back to the Tag.

## MicroPython Example

#### Simple DS-TWR Anchor

The anchor receives Poll and Final frames, calculates the distance locally,
and prints the non-negative ranging result.

```python
import os, sys, io
import M5
from M5 import *
import uwb
from stamp import StampUWB
import time
import struct
import math

stamp_uwb = None
status = None
sequence = None
poll = None
poll_rx = None
response_frame = None
final_frame = None
response_tx = None
final_rx = None
round_a = None
round_b = None
delay_a = None
response_rx = None
poll_tx = None
delay_b = None
denominator = None
final_tx = None
tof_dtu = None
distance = None
display_distance = None

def setup():
    global \
        stamp_uwb, \
        status, \
        sequence, \
        poll, \
        poll_rx, \
        response_frame, \
        final_frame, \
        response_tx, \
        final_rx, \
        round_a, \
        round_b, \
        delay_a, \
        response_rx, \
        poll_tx, \
        delay_b, \
        denominator, \
        final_tx, \
        tof_dtu, \
        distance, \
        display_distance

    M5.begin()
    stamp_uwb = StampUWB()
    stamp_uwb.configure(
        preamble_length=128,
        pac=8,
        tx_code=9,
        rx_code=9,
        sfd_type=uwb.SFD_DW_8,
        data_rate=uwb.BR_6M8,
        phr_mode=uwb.PHR_STD,
        phr_rate=uwb.PHR_RATE_STD,
        sfd_timeout=129,
    )
    stamp_uwb.configure_tx_rf(pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0)
    stamp_uwb.set_antenna_delay(tx=16385, rx=16385)
    stamp_uwb.set_lna_pa(lna=True, pa=True)
    stamp_uwb.set_rx_timeout(30000)
    sequence = 0

def loop():
    global \
        stamp_uwb, \
        status, \
        sequence, \
        poll, \
        poll_rx, \
        response_frame, \
        final_frame, \
        response_tx, \
        final_rx, \
        round_a, \
        round_b, \
        delay_a, \
        response_rx, \
        poll_tx, \
        delay_b, \
        denominator, \
        final_tx, \
        tof_dtu, \
        distance, \
        display_distance
    M5.update()
    try:
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
        stamp_uwb.rx_enable(uwb.RX_IMMEDIATE)
        status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
        if status & uwb.STATUS_RX_GOOD:
            poll = stamp_uwb.read_rx_frame()
            if len(poll) == 2 and poll[0] == 1:
                sequence = poll[1]
                poll_rx = stamp_uwb.rx_timestamp() & 0xFFFFFFFF
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
                stamp_uwb.set_rx_after_tx_delay(0)
                response_frame = bytearray(2)
                response_frame[0] = 2
                response_frame[1] = sequence
                stamp_uwb.write_tx_frame(response_frame, True)
                stamp_uwb.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
                status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
                if status & uwb.STATUS_RX_GOOD:
                    final_frame = stamp_uwb.read_rx_frame()
                    if (
                        len(final_frame) == 14
                        and final_frame[0] == 3
                        and final_frame[1] == sequence
                    ):
                        response_tx = stamp_uwb.tx_timestamp() & 0xFFFFFFFF
                        final_rx = stamp_uwb.rx_timestamp() & 0xFFFFFFFF
                        poll_tx, response_rx, final_tx = struct.unpack_from("<III", final_frame, 2)
                        round_a = response_rx - poll_tx & 0xFFFFFFFF
                        round_b = final_rx - response_tx & 0xFFFFFFFF
                        delay_a = final_tx - response_rx & 0xFFFFFFFF
                        delay_b = response_tx - poll_rx & 0xFFFFFFFF
                        denominator = (round_a + round_b) + (delay_a + delay_b)
                        if denominator != 0:
                            tof_dtu = (round_a * round_b - delay_a * delay_b) / denominator
                            distance = math.fabs((tof_dtu * (1 / (499200000 * 128))) * 299702547)
                            display_distance = round(distance * 100) / 100
                            if distance >= 0 and distance <= 100:
                                print(
                                    (
                                        str(
                                            (
                                                str(
                                                    (
                                                        str((str("sequence=") + str(sequence)))
                                                        + str(" distance=")
                                                    )
                                                )
                                                + str(display_distance)
                                            )
                                        )
                                        + str(" m")
                                    )
                                )
                            else:
                                print((str("invalid distance: ") + str(distance)))
                    else:
                        print("invalid final")
                else:
                    print("final timeout")
    except:
        print("ranging retry")
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)

    time.sleep_ms(10)

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

#### Simple DS-TWR Tag

The tag sends Poll, waits for Response, and sends a delayed Final frame. This
minimal protocol does not return the calculated distance to the tag.

```python
import os, sys, io
import M5
from M5 import *
import uwb
from stamp import StampUWB
import time
import struct

stamp_uwb = None
poll_frame = None
sequence = None
status = None
response = None
expected_response = None
poll_tx = None
response_rx = None
delayed_time = None
delayed_time_even = None
final_tx = None
final_frame = None

def setup():
    global \
        stamp_uwb, \
        poll_frame, \
        sequence, \
        status, \
        response, \
        expected_response, \
        poll_tx, \
        response_rx, \
        delayed_time, \
        delayed_time_even, \
        final_tx, \
        final_frame

    M5.begin()
    stamp_uwb = StampUWB()
    stamp_uwb.configure(
        preamble_length=128,
        pac=8,
        tx_code=9,
        rx_code=9,
        sfd_type=uwb.SFD_DW_8,
        data_rate=uwb.BR_6M8,
        phr_mode=uwb.PHR_STD,
        phr_rate=uwb.PHR_RATE_STD,
        sfd_timeout=129,
    )
    stamp_uwb.configure_tx_rf(pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0)
    stamp_uwb.set_antenna_delay(tx=16385, rx=16385)
    stamp_uwb.set_lna_pa(lna=True, pa=True)
    stamp_uwb.set_rx_after_tx_delay(0)
    stamp_uwb.set_rx_timeout(30000)
    sequence = 0

def loop():
    global \
        stamp_uwb, \
        poll_frame, \
        sequence, \
        status, \
        response, \
        expected_response, \
        poll_tx, \
        response_rx, \
        delayed_time, \
        delayed_time_even, \
        final_tx, \
        final_frame
    M5.update()
    try:
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
        poll_frame = bytearray(2)
        poll_frame[0] = 1
        poll_frame[1] = sequence
        stamp_uwb.write_tx_frame(poll_frame, True)
        stamp_uwb.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
        status = stamp_uwb.wait_status(uwb.STATUS_RX_ALL, 50)
        if not (status & uwb.STATUS_RX_GOOD):
            print("response timeout")
            time.sleep_ms(200)
        else:
            response = stamp_uwb.read_rx_frame()
            expected_response = bytearray(2)
            expected_response[0] = 2
            expected_response[1] = sequence
            if response != expected_response:
                print("invalid response")
                time.sleep_ms(200)
            else:
                poll_tx = stamp_uwb.tx_timestamp()
                response_rx = stamp_uwb.rx_timestamp()
                delayed_time = response_rx + 10000 * 63898 >> 8
                delayed_time_even = delayed_time & 0xFFFFFFFE
                final_tx = (delayed_time_even << 8) + 16385
                final_frame = struct.pack(
                    "<BBIII",
                    3,
                    sequence,
                    poll_tx & 0xFFFFFFFF,
                    response_rx & 0xFFFFFFFF,
                    final_tx & 0xFFFFFFFF,
                )
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)
                stamp_uwb.set_delayed_trx_time(delayed_time)
                stamp_uwb.write_tx_frame(final_frame, True)
                stamp_uwb.start_tx(uwb.TX_DELAYED)
                status = stamp_uwb.wait_status(uwb.STATUS_TX_DONE, 30)
                stamp_uwb.clear_status(uwb.STATUS_TX_DONE)
                print((str("final sent, sequence=") + str(sequence)))
                sequence = sequence + 1 & 0xFF
    except:
        print("ranging retry")
        stamp_uwb.force_trx_off()
        stamp_uwb.clear_status(uwb.STATUS_TX_DONE | uwb.STATUS_RX_ALL)

    time.sleep_ms(200)

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

## class StampUWB

## Constructors

### `class StampUWB()`

    Create a Stamp UWB object using the pin mapping of the current Stamp host.
    Only one active instance is supported.

        or the UWB device cannot be probed or initialized.

```python
from stamp import StampUWB

stamp_uwb_0 = StampUWB()
```
## Constants

The option block supplies the PHY, TX/RX mode, and status-mask constants used
by the methods below.

### `uwb.SFD_DW_8`

    Decawave 8-symbol SFD used by `StampUWB.configure`.

### `uwb.BR_6M8`

    6.8 Mbit/s PHY data rate used by `StampUWB.configure`.

### `uwb.PHR_STD`

    Standard PHY header mode used by `StampUWB.configure`.

### `uwb.PHR_RATE_STD`

    Standard PHY header rate used by `StampUWB.configure`.

### `uwb.TX_IMMEDIATE`

    Start transmission immediately.

### `uwb.TX_DELAYED`

    Start transmission at the time set by
    `StampUWB.set_delayed_trx_time`.

### `uwb.RESPONSE_EXPECTED`

    Automatically enable the receiver after transmission. Combine this flag
    with a TX start mode.

### `uwb.RX_IMMEDIATE`

    Enable the receiver immediately.

### `uwb.RX_DELAYED`

    Enable the receiver at the configured delayed RX time.

### `uwb.IDLE_ON_DELAY_ERROR`

    Return to idle if a delayed RX operation is already too late.

### `uwb.STATUS_TX_DONE`

    Transmission-complete status bit.

### `uwb.STATUS_RX_GOOD`

    Good-frame-received status bit.

### `uwb.STATUS_RX_TIMEOUT`

    Combined receive-timeout status mask.

### `uwb.STATUS_RX_ERROR`

    Combined receive-error status mask.

### `uwb.STATUS_RX_ALL`

    Combined mask containing good-frame, receive-timeout, and receive-error
    status bits.

## Methods

### `StampUWB.configure(preamble_length=128, pac=8, tx_code=9, rx_code=9, sfd_type=uwb.SFD_DW_8, data_rate=uwb.BR_6M8, phr_mode=uwb.PHR_STD, phr_rate=uwb.PHR_RATE_STD, sfd_timeout=129)`

    Configure the channel 9 UWB PHY.

    - Parameter `preamble_length` (`int`): Preamble length in symbols. Allowed values are `32`, `64`, `72`, `128`, `256`, `512`, `1024`, `1536`, `2048`, and `4096`. Default is `128`.
    - Parameter `pac` (`int`): Preamble acquisition chunk size. Allowed values are `4`, `8`, `16`, and `32`. Default is `8`.
    - Parameter `tx_code` (`int`): TX preamble code, range `9` to `12`. Default is `9`.
    - Parameter `rx_code` (`int`): RX preamble code, range `9` to `12`. Default is `9`.
    - Parameter `sfd_type` (`int`): SFD type. Use `uwb.SFD_DW_8`.
    - Parameter `data_rate` (`int`): PHY data rate. Use `uwb.BR_6M8`.
    - Parameter `phr_mode` (`int`): PHR mode. Use `uwb.PHR_STD`.
    - Parameter `phr_rate` (`int`): PHR rate. Use `uwb.PHR_RATE_STD`.
    - Parameter `sfd_timeout` (`int`): SFD timeout in symbols, range `0` to `65535`. Default is `129`.

```python
import uwb

stamp_uwb_0.configure(
    preamble_length=128,
    pac=8,
    tx_code=9,
    rx_code=9,
    sfd_type=uwb.SFD_DW_8,
    data_rate=uwb.BR_6M8,
    phr_mode=uwb.PHR_STD,
    phr_rate=uwb.PHR_RATE_STD,
    sfd_timeout=129,
)
```
### `StampUWB.configure_tx_rf(pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0)`

    Configure the channel 9 transmitter RF settings.

    - Parameter `pg_delay` (`int`): Pulse generator delay, range `0x00` to `0xFF`. Default is `0x34`.
    - Parameter `tx_power` (`int`): 32-bit TX power value, range `0x00000000` to `0xFFFFFFFF`. Default is `0xFEFEFEFE`.
    - Parameter `pg_count` (`int`): Pulse generator count, range `0x00` to `0xFF`. Default is `0`.

```python
stamp_uwb_0.configure_tx_rf(0x34, 0xFEFEFEFE, 0)
```
### `StampUWB.set_antenna_delay(tx=16385, rx=16385)`

    Set the TX and RX antenna delays.

    - Parameter `tx` (`int`): TX antenna delay in device time units, range `0` to `65535`. Default is `16385`.
    - Parameter `rx` (`int`): RX antenna delay in device time units, range `0` to `65535`. Default is `16385`.

```python
stamp_uwb_0.set_antenna_delay(tx=16385, rx=16385)
```
### `StampUWB.set_lna_pa(lna=True, pa=True)`

    Enable or disable the low-noise amplifier and power amplifier controls.

    - Parameter `lna` (`bool`): Enable the LNA. Default is `True`.
    - Parameter `pa` (`bool`): Enable the PA. Default is `True`.

```python
stamp_uwb_0.set_lna_pa(lna=True, pa=True)
```
### `StampUWB.set_rx_after_tx_delay(delay_uus=0)`

    Set the delay from TX completion to automatic RX enable.

    - Parameter `delay_uus` (`int`): Delay in UWB microseconds, range `0` to `4294967295`. Default is `0`.

```python
stamp_uwb_0.set_rx_after_tx_delay(0)
```
### `StampUWB.set_rx_timeout(timeout_uus=30000)`

    Set the RX frame timeout. A value of `0` disables the timeout.

    - Parameter `timeout_uus` (`int`): Timeout in UWB microseconds, range `0` to `4294967295`. Default is `30000`.

```python
stamp_uwb_0.set_rx_timeout(30000)
```
### `StampUWB.set_preamble_timeout(timeout=0)`

    Set the preamble detection timeout. A value of `0` disables the timeout.

    - Parameter `timeout` (`int`): Timeout in PAC units, range `0` to `65535`. Default is `0`.

```python
stamp_uwb_0.set_preamble_timeout(0)
```
### `StampUWB.write_tx_frame(data, ranging=True)`

    Write a payload to the TX buffer. Do not include the two-byte FCS.

    - Parameter `data`: Bytes-like payload, range `0` to `125` bytes.
    - Parameter `ranging` (`bool`): Set the ranging bit in TX frame control. Default is `True`.

```python
stamp_uwb_0.write_tx_frame(b"hello", ranging=True)
```
### `StampUWB.set_delayed_trx_time(device_time)`

    Set the delayed TX/RX device time.

    - Parameter `device_time` (`int`): Low 32 bits of the 40-bit device timestamp shifted right by 8, range `0` to `4294967295`.

```python
delayed_time = (stamp_uwb_0.rx_timestamp() + 4500 * 63898) >> 8
stamp_uwb_0.set_delayed_trx_time(delayed_time)
```
### `StampUWB.start_tx(mode)`

    Start an immediate or delayed transmission.

    - Parameter `mode` (`int`): TX mode composed from `uwb.TX_IMMEDIATE` or `uwb.TX_DELAYED` and optional `uwb.RESPONSE_EXPECTED`.

```python
stamp_uwb_0.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
```
### `StampUWB.rx_enable(mode=uwb.RX_IMMEDIATE)`

    Enable the receiver.

    - Parameter `mode` (`int`): Use `uwb.RX_IMMEDIATE` or `uwb.RX_DELAYED`. Delayed RX can be combined with `uwb.IDLE_ON_DELAY_ERROR`. Default is `uwb.RX_IMMEDIATE`.

```python
stamp_uwb_0.rx_enable(uwb.RX_IMMEDIATE)
```
### `StampUWB.wait_status(mask, timeout_ms=-1)`

    Wait until any requested system status bit is set.

    - Parameter `mask` (`int`): Status mask composed from `uwb.STATUS_*` constants, range `0x00000000` to `0xFFFFFFFF`.
    - Parameter `timeout_ms` (`int`): Software timeout in milliseconds, range `-1` to `1073741823`. `-1` waits indefinitely. Default is `-1`.
    - Returns: Raw 32-bit system status value.
    - Return type: int
        software timeout.

```python
stamp_uwb_0.wait_status(uwb.STATUS_RX_ALL, 50)
```
### `StampUWB.read_status()`

    Read the low 32 bits of the system status register.

    - Returns: Raw 32-bit system status value.
    - Return type: int

```python
stamp_uwb_0.read_status()
```
### `StampUWB.clear_status(mask)`

    Clear selected system status bits.

    - Parameter `mask` (`int`): Status mask, range `0x00000000` to `0xFFFFFFFF`.

```python
stamp_uwb_0.clear_status(uwb.STATUS_TX_DONE)
```
### `StampUWB.force_trx_off()`

    Force the transmitter and receiver to the idle state.

```python
stamp_uwb_0.force_trx_off()
```
### `StampUWB.frame_length()`

    Get the last received frame length including the two-byte FCS.

    - Returns: Received frame length in bytes, range `2` to `127`.
    - Return type: int

```python
stamp_uwb_0.frame_length()
```
### `StampUWB.read_rx_frame()`

    Read the last received payload without the two-byte FCS.

    - Returns: Received payload, range `0` to `125` bytes.
    - Return type: bytes

```python
stamp_uwb_0.read_rx_frame()
```
### `StampUWB.tx_timestamp()`

    Read the last TX timestamp.

    - Returns: Full 40-bit TX timestamp in device time units.
    - Return type: int

```python
stamp_uwb_0.tx_timestamp()
```
### `StampUWB.rx_timestamp()`

    Read the last RX timestamp.

    - Returns: Full 40-bit RX timestamp in device time units.
    - Return type: int

```python
stamp_uwb_0.rx_timestamp()
```
### `StampUWB.system_timestamp()`

    Read the current UWB system timestamp.

    - Returns: Full 40-bit system timestamp in device time units.
    - Return type: int

```python
stamp_uwb_0.system_timestamp()
```
### `StampUWB.reset()`

    Reset, probe, and reinitialise the UWB device. Configure the PHY and RF
    settings again after reset.

```python
stamp_uwb_0.reset()
stamp_uwb_0.configure(
    preamble_length=128,
    pac=8,
    tx_code=9,
    rx_code=9,
    sfd_type=uwb.SFD_DW_8,
    data_rate=uwb.BR_6M8,
    phr_mode=uwb.PHR_STD,
    phr_rate=uwb.PHR_RATE_STD,
    sfd_timeout=129,
)
stamp_uwb_0.configure_tx_rf(
    pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0
)
```
### `StampUWB.wakeup()`

    Pulse the WAKEUP pin to wake the UWB device.

```python
stamp_uwb_0.wakeup()
```
### `StampUWB.deinit()`

    Stop TX/RX and release the SPI and GPIO resources. This method is
    idempotent. After deinitialization, other methods raise `OSError(ENODEV)`.

```python
stamp_uwb_0.deinit()
```
