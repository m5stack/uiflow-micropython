# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus

import machine
import micropython
from lora import SX1278
from lora import SX1276
from lora import RxPacket
import M5


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
        lora = LoraModule(pin_irq=35, pin_rst=13) # basic
        lora = LoraModule(pin_irq=35, pin_rst=25) # core2
        lora = LoraModule(pin_irq=10, pin_rst=5) # cores3
        lora.send("Hello, LoRa!")

        print(lora.recv())

        def callback(received_data):
            global lora
            print(received_data)
            lora.start_recv()
        lora.set_irq_callback(callback)
        lora.start_recv()

    """

    """
    constant: Select the LoRa frequency band.
    """
    LORA_433 = micropython.const(1)
    LORA_868 = micropython.const(2)

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
        bw: str = "125",
        coding_rate=8,
        preamble_len=12,
        output_power=20,
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

        if M5.getBoard() in (M5.BOARD.M5Stack, M5.BOARD.M5StackCore2, M5.BOARD.M5Tough):
            mbus.spi.init(baudrate=1000000, polarity=0, phase=0)
        print(mbus.spi)
        self.modem = sx_instance(
            spi=mbus.spi,
            cs=machine.Pin(pin_cs),
            dio0=machine.Pin(pin_irq),
            # dio1=machine.Pin(35),
            reset=machine.Pin(pin_rst),
            lora_cfg=lora_cfg,
        )

        self.irq_callback = None

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
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, list | tuple):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes([packet])

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

    def start_recv(self):
        """
        note: Start receiving data once, trigger an interrupt when data is received.
        """
        self.modem.start_recv(continuous=True)

    def set_irq_callback(self, callback):
        """
        note: Set the IRQ callback function.

        params:
            callback:
              note: The callback function. The function should accept one argument, which is the received data.
        """

        def _irq_callback():
            if self.irq_callback:
                micropython.schedule(self.irq_callback, self.modem.poll_recv())

        self.irq_callback = callback
        self.modem.set_irq_callback(_irq_callback)

    def standby(self):
        """
        note: Set the modem to standby mode.
        """
        self.modem.standby()

    def sleep(self):
        """
        note: Set the modem to sleep mode.
        """
        self.modem.sleep()

    def irq_triggered(self) -> bool:
        """
        note: Check if the IRQ has been triggered.
        """
        return self.modem.irq_triggered()
