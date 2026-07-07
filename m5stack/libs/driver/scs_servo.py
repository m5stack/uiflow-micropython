# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from machine import UART, Pin


# Instruction definitions
INST_PING = 0x01  # ping
INST_READ = 0x02  # read
INST_WRITE = 0x03  # write
INST_REG_WRITE = 0x04  # register write
INST_REG_ACTION = 0x05  # register write action
INST_SYNC_READ = 0x82  # sync read
INST_SYNC_WRITE = 0x83  # sync write

# SCSCL memory table definition
# EPROM (read-only)
SCSCL_VERSION_L = 3
SCSCL_VERSION_H = 4

# EPROM (read and write)
SCSCL_ID = 5
SCSCL_BAUD_RATE = 6
SCSCL_MIN_ANGLE_LIMIT_L = 9
SCSCL_MIN_ANGLE_LIMIT_H = 10
SCSCL_MAX_ANGLE_LIMIT_L = 11
SCSCL_MAX_ANGLE_LIMIT_H = 12
SCSCL_CW_DEAD = 26
SCSCL_CCW_DEAD = 27

# SRAM (read and write)
SCSCL_TORQUE_ENABLE = 40
SCSCL_GOAL_POSITION_L = 42
SCSCL_GOAL_POSITION_H = 43
SCSCL_GOAL_TIME_L = 44
SCSCL_GOAL_TIME_H = 45
SCSCL_GOAL_SPEED_L = 46
SCSCL_GOAL_SPEED_H = 47
SCSCL_LOCK = 48

# SRAM (read only)
SCSCL_PRESENT_POSITION_L = 56
SCSCL_PRESENT_POSITION_H = 57
SCSCL_PRESENT_SPEED_L = 58
SCSCL_PRESENT_SPEED_H = 59
SCSCL_PRESENT_LOAD_L = 60
SCSCL_PRESENT_LOAD_H = 61
SCSCL_PRESENT_VOLTAGE = 62
SCSCL_PRESENT_TEMPERATURE = 63
SCSCL_MOVING = 66
SCSCL_PRESENT_CURRENT_L = 69
SCSCL_PRESENT_CURRENT_H = 70

SCSCL_POSITION_MIN = 0
SCSCL_POSITION_MAX = 1000


