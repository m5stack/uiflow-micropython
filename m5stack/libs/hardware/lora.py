# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import Pin, SPI
from lora import SX1262
from lora import RxPacket
from micropython import const, schedule
import machine


class LoRa:
    def __init__(
        self,
        pin_rst: int = -1,
        pin_cs: int = 23,
        pin_irq: int = 7,
        pin_busy: int = 19,
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
            spi=machine.SPI(1, sck=machine.Pin(20), mosi=machine.Pin(21), miso=machine.Pin(22)),
            reset=None,
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

    def set_freq(self, freq_khz: int = 868000) -> None:
        self._validate_range(freq_khz, 850000, 930000)
        lora_cfg = {"freq_khz": freq_khz}
        self.modem.configure(lora_cfg)

    def set_sf(self, sf: int) -> None:
        self._validate_range(sf, 6, 12)
        lora_cfg = {"sf": sf}
        self.modem.configure(lora_cfg)

    def set_bw(self, bw: str) -> None:
        if bw not in self.BANDWIDTHS:
            raise ValueError(f"Invalid bandwidth '{bw}', must be one of {self.BANDWIDTHS}")
        lora_cfg = {"bw": bw}
        self.modem.configure(lora_cfg)

    def set_coding_rate(self, coding_rate: int) -> None:
        self._validate_range(coding_rate, 5, 8)
        lora_cfg = {"coding_rate": coding_rate}
        self.modem.configure(lora_cfg)

    def set_syncword(self, syncword: int) -> None:
        self._validate_range(syncword, 1, 255)
        lora_cfg = {"syncword": syncword}
        self.modem.configure(lora_cfg)

    def set_preamble_len(self, preamble_len: int) -> None:
        self._validate_range(preamble_len, 5, 255)
        lora_cfg = {"preamble_len": preamble_len}
        self.modem.configure(lora_cfg)

    def set_output_power(self, output_power: int) -> None:
        self._validate_range(output_power, -9, 22)
        lora_cfg = {"output_power": output_power}
        self.modem.configure(lora_cfg)

    def send(self, packet: str | list | tuple | int | bytearray, tx_at_ms: int = None) -> int:
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, (list, tuple)):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes([packet])
        return self.modem.send(packet, tx_at_ms)

    def recv(
        self, timeout_ms: int = None, rx_length: int = 0xFF, rx_packet: RxPacket = None
    ) -> RxPacket:
        return self.modem.recv(timeout_ms, rx_length, rx_packet)

    def start_recv(self) -> None:
        self.modem.start_recv(continuous=True)

    def set_irq_callback(self, callback) -> None:
        self.irq_callback = callback

        def _irq_callback():
            if self.irq_callback:
                schedule(self.irq_callback, self.modem.poll_recv())

        self.modem.set_irq_callback(_irq_callback)

    def standby(self) -> None:
        self.modem.standby()

    def sleep(self) -> None:
        self.modem.sleep()

    def irq_triggered(self) -> bool:
        return self.modem.irq_triggered()
