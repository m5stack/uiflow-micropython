# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Module13.2 LoRa-1262 support."""

import machine
from driver.m5ioe1 import M5IOE1, Pin, RGB
from lora import RxPacket, SX1262

from . import mbus
from .lora868_v12 import LoRa868V12Module


_IOE_ADDR_MIN = 0x71
_IOE_ADDR_MAX = 0x74
_RGB_POWER_PIN = 1
_LORA_RESET_PIN = 2
_LORA_SWITCH_PIN = 3
_LORA_POWER_PIN = 5
_RGB_DATA_PIN = 14
_RGB_LED_COUNT = 3


class LoRa1262Module(LoRa868V12Module):
    """Create a Module13.2 LoRa-1262 object.

    The module uses the M-Bus SPI and I2C buses. M5IOE1 controls RGB power on
    G1, SX1262 reset on G2, antenna-switch enable on G3, LoRa power on G5, and
    three NeoPixels on G14.

    :param int pin_cs: SX1262 chip-select MCU pin. Default is 1 for CoreS3.
    :param int pin_irq: SX1262 DIO1 MCU pin. Default is 10 for CoreS3.
    :param int pin_busy: SX1262 BUSY MCU pin. Default is 2 for CoreS3.
    :param int ioe_addr: M5IOE1 I2C address, from 0x71 through 0x74.
    :param int freq_khz: RF frequency in kHz, from 850000 through 930000.
    :param str bw: LoRa bandwidth in kHz.
    :param int sf: Spreading factor, from 6 through 12.
    :param int coding_rate: Coding rate denominator, from 5 through 8.
    :param int preamble_len: Preamble length, from 5 through 255 symbols.
    :param int syncword: Sync word, from 1 through 255.
    :param int output_power: Output power in dBm, from -9 through 22.

    MicroPython Code Block:

        .. code-block:: python

            from module import LoRa1262Module

            lora1262 = LoRa1262Module(ioe_addr=0x71)
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
        pin_cs: int = 1,
        pin_irq: int = 10,
        pin_busy: int = 2,
        ioe_addr: int = 0x71,
        freq_khz: int = 868000,
        bw: str = "250",
        sf: int = 8,
        coding_rate: int = 8,
        preamble_len: int = 12,
        syncword: int = 0x12,
        output_power: int = 10,
    ) -> None:
        ioe_addr = int(ioe_addr)
        if not _IOE_ADDR_MIN <= ioe_addr <= _IOE_ADDR_MAX:
            raise ValueError("ioe_addr must be 0x71..0x74")
        self._validate_range(freq_khz, 850000, 930000)
        self._validate_range(sf, 6, 12)
        self._validate_range(coding_rate, 5, 8)
        self._validate_range(preamble_len, 5, 255)
        self._validate_range(syncword, 1, 255)
        self._validate_range(output_power, -9, 22)
        if bw not in self.BANDWIDTHS:
            raise ValueError("Invalid bandwidth %s" % bw)

        self.ioe1 = M5IOE1(mbus.i2c1, ioe_addr)
        self.rgb_power = Pin(self.ioe1, _RGB_POWER_PIN, Pin.OUT, value=1)
        self.lora_power = Pin(self.ioe1, _LORA_POWER_PIN, Pin.OUT, value=1)
        self.lora_switch = Pin(self.ioe1, _LORA_SWITCH_PIN, Pin.OUT, value=1)
        self.lora_reset = Pin(self.ioe1, _LORA_RESET_PIN, Pin.OUT, value=1)
        self.rgb = None
        self.modem = None
        self.irq_callback = None

        try:
            self.rgb = RGB(self.ioe1, io=_RGB_DATA_PIN, n=_RGB_LED_COUNT)
            self.rgb.clear()
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
        if self.rgb is not None:
            try:
                self.rgb.clear()
            except OSError:
                pass
        self.lora_switch.off()
        self.lora_power.off()
        self.rgb_power.off()

    def set_rgb_color(self, index: int, color: int) -> bool:
        """Set one of the three RGB LEDs.

        :param int index: LED index, from 0 through 2.
        :param int color: RGB888 color, from 0x000000 through 0xFFFFFF.
        :returns: True when the color is written.
        :rtype: bool
        """
        index = int(index)
        if not 0 <= index < _RGB_LED_COUNT:
            raise ValueError("index must be 0..2")
        return self.rgb.set_color(index, color, refresh=True)

    def fill_rgb(self, color: int) -> bool:
        """Set all three RGB LEDs to one RGB888 color."""
        return self.rgb.fill_color(color, refresh=True)

    def clear_rgb(self) -> bool:
        """Turn off all three RGB LEDs."""
        return self.rgb.clear(refresh=True)

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
        return super().send(packet, tx_at_ms)

    def recv(
        self, timeout_ms: int = None, rx_length: int = 0xFF, rx_packet: RxPacket = None
    ) -> RxPacket:
        """Receive one LoRa packet, or return None on timeout."""
        return super().recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self) -> None:
        """Start continuous LoRa reception."""
        return super().start_recv()

    def set_irq_callback(self, callback) -> None:
        """Register a callback for received LoRa packets."""
        return super().set_irq_callback(callback)

    def standby(self) -> None:
        """Put the SX1262 in standby mode."""
        return super().standby()

    def sleep(self) -> None:
        """Put the SX1262 in sleep mode."""
        return super().sleep()

    def irq_triggered(self) -> bool:
        """Return whether the SX1262 IRQ has triggered."""
        return super().irq_triggered()

    def deinit(self) -> None:
        """Clear LEDs, sleep the radio, and disable all module power controls."""
        if self.modem is not None:
            self.modem.sleep()
        self._power_off()
