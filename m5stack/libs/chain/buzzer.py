# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class BuzzerChain(KeyChain):
    """Buzzer Chain class for interacting with buzzer devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the buzzer on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import BuzzerChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_buzzer_0 = BuzzerChain(bus2, 1)
    """

    CMD_SET_MODE = 0x30
    CMD_GET_MODE = 0x31
    CMD_SET_AUTO_PLAY = 0x32
    CMD_SET_FREQ = 0x33
    CMD_GET_FREQ = 0x34
    CMD_SET_DUTY = 0x35
    CMD_GET_DUTY = 0x36
    CMD_SET_STATUS = 0x37
    CMD_GET_STATUS = 0x38
    CMD_SET_NOTE_PLAY = 0x39

    MODE_AUTO_PLAY = 0x00  # Auto play mode
    MODE_MANUAL_PLAY = 0x01  # Manual play mode
    MODE_NOTE_PLAY = 0x02  # Note play mode

    STATUS_OFF = 0x00  # Buzzer off
    STATUS_ON = 0x01  # Buzzer on

    # NOTE_PLAY uses note indexes from 0 to 61.

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def set_mode(self, mode: int) -> bool:
        """Set the buzzer mode.

        :param int mode: Buzzer mode. Use :attr:`BuzzerChain.MODE_AUTO_PLAY` (0), :attr:`BuzzerChain.MODE_MANUAL_PLAY` (1), or :attr:`BuzzerChain.MODE_NOTE_PLAY` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.set_mode(BuzzerChain.MODE_AUTO_PLAY)
        """
        if mode not in (0, 1, 2):
            mode = 0

        payload = struct.pack("<B", mode & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_MODE, payload)
        if state:
            return response[0] == 1
        return False

    def get_mode(self) -> int:
        """Get the buzzer mode.

        :return: Buzzer mode. :attr:`BuzzerChain.MODE_AUTO_PLAY` (0), :attr:`BuzzerChain.MODE_MANUAL_PLAY` (1), or :attr:`BuzzerChain.MODE_NOTE_PLAY` (2). Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = chain_buzzer_0.get_mode()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_MODE, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def tone(self, freq: int = 2700, duty: int = 50, duration_ms: int = 100) -> bool:
        """Play tone (only works in AUTO_PLAY mode).

        :param int freq: Frequency in Hz. Range: 100-10000. Default: 2700.
        :param int duty: Duty cycle (0-100). Default: 50.
        :param int duration_ms: Duration in milliseconds. Default: 100.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |tone.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.tone(2700, 50, 1000)
                success = chain_buzzer_0.tone()  # Use default values: 2700Hz, 50% duty, 100ms
        """
        # Clamp values to valid ranges
        if freq < 100:
            freq = 100
        elif freq > 10000:
            freq = 10000

        if duty < 0:
            duty = 0
        elif duty > 100:
            duty = 100

        # Pack as: freq_low, freq_high, duty, duration_low, duration_high (5 bytes total)
        payload = struct.pack("<HBH", freq & 0xFFFF, duty & 0xFF, duration_ms & 0xFFFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_AUTO_PLAY, payload)
        if state:
            return response[0] == 1
        return False

    def set_freq(self, freq: int = 2700) -> bool:
        """Set the buzzer frequency.

        :param int freq: Frequency in Hz. Range: 100-10000. Default: 2700.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.set_freq(2700)
                success = chain_buzzer_0.set_freq()  # Use default: 2700Hz
        """
        # Clamp freq to valid range
        if freq < 100:
            freq = 100
        elif freq > 10000:
            freq = 10000

        payload = struct.pack("<H", freq & 0xFFFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_FREQ, payload)
        if state:
            return response[0] == 1
        return False

    def get_freq(self) -> int:
        """Get the buzzer frequency.

        :return: Frequency in Hz, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                freq = chain_buzzer_0.get_freq()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_FREQ, bytes())
        if state:
            if len(response) >= 2:
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def set_duty(self, duty: int = 50) -> bool:
        """Set the buzzer duty cycle.

        :param int duty: Duty cycle (0-100). Default: 50.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_duty.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.set_duty(50)
                success = chain_buzzer_0.set_duty()  # Use default: 50%
        """
        # Clamp duty to valid range
        if duty < 0:
            duty = 0
        elif duty > 100:
            duty = 100

        payload = struct.pack("<B", duty & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_DUTY, payload)
        if state:
            return response[0] == 1
        return False

    def get_duty(self) -> int:
        """Get the buzzer duty cycle.

        :return: Duty cycle (0-100), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_duty.png|

        MicroPython Code Block:

            .. code-block:: python

                duty = chain_buzzer_0.get_duty()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_DUTY, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_status(self, status: int) -> bool:
        """Set the buzzer status (only works in MANUAL_PLAY mode).

        :param int status: Buzzer status. Use :attr:`BuzzerChain.STATUS_OFF` (0) or :attr:`BuzzerChain.STATUS_ON` (1).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_status.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.set_status(BuzzerChain.STATUS_ON)
        """
        if status not in (0, 1):
            status = 0

        payload = struct.pack("<B", status & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_STATUS, payload)
        if state:
            return response[0] == 1
        return False

    def get_status(self) -> int:
        """Get the buzzer status.

        :return: Buzzer status. :attr:`BuzzerChain.STATUS_OFF` (0) or :attr:`BuzzerChain.STATUS_ON` (1). Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = chain_buzzer_0.get_status()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_STATUS, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def note(self, note_index: int, duration_ms: int = 100) -> bool:
        """Play note (only works in NOTE_PLAY mode).

        :param int note_index: Note index (0-61). 0 is rest (silence), 13 is C4, and 61 is C8.
        :param int duration_ms: Duration in milliseconds. Default: 100.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |note.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_buzzer_0.note(25, 500)  # Play C5 for 500ms
                success = chain_buzzer_0.note(25)  # Play C5 for 100ms (default duration)
        """
        # Clamp note_index to valid range (0-61)
        if note_index < 0:
            note_index = 0
        elif note_index > 61:
            note_index = 61

        payload = struct.pack("<BH", note_index & 0xFF, duration_ms & 0xFFFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_NOTE_PLAY, payload)
        if state:
            return response[0] == 1
        return False