class Scs:
    """SCS protocol layer - basic communication protocol implementation"""

    def __init__(self, end=0, level=1):
        self.level = level
        self.end = end
        self.error = 0
        self.sync_read_rx_packet_index = 0
        self.sync_read_rx_packet_len = 0
        self.sync_read_rx_packet = None

    def host2scs(self, data):
        """convert 16-bit data to two 8-bit data (consider byte order)"""
        if self.end:
            # big endian: high byte first
            return ((data >> 8) & 0xFF, data & 0xFF)
        else:
            # little endian: low byte first
            return (data & 0xFF, (data >> 8) & 0xFF)

    def scs2host(self, data_l, data_h):
        """convert two 8-bit data to 16-bit data (consider byte order)"""
        if self.end:
            # big endian: high byte first
            return (data_l << 8) | data_h
        else:
            # little endian: low byte first
            return (data_h << 8) | data_l

    def _write_buf(self, servo_id, mem_addr, data, inst):
        """build and send command packet"""
        msg_len = 2  # basic length: ID + Length + Instruction
        check_sum = servo_id

        # header
        self.write_scs(0xFF)
        self.write_scs(0xFF)
        self.write_scs(servo_id)

        if data and len(data) > 0:
            msg_len += len(data) + 1  # +1 for mem_addr
            self.write_scs(msg_len)
            self.write_scs(inst)
            self.write_scs(mem_addr)
            check_sum += msg_len + inst + mem_addr
            # write data
            for b in data:
                self.write_scs(b)
                check_sum += b
        else:
            self.write_scs(msg_len)
            self.write_scs(inst)
            check_sum += msg_len + inst

        # checksum (bitwise inversion)
        self.write_scs(~check_sum & 0xFF)

    def gen_write(self, servo_id, mem_addr, data):
        """normal write command

        :param servo_id: servo id
        :param mem_addr: memory address
        :param data: data bytes
        :return: success return 1, failure return 0
        """
        self.r_flush_scs()
        self._write_buf(servo_id, mem_addr, data, INST_WRITE)
        self.w_flush_scs()
        return self._ack(servo_id)

    def reg_write(self, servo_id, mem_addr, data):
        """async write command

        :param servo_id: servo id
        :param mem_addr: memory address
        :param data: data bytes
        :return: success return 1, failure return 0
        """
        self.r_flush_scs()
        self._write_buf(servo_id, mem_addr, data, INST_REG_WRITE)
        self.w_flush_scs()
        return self._ack(servo_id)

    def reg_write_action(self, servo_id=0xFE):
        """async write action command

        :param servo_id: servo id (default 0xFE is broadcast)
        :return: success return 1, failure return 0
        """
        self.r_flush_scs()
        self._write_buf(servo_id, 0, None, INST_REG_ACTION)
        self.w_flush_scs()
        return self._ack(servo_id)

    def sync_write(self, servo_ids, mem_addr, data_list):
        """sync write command (multiple servos)

        :param servo_ids: servo id list
        :type servo_ids: list
        :param mem_addr: memory address
        :param data_list: data list for each servo (each servo data length is the same)
        """
        self.r_flush_scs()

        idn = len(servo_ids)
        if idn == 0 or len(data_list) == 0:
            return

        data_len = len(data_list[0])  # each servo data length
        mes_len = (data_len + 1) * idn + 4

        check_sum = 0xFE + mes_len + INST_SYNC_WRITE + mem_addr + data_len

        # header
        self.write_scs(0xFF)
        self.write_scs(0xFF)
        self.write_scs(0xFE)  # broadcast id
        self.write_scs(mes_len)
        self.write_scs(INST_SYNC_WRITE)
        self.write_scs(mem_addr)
        self.write_scs(data_len)

        # write data for each servo
        for i, servo_id in enumerate(servo_ids):
            self.write_scs(servo_id)
            check_sum += servo_id
            for j, byte_val in enumerate(data_list[i]):
                self.write_scs(byte_val)
                check_sum += byte_val

        # checksum
        self.write_scs(~check_sum & 0xFF)
        self.w_flush_scs()

    def write_byte(self, servo_id, mem_addr, byte_val):
        """write 1 byte

        :param servo_id: servo id
        :param mem_addr: memory address
        :param byte_val: byte value
        :return: success return 1, failure return 0
        """
        return self.gen_write(servo_id, mem_addr, bytes([byte_val & 0xFF]))

    def write_word(self, servo_id, mem_addr, word_val):
        """write 2 bytes (16-bit)

        :param servo_id: servo id
        :param mem_addr: memory address
        :param word_val: 16-bit value
        :return: success return 1, failure return 0
        """
        data_l, data_h = self.host2scs(word_val)
        return self.gen_write(servo_id, mem_addr, bytes([data_l, data_h]))

    def read(self, servo_id, mem_addr, data_len):
        """read command

        :param servo_id: servo id
        :param mem_addr: memory address
        :param data_len: read length
        :return: read data bytes array, failure return None
        """
        self.r_flush_scs()
        self._write_buf(servo_id, mem_addr, bytes([data_len]), INST_READ)
        self.w_flush_scs()

        if not self._check_head():
            return None

        # read response header
        header = self.read_scs(3)
        if len(header) != 3:
            return None

        # read data
        data = self.read_scs(data_len)
        if len(data) != data_len:
            return None

        # read checksum
        checksum_byte = self.read_scs(1)
        if len(checksum_byte) != 1:
            return None

        # verify checksum
        cal_sum = header[0] + header[1] + header[2]
        for b in data:
            cal_sum += b
        cal_sum = ~cal_sum & 0xFF

        if cal_sum != checksum_byte[0]:
            return None

        self.error = header[2]  # error status
        return data

    def read_byte(self, servo_id, mem_addr):
        """read 1 byte

        :param servo_id: servo id
        :param mem_addr: memory address
        :return: read byte value, failure return -1
        """
        data = self.read(servo_id, mem_addr, 1)
        if data and len(data) == 1:
            return data[0]
        return -1

    def read_word(self, servo_id, mem_addr):
        """read 2 bytes (16-bit)

        :param servo_id: servo id
        :param mem_addr: memory address
        :return: read 16-bit value, failure return -1
        """
        data = self.read(servo_id, mem_addr, 2)
        if data and len(data) == 2:
            return self.scs2host(data[0], data[1])
        return -1

    def ping(self, servo_id):
        """ping command, return servo id

        :param servo_id: servo id
        :return: success return servo id, failure return -1
        """
        self.r_flush_scs()
        self._write_buf(servo_id, 0, None, INST_PING)
        self.w_flush_scs()

        self.error = 0
        if not self._check_head():
            return -1

        header = self.read_scs(4)
        if len(header) != 4:
            return -1

        if header[0] != servo_id and servo_id != 0xFE:
            return -1

        if header[1] != 2:
            return -1

        # verify checksum
        cal_sum = ~(header[0] + header[1] + header[2]) & 0xFF
        if cal_sum != header[3]:
            return -1

        self.error = header[2]
        return header[0]

    def _check_head(self):
        """check and wait response header (0xFF 0xFF)"""
        buf = [0, 0]
        cnt = 0

        while True:
            byte_data = self.read_scs(1)
            if len(byte_data) == 0:
                return False

            buf[1] = buf[0]
            buf[0] = byte_data[0]

            if buf[0] == 0xFF and buf[1] == 0xFF:
                return True

            cnt += 1
            if cnt > 10:
                return False

    def _ack(self, servo_id):
        """wait and verify ACK response

        :param servo_id: servo id
        :return: success return 1, failure return 0
        """
        self.error = 0
        if servo_id != 0xFE and self.level:
            if not self._check_head():
                return 0

            header = self.read_scs(4)
            if len(header) != 4:
                return 0

            if header[0] != servo_id:
                return 0

            if header[1] != 2:
                return 0

            # verify checksum
            cal_sum = ~(header[0] + header[1] + header[2]) & 0xFF
            if cal_sum != header[3]:
                return 0

            self.error = header[2]

        return 1

    # abstract method, need subclass implementation
    def write_scs(self, data):
        """write data"""
        raise NotImplementedError

    def read_scs(self, length):
        """read data"""
        raise NotImplementedError

    def r_flush_scs(self):
        """flush receive buffer"""
        raise NotImplementedError

    def w_flush_scs(self):
        """flush send buffer"""
        raise NotImplementedError


