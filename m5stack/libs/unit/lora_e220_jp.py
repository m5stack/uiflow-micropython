# -*- encoding: utf-8 -*-
'''
@File    :   _imu_pro.py
@Time    :   2023/11/06 xx:xx:xx
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2023, M5STACK
@Desc    :   The LoRaE220 Unit is a LoRa communication module, designed for the 920MHz frequency band.
'''
# UART: ['any', 'read', 'readinto', 'readline', 'write', 'INV_CTS', 'INV_RTS', 'INV_RX', 'INV_TX', 'deinit', 'init', 'sendbreak']
import machine
import time
import _thread

class Def:
    # Baud Rate Values
    BAUD_1200   = 0b000
    BAUD_2400   = 0b001
    BAUD_4800   = 0b010
    BAUD_9600   = 0b011
    BAUD_19200  = 0b100
    BAUD_38400  = 0b101
    BAUD_57600  = 0b110
    BAUD_115200 = 0b111

    # Data Rate Values
    BW125K_SF5 = 0b00000
    BW125K_SF6 = 0b00100
    BW125K_SF7 = 0b01000
    BW125K_SF8 = 0b01100
    BW125K_SF9 = 0b10000
    BW250K_SF5 = 0b00001
    BW250K_SF6 = 0b00101
    BW250K_SF7 = 0b01001
    BW250K_SF8 = 0b01101
    BW250K_SF9 = 0b10001
    BW250K_SF10 = 0b10101
    BW500K_SF5 = 0b00010
    BW500K_SF6 = 0b00110
    BW500K_SF7 = 0b01010
    BW500K_SF8 = 0b01110
    BW500K_SF9 = 0b10010
    BW500K_SF10 = 0b10110
    BW500K_SF11 = 0b11010

    # Subpacket Size Values
    SUBPACKET_200_BYTE = 0b00
    SUBPACKET_128_BYTE = 0b01
    SUBPACKET_64_BYTE = 0b10
    SUBPACKET_32_BYTE = 0b11

    # RSSI Ambient Noise Flag Values
    RSSI_AMBIENT_NOISE_ENABLE = 0b1
    RSSI_AMBIENT_NOISE_DISABLE = 0b0

    # Transmitting Power Values
    TX_POWER_13dBm = 0b01
    TX_POWER_7dBm = 0b10
    TX_POWER_0dBm = 0b11

    # RSSI Byte Flag Values
    RSSI_BYTE_ENABLE = 0b1
    RSSI_BYTE_DISABLE = 0b0

    # Transmission Method Type Values
    UART_TT_MODE = 0b0
    UART_P2P_MODE = 0b1

    # LBT Flag Values
    LBT_ENABLE = 0b1
    LBT_DISABLE = 0b0

    # WOR Cycle Values
    WOR_500MS = 0b000
    WOR_1000MS = 0b001
    WOR_1500MS = 0b010
    WOR_2000MS = 0b011

class LoRaE220JPUnit:
    def __init__(self, port, port_id = 1) -> None:
        # print('Port: ', port)
        self.uart = machine.UART(port_id, tx=port[1], rx=port[0])
        self.uart.init(9600, bits=0, parity=None, stop=1, rxbuf=1024)
        self.recv_running = False
        self.receive_callback = None

    def _conf_range(self, target, min, max):
        return min <= target <= max
    
    def setup(self, own_address = 0, own_channel = 0, encryption_key = 0x2333, air_data_rate = Def.BW125K_SF9, subpacket_size = Def.SUBPACKET_200_BYTE, rssi_ambient_noise_flag = Def.RSSI_AMBIENT_NOISE_ENABLE, transmitting_power = Def.TX_POWER_13dBm,rssi_byte_flag = Def.RSSI_BYTE_ENABLE, transmission_method_type = Def.UART_P2P_MODE, lbt_flag = Def.LBT_DISABLE, wor_cycle = Def.WOR_2000MS):
        if not self._conf_range(own_channel, 0, 30):
            return False
        
        self.subpacket_size = subpacket_size
        self.max_len = 0
        if self.subpacket_size == Def.SUBPACKET_128_BYTE:
            self.max_len = 128
        elif self.subpacket_size == Def.SUBPACKET_64_BYTE:
            self.max_len = 64
        elif self.subpacket_size == Def.SUBPACKET_32_BYTE:
            self.max_len = 32
        else:
            self.max_len = 200

        command = [0xc0, 0x00, 0x08]
        ADDH = own_address >> 8
        ADDL = own_address & 0xff
        command.extend([ADDH, ADDL])

        REG0 = (Def.BAUD_9600 << 5) | air_data_rate
        command.append(REG0)

        REG1 = (subpacket_size << 6) | (rssi_ambient_noise_flag << 5) | transmitting_power
        command.append(REG1)

        command.append(own_channel)

        REG3 = (rssi_byte_flag << 7) | (transmission_method_type << 6) | (lbt_flag << 4) | wor_cycle
        command.append(REG3)

        CRYPT_H = encryption_key >> 8
        CRYPT_L = encryption_key & 0xff
        command.extend([CRYPT_H, CRYPT_L])

        self.uart.write(bytes(command))
        
        time.sleep_ms(100) # wait for response

        response = []
        if self.uart.any():
            response = self.uart.read()

        if len(response) != len(command):
            print("[WARN] Setup LoRa unit failed, please check connection and wether unit in configuration mode.")
            return False
        return True
    
    def _recvCallback(self):
        response = bytes()
        rssi = 0
        _ = self.uart.read()
        while self.recv_running:
            if self.uart.any():
                response += self.uart.read()
            elif len(response) > 0:
                time.sleep_ms(10)
                if not self.uart.any():
                    rssi = int(response[-1]) - 256
                    self.receive_callback(response[:-1], rssi)
                    response = bytes()
            time.sleep_ms(10)
    
    def receiveNoneBlock(self, receive_callback):
        if not self.recv_running:
            self.recv_running = True
            self.receive_callback = receive_callback
            _thread.start_new_thread(self._recvCallback, ())

    def stopReceive(self):
        self.recv_running = False
        time.sleep_ms(50)
        self.receive_callback = None
    
    def receive(self, timeout = 1000):
        start = time.ticks_ms() 
        response = bytes()
        rssi = 0
        while True:
            if time.ticks_ms() - start > timeout:
                break

            if self.uart.any():
                response += self.uart.read()

            elif len(response) > 0:
                time.sleep_ms(10)
                if not self.uart.any():
                    rssi = int(response[-1]) - 256
                    break
            time.sleep_ms(10)
        return response[:-1], rssi
    
    def send(self, target_address, target_channel, send_data):
        if type(send_data) is str:
            send_data = send_data.encode('utf-8')

        if type(send_data) is list:
            send_data = bytearray(send_data)
            
        if len(send_data) > self.max_len:  # Adjust based on allowed packet size
            print('ERROR: Length of send_data over %d bytes.' %self.max_len)
            return False

        target_address_H = target_address >> 8
        target_address_L = target_address & 0xff

        frame = bytearray([target_address_H, target_address_L, target_channel])
        frame.extend(send_data)

        self.uart.write(frame)

        return True