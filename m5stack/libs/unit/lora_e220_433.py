# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import UART
import time
import struct
import _thread


class LoRaE220433Unit:
    #! Serial Port Baudrate
    BAUD_1200 = 0b000
    BAUD_2400 = 0b001
    BAUD_4800 = 0b010
    BAUD_9600 = 0b011
    BAUD_19200 = 0b100
    BAUD_38400 = 0b101
    BAUD_57600 = 0b110
    BAUD_115200 = 0b111

    #! Serial Port Parity Bit
    PARITY_NONE = 0b00
    PARITY_ODD = 0b01
    PARITY_EVEN = 0b10

    #! Air Rate Values
    AIRRATE_2_4K = 0b010
    AIRRATE_4_8K = 0b011
    AIRRATE_9_6K = 0b100
    AIRRATE_19_2K = 0b101
    AIRRATE_38_4K = 0b110
    AIRRATE_62_5K = 0b111

    #! Subpacket Size Values
    SUBPACKET_200_BYTE = 0b00
    SUBPACKET_128_BYTE = 0b01
    SUBPACKET_64_BYTE = 0b10
    SUBPACKET_32_BYTE = 0b11

    #! RSSI Ambient Noise Flag Values
    RSSI_AMBIENT_NOISE_ENABLE = 0b1
    RSSI_AMBIENT_NOISE_DISABLE = 0b0

    #! Transmitting Power Values
    TX_POWER_22dBm = 0b00
    TX_POWER_17dBm = 0b01
    TX_POWER_13dBm = 0b10
    TX_POWER_10dBm = 0b11

    #! Channel Control
    MIN_CHANNEL = 0
    MAX_CHANNEL = 83

    #! RSSI Byte Flag Values
    RSSI_BYTE_ENABLE = 0b1
    RSSI_BYTE_DISABLE = 0b0

    #! Transmission Method Type Values
    UART_TT_MODE = 0b0
    UART_P2P_MODE = 0b1

    #! LBT Flag Values
    LBT_ENABLE = 0b1
    LBT_DISABLE = 0b0

    #! WOR Cycle Values
    WOR_500MS = 0b000
    WOR_1000MS = 0b001
    WOR_1500MS = 0b010
    WOR_2000MS = 0b011
    WOR_2500MS = 0b100
    WOR_3000MS = 0b101
    WOR_3500MS = 0b110
    WOR_4000MS = 0b111

    def __init__(self, id=1, port=None) -> None:
        #! Initial the LoRa E220-433 Mhz Unit.
        self._uart = UART(
            id, tx=port[1], rx=port[0], baudrate=9600, bits=8, parity=None, stop=1, rxbuf=1024
        )
        self.tx = port[1]
        self.rx = port[0]
        self.recv_running = False
        self.receive_callback = None
        self.max_len = 200
        self._TXD_BUFFER = bytearray(self.max_len)
        self._RXD_BUFFER = bytearray(self.max_len)
        self.rssi_byte_flag = self.RSSI_BYTE_DISABLE

    def setup(
        self,
        own_address=0x0000,
        own_channel=0,
        encryption_key=0x0000,
        air_data_rate=AIRRATE_2_4K,  # noqa: N806
        subpacket_size=SUBPACKET_200_BYTE,  # noqa: N806
        rssi_ambient_noise_flag=RSSI_AMBIENT_NOISE_ENABLE,  # noqa: N806
        transmitting_power=TX_POWER_22dBm,  # noqa: N806
        rssi_byte_flag=RSSI_BYTE_ENABLE,
        transmission_method_type=UART_P2P_MODE,
        lbt_flag=LBT_DISABLE,
        wor_cycle=WOR_2000MS,
    ) -> None | bool:
        #! setup the fixed address, channel, baudrate, parity, air data rate etc...
        if not (self.MIN_CHANNEL <= own_channel <= self.MAX_CHANNEL):
            return False
        REG2 = (self.BAUD_9600 << 5) | (self.PARITY_NONE << 3) | air_data_rate  # noqa: N806
        REG3 = (subpacket_size << 6) | (rssi_ambient_noise_flag << 5) | transmitting_power  # noqa: N806
        REG4 = own_channel  # noqa: N806
        REG5 = (  # noqa: N806
            (rssi_byte_flag << 7) | (transmission_method_type << 6) | (lbt_flag << 4) | wor_cycle
        )
        self.rssi_byte_flag = rssi_byte_flag
        return self.write_command_format(own_address, REG2, REG3, REG4, REG5, encryption_key)

    def write_command_format(self, address, reg2, reg3, reg4, reg5, crypt=0x0000) -> None:
        #! write control command registers.
        command = [0xC0, 0x00, 0x08]
        command.extend([address >> 8, address & 0xFF])
        command.append(reg2)
        command.append(reg3)
        command.append(reg4)
        command.append(reg5)
        command.extend([crypt >> 8, crypt & 0xFF])
        self._uart.write(bytes(command))
        time.sleep_ms(100)  #! wait for response
        response = []
        if self._uart.any():
            response = self._uart.read()

        if len(response) != len(command):
            print(
                "[WARN] Setup LoRa unit failed, please check connection and wether unit in configuration mode."
            )
            return False
        return True

    def read_command_format(self) -> list:
        #! read control command registers.
        command = [0xC1, 0x00, 0x08]
        self._uart.write(bytes(command))
        time.sleep_ms(100)  #! wait for response
        response = []
        if self._uart.any():
            response = self._uart.read()

        if len(response) != (len(command) + 8):
            print(
                "[WARN] Setup LoRa unit failed, please check connection and wether unit in configuration mode."
            )

        own_address = (response[3] << 8 | response[4]) & 0xFFFF
        baudrate, parity, air_data_rate = (
            (response[5] >> 5) & 0x07,
            (response[5] >> 3) & 0x03,
            response[5] & 0x07,
        )
        subpacket_size, rssi_ambient_noise_flag, transmitting_power = (
            (response[6] >> 6) & 0x07,
            (response[6] >> 5) & 0x03,
            response[6] & 0x07,
        )
        channel = response[7] & 0x7F
        rssi_byte_flag, transmission_method_type, lbt_flag, wor_cycle = (
            (response[8] >> 7) & 0x01,
            (response[8] >> 6) & 0x01,
            (response[8] >> 4) & 0x01,
            response[8] & 0x07,
        )
        return (
            own_address,
            baudrate,
            parity,
            air_data_rate,
            subpacket_size,
            rssi_ambient_noise_flag,
            transmitting_power,
            channel,
            rssi_byte_flag,
            transmission_method_type,
            lbt_flag,
            wor_cycle,
        )

    def _recv_task(self) -> None:
        #! receive callback function.
        _ = self._uart.read()
        while self.recv_running:
            response, rssi = self.receive()
            if len(response):
                self.receive_callback(response, rssi)
            time.sleep_ms(10)

    def receive_none_block(self, receive_callback) -> None:
        #! start receive callback.
        if not self.recv_running:
            self.recv_running = True
            self.receive_callback = receive_callback
            _thread.start_new_thread(self._recv_task, ())

    def stop_receive(self) -> None:
        #! stop receive callback.
        self.recv_running = False
        time.sleep_ms(50)
        self.receive_callback = None

    def available_data(self) -> int:
        #! available of data.
        return self._uart.any()

    def receive(self, timeout=1000) -> None:
        #! receive of polling message.
        start = time.ticks_ms()
        read_length = 0
        response = bytes()
        rssi = 1
        while True:
            if time.ticks_ms() - start > timeout:
                break

            if self._uart.any():
                read_length += self._uart.readinto(self._RXD_BUFFER)
            elif read_length > 0:
                time.sleep_ms(10)
                if not self._uart.any():
                    rxd_buffer = memoryview(self._RXD_BUFFER[0:read_length])
                    if self.rssi_byte_flag == self.RSSI_BYTE_ENABLE:
                        response, rssi = struct.unpack_from(
                            "<%dsB" % (read_length - 1), rxd_buffer
                        )
                        rssi = rssi - 256
                    else:
                        response = struct.unpack_from("<%ds" % read_length, rxd_buffer)[0]
                    break
            time.sleep_ms(10)
        return response, rssi

    def send(self, target_address, target_channel, send_data) -> None:
        #! send the message.
        if len(send_data) > self.max_len:  # Adjust based on allowed packet size
            print("ERROR: Length of send_data over %d bytes." % self.max_len)
            return False

        frame = memoryview(self._TXD_BUFFER[0 : 3 + len(send_data)])
        struct.pack_into(">HB", frame, 0, target_address, target_channel)
        if isinstance(send_data, str):
            struct.pack_into("%ds" % len(send_data), frame, 3, send_data)
        else:
            for i in range(len(send_data)):
                frame[3 + i] = send_data[i]
        self._uart.write(frame)

        return True