class ScsSerial(Scs):
    """SCS UART hardware interface layer"""

    def __init__(self, uart, end=1, level=1):
        """initialize UART interface

        :param uart: MicroPython UART object
        :param end: byte order (0=little endian, 1=big endian)
        :param level: return level
        """
        super().__init__(end, level)
        self.uart = uart
        self.io_timeout = 250  # milliseconds

    def write_scs(self, data):
        """write data to UART

        :param data: can be integer (single byte) or byte array
        :type data: int or bytes
        """
        if isinstance(data, int):
            self.uart.write(bytes([data & 0xFF]))
        else:
            self.uart.write(data)

    def read_scs(self, length):
        """read data from UART (with timeout)

        :param length: length to read
        :return: read byte array
        """
        data = bytearray()
        start_time = time.ticks_ms()

        while len(data) < length:
            if self.uart.any() > 0:
                byte_data = self.uart.read(1)
                if byte_data:
                    data.extend(byte_data)
                    start_time = time.ticks_ms()  # 重置超时

            # 检查超时
            elapsed = time.ticks_diff(time.ticks_ms(), start_time)
            if elapsed > self.io_timeout:
                break

            time.sleep_ms(1)

        return bytes(data)

    def r_flush_scs(self):
        """flush receive buffer"""
        while self.uart.any() > 0:
            self.uart.read(self.uart.any())

    def w_flush_scs(self):
        """wait for send complete"""
        time.sleep_ms(1)


