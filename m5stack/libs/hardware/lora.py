# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
import machine
from lora import SX1262
from lora import RxPacket
from micropython import const, schedule


_M5PM1_ADDR = const(0x6E)
_M5PM1_REG_GPIO_MODE = const(0x10)
_M5PM1_REG_GPIO_OUT = const(0x11)
_M5PM1_REG_GPIO_DRV = const(0x13)
_M5PM1_REG_GPIO_FUNC0 = const(0x16)
_M5PM1_GPIO2_MASK = const(1 << 2)
_M5PM1_GPIO2_FUNC_MASK = const(0x03 << 4)

# SPI ID, SCK, MOSI, MISO, CS, BUSY, IRQ
_PORT_TABLE = {
    M5.BOARD.M5UnitC6L: (1, 20, 21, 22, 23, 19, 7),
    M5.BOARD.ArduinoNessoN1: (1, 20, 21, 22, 23, 19, 15),
    M5.BOARD.M5PaperMono: (2, 39, 38, 40, 41, 21, 5),
}


class LoRa:
    def __init__(
        self,
        pin_rst: int = -1,
        pin_cs: int = None,
        pin_irq: int = None,
        pin_busy: int = None,
        freq_khz: int = 868000,
        bw: str = "250",
        sf: int = 8,
        coding_rate: int = 8,
        preamble_len: int = 12,
        syncword: int = 0x12,
        output_power: int = 10,
    ):
        board_id = M5.getBoard()
        port = _PORT_TABLE.get(board_id, _PORT_TABLE[M5.BOARD.M5UnitC6L])

        spi_id, spi_sck, spi_mosi, spi_miso, default_cs, default_busy, default_irq = port
        pin_cs = default_cs if pin_cs is None else pin_cs
        pin_busy = default_busy if pin_busy is None else pin_busy
        pin_irq = default_irq if pin_irq is None else pin_irq

        if board_id == M5.BOARD.M5PaperMono:
            self._enable_papermono_lora()

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
            spi=machine.SPI(
                spi_id,
                sck=machine.Pin(spi_sck),
                mosi=machine.Pin(spi_mosi),
                miso=machine.Pin(spi_miso),
            ),
            reset=None,
            cs=machine.Pin(pin_cs),
            busy=machine.Pin(pin_busy),
            dio1=machine.Pin(pin_irq),
            dio3_tcxo_millivolts=3300,  # 3300mV
            lora_cfg=lora_cfg,
        )
        self.irq_callback = None

    def _enable_papermono_lora(self) -> None:
        i2c = machine.I2C(1, scl=machine.Pin(48), sda=machine.Pin(47), freq=100000)

        def update_register(register, mask, enabled):
            value = i2c.readfrom_mem(_M5PM1_ADDR, register, 1)[0]
            value = value | mask if enabled else value & ~mask
            i2c.writeto_mem(_M5PM1_ADDR, register, bytes((value,)))

        update_register(_M5PM1_REG_GPIO_FUNC0, _M5PM1_GPIO2_FUNC_MASK, False)
        update_register(_M5PM1_REG_GPIO_MODE, _M5PM1_GPIO2_MASK, True)
        update_register(_M5PM1_REG_GPIO_DRV, _M5PM1_GPIO2_MASK, False)
        update_register(_M5PM1_REG_GPIO_OUT, _M5PM1_GPIO2_MASK, True)

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
