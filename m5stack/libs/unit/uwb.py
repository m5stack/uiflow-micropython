# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import UART, Pin
from .unit_helper import UnitError
import time

UWB_RESULT_HEADER = "an"
UWB_GET_TIMEOUT = 12


class UWBUnit:
    def __init__(self, port, id=None, debug=False):
        self._debug = debug
        Pinx = Pin(port[0], Pin.IN, Pin.PULL_UP)
        self._uart = UART(1, tx=port[1], rx=port[0])
        self._uart.init(115200, bits=8, parity=None, stop=1)
        self.tx = port[1]
        self.rx = port[0]
        self.get_distance_measure = [0.0, 0.0, 0.0, 0.0]
        self.continuous_op = False
        self.device_id = ""
        self.reset()
        time.sleep(0.2)
        if self.check_device is False:
            raise UnitError("UWB unit maybe not connect")
        self.continuous_output_value(0)
        if id == None:
            self.set_mode()
            self.set_range_interval(5)
            self.continuous_output_value(1)
        else:
            self.set_mode(id)

    def uart_port_id(self, id_num):
        self._uart = UART(id_num, tx=self.tx, rx=self.rx)
        self._uart.init(115200, bits=8, parity=None, stop=1)

    @property
    def check_device(self):
        cmd = "AT\r\n"
        resp = self.at_cmd_send(cmd, keyword="OK")
        if len(resp):
            if self.remove_lfcr(resp)[0] == "OK":
                return True
            else:
                return False

    def get_version(self):
        cmd = "AT+version?\r\n"
        response = self.at_cmd_send(cmd, keyword="OK")
        if len(response) > 2:
            if "OK" in response[2]:
                return response[0]

    def reset(self):
        cmd = "AT+RST\r\n"
        resp = self.at_cmd_send(cmd, keyword="OK")
        resp = ",".join(self.remove_lfcr(resp))
        if resp.find("device:") != -1:
            self.device_id = resp[resp.find("device:") + 7 :]

    def set_range_interval(self, interval):
        cmd = "AT+interval=" + str(interval) + "\r\n"
        self.at_cmd_send(cmd, keyword="OK")

    def set_mode(self, id=None):
        cmd = "AT+anchor_tag=1," + str(id) + "\r\n" if (id != None) else "AT+anchor_tag=0\r\n"
        self.at_cmd_send(cmd, keyword="OK")
        time.sleep(0.1)
        self.reset()

    def continuous_output_value(self, start=1):
        cmd = "AT+switchdis=" + str(start) + "\r\n"
        self.at_cmd_send(cmd, keyword="OK")
        self.continuous_op = bool(start)

    def at_cmd_send(self, cmd, keyword=None, timeout=2):
        if self._debug:
            print("AT command:" + cmd[:-2])
        self._uart.read()
        time.sleep(0.1)
        self._uart.write(cmd)
        wait_time = time.time() + timeout
        msgs = []
        find_keyword = False
        time.sleep(0.1)
        while wait_time > time.time():
            time.sleep(0.05)
            line = self._uart.readline()
            if line is not None:
                line = line.decode()
                msgs.append(line)
            elif line is None or line == "":
                continue
            if keyword is not None and keyword in line:
                if self._debug:
                    print("Got KEYWORD")
                find_keyword = True
            if find_keyword == True and self._uart.any() == 0:
                break

        if self._debug:
            print(msgs)
        return msgs

    def remove_lfcr(self, msgs):
        # remove "\r\n"
        respon = []
        for i in msgs:
            if i != "\r\n":
                if len(i) > 2 and i[-2:] == "\r\n":
                    i = i[:-2]
                respon.append(i)
        if self._debug:
            print(respon)
        return respon

    def update_new_value_loop(self):
        rx_times = 0
        while True:
            if self._uart.any() < 40:
                break
            while (rx_times < 4) and self.continuous_op and ("TAG ID:" in self.device_id):
                if self._uart.any():
                    line = self._uart.readline()
                    if line is not None:
                        if UWB_RESULT_HEADER in line:
                            line = line.decode()
                            separate = line.find(":")
                            if rx_times == int(line[separate - 1]):
                                self.get_distance_measure[int(line[separate - 1])] = float(
                                    line[separate + 1 : -3]
                                )
                                rx_times += 1
