# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import spi2

from machine import Pin, SPI
from lora import SX1278
from lora import SX1276
from lora import RxPacket
from micropython import const


class LoraModule:
    """
    note:
        cn: LoRa433_V1.1 模块是 M5Stack 堆叠模块系列的一部分，它是一个在 433MHz 频率下运行的 LoRa 通信模块，使用了 Ra-02 模块（SX1278 芯片）方案。
        en: The LoRa433_V1.1 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 433MHz frequency and utilizes the Ra-02 module (SX1278 chip) solution.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/module/Module-LoRa433_V1.1
        image: https://static-cdn.m5stack.com/resource/docs/products/module/Module-LoRa433_V1.1/img-dac09b0a-7367-4ed9-9374-b604f646ec3b.webp
        category: Module

    example: |
        from module import LoraModule
        lora = LoraModule()
        lora.send("Hello, LoRa!")
        print(lora.recv())

    """

    """
    constant: Select the LoRa frequency band.
    """
    LORA_433 = const(1)
    LORA_868 = const(2)

    """
    constant: Valid bandwidth
    """
    BANDWIDTHS = ("7.8", "10.4", "15.6", "20.8", "31.25", "41.7", "62.5", "125", "250", "500")

    def __init__(
        self,
        pin_cs=0,
        pin_irq=35,
        pin_rst=25,
        freq_band=LORA_433,
        sf=8,
        bw: str = "500",
        coding_rate=8,
        preamble_len=12,
        output_power=0,
    ):
        """
        note: Initialize the LoRa module.

        params:
            pin_cs:
              note: Chip select pin
            pin_irq:
              note: Interrupt pin
            pin_rst:
              note: Reset pin
            freq_band:
              field: dropdown
              note: LoRa RF frequency in kHz.
              options:
                433M: LORA_433
                868M: LORA_868
            sf:
              note: Spreading factor, Higher spreading factors allow reception of weaker signals but have slower data rate.
            bw:
              note: Bandwidth value in kHz. Must be exactly one of BANDWIDTHS
            coding_rate:
              note: Forward Error Correction (FEC) coding rate is expressed as a ratio, `4/N`.
            preamble_len:
              note: Length of the preamble sequence, in units of symbols.
            output_power:
              note: Output power in dBm.
        """
        freq_khz = freq_band == self.LORA_433 and 433000 or 868000
        sx_instance = freq_band == self.LORA_433 and SX1278 or SX1276
        self._validate_range(sf, 6, 12)
        self._validate_range(coding_rate, 5, 8)

        if bw not in self.BANDWIDTHS:
            raise ValueError(f"Invalid bandwidth {bw}")

        lora_cfg = {
            "freq_khz": freq_khz,
            "sf": sf,
            "bw": bw,  # kHz
            "coding_rate": coding_rate,
            "preamble_len": preamble_len,
            "output_power": output_power,  # dBm
        }

        self.modem = sx_instance(
            spi=spi2,
            cs=Pin(pin_cs),
            dio0=Pin(pin_irq),
            # dio1=Pin(35),
            reset=Pin(pin_rst),
            lora_cfg=lora_cfg,
        )

    def _validate_range(self, value, min, max):
        if value < min or value > max:
            raise ValueError(f"Value {value} out of range {min} to {max}")

    def send(self, packet, tx_at_ms=None) -> int:
        """
        note: Send a data packet.

        label:
            en: "%1 send packet %2 at time %3"
            cn: "%1 在 %3 时发送数据包 %2"

        params:
            packet:
              note: The data packet to send.
            tx_at_ms:
              note: Time to transmit the packet in milliseconds. For precise timing of sent packets, there is an optional `tx_at_ms` argument which is a timestamp (as a `time.ticks_ms()` value). If set, the packet will be sent as close as possible to this timestamp and the function will block until that time arrives

        return:
            note: The return value is the timestamp when transmission completed, as a`time.ticks_ms()` result. It will be more accurate if the modem was initialized to use interrupts.
        """
        return self.modem.send(packet, tx_at_ms)

    def recv(self, timeout_ms=None, rx_length=0xFF, rx_packet: RxPacket = None) -> RxPacket:
        """

        note: Receive a data packet.

        label:
            en: "%1 receive packet with timeout %2, rx_length %3, rx_packet %4"
            cn: "%1 接收数据包，超时 %2, 接收长度 %3, 接收数据包 %4"

        params:
            timeout_ms:
              note: Optional, sets a receive timeout in milliseconds. If None (default value), then the function will block indefinitely until a packet is received.
            rx_length:
              note: Necessary to set if `implicit_header` is set to `True` (see above). This is the length of the packet to receive. Ignored in the default LoRa explicit header mode, where the received radio header includes the length.
            rx_packet:
              note: Optional, this can be an `RxPacket` object previously received from the modem. If the newly received packet has the same length, this object is reused and returned to save an allocation. If the newly received packet has a different length, a new `RxPacket` object is allocated and returned instead.

        return:
            note: Returns None on timeout, or an `RxPacket` instance with the packet on success.
        """
        return self.modem.recv(timeout_ms, rx_length, rx_packet)
