# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus
import machine
import micropython
from driver.cc1101 import CC1101 as CC1101Driver, CC1101Packet


class CC1101Module:
    """Create a CC1101Module object.

    :param int pin_cs: (CS) Chip select pin number.
    :param int pin_gdo0: (GDO0) Interrupt pin number.
    :param int pin_gdo2: (GDO2) Optional interrupt pin number.
    :param float freq_khz: CC1101 RF frequency in kHz, with a range of 855000 kHz to 928000 kHz.
    :param float bitrate_kbps: Data rate in kbps, range from 0.6 to 6.0 kbps.
    :param float freq_dev_khz: Frequency deviation in kHz, range from 1.6 to 380 kHz.
    :param float rx_bw_khz: Receiver bandwidth in kHz, range from 58 to 812 kHz.
    :param int output_power: Output power in dBm, range from -30 to 10 dBm.
    :param int preamble_length: Preamble length in bits, options: 16, 24, 32, 48, 64, 96, 128, 192.
    :param int sync_word_h: High byte of sync word (0x00 to 0xFF).
    :param int sync_word_l: Low byte of sync word (0x00 to 0xFF).

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import CC1101Module

            module_cc1101_0 = CC1101Module(5, 7, 10, 868000.0, 2.4, 25.4, 58.0, 10, 16, 0x12, 0xAD)
    """

    def __init__(
        self,
        pin_cs: int = 5,
        pin_gdo0: int = 7,
        pin_gdo2: int = 10,
        freq_khz: float = 868000.0,
        bitrate_kbps: float = 2.4,
        freq_dev_khz: float = 25.4,
        rx_bw_khz: float = 58.0,
        output_power: int = 10,
        preamble_length: int = 16,
        sync_word_h: int = 0x12,
        sync_word_l: int = 0xAD,
    ):
        # Valid preamble lengths
        self.PREAMBLE_LENGTHS = (16, 24, 32, 48, 64, 96, 128, 192)
        self._validate_range(preamble_length, 16, 192)
        self._validate_range(sync_word_h, 0, 0xFF)
        self._validate_range(sync_word_l, 0, 0xFF)
        self._validate_range(output_power, -30, 10)

        # Initialize the CC1101 driver
        self.driver = CC1101Driver(spi=mbus.spi, ss=pin_cs, gdo0=pin_gdo0, gdo2=pin_gdo2)

        # Configuration parameters (store in kHz for consistency, but convert to MHz for driver)
        self.frequency = freq_khz  # Store in kHz
        self.bitrate = bitrate_kbps
        self.freq_dev = freq_dev_khz
        self.rx_bw = rx_bw_khz
        self.power = output_power
        self.preamble_length = preamble_length
        self.sync_word_h = sync_word_h
        self.sync_word_l = sync_word_l

        # Set sync words
        self.driver.sync_word_h = self.sync_word_h
        self.driver.sync_word_l = self.sync_word_l

        # Initialize the module (same as original simple_impl)
        # Convert kHz to MHz for driver (driver expects MHz)
        cc1101_cfg = {
            "freq": self.frequency / 1000.0,  # Convert kHz to MHz
            "br": self.bitrate,
            "freq_dev": self.freq_dev,
            "rx_bw": self.rx_bw,
            "pwr": self.power,
            "preamble_length": self.preamble_length,
        }
        self.driver.begin(**cc1101_cfg)

        # Start receive mode for polling
        self.driver._start_receive()

        self.rx_irq_callback = None
        self.tx_irq_callback = None

    def _validate_range(self, value, min_val, max_val):
        if value < min_val or value > max_val:
            raise ValueError(f"Value {value} out of range {min_val} to {max_val}")

    def set_freq(self, freq_khz: int = 868000) -> None:
        """Set frequency in kHz.

        :param int freq_khz: Frequency in kHz. Valid ranges: 855000-928000. Default is 868000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_freq(868000.0)
        """
        # Check if frequency is in any of the valid ranges
        valid = 855000 <= freq_khz <= 928000
        if not valid:
            raise ValueError(f"Frequency {freq_khz} kHz not in valid ranges (855000-928000)")

        self.frequency = freq_khz
        # Convert kHz to MHz for driver (driver expects MHz)
        self.driver._set_frequency(freq_khz / 1000.0)

    def set_bitrate(self, bitrate_kbps: float) -> None:
        """Set data rate in kbps.

        :param float bitrate_kbps: Data rate in kbps (0.6 ~ 6.0)

        UiFlow2 Code Block:

            |set_bitrate.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_bitrate(2.4)
        """
        self._validate_range(bitrate_kbps, 0.6, 6.0)
        self.bitrate = bitrate_kbps
        self.driver._set_bitrate(bitrate_kbps)

    def set_freq_dev(self, freq_dev_khz: float) -> None:
        """Set frequency deviation in kHz.

        :param float freq_dev_khz: Frequency deviation in kHz (1.6 ~ 380)

        UiFlow2 Code Block:

            |set_freq_dev.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_freq_dev(25.4)
        """
        self._validate_range(freq_dev_khz, 1.6, 380)
        self.freq_dev = freq_dev_khz
        self.driver._set_frequency_deviation(freq_dev_khz)

    def set_rx_bw(self, rx_bw_khz: float) -> None:
        """Set receiver bandwidth in kHz.

        :param float rx_bw_khz: Receiver bandwidth in kHz (58 ~ 812)

        UiFlow2 Code Block:

            |set_rx_bw.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_rx_bw(58.0)
        """
        self._validate_range(rx_bw_khz, 58, 812)
        self.rx_bw = rx_bw_khz
        self.driver._set_rx_bandwidth(rx_bw_khz)

    def set_output_power(self, output_power: int) -> None:
        """Set output power in dBm.

        :param int output_power: Output power in dBm (-30 ~ 10)

        UiFlow2 Code Block:

            |set_output_power.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_output_power(10)
        """
        self._validate_range(output_power, -30, 10)
        self.power = output_power
        self.driver._set_output_power(output_power)

    def set_preamble_length(self, preamble_length: int) -> None:
        """Set preamble length in bits.

        :param int preamble_length: Preamble length in bits, must be one of:
                                   16, 24, 32, 48, 64, 96, 128, 192.

        UiFlow2 Code Block:

            |set_preamble_length.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_preamble_length(16)
        """
        if preamble_length not in self.PREAMBLE_LENGTHS:
            raise ValueError(
                f"Invalid preamble length {preamble_length}, must be one of {self.PREAMBLE_LENGTHS}"
            )
        self.preamble_length = preamble_length
        self.driver._set_preamble_length(preamble_length)

    def set_sync_word(self, sync_word_h: int, sync_word_l: int) -> None:
        """Set sync word.

        :param int sync_word_h: High byte of sync word (0 ~ 0xFF)
        :param int sync_word_l: Low byte of sync word (0 ~ 0xFF)

        UiFlow2 Code Block:

            |set_sync_word.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.set_sync_word(0x12, 0xAD)
        """
        self._validate_range(sync_word_h, 0, 0xFF)
        self._validate_range(sync_word_l, 0, 0xFF)
        self.sync_word_h = sync_word_h
        self.sync_word_l = sync_word_l
        self.driver._set_sync_word(sync_word_h, sync_word_l)

    def send(self, packet: str | list | tuple | int | bytearray) -> bool:
        """Send data

        :param str | list | tuple | int | bytearray packet: The data to be sent.
        :returns: True if successful, False otherwise
        :rtype: bool

        Send a data packet and return True if successful.

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.send("Hello World")
        """
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, list | tuple):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes([packet])

        return self.driver.transmit(packet)

    def recv(self, timeout_ms: int = None) -> CC1101Packet | None:
        """Receive data

        :param int timeout_ms: Timeout in milliseconds (optional). Default is None.
        :returns: Received packet instance or None if timeout
        :rtype: CC1101Packet | None

        Attempt to receive a CC1101 packet. Returns `None` if timeout occurs, or returns the received packet instance.

        UiFlow2 Code Block:

            |recv.png|

        MicroPython Code Block:

            .. code-block:: python

                packet = module_cc1101_0.recv()
                if packet:
                    if packet.crc_ok:
                        print(f"Received: {packet.decode()}")
                        print(f"RSSI: {packet.rssi} dBm")
                        print(f"LQI: {packet.lqi}")
                    else:
                        print("CRC error")
        """
        # 轮询模式：检查是否有数据包可用
        if self.driver.check_for_packet():
            result = self.driver._read_data()
            if result and len(result) == 2:
                data, crc_ok = result
                if data:
                    return CC1101Packet(
                        data, self.driver.get_rssi(), self.driver.get_lqi(), crc_ok
                    )
        return None

    def start_recv(self) -> None:
        """Start receive data

        This method initiates the process to begin receiving data.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.start_recv()
        """
        self.driver.start_receive()

    def set_rx_irq_callback(self, callback) -> None:
        """Set the receive interrupt callback function to be executed on IRQ.

        :param callback: The callback function to be invoked when the interrupt is triggered.
                          The callback should take a CC1101Packet parameter and return nothing.

        UiFlow2 Code Block:

            |set_rx_irq_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_packet_received(packet):
                    print(f"Received: {packet.decode()}")

                module_cc1101_0.set_rx_irq_callback(on_packet_received)
        """
        self.rx_irq_callback = callback

        def _rx_irq_callback(packet):
            if self.rx_irq_callback:
                micropython.schedule(self.rx_irq_callback, packet)

        self.driver.set_rx_callback(_rx_irq_callback)

    def set_tx_irq_callback(self, callback) -> None:
        """Set the transmit interrupt callback function to be executed on IRQ.

        :param callback: The callback function to be invoked when the interrupt is triggered.
                          The callback should take one parameter (pin object, can be ignored) and return nothing.

        UiFlow2 Code Block:

            |set_tx_irq_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_packet_sent(_):
                    print("Packet sent successfully")

                module_cc1101_0.set_tx_irq_callback(on_packet_sent)
        """
        self.tx_irq_callback = callback

        def _tx_irq_callback(_):
            if self.tx_irq_callback:
                micropython.schedule(self.tx_irq_callback, None)

        self.driver.set_tx_callback(_tx_irq_callback)

    def standby(self) -> None:
        """Set module to standby mode.

        Puts the CC1101 module into standby mode, consuming less power.

        UiFlow2 Code Block:

            |standby.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.standby()
        """
        self.driver.standby()

    def rx_irq_triggered(self) -> bool:
        """Check IRQ trigger.

        :returns: Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or receive started.
        :rtype: bool

        UiFlow2 Code Block:

            |rx_irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.rx_irq_triggered()
        """
        return self.driver.rx_irq_triggered()

    def tx_irq_triggered(self) -> bool:
        """Check TX IRQ trigger.

        :returns: Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or a receive started.
        :rtype: bool

        UiFlow2 Code Block:

            |tx_irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                module_cc1101_0.tx_irq_triggered()
        """
        return self.driver.tx_irq_triggered()

    def get_rssi(self) -> float:
        """Get last received RSSI in dBm.

        :returns: RSSI value in dBm
        :rtype: float

        UiFlow2 Code Block:

            |get_rssi.png|

        MicroPython Code Block:

            .. code-block:: python

                rssi = module_cc1101_0.get_rssi()
        """
        return self.driver.get_rssi()

    def get_lqi(self) -> int:
        """Get last received LQI (Link Quality Indicator).

        :returns: LQI value (0-127)
        :rtype: int

        UiFlow2 Code Block:

            |get_lqi.png|

        MicroPython Code Block:

            .. code-block:: python

                lqi = module_cc1101_0.get_lqi()
        """
        return self.driver.get_lqi()

    def get_status(self) -> dict:
        """Get module status.

        :returns: Dictionary containing MARC state, RSSI, and LQI
        :rtype: dict

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = module_cc1101_0.get_status()
        """
        return self.driver.get_status()