class Scscl(ScsSerial):
    """SCSCL application layer - advanced servo control interface"""

    def __init__(self, uart, end=1, level=1):
        """initialize SCSCL

        :param uart: MicroPython UART object
        :param end: byte order (default 1=big endian)
        :param level: return level
        """
        super().__init__(uart, end, level)
        self.mem = bytearray(SCSCL_PRESENT_CURRENT_H - SCSCL_PRESENT_POSITION_L + 1)
        # indexed by servo_id (1..15); avoid IndexError on switch_mode(servo_id=2)
        self.min_angle = [0] * 16
        self.max_angle = [0] * 16

    def write_pos(self, servo_id, position, time_ms=0, speed=0):
        """write position command

        :param servo_id: servo id
        :param position: target position (0-1000)
        :param time_ms: movement time (milliseconds)
        :param speed: speed
        :return: success return 1, failure return 0
        """
        data_l, data_h = self.host2scs(position)
        time_l, time_h = self.host2scs(time_ms)
        speed_l, speed_h = self.host2scs(speed)

        data = bytes([data_l, data_h, time_l, time_h, speed_l, speed_h])
        return self.gen_write(servo_id, SCSCL_GOAL_POSITION_L, data)

    def reg_write_pos(self, servo_id, position, time_ms=0, speed=0):
        """async write position command

        :param servo_id: servo id
        :param position: target position
        :param time_ms: movement time
        :param speed: speed
        :return: success return 1, failure return 0
        """
        data_l, data_h = self.host2scs(position)
        time_l, time_h = self.host2scs(time_ms)
        speed_l, speed_h = self.host2scs(speed)

        data = bytes([data_l, data_h, time_l, time_h, speed_l, speed_h])
        return self.reg_write(servo_id, SCSCL_GOAL_POSITION_L, data)

    def sync_write_pos(self, servo_ids, positions, times=None, speeds=None):
        """sync write multiple servo positions

        :param servo_ids: servo id list
        :param positions: position list
        :param times: time list (optional)
        :param speeds: speed list (optional)
        """
        if times is None:
            times = [0] * len(servo_ids)
        if speeds is None:
            speeds = [0] * len(servo_ids)

        data_list = []
        for i in range(len(servo_ids)):
            pos_l, pos_h = self.host2scs(positions[i])
            time_l, time_h = self.host2scs(times[i])
            speed_l, speed_h = self.host2scs(speeds[i])
            data_list.append(bytes([pos_l, pos_h, time_l, time_h, speed_l, speed_h]))

        self.sync_write(servo_ids, SCSCL_GOAL_POSITION_L, data_list)

    def enable_torque(self, servo_id, enable):
        """enable/disable torque

        :param servo_id: servo id
        :param enable: 1=enable, 0=disable, 2=damping
        :return: success return 1, failure return 0
        """
        return self.write_byte(servo_id, SCSCL_TORQUE_ENABLE, enable)

    def read_torque_enable(self, servo_id):
        """read torque enable state

        :param servo_id: servo id
        :return: torque enable state, failure return -1
        """
        return self.read_word(servo_id, SCSCL_TORQUE_ENABLE)

    def pwm_mode(self, servo_id):
        """switch to PWM mode

        :param servo_id: servo id
        :return: success return 1, failure return 0
        """
        # PWM mode: set angle limit to 0
        return self.write_word(servo_id, SCSCL_MIN_ANGLE_LIMIT_L, 0) and self.write_word(
            servo_id, SCSCL_MAX_ANGLE_LIMIT_L, 0
        )

    def write_pwm(self, servo_id, pwm_out):
        """write PWM value (PWM mode)

        :param servo_id: servo id
        :param pwm_out: PWM value (signed, -1023 to 1023)
        :return: success return 1, failure return 0
        """
        if pwm_out < 0:
            pwm_out = -pwm_out
            pwm_out |= 1 << 10

        return self.write_word(servo_id, SCSCL_GOAL_TIME_L, pwm_out)

    def switch_mode(self, servo_id, mode):
        """switch mode

        :param servo_id: servo id
        :param mode: 0=position mode, 1=PWM mode
        :return: success return 0, failure return negative value
        """
        if mode == 1:  # PWM mode
            min_a = self.min_angle[servo_id]
            max_a = self.max_angle[servo_id]
            if min_a == 0 and max_a == 0:
                min_a = self.read_word(servo_id, SCSCL_MIN_ANGLE_LIMIT_L)
                max_a = self.read_word(servo_id, SCSCL_MAX_ANGLE_LIMIT_L)

                if min_a == -1 or max_a == -1:
                    return -3
                if min_a == 0 and max_a == 0:
                    min_a, max_a = SCSCL_POSITION_MIN, SCSCL_POSITION_MAX
                self.min_angle[servo_id] = min_a
                self.max_angle[servo_id] = max_a

            if self.pwm_mode(servo_id):
                time.sleep_ms(200)
                return 0
            return -1
        else:  # position mode
            min_a = self.min_angle[servo_id]
            max_a = self.max_angle[servo_id]
            # When the runtime cache is empty, read the current limit first. If the servo
            # is already in PWM mode after a soft reset, restore the normal SCSCL window.
            if min_a == 0 and max_a == 0:
                rmin = self.read_word(servo_id, SCSCL_MIN_ANGLE_LIMIT_L)
                rmax = self.read_word(servo_id, SCSCL_MAX_ANGLE_LIMIT_L)
                if rmin == -1 or rmax == -1:
                    min_a, max_a = SCSCL_POSITION_MIN, SCSCL_POSITION_MAX
                elif rmin == 0 and rmax == 0:
                    min_a, max_a = SCSCL_POSITION_MIN, SCSCL_POSITION_MAX
                else:
                    min_a, max_a = rmin, rmax
                self.min_angle[servo_id] = min_a
                self.max_angle[servo_id] = max_a
            if self.write_word(servo_id, SCSCL_MIN_ANGLE_LIMIT_L, min_a) != 1:
                return -4
            if self.write_word(servo_id, SCSCL_MAX_ANGLE_LIMIT_L, max_a) != 1:
                return -5
            time.sleep_ms(200)
            return 0

    def read_mode(self, servo_id):
        """read current mode

        :param servo_id: servo id
        :return: 0=position mode, 1=PWM mode, -1=failure
        """
        min_value = self.read_word(servo_id, SCSCL_MIN_ANGLE_LIMIT_L)
        max_value = self.read_word(servo_id, SCSCL_MAX_ANGLE_LIMIT_L)
        if min_value == -1 or max_value == -1:
            return -1
        if min_value == 0 and max_value == 0:
            return 1  # PWM mode
        return 0  # position mode

    def feedback(self, servo_id):
        """feedback servo information (batch read)

        :param servo_id: servo id
        :return: success return read byte count, failure return -1
        """
        data = self.read(servo_id, SCSCL_PRESENT_POSITION_L, len(self.mem))
        if data and len(data) == len(self.mem):
            self.mem = bytearray(data)
            return len(data)
        return -1

    def read_pos(self, servo_id=-1):
        """read current position

        :param servo_id: servo id (-1 means use cache data)
        :return: position value, failure return -1
        """
        if servo_id == -1:
            # use cache data
            pos = (self.mem[SCSCL_PRESENT_POSITION_L - SCSCL_PRESENT_POSITION_L] << 8) | self.mem[
                SCSCL_PRESENT_POSITION_H - SCSCL_PRESENT_POSITION_L
            ]
            return pos
        else:
            return self.read_word(servo_id, SCSCL_PRESENT_POSITION_L)

    def read_speed(self, servo_id=-1):
        """read current speed

        :param servo_id: servo id (-1 means use cache data)
        :return: speed value (signed), failure return -1
        """
        if servo_id == -1:
            speed = (self.mem[SCSCL_PRESENT_SPEED_L - SCSCL_PRESENT_POSITION_L] << 8) | self.mem[
                SCSCL_PRESENT_SPEED_H - SCSCL_PRESENT_POSITION_L
            ]
        else:
            speed = self.read_word(servo_id, SCSCL_PRESENT_SPEED_L)
            if speed == -1:
                return -1

        # handle sign bit (bit 15)
        if speed & (1 << 15):
            speed = -(speed & ~(1 << 15))

        return speed

    def read_load(self, servo_id=-1):
        """read load (output voltage percentage to motor 0~1000)

        :param servo_id: servo id (-1 means use cache data)
        :return: load value (signed), failure return -1
        """
        if servo_id == -1:
            load = (self.mem[SCSCL_PRESENT_LOAD_L - SCSCL_PRESENT_POSITION_L] << 8) | self.mem[
                SCSCL_PRESENT_LOAD_H - SCSCL_PRESENT_POSITION_L
            ]
        else:
            load = self.read_word(servo_id, SCSCL_PRESENT_LOAD_L)
            if load == -1:
                return -1

        if load & (1 << 10):
            load = -(load & ~(1 << 10))

        return load

    def read_voltage(self, servo_id=-1):
        """read voltage

        :param servo_id: servo id (-1 means use cache data)
        :return: voltage value, failure return -1
        """
        if servo_id == -1:
            return self.mem[SCSCL_PRESENT_VOLTAGE - SCSCL_PRESENT_POSITION_L]
        else:
            return self.read_byte(servo_id, SCSCL_PRESENT_VOLTAGE)

    def read_temperature(self, servo_id=-1):
        """read temperature

        :param servo_id: servo id (-1 means use cache data)
        :return: temperature value, failure return -1
        """
        if servo_id == -1:
            return self.mem[SCSCL_PRESENT_TEMPERATURE - SCSCL_PRESENT_POSITION_L]
        else:
            return self.read_byte(servo_id, SCSCL_PRESENT_TEMPERATURE)

    def read_moving(self, servo_id=-1):
        """read moving state

        :param servo_id: servo id (-1 means use cache data)
        :return: 0=stopped, 1=moving, -1=failure
        """
        if servo_id == -1:
            return self.mem[SCSCL_MOVING - SCSCL_PRESENT_POSITION_L]
        else:
            return self.read_byte(servo_id, SCSCL_MOVING)

    def read_current(self, servo_id=-1):
        """read current

        :param servo_id: servo id (-1 means use cache data)
        :return: current value (signed), failure return -1
        """
        if servo_id == -1:
            current = (
                self.mem[SCSCL_PRESENT_CURRENT_L - SCSCL_PRESENT_POSITION_L] << 8
            ) | self.mem[SCSCL_PRESENT_CURRENT_H - SCSCL_PRESENT_POSITION_L]
        else:
            current = self.read_word(servo_id, SCSCL_PRESENT_CURRENT_L)
            if current == -1:
                return -1

        # handle sign bit (bit 15)
        if current & (1 << 15):
            current = -(current & ~(1 << 15))

        return current
