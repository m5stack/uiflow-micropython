# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import sys
import re
import machine
import micropython
from .unit_helper import UnitError

if sys.platform != "esp32":
    from typing import Literal


class UWBUnit:
    """
    note:
        en: |
            UWB is a Unit which integrates the UWB(Ultra Wide Band) communication protocol which uses nanosecond pulses to locate objects and define position and orientation. The design uses the Ai-ThinkerBU01 Transceiver module which is based on Decawave's DW1000 design. The internal STM32 chip with its integrated ranging algorithm,is capable of 10cm positioning accuracy and also supports AT command control. Applications include: Indoor wireless tracking/range finding of assets,which works by triangulating the position of the base station/s and tag (the base station resolves the position information and outputs it to the tag).
            The firmware currently carried by this Unit only supports the transmission of ranging information, and does not currently support the transmission of custom information. When in use, it supports the configuration of 4 base station devices (using different IDs), and only a single tag device is allowed to operate at the same time.
    details:
        color: '#0fb1d2'
        link: https://docs.m5stack.com/en/unit/uwb
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/uwb/uwb_01.webp
        category: unit
    example:
        - ../../../examples/unit/uwb/core2_uwb_anchor_example.py
        - ../../../examples/unit/uwb/stickc_plus2_uwb_tag_example.py
    """

    """
    constant: device role
    """
    UNKNOWN = -1
    ANCHOR = 1
    TAG = 0

    """
    constant: device status
    """
    OFFLINE = 0
    ONLINE = 1

    _mode_map = {
        "ANCHOR": ANCHOR,
        "TAG": TAG,
    }

    def __init__(
        self,
        id: Literal[0, 1, 2],
        port: list | tuple = None,
        device_mode=TAG,
        device_id=None,
        verbose: bool = False,
    ):
        """
        note:
            en: Create a UWB unit object.
        label:
            en: init %1 UART %5 as %2 with ID %3 verbose %4
        params:
            id:
                name: id
                type: int
                default: '2'
                field: number
                note: UART ID.
            device_mode:
                name: device_mode
                field: dropdown
                options:
                    Anchor: UWBUnit.ANCHOR
                    Tag: UWBUnit.TAG
                note: device mode.
            device_id:
                name: device_id
                type: int
                default: '0'
                field: number
                note: device ID.
            verbose:
                name: verbose
                type: bool
                default: 'False'
                field: switch
                note: verbose output.
        """
        machine.Pin(port[0], machine.Pin.IN, machine.Pin.PULL_UP)
        self._uart = machine.UART(id, 115200, tx=port[1], rx=port[0])
        self._device_mode = device_mode
        self._device_id = device_id
        self._verbose = verbose

        if self.isconnected() is False:
            raise UnitError("UWB unit maybe not connect")

        self._rb = micropython.RingIO(512)

        self._interval = 5
        self.set_device_mode(self._device_mode, self._device_id)

        self._anchor_status = [False, False, False, False]
        self._last_anchor_status = [False, False, False, False]
        self._distances = [0.0, 0.0, 0.0, 0.0]
        self._callbacks = [None, None, None, None, None, None, None, None]
        self._anchors = []
        self._last_time = time.time()

    def get_distance(self, index: int) -> float:
        """
        note:
            en: Get the distance to the anchor ID (0 ~ 3).
        label:
            en: get %1 distance to anchor ID (0 ~ 3) %2 (meters, return float)
        params:
            index:
                name: index
                type: int
                default: '0'
                field: number
                note: anchor ID (0 ~ 3).
        return:
            note: distance in meters.
        """
        return self._distances[index]

    def get_device_id(self) -> int:
        """
        note:
            en: Get the device ID.
        label:
            en: get %1 device ID(return int)
        return:
            note: device ID.
        """
        return self._device_id

    def get_device_mode(self) -> int:
        """
        note:
            en: Get the device mode.
        label:
            en: get %1 device mode(return int)
        return:
            note: device mode.
        """
        return self._device_mode

    def set_device_mode(self, mode: int, id: int) -> None:
        """
        note:
            en: Set the device mode and ID.
        label:
            en: set %1 as %2 with ID %3
        params:
            mode:
                name: mode
                field: dropdown
                options:
                    Anchor: UWBUnit.ANCHOR
                    Tag: UWBUnit.TAG
                note: device mode.
            id:
                name: id
                type: int
                default: '0'
                field: number
                note: device ID.
        """
        cmd = f"AT+anchor_tag={mode},{id}\r\n"
        self._at_cmd_send(cmd, keyword="OK")
        time.sleep(0.1)
        self.reset()
        self.set_measurement_interval(self._interval)
        if mode == self.TAG:
            self.set_measurement(True)
        self._device_mode = mode
        self._device_id = id

    def isconnected(self):
        """
        note:
            en: Check if the UWB unit is connected.
        label:
            en: check %1 is connected (return True or False)
        return:
            note: True if connected, False otherwise.
        """
        cmd = "AT\r\n"
        resp = self._at_cmd_send(cmd, keyword="OK")
        for line in resp:
            if line.find("OK") != -1:
                return True
        return False

    def get_version(self):
        """
        note:
            en: Get the UWB unit firmware version.
        label:
            en: get %1 firmware version(return string)
        return:
            note: firmware version.
        """
        cmd = "AT+version?\r\n"
        response = self._at_cmd_send(cmd, keyword="OK")
        if len(response) > 2:
            if "OK" in response[2]:
                return response[0]

    def reset(self) -> None:
        """
        note:
            en: Reset the UWB unit.
        label:
            en: reset %1
        """
        resp = self._at_cmd_send("AT+RST\r\n", keyword="OK")
        for line in resp:
            if line.find("device:") != -1:
                text = self._extract_text(line, "device:", " ")
                if text:
                    self._device_mode = self._mode_map.get(text, self.UNKNOWN)
                text = self._extract_text(line, "ID:", "\r\n")
                if text:
                    self._device_id = int(text)

    @staticmethod
    def _extract_text(text, start_str, end_str):
        pattern = f"{start_str}(.*?){end_str}"
        match = re.search(pattern, text)
        return match.group(1) if match else None

    def set_measurement_interval(self, interval: int) -> None:
        """
        note:
            en: Set the measurement interval.
        label:
            en: set %1 range interval %2 (5 ~ 50) times before value output
        params:
            interval:
                name: interval
                type: int
                default: '5'
                field: number
                note: measurement interval.
        """
        cmd = f"AT+interval={interval}\r\n"
        self._at_cmd_send(cmd, keyword="OK")
        self._interval = interval

    def set_measurement(self, enable: bool):
        """
        note:
            en: Set the measurement output.
        label:
            en: set %1 measurement output %2
        params:
            enable:
                name: enable
                type: bool
                default: 'False'
                field: switch
                note: enable or disable measurement output.
        """
        cmd = f"AT+switchdis={int(enable)}\r\n"
        self._at_cmd_send(cmd, keyword="OK")
        self.continuous_op = enable

    def _at_cmd_send(self, cmd, keyword=None, timeout=2):
        self._verbose and print("AT command:" + cmd[:-2])
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
                if "an" in line:
                    self._rb.write(line)
                else:
                    msgs.append(line)
            elif line is None or line == "":
                continue

            if keyword is not None and keyword in line:
                self._verbose and print("Got KEYWORD")
                find_keyword = True
            if find_keyword is True and self._uart.any() == 0:
                break

        self._verbose and print(msgs)
        return msgs

    def set_callback(self, anchor: int, event: int, callback):
        """
        note:
            en: Set the callback function for the anchor status.
        params:
            anchor:
                name: anchor
                type: int
                default: '0'
                field: number
                note: anchor ID (0 ~ 3).
            event:
                name: event
                field: dropdown
                options:
                    ONLINE: UWBUnit.ONLINE
                    OFFLINE: UWBUnit.OFFLINE
                note: anchor status.
            callback:
                name: callback
                type: function
                note: callback function.
        """
        self._callbacks[anchor * 2 + event] = callback

    def update(self):
        """
        note:
            en: Update the distances and anchor status.
        label:
            en: '%1 update in loop'
        """
        if (
            self.continuous_op
            and self._device_mode == self.TAG
            and self._uart.any()
            or self._rb.any()
        ):
            line = None
            if self._rb.any():
                line = self._rb.read()
            elif self._uart.any():
                line = self._uart.readline()
            # parse anchor id and distance
            text = self._extract_text(line, "an", ":")
            index = int(text) if text else None
            text = self._extract_text(line, ":", "m\r\n")
            distance = float(text) if text else None
            if index is None or distance is None:
                return

            self._last_time = time.time()

            if self._anchors.count(index) == 0:
                self._anchors.append(index)
            else:
                self._anchor_status = [False, False, False, False]
                for i in self._anchors:
                    self._anchor_status[i] = True
                self._anchors.clear()

            # handler anchor status
            for i in range(4):
                if self._last_anchor_status[i] != self._anchor_status[i]:
                    self._last_anchor_status[i] = self._anchor_status[i]
                    callback = self._callbacks[i * 2 + int(self._anchor_status[i])]
                    callback and micropython.schedule(callback, (self, i))

            # handler distance
            self._distances[index] = distance
            # FIXME: Create a callback for each measurement?
            # callback = self._callbacks[index * 2]
            # callback and micropython.schedule(callback, (self, index))

        # timeout seconds
        if time.time() - self._last_time > self._interval:
            self._anchors.clear()
            # handler anchor status
            for i in range(4):
                self._anchor_status[i] = False
                if self._last_anchor_status[i] != self._anchor_status[i]:
                    self._last_anchor_status[i] = self._anchor_status[i]
                    callback = self._callbacks[i * 2 + int(self._anchor_status[i])]
                    callback and micropython.schedule(callback, (self, i))
            self._last_time = time.time()

    def __del__(self):
        self._rb.close()
