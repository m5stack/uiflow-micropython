# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import spi2
from machine import Pin, SPI
from lora import SX1262
from lora import RxPacket
from micropython import const, schedule


class LoRaSx1262Module:
    """
    constant: Valid bandwidth
    """

    BANDWIDTHS = ("7.8", "10.4", "15.6", "20.8", "31.25", "41.7", "62.5", "125", "250", "500")

    def __init__(
        self,
        pin_rst=5,
        pin_cs=1,
        pin_irq=10,
        pin_busy=2,
        freq_khz=868000,
        bw: str = "250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    ):
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
            spi=spi2,
            reset=Pin(pin_rst),
            cs=Pin(pin_cs),
            busy=Pin(pin_busy),
            dio1=Pin(pin_irq),
            dio3_tcxo_millivolts=3300,  # 3300mV
            lora_cfg=lora_cfg,
        )

        self.irq_callback = None

    def _validate_range(self, value, min, max):
        if value < min or value > max:
            raise ValueError(f"Value {value} out of range {min} to {max}")

    def send(self, packet, tx_at_ms=None) -> int:
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, list | tuple):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes([packet])

        return self.modem.send(packet, tx_at_ms)

    def recv(self, timeout_ms=None, rx_length=0xFF, rx_packet: RxPacket = None) -> RxPacket:
        return self.modem.recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self):
        self.modem.start_recv(continuous=True)

    def set_irq_callback(self, callback):
        def _irq_callback():
            if self.irq_callback:
                schedule(self.irq_callback, self.modem.poll_recv())

        self.irq_callback = callback
        self.modem.set_irq_callback(_irq_callback)

    def standby(self):
        self.modem.standby()

    def sleep(self):
        self.modem.sleep()

    def irq_triggered(self) -> bool:
        return self.modem.irq_triggered()
