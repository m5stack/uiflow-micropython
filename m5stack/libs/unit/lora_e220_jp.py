# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# UART: ['any', 'read', 'readinto', 'readline', 'write', 'INV_CTS', 'INV_RTS', 'INV_RX', 'INV_TX', 'deinit', 'init', 'sendbreak']
import machine
import time
import _thread
import struct


class LoRaE220JPUnit:
    # Baud Rate Values
    BAUD_1200 = 0b0000_0000
    BAUD_2400 = 0b0010_0000
    BAUD_4800 = 0b0100_0000
    BAUD_9600 = 0b0110_0000
    BAUD_19200 = 0b1000_0000
    BAUD_38400 = 0b1010_0000
    BAUD_57600 = 0b1100_0000
    BAUD_115200 = 0b1110_0000

    # Data Rate Values
    BW125K_SF5 = 0b0000_0000
    BW125K_SF6 = 0b0000_0100
    BW125K_SF7 = 0b0000_1000
    BW125K_SF8 = 0b0000_1100
    BW125K_SF9 = 0b0001_0000
    BW250K_SF5 = 0b0000_0001
    BW250K_SF6 = 0b0000_0101
    BW250K_SF7 = 0b0000_1001
    BW250K_SF8 = 0b0000_1101
    BW250K_SF9 = 0b0001_0001
    BW250K_SF10 = 0b0001_0101
    BW500K_SF5 = 0b0000_0010
    BW500K_SF6 = 0b0000_0110
    BW500K_SF7 = 0b0000_1010
    BW500K_SF8 = 0b0000_1110
    BW500K_SF9 = 0b0001_0010
    BW500K_SF10 = 0b0001_0110
    BW500K_SF11 = 0b0001_1010

    # Subpacket Size Values
    SUBPACKET_200_BYTE = 0b0000_0000
    SUBPACKET_128_BYTE = 0b0100_0000
    SUBPACKET_64_BYTE = 0b1000_0000
    SUBPACKET_32_BYTE = 0b1100_0000

    # RSSI Ambient Noise Flag Values
    RSSI_AMBIENT_NOISE_ENABLE = 0b0010_0000
    RSSI_AMBIENT_NOISE_DISABLE = 0b0000_0000

    # Transmitting Power Values
    TX_POWER_13dBm = 0b0000_0000
    TX_POWER_12dBm = 0b0000_0001
    TX_POWER_7dBm = 0b0000_0010
    TX_POWER_0dBm = 0b0000_0011

    # RSSI Byte Flag Values
    RSSI_BYTE_ENABLE = 0b1000_0000
    RSSI_BYTE_DISABLE = 0b0000_0000

    # Transmission Method Type Values
    UART_TT_MODE = 0b0000_0000
    UART_P2P_MODE = 0b0100_0000

    # LBT Flag Values
    # LBT_ENABLE = 0b0001_0000
    # LBT_DISABLE = 0b0000_0000

    # WOR Cycle Values
    WOR_500MS = 0b0000_0000
    WOR_1000MS = 0b0000_0001
    WOR_1500MS = 0b0000_0010
    WOR_2000MS = 0b0000_0011
    WOR_2500MS = 0b0000_0100
    WOR_3000MS = 0b0000_0101

    def __init__(self, id=1, port=None, port_id=1) -> None:
        # TODO: 2.0.6 移除 port_id 参数
        id = port_id
        self.uart = machine.UART(id, tx=port[1], rx=port[0])
        self.uart.init(9600, bits=0, parity=None, stop=1, rxbuf=1024)
        self.recv_running = False
        self.receive_callback = None
        self._TXD_BUFFER = bytearray(200)
        self._RXD_BUFFER = bytearray(200)
        self.max_len = 200
        self.rssi_byte_flag = self.RSSI_BYTE_DISABLE

    def _conf_range(self, target, min, max) -> bool:
        return min <= target <= max

    def setup(
        self,
        own_address=0,
        own_channel=0,
        encryption_key=0x2333,
        air_data_rate=0b0000_0010,  # BW500K_SF5
        subpacket_size=0b0000_0000,  # SUBPACKET_200_BYTE
        rssi_ambient_noise_flag=0b0000_0000,  # RSSI_AMBIENT_NOISE_DISABLE
        transmitting_power=0b0000_0000,  # TX_POWER_13dBm
        rssi_byte_flag=0b0000_0000,  # RSSI_BYTE_DISABLE
        transmission_method_type=0b0000_0000,  # UART_TT_MODE
        lbt_flag=0b0000_0000,  # LBT_DISABLE
        wor_cycle=0b0000_0011,  # WOR_2000MS
    ) -> bool:
        if not self._conf_range(own_channel, 0, 30):
            return False

        if subpacket_size == self.SUBPACKET_128_BYTE:
            self.max_len = 128
        elif subpacket_size == self.SUBPACKET_64_BYTE:
            self.max_len = 64
        elif subpacket_size == self.SUBPACKET_32_BYTE:
            self.max_len = 32
        else:
            self.max_len = 200

        # Configuration
        struct.pack_into(">B", self._TXD_BUFFER, 0, 0xC0)
        struct.pack_into(">B", self._TXD_BUFFER, 1, 0x00)
        struct.pack_into(">B", self._TXD_BUFFER, 2, 0x08)

        # Register Address 00H, 01H
        struct.pack_into(">H", self._TXD_BUFFER, 3, own_address)

        # Register Address 02H
        reg0 = self.BAUD_9600 | air_data_rate
        struct.pack_into(">B", self._TXD_BUFFER, 5, reg0)

        # Register Address 03H
        reg1 = subpacket_size | rssi_ambient_noise_flag | transmitting_power
        struct.pack_into(">B", self._TXD_BUFFER, 6, reg1)

        # Register Address 04H
        struct.pack_into(">B", self._TXD_BUFFER, 7, own_channel)

        # Register Address 05H
        self.rssi_byte_flag = rssi_byte_flag
        reg3 = self.rssi_byte_flag | transmission_method_type | wor_cycle
        struct.pack_into(">B", self._TXD_BUFFER, 8, reg3)

        # Register Address 06H, 07H
        struct.pack_into(">H", self._TXD_BUFFER, 9, encryption_key)

        command = memoryview(self._TXD_BUFFER[0:11])
        self.uart.write(command)
        time.sleep_ms(100)  # wait for response

        response = []
        if self.uart.any():
            response = self.uart.read()

        if len(response) != len(command):
            print(
                "[WARN] Setup LoRa unit failed, please check connection and wether unit in configuration mode."
            )
            return False
        return True

    def _recv_task(self) -> None:
        response = bytes()
        rssi = 0
        _ = self.uart.read()
        while self.recv_running:
            response, rssi = self.receive()
            if len(response):
                self.receive_callback(response, rssi)
            time.sleep_ms(10)

    def receive_none_block(self, receive_callback) -> None:
        if not self.recv_running:
            self.recv_running = True
            self.receive_callback = receive_callback
            # FIXME: Threads cannot be automatically destroyed when the
            # application is interrupted.
            _thread.start_new_thread(self._recv_task, ())

    def receiveNoneBlock(self, receive_callback) -> None:  # noqa: N802
        return self.receive_none_block(receive_callback)

    def stop_receive(self) -> None:
        self.recv_running = False
        time.sleep_ms(50)
        self.receive_callback = None

    def stopReceive(self) -> None:  # noqa: N802
        return self.stop_receive()

    def receive(self, timeout=1000) -> tuple[bytes, int]:
        start = time.ticks_ms()
        read_length = 0
        response = bytes()
        rssi = 1
        while True:
            if time.ticks_ms() - start > timeout:
                break

            if self.uart.any():
                read_length += self.uart.readinto(self._RXD_BUFFER)
            elif read_length > 0:
                time.sleep_ms(10)
                if not self.uart.any():
                    rxd_buffer = memoryview(self._RXD_BUFFER[0:read_length])
                    if self.rssi_byte_flag == self.RSSI_BYTE_ENABLE:
                        response, rssi = struct.unpack_from(
                            "<%dsB" % (read_length - 1), rxd_buffer
                        )
                        rssi = rssi - 256
                    else:
                        response = struct.unpack_from("<%ds" % read_length, rxd_buffer)
                    break
            time.sleep_ms(10)
        return response, rssi

    def send(self, target_address: int, target_channel: int, send_data: bytes | str) -> bool:
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
        self.uart.write(frame)

        return True
