# nec.py Encoder for IR remote control using synchronous code
# NEC protocol.

# Author: Peter Hinch
# Copyright Peter Hinch 2020-2022 Released under the MIT license
# Copyright (c) 2024 M5Stack Technology CO LTD

# With thanks to J.E. Tannenbaum for information re Samsung protocol
from micropython import const
from .transmitter import IR, STOP

_TBURST = const(563)
_T_ONE = const(1687)


class NEC(IR):
    valid = (0xFFFF, 0xFF, 0)  # Max addr, data, toggle
    samsung = False

    def __init__(self, pin, freq=38000, verbose=False):  # NEC specifies 38KHz also Samsung
        super().__init__(pin, freq, 68, 33, verbose)  # Measured duty ratio 33%

    def _bit(self, b):
        self.append(_TBURST, _T_ONE if b else _TBURST)

    def tx(self, addr, data, _):  # Ignore toggle
        if self.samsung:
            self.append(4500, 4500)
        else:
            self.append(9000, 4500)
        if addr < 256:  # Short address: append complement
            if self.samsung:
                addr |= addr << 8
            else:
                addr |= (addr ^ 0xFF) << 8
        for _ in range(16):
            self._bit(addr & 1)
            addr >>= 1
        data |= (data ^ 0xFF) << 8
        for _ in range(16):
            self._bit(data & 1)
            data >>= 1
        self.append(_TBURST)

    def repeat(self):
        self.aptr = 0
        self.append(9000, 2250, _TBURST)
        self.trigger()  # Initiate physical transmission.


# nec.py Decoder for IR remote control using synchronous code
# Supports NEC and Samsung protocols.
# With thanks to J.E. Tannenbaum for information re Samsung protocol

# For a remote using NEC see https://www.adafruit.com/products/389

# Author: Peter Hinch
# Copyright Peter Hinch 2020-2022 Released under the MIT license

from utime import ticks_us, ticks_diff
from .receiver import IR_RX


class NEC_ABC(IR_RX):
    def __init__(self, pin, extended, samsung, callback, *args):
        # Block lasts <= 80ms (extended mode) and has 68 edges
        super().__init__(pin, 68, 80, callback, *args)
        self._extended = extended
        self._addr = 0
        self._leader = 2500 if samsung else 4000  # 4.5ms for Samsung else 9ms

    def decode(self, _):
        try:
            if self.edge > 68:
                raise RuntimeError(self.OVERRUN)
            width = ticks_diff(self._times[1], self._times[0])
            if width < self._leader:  # 9ms leading mark for all valid data
                raise RuntimeError(self.BADSTART)
            width = ticks_diff(self._times[2], self._times[1])
            if width > 3000:  # 4.5ms space for normal data
                if self.edge < 68:  # Haven't received the correct number of edges
                    raise RuntimeError(self.BADBLOCK)
                # Time spaces only (marks are always 562.5µs)
                # Space is 1.6875ms (1) or 562.5µs (0)
                # Skip last bit which is always 1
                val = 0
                for edge in range(3, 68 - 2, 2):
                    val >>= 1
                    if ticks_diff(self._times[edge + 1], self._times[edge]) > 1120:
                        val |= 0x80000000
            elif width > 1700:  # 2.5ms space for a repeat code. Should have exactly 4 edges.
                raise RuntimeError(
                    self.REPEAT if self.edge == 4 else self.BADREP
                )  # Treat REPEAT as error.
            else:
                raise RuntimeError(self.BADSTART)
            addr = val & 0xFF  # 8 bit addr
            cmd = (val >> 16) & 0xFF
            if cmd != (val >> 24) ^ 0xFF:
                raise RuntimeError(self.BADDATA)
            if addr != ((val >> 8) ^ 0xFF) & 0xFF:  # 8 bit addr doesn't match check
                if not self._extended:
                    raise RuntimeError(self.BADADDR)
                addr |= val & 0xFF00  # pass assumed 16 bit address to callback
            self._addr = addr
            self._cmd = cmd
        except RuntimeError as e:
            cmd = self._cmd if e.args[0] == self.REPEAT else -1
            addr = self._addr if cmd == self.REPEAT else 0  # REPEAT uses last address
        # Set up for new data burst and run user callback
        self.do_callback(cmd, addr, 0, self.REPEAT)


class NEC_8(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, False, False, callback, *args)


class NEC_16(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, False, callback, *args)


class SAMSUNG(NEC_ABC):
    def __init__(self, pin, callback, *args):
        super().__init__(pin, True, True, callback, *args)
