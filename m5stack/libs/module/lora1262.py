# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Module13.2 LoRa-1262 support."""

import machine
from driver.m5ioe1 import M5IOE1, Pin
from lora import RxPacket, SX1262
from micropython import schedule

from . import mbus
from .lora868_v12 import LoRa868V12Module


_IOE_ADDR_MIN = 0x71
_IOE_ADDR_MAX = 0x74
_LORA_RESET_PIN = 2
_LORA_SWITCH_PIN = 3
_LORA_POWER_PIN = 5


class LoRa1262Module(LoRa868V12Module):
    """Create a Module13.2 LoRa-1262 object.

    The module uses the M-Bus SPI bus and a caller-supplied I2C bus. M5IOE1
    controls SX1262 reset on G2, antenna-switch enable on G3, and LoRa power
    on G5.

    :param i2c: Initialized I2C bus used to access the M5IOE1.
    :type i2c: machine.I2C
    :param int pin_cs: SX1262 chip-select MCU pin. Default is 1 for CoreS3.
    :param int pin_irq: SX1262 DIO1 MCU pin. Default is 10 for CoreS3.
    :param int pin_busy: SX1262 BUSY MCU pin. Default is 2 for CoreS3.
    :param int address: M5IOE1 I2C address, from 0x71 through 0x74.
    :param int freq_khz: RF frequency in kHz, from 850000 through 930000.
    :param str bw: LoRa bandwidth in kHz.
    :param int sf: Spreading factor, from 6 through 12.
    :param int coding_rate: Coding rate denominator, from 5 through 8.
    :param int preamble_len: Preamble length, from 5 through 255 symbols.
    :param int syncword: Sync word, from 1 through 255.
    :param int output_power: Output power in dBm, from -9 through 22.

    MicroPython Code Block:

        .. code-block:: python

            import M5
            from module import LoRa1262Module, mbus

            M5.begin()
            lora1262 = LoRa1262Module(mbus.i2c1, address=0x71)
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

    def __init__(
        self,
        i2c=None,
        pin_cs: int = 1,
        pin_irq: int = 10,
        pin_busy: int = 2,
        address: int = 0x71,
        freq_khz: int = 868000,
        bw: str = "250",
        sf: int = 8,
        coding_rate: int = 8,
        preamble_len: int = 12,
        syncword: int = 0x12,
        output_power: int = 10,
    ) -> None:
        address = int(address)
        if not _IOE_ADDR_MIN <= address <= _IOE_ADDR_MAX:
            raise ValueError("address must be 0x71..0x74")
        self._validate_range(freq_khz, 850000, 930000)
        self._validate_range(sf, 6, 12)
        self._validate_range(coding_rate, 5, 8)
        self._validate_range(preamble_len, 5, 255)
        self._validate_range(syncword, 1, 255)
        self._validate_range(output_power, -9, 22)
        if bw not in self.BANDWIDTHS:
            raise ValueError("Invalid bandwidth %s" % bw)

        if i2c is None:
            self.i2c = mbus.i2c1
        else:
            self.i2c = i2c
        self.ioe1 = M5IOE1(self.i2c, address)
        self.lora_power = Pin(self.ioe1, _LORA_POWER_PIN, Pin.OUT, value=1)
        self.lora_switch = Pin(self.ioe1, _LORA_SWITCH_PIN, Pin.OUT, value=1)
        self.lora_reset = Pin(self.ioe1, _LORA_RESET_PIN, Pin.OUT, value=1)
        self.modem = None
        self.tx_callback = None
        self.rx_callback = None
        self._tx_active = False
        self._continuous_rx = False
        self._scheduled_tx = self._dispatch_tx
        self._scheduled_rx = self._dispatch_rx

        try:
            self.modem = SX1262(
                spi=mbus.spi,
                reset=self.lora_reset,
                cs=machine.Pin(pin_cs, machine.Pin.OUT, value=1),
                busy=machine.Pin(pin_busy, machine.Pin.IN),
                dio1=machine.Pin(pin_irq, machine.Pin.IN),
                dio2_rf_sw=True,
                dio3_tcxo_millivolts=3300,
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
        except Exception:
            self._power_off()
            raise

    def _power_off(self):
        self.lora_switch.off()
        self.lora_power.off()

    def set_freq(self, freq_khz: int = 868000) -> None:
        """Set RF frequency in kHz, from 850000 through 930000."""
        return super().set_freq(freq_khz)

    def set_sf(self, sf: int) -> None:
        """Set the spreading factor from 6 through 12."""
        return super().set_sf(sf)

    def set_bw(self, bw: str) -> None:
        """Set bandwidth to a supported kHz string."""
        return super().set_bw(bw)

    def set_coding_rate(self, coding_rate: int) -> None:
        """Set the coding-rate denominator from 5 through 8."""
        return super().set_coding_rate(coding_rate)

    def set_syncword(self, syncword: int) -> None:
        """Set the sync word from 1 through 255."""
        return super().set_syncword(syncword)

    def set_preamble_len(self, preamble_len: int) -> None:
        """Set preamble length from 5 through 255 symbols."""
        return super().set_preamble_len(preamble_len)

    def set_output_power(self, output_power: int) -> None:
        """Set output power from -9 through 22 dBm."""
        return super().set_output_power(output_power)

    def send(self, packet: str | list | tuple | int | bytearray, tx_at_ms: int = None) -> int:
        """Send a LoRa packet and return its timestamp."""
        self._tx_active = True
        try:
            return super().send(packet, tx_at_ms)
        finally:
            self._tx_active = False

    def recv(
        self, timeout_ms: int = None, rx_length: int = 0xFF, rx_packet: RxPacket = None
    ) -> RxPacket:
        """Receive one LoRa packet, or return None on timeout."""
        self._continuous_rx = False
        return super().recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self) -> None:
        """Start continuous LoRa reception."""
        self._continuous_rx = True
        return super().start_recv()

    def set_tx_callback(self, callback) -> None:
        """Register a no-argument callback for completed transmissions."""
        self.tx_callback = callback
        self._configure_irq_callback()

    def set_rx_callback(self, callback) -> None:
        """Register a callback receiving an ``RxPacket`` for valid packets."""
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

    def standby(self) -> None:
        """Put the SX1262 in standby mode."""
        self._continuous_rx = False
        return super().standby()

    def sleep(self) -> None:
        """Put the SX1262 in sleep mode."""
        self._continuous_rx = False
        return super().sleep()

    def irq_triggered(self) -> bool:
        """Return whether the SX1262 IRQ has triggered."""
        return super().irq_triggered()

    def deinit(self) -> None:
        """Put the radio to sleep and disable its module power controls."""
        if self.modem is not None:
            self.sleep()
        self._power_off()
