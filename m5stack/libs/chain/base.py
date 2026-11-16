# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus


class ChainDevice:
    """Common device registration, RGB control and identity queries for Chain devices.

    :param ChainBus bus: Chain bus instance.
    :param int device_id: Device position on the Chain bus, starting at 1.
    """

    RGB_COUNT = 1
    """Number of RGB LEDs addressed by the generic RGB API."""

    def __init__(self, bus: ChainBus, device_id: int):
        self.bus = bus
        self.device_id = device_id
        self.bus.register_device(self)

    def set_rgb_color(self, index: int, color: int) -> bool:
        """set RGB color.

        :param int index: Index of the RGB LED.
        :param int color: RGB color value.
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_rgb_color(0, 0xFF0000)
        """
        return self.bus.chainll.set_rgb_color(self.device_id, index, color)

    def get_rgb_color(self, index: int) -> int:
        """get RGB color.

        :param int index: Index of the RGB LED.
        :return: RGB color value.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                color = device.get_rgb_color(0)
        """
        return self.bus.chainll.get_rgb_color(self.device_id, index)

    def fill_rgb_color(self, color: int) -> bool:
        """fill RGB color.

        :param int color: RGB color value.
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |fill_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                device.fill_rgb_color(0xFF0000)
        """
        return self.bus.chainll.fill_rgb_color(self.device_id, 0, self.RGB_COUNT, color)

    def set_rgb_brightness(self, brightness: int, save: bool = False) -> bool:
        """set RGB brightness.

        :param int brightness: Brightness value (0-100).
        :param bool save: Whether to save the brightness setting to flash.
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_rgb_brightness(80)
        """
        return self.bus.chainll.set_rgb_brightness(self.device_id, brightness, save)

    def get_rgb_brightness(self) -> int:
        """get RGB brightness.

        :return: Brightness value (0-100).
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = device.get_rgb_brightness()
        """
        return self.bus.chainll.get_rgb_brightness(self.device_id)

    def get_bootloader_version(self) -> int:
        """get bootloader version.

        :return: Bootloader version.
        :rtype: int

        UiFlow2 Code Block:

            |get_bootloader_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = device.get_bootloader_version()
        """
        return self.bus.chainll.get_bootloader_version(self.device_id)

    def get_firmware_version(self) -> int:
        """get firmware version.

        :return: Firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = device.get_firmware_version()
        """
        return self.bus.chainll.get_firmware_version(self.device_id)

    def get_device_type(self) -> int:
        """get device type.

        :return: Device type. Returns -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_device_type.png|

        MicroPython Code Block:

            .. code-block:: python

                device_type = device.get_device_type()
        """
        return self.bus.chainll.get_device_type(self.device_id)

    def get_device_uid(self, uid_type: int) -> tuple:
        """get device UID.

        :param int uid_type: UID type, 0 for 4-byte UID, 1 for 12-byte UID.
        :return: Tuple of UID bytes (4 bytes or 12 bytes). Returns empty tuple on error.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_device_uid.png|

        MicroPython Code Block:

            .. code-block:: python

                uid = device.get_device_uid(0)  # 4-byte UID
                uid = device.get_device_uid(1)  # 12-byte UID
        """
        if uid_type not in (0, 1):
            raise ValueError("uid_type must be 0 or 1")
        return self.bus.chainll.get_device_uid(self.device_id, uid_type)
