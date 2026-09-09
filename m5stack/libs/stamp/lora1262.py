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
        """Create and configure an SX1262 LoRa radio.

        :param int freq_khz: Carrier frequency in kHz, from 868000 to 923000.
        :param str bw: Bandwidth in kHz. Supported values are ``"7.8"``,
                       ``"10.4"``, ``"15.6"``, ``"20.8"``, ``"31.25"``,
                       ``"41.7"``, ``"62.5"``, ``"125"``, ``"250"``, and
                       ``"500"``.
        :param int sf: Spreading factor, from 6 to 12.
        :param int coding_rate: Coding-rate denominator, from 5 to 8 for 4/N.
        :param int preamble_len: Preamble length in symbols, from 5 to 255.
        :param int syncword: LoRa sync word, from 1 to 255.
        :param int output_power: Output power in dBm, from -9 to 22.
        :param int sw: RF switch-enable pin. ``None`` uses the FPC12 mapping.
        :param int irq: SX1262 DIO1 pin. ``None`` uses the FPC12 mapping.
        :param int busy: SX1262 BUSY pin. ``None`` uses the FPC12 mapping.
        :param int reset: SX1262 reset pin. ``None`` uses the FPC12 mapping.
        :param int miso: SPI MISO pin. ``None`` uses the FPC12 mapping.
        :param int mosi: SPI MOSI pin. ``None`` uses the FPC12 mapping.
        :param int cs: SPI chip-select pin. ``None`` uses the FPC12 mapping.
        :param int clock: SPI clock pin. ``None`` uses the FPC12 mapping.
        :param int spi_id: Machine SPI controller ID. Default is 1.
        :raises ValueError: If a configuration value is out of range or the
                            current host has no FPC12 mapping and a pin is
                            missing.

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                from stamp import StampLoRa1262

                radio = StampLoRa1262()
        """
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
        self.tx_callback = None
        self.rx_callback = None
        self._tx_active = False
        self._continuous_rx = False
        self._scheduled_tx = self._dispatch_tx
        self._scheduled_rx = self._dispatch_rx

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
        """Set the LoRa carrier frequency.

        :param int freq_khz: Carrier frequency in kHz, from 868000 to 923000.
        :raises ValueError: If ``freq_khz`` is outside the supported range.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_freq(868000)
        """
        self._validate_range("freq_khz", freq_khz, self.MIN_FREQ_KHZ, self.MAX_FREQ_KHZ)
        self.modem.configure({"freq_khz": freq_khz})

    def set_sf(self, sf):
        """Set the LoRa spreading factor.

        :param int sf: Spreading factor, from 6 to 12.
        :raises ValueError: If ``sf`` is outside the supported range.

        UiFlow2 Code Block:

            |set_sf.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_sf(8)
        """
        self._validate_range("sf", sf, 6, 12)
        self.modem.configure({"sf": sf})

    def set_bw(self, bw):
        """Set the LoRa bandwidth.

        :param str bw: Bandwidth in kHz. Use one of :attr:`BANDWIDTHS`.
        :raises ValueError: If ``bw`` is not supported.

        UiFlow2 Code Block:

            |set_bw.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_bw("250")
        """
        if bw not in self.BANDWIDTHS:
            raise ValueError("invalid bandwidth %s" % bw)
        self.modem.configure({"bw": bw})

    def set_coding_rate(self, coding_rate):
        """Set the coding-rate denominator for 4/N coding.

        :param int coding_rate: Coding-rate denominator, from 5 to 8.
        :raises ValueError: If ``coding_rate`` is outside the supported range.

        UiFlow2 Code Block:

            |set_coding_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_coding_rate(8)
        """
        self._validate_range("coding_rate", coding_rate, 5, 8)
        self.modem.configure({"coding_rate": coding_rate})

    def set_syncword(self, syncword):
        """Set the LoRa sync word.

        :param int syncword: Sync word value, from 1 to 255.
        :raises ValueError: If ``syncword`` is outside the supported range.

        UiFlow2 Code Block:

            |set_syncword.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_syncword(0x12)
        """
        self._validate_range("syncword", syncword, 1, 255)
        self.modem.configure({"syncword": syncword})

    def set_preamble_len(self, preamble_len):
        """Set the LoRa preamble length.

        :param int preamble_len: Preamble length in symbols, from 5 to 255.
        :raises ValueError: If ``preamble_len`` is outside the supported range.

        UiFlow2 Code Block:

            |set_preamble_len.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_preamble_len(12)
        """
        self._validate_range("preamble_len", preamble_len, 5, 255)
        self.modem.configure({"preamble_len": preamble_len})

    def set_output_power(self, output_power):
        """Set the LoRa output power.

        :param int output_power: Output power in dBm, from -9 to 22.
        :raises ValueError: If ``output_power`` is outside the supported range.

        UiFlow2 Code Block:

            |set_output_power.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_output_power(10)
        """
        self._validate_range("output_power", output_power, -9, 22)
        self.modem.configure({"output_power": output_power})

    def send(self, packet, tx_at_ms=None):
        """Send a packet and return its transmission timestamp.

        :param packet: String, bytes-like object, list, tuple, or integer
                       payload. Strings are encoded as UTF-8 and integers are
                       sent as one-byte payloads.
        :param int tx_at_ms: Optional scheduled transmission timestamp.
        :returns: Transmission timestamp in milliseconds.
        :rtype: int

        UiFlow2 Code Block:

            |send.png| |send_return.png| |send_with_time_return.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.send("hello")
        """
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, (list, tuple)):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes((packet,))

        self._tx_active = True
        try:
            return self.modem.send(packet, tx_at_ms)
        finally:
            self._tx_active = False

    def recv(self, timeout_ms=None, rx_length=0xFF, rx_packet: RxPacket = None):
        """Receive one packet.

        :param int timeout_ms: Optional receive timeout in milliseconds.
        :param int rx_length: Maximum receive length in bytes.
        :param RxPacket rx_packet: Optional packet object to reuse.
        :returns: Received packet, or ``None`` on timeout.
        :rtype: RxPacket or None

        UiFlow2 Code Block:

            |recv.png| |recv_data_param.png|

        MicroPython Code Block:

            .. code-block:: python

                packet = radio.recv(timeout_ms=1000)
        """
        self._continuous_rx = False
        return self.modem.recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self):
        """Start continuous packet reception.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.start_recv()
        """
        self._continuous_rx = True
        self.modem.start_recv(continuous=True)

    def set_tx_callback(self, callback):
        """Register a callback for completed transmissions.

        :param callback: A no-argument callable, or ``None`` to clear it.

        UiFlow2 Code Block:

            |send_event.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_tx_callback(on_transmit)
        """
        self.tx_callback = callback
        self._configure_irq_callback()

    def set_rx_callback(self, callback):
        """Register a callback for valid packets in continuous reception.

        :param callback: A callable accepting one :class:`lora.RxPacket`, or
                         ``None`` to clear it. Call :meth:`start_recv` to
                         enable continuous reception.

        UiFlow2 Code Block:

            |receive_event.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.set_rx_callback(on_receive)
        """
        self.rx_callback = callback
        self._configure_irq_callback()

    def _configure_irq_callback(self):
        if self.tx_callback is None and self.rx_callback is None:
            self.modem.set_irq_callback(None)
            return

        def _irq_callback():
            if self._tx_active:
                if self.tx_callback:
                    schedule(self._scheduled_tx, None)
            elif self._continuous_rx:
                schedule(self._scheduled_rx, None)

        self.modem.set_irq_callback(_irq_callback)

    def _dispatch_tx(self, _):
        if self.tx_callback:
            self.tx_callback()

    def _dispatch_rx(self, _):
        packet = self.modem.poll_recv()
        if self.rx_callback and isinstance(packet, RxPacket):
            self.rx_callback(packet)

    def standby(self):
        """Put the radio in standby mode and stop continuous reception.

        UiFlow2 Code Block:

            |standby.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.standby()
        """
        self._continuous_rx = False
        self.modem.standby()

    def sleep(self):
        """Put the radio in sleep mode and stop continuous reception.

        UiFlow2 Code Block:

            |sleep.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.sleep()
        """
        self._continuous_rx = False
        self.modem.sleep()

    def irq_triggered(self):
        """Return whether a radio IRQ has been triggered.

        :returns: ``True`` if an IRQ is pending; otherwise ``False``.
        :rtype: bool

        UiFlow2 Code Block:

            |irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                radio.irq_triggered()
        """
        return self.modem.irq_triggered()

    def deinit(self):
        """Stop reception and put the radio in sleep mode.

        UiFlow2 Code Block:

            Use the deinit block in UiFlow2.

        MicroPython Code Block:

            .. code-block:: python

                radio.deinit()
        """
        self.sleep()
