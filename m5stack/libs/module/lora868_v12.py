# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus
import machine
import micropython
from lora import SX1262
from lora import RxPacket


class LoRa868V12Module:
    """Create an LoRa868V12Module object.

    :param int timer_id: The Timer ID. Range: 0~3. Default is 0.
    :param int pin_rst: (RST) Reset pin number.
    :param int pin_cs: (NSS) Chip select pin number.
    :param int pin_irq: (IRQ) Interrupt pin number.
    :param int pin_busy: (BUSY) Busy pin number.
    :param int freq_khz: LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
    :param str bw: Bandwidth, options include:
        - ``"7.8"``: 7.8 KHz
        - ``"10.4"``: 10.4 KHz
        - ``"15.6"``: 15.6 KHz
        - ``"20.8"``: 20.8 KHz
        - ``"31.25"``: 31.25 KHz
        - ``"41.7"``: 41.7 KHz
        - ``"62.5"``: 62.5 KHz
        - ``"125"``: 125 KHz
        - ``"250"``: 250 KHz
        - ``"500"``: 500 KHz
    :param int sf: Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    :param int coding_rate: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    :param int preamble_len: Length of the preamble sequence in symbols, range from 0 to 255.
    :param int syncword: Sync word to mark the start of the data frame, default is 0x12.
    :param int output_power: Output power in dBm, range from -9 to 22.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import LoRa868V12Module

            module_lora868v12_0 = LoRa868V12Module(5, 1, 10, 2, 868000, '250', 8, 8, 12, 0x12, 10)
    """

    def __init__(
        self,
        pin_rst: int = 5,
        pin_cs: int = 1,
        pin_irq: int = 10,
        pin_busy: int = 2,
        freq_khz: int = 868000,
        bw: str = "250",
        sf: int = 8,
        coding_rate: int = 8,
        preamble_len: int = 12,
        syncword: int = 0x12,
        output_power: int = 10,
    ):
        # Valid bandwidth
        self.BANDWIDTHS = (
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
        self._validate_range(sf, 6, 12)
        self._validate_range(coding_rate, 5, 8)
        if bw not in self.BANDWIDTHS:
            raise ValueError(f"Invalid bandwidth {bw}")

        lora_cfg = {
            "freq_khz": freq_khz,
            "sf": sf,
            "bw": bw,  # kHz
            "coding_rate": coding_rate,
            "syncword": syncword,
            "preamble_len": preamble_len,
            "output_power": output_power,  # -9dBm ~ 22dBm
        }

        self.modem = SX1262(
            spi=mbus.spi2,
            reset=machine.Pin(pin_rst),
            cs=machine.Pin(pin_cs),
            busy=machine.Pin(pin_busy),
            dio1=machine.Pin(pin_irq),
            dio3_tcxo_millivolts=3300,  # 3300mV
            lora_cfg=lora_cfg,
        )

        self.irq_callback = None

    def _validate_range(self, value, min, max):
        if value < min or value > max:
            raise ValueError(f"Value {value} out of range {min} to {max}")

    def set_freq(self, freq_khz: int = 868000) -> None:
        """Set frequency in kHz.

        :param int freq_khz: Frequency in kHz (850000 ~ 930000), default is 868000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_freq(868000)
        """
        self._validate_range(freq_khz, 850000, 930000)
        lora_cfg = {"freq_khz": freq_khz}
        self.modem.configure(lora_cfg)

    def set_sf(self, sf: int) -> None:
        """Set spreading factor (SF).

        :param int sf: Spreading factor (7 ~ 12)

        UiFlow2 Code Block:

            |set_sf.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_sf(7)
        """
        self._validate_range(sf, 7, 12)
        lora_cfg = {"sf": sf}
        self.modem.configure(lora_cfg)

    def set_bw(self, bw: str) -> None:
        """Set bandwidth.

        :param str bw: Bandwidth in kHz as string. Must be one of:
                       '7.8', '10.4', '15.6', '20.8', '31.25', '41.7',
                       '62.5', '125', '250', '500'.

        UiFlow2 Code Block:

            |set_bw.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_bw(bw)
        """
        if bw not in self.BANDWIDTHS:
            raise ValueError(f"Invalid bandwidth '{bw}', must be one of {self.BANDWIDTHS}")
        lora_cfg = {"bw": bw}
        self.modem.configure(lora_cfg)

    def set_coding_rate(self, coding_rate: int) -> None:
        """Set coding rate.

        :param int coding_rate: Coding rate (5 ~ 8)

        UiFlow2 Code Block:

            |set_coding_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_coding_rate(coding_rate)
        """
        self._validate_range(coding_rate, 5, 8)
        lora_cfg = {"coding_rate": coding_rate}
        self.modem.configure(lora_cfg)

    def set_syncword(self, syncword: int) -> None:
        """Set syncword.

        :param int syncword: Sync word (0 ~ 0xFF)

        UiFlow2 Code Block:

            |set_syncword.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_syncword(syncword)
        """
        self._validate_range(syncword, 0, 0xFF)
        lora_cfg = {"syncword": syncword}
        self.modem.configure(lora_cfg)

    def set_preamble_len(self, preamble_len: int) -> None:
        """Set preamble length.

        :param int preamble_len: Preamble length, range: 0~255.

        UiFlow2 Code Block:

            |set_preamble_len.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_preamble_len(preamble_len)
        """
        self._validate_range(preamble_len, 6, 65535)
        lora_cfg = {"preamble_len": preamble_len}
        self.modem.configure(lora_cfg)

    def set_output_power(self, output_power: int) -> None:
        """Set output power in dBm.

        :param int output_power: Output power in dBm (-9 ~ 22)

        UiFlow2 Code Block:

            |set_output_power.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_output_power(output_power)
        """
        self._validate_range(output_power, -9, 22)
        lora_cfg = {"output_power": output_power}
        self.modem.configure(lora_cfg)

    def send(self, packet: str | list | tuple | int | bytearray, tx_at_ms: int = None) -> int:
        """Send data

        :param str | list | tuple | int | bytearray packet: The data to be sent.
        :param int tx_at_ms: The timestamp in milliseconds when to send the data (optional). Default is None.
        :returns: timestamp
        :rtype: int

        Send a data packet and return the timestamp after the packet is sent.

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.send()
        """
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, list | tuple):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes([packet])
        return self.modem.send(packet, tx_at_ms)

    def recv(
        self, timeout_ms: int = None, rx_length: int = 0xFF, rx_packet: RxPacket = None
    ) -> RxPacket:
        """Receive data

        :param int timeout_ms: Timeout in milliseconds (optional). Default is None.
        :param int rx_length: Length of the data to be read. Default is 0xFF.
        :param RxPacket rx_packet: An instance of `RxPacket` (optional) to reuse.
        :returns: Received packet instance
        :rtype: RxPacket

        Attempt to receive a LoRa packet. Returns `None` if timeout occurs, or returns the received packet instance.

        UiFlow2 Code Block:

            |recv.png|

        MicroPython Code Block:

            .. code-block:: python

                data = module_lora868v12_0.recv()
        """
        return self.modem.recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self) -> None:
        """Start receive data

        This method initiates the process to begin receiving data.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.start_recv()
        """
        self.modem.start_recv(continuous=True)

    def set_irq_callback(self, callback) -> None:
        """Set the interrupt callback function to be executed on IRQ.

        :param callback: The callback function to be invoked when the interrupt is triggered.
                          The callback should not take any arguments and should return nothing.

        UiFlow2 Code Block:

            |set_irq_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.set_irq_callback()
        """
        self.irq_callback = callback

        def _irq_callback():
            if self.irq_callback:
                micropython.schedule(self.irq_callback, self.modem.poll_recv())

        self.modem.set_irq_callback(_irq_callback)

    def standby(self) -> None:
        """Set module to standby mode.

        Puts the LoRa module into standby mode, consuming less power.

        UiFlow2 Code Block:

            |standby.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.standby()
        """
        self.modem.standby()

    def sleep(self) -> None:
        """Set module to sleep mode.

        Reduces the power consumption by putting the module into deep sleep mode.

        UiFlow2 Code Block:

            |sleep.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.sleep()
        """
        self.modem.sleep()

    def irq_triggered(self) -> bool:
        """Check IRQ trigger.

        :returns: Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or receive started.
        :rtype: bool

        UiFlow2 Code Block:

            |irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                module_lora868v12_0.irq_triggered()
        """
        return self.modem.irq_triggered()
