# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from lora import RxPacket, SX1262
from micropython import schedule

from .f12 import StampF12


_F12_POSITIONS = {
    "sw": 3,
    "irq": 4,
    "busy": 5,
    "reset": 6,
    "miso": 8,
    "mosi": 9,
    "cs": 10,
    "clock": 12,
}


class StampLoRa1262:
    """SX1262 LoRa radio connected through the Stamp FPC12 interface.

    Passing ``None`` for a pin uses the current Stamp host's FPC12 mapping.
    StampC5, StampC6, and StampS3Mini are supported by default. Other hosts
    can be used when every signal pin is provided explicitly.
    """

    BANDWIDTHS = (
        "7.8",
        "10.4",
        "15.6",
        "20.8",
        "31.25",
        "41.7",
        "62.5",
        "125",
        "250",
        "500",
    )
    MIN_FREQ_KHZ = 868000
    MAX_FREQ_KHZ = 923000

    def __init__(
        self,
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
        sw=None,
        irq=None,
        busy=None,
        reset=None,
        miso=None,
        mosi=None,
        cs=None,
        clock=None,
        spi_id=1,
    ):
        pins = {
            "sw": sw,
            "irq": irq,
            "busy": busy,
            "reset": reset,
            "miso": miso,
            "mosi": mosi,
            "cs": cs,
            "clock": clock,
        }
        if any(pin is None for pin in pins.values()):
            try:
                f12 = StampF12()
            except NotImplementedError:
                missing = ", ".join(name for name, pin in pins.items() if pin is None)
                raise ValueError("%s are required for this Stamp host" % missing)
            for name, position in _F12_POSITIONS.items():
                if pins[name] is None:
                    pins[name] = f12.pin(position)

        self._validate_config(
            freq_khz,
            bw,
            sf,
            coding_rate,
            preamble_len,
            syncword,
            output_power,
        )

        self._sw = machine.Pin(pins["sw"], machine.Pin.OUT, value=1)
        self._spi = machine.SPI(
            spi_id,
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=machine.Pin(pins["clock"]),
            mosi=machine.Pin(pins["mosi"]),
            miso=machine.Pin(pins["miso"]),
        )
        self.modem = SX1262(
            spi=self._spi,
            reset=machine.Pin(pins["reset"], machine.Pin.OUT, value=1),
            cs=machine.Pin(pins["cs"], machine.Pin.OUT, value=1),
            busy=machine.Pin(pins["busy"], machine.Pin.IN),
            dio1=machine.Pin(pins["irq"], machine.Pin.IN),
            dio3_tcxo_millivolts=3000,
            lora_cfg={
                "freq_khz": freq_khz,
                "sf": sf,
                "bw": bw,
                "coding_rate": coding_rate,
                "syncword": syncword,
                "preamble_len": preamble_len,
                "output_power": output_power,
            },
        )
        self.irq_callback = None

    @staticmethod
    def _validate_range(name, value, minimum, maximum):
        if not minimum <= value <= maximum:
            raise ValueError("%s must be in range %d-%d" % (name, minimum, maximum))

    def _validate_config(
        self,
        freq_khz,
        bw,
        sf,
        coding_rate,
        preamble_len,
        syncword,
        output_power,
    ):
        self._validate_range("freq_khz", freq_khz, self.MIN_FREQ_KHZ, self.MAX_FREQ_KHZ)
        if bw not in self.BANDWIDTHS:
            raise ValueError("invalid bandwidth %s" % bw)
        self._validate_range("sf", sf, 6, 12)
        self._validate_range("coding_rate", coding_rate, 5, 8)
        self._validate_range("preamble_len", preamble_len, 5, 255)
        self._validate_range("syncword", syncword, 1, 255)
        self._validate_range("output_power", output_power, -9, 22)

    def set_freq(self, freq_khz=868000):
        """Set the LoRa carrier frequency in kHz."""
        self._validate_range("freq_khz", freq_khz, self.MIN_FREQ_KHZ, self.MAX_FREQ_KHZ)
        self.modem.configure({"freq_khz": freq_khz})

    def set_sf(self, sf):
        """Set the spreading factor."""
        self._validate_range("sf", sf, 6, 12)
        self.modem.configure({"sf": sf})

    def set_bw(self, bw):
        """Set the bandwidth in kHz."""
        if bw not in self.BANDWIDTHS:
            raise ValueError("invalid bandwidth %s" % bw)
        self.modem.configure({"bw": bw})

    def set_coding_rate(self, coding_rate):
        """Set the coding rate denominator for 4/N coding."""
        self._validate_range("coding_rate", coding_rate, 5, 8)
        self.modem.configure({"coding_rate": coding_rate})

    def set_syncword(self, syncword):
        """Set the LoRa sync word."""
        self._validate_range("syncword", syncword, 1, 255)
        self.modem.configure({"syncword": syncword})

    def set_preamble_len(self, preamble_len):
        """Set the preamble length in symbols."""
        self._validate_range("preamble_len", preamble_len, 5, 255)
        self.modem.configure({"preamble_len": preamble_len})

    def set_output_power(self, output_power):
        """Set the output power in dBm."""
        self._validate_range("output_power", output_power, -9, 22)
        self.modem.configure({"output_power": output_power})

    def send(self, packet, tx_at_ms=None):
        """Send a packet and return its transmission timestamp."""
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, (list, tuple)):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes((packet,))
        return self.modem.send(packet, tx_at_ms)

    def recv(self, timeout_ms=None, rx_length=0xFF, rx_packet: RxPacket = None):
        """Receive a packet, returning ``None`` on timeout."""
        return self.modem.recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self):
        """Start continuous reception."""
        self.modem.start_recv(continuous=True)

    def set_irq_callback(self, callback):
        """Schedule ``callback`` with the received packet after an IRQ."""
        self.irq_callback = callback

        def _irq_callback():
            if self.irq_callback:
                schedule(self.irq_callback, self.modem.poll_recv())

        self.modem.set_irq_callback(_irq_callback)

    def standby(self):
        """Put the radio in standby mode."""
        self.modem.standby()

    def sleep(self):
        """Put the radio in sleep mode."""
        self.modem.sleep()

    def irq_triggered(self):
        """Return whether a radio IRQ has been triggered."""
        return self.modem.irq_triggered()

    def deinit(self):
        """Put the radio in sleep mode."""
        self.sleep()
