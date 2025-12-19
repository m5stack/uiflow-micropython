# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class ToFChain(KeyChain):
    """ToF Chain class for interacting with ToF (Time of Flight) devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the ToF sensor on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import ToFChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_tof_0 = ToFChain(bus2, 1)
    """

    CMD_GET_DISTANCE = 0x50
    CMD_SET_MEASURE_TIME = 0x51
    CMD_GET_MEASURE_TIME = 0x52
    CMD_SET_MEASURE_MODE = 0x53
    CMD_GET_MEASURE_MODE = 0x54
    CMD_SET_MEASURE_STATUS = 0x55
    CMD_GET_MEASURE_STATUS = 0x56
    CMD_GET_MEASURE_COMPLETE_FLAG = 0x57

    MODE_STOP = 0  # Stop measurement mode
    MODE_SINGLE = 1  # Single measurement mode
    MODE_CONTINUOUS = 2  # Continuous measurement mode

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_distance(self) -> int:
        """Get the distance measurement.

        :return: Distance in millimeters, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_distance.png|

        MicroPython Code Block:

            .. code-block:: python

                distance = chain_tof_0.get_distance()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_DISTANCE, bytes())
        if state:
            if len(response) >= 2:
                # Distance is 2 bytes, little-endian
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def set_measure_time(self, time_ms: int = 33) -> bool:
        """Set the measurement time.

        :param int time_ms: Measurement time in milliseconds. Range: 20-200, default: 33.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_measure_time.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_tof_0.set_measure_time(33)
        """
        # Clamp time_ms to valid range
        if time_ms < 20:
            time_ms = 20
        elif time_ms > 200:
            time_ms = 200

        payload = struct.pack("<B", time_ms & 0xFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_MEASURE_TIME, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_measure_time(self) -> int:
        """Get the measurement time.

        :return: Measurement time in milliseconds, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_measure_time.png|

        MicroPython Code Block:

            .. code-block:: python

                time = chain_tof_0.get_measure_time()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_MEASURE_TIME, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_measure_mode(self, mode: int = 2) -> bool:
        """Set the measurement mode.

        :param int mode: Measurement mode. Use :attr:`ToFChain.MODE_STOP` (0), :attr:`ToFChain.MODE_SINGLE` (1), or :attr:`ToFChain.MODE_CONTINUOUS` (2). Default: 2.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_measure_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_tof_0.set_measure_mode(ToFChain.MODE_CONTINUOUS)
        """
        # Validate mode
        if mode not in (0, 1, 2):
            mode = 2

        payload = struct.pack("<B", mode & 0xFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_MEASURE_MODE, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_measure_mode(self) -> int:
        """Get the measurement mode.

        :return: Measurement mode. :attr:`ToFChain.MODE_STOP` (0), :attr:`ToFChain.MODE_SINGLE` (1), or :attr:`ToFChain.MODE_CONTINUOUS` (2). Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_measure_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = chain_tof_0.get_measure_mode()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_MEASURE_MODE, bytes()
        )
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_measure_status(self, status: int) -> bool:
        """Set the measurement status.

        :param int status: Measurement status. 0 means not measuring, 1 means measuring.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_measure_status.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_tof_0.set_measure_status(1)
        """
        # Validate status
        if status not in (0, 1):
            status = 0

        payload = struct.pack("<B", status & 0xFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_MEASURE_STATUS, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_measure_status(self) -> int:
        """Get the measurement status.

        :return: Measurement status. 0 means not measuring, 1 means measuring. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_measure_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = chain_tof_0.get_measure_status()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_MEASURE_STATUS, bytes()
        )
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def get_measure_complete_flag(self) -> int:
        """Get the measurement complete flag.

        :return: Measurement complete flag. 0 means measurement not complete, 1 means measurement complete. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_measure_complete_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                flag = chain_tof_0.get_measure_complete_flag()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_MEASURE_COMPLETE_FLAG, bytes()
        )
        if state:
            if len(response) >= 1:
                return response[0]
        return None
