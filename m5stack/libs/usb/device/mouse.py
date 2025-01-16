# MicroPython USB Mouse module
#
# MIT license; Copyright (c) 2023-2024 Angus Gratton
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
from micropython import const
import struct
import machine
from usb.device.hid import HIDInterface
import usb.device


_INTERFACE_PROTOCOL_MOUSE = const(0x02)


class Mouse(HIDInterface):
    # A basic three button USB mouse HID interface
    def __init__(self, interface_str="M5Mouse", builtin_driver=True):
        super().__init__(
            _MOUSE_REPORT_DESC,
            protocol=_INTERFACE_PROTOCOL_MOUSE,
            interface_str=interface_str,
        )
        self.x = 0
        self.y = 0
        self.w = 0
        self.b1 = 0  # left button
        self.b2 = 0  # right button
        self.b3 = 0  # middle button (wheel)
        self.fw = 0  # 前进
        self.bw = 0  # 后退
        self.buf = bytearray(5)
        # 自动初始化 USB 设备
        self.builtin_driver = builtin_driver
        self._usb_device = usb.device.get()
        self._init_usb()

    def _init_usb(self):
        self._usb_device.init(self, builtin_driver=self.builtin_driver)

    # Set the mouse axes values.
    def set_axes(self, x=0, y=0):
        self.x = max(-127, min(127, x))
        self.y = max(-127, min(127, y))

    # Set the mouse scroll wheel value.
    def set_wheel(self, w=0):
        self.w = max(-127, min(127, w))

    # Set the mouse button values.
    def set_buttons(self, b1=0, b2=0, b3=0, fw=0, bw=0):
        self.b1 = b1  # left
        self.b2 = b2  # right
        self.b3 = b3  # middle
        self.fw = fw
        self.bw = bw

    def send_report(self, dx=0, dy=0):
        # Wait for any pending report to be sent to the host
        # before updating contents of buf.
        #
        # This loop can be removed if you don't care about possibly missing a
        # transient report, the final report buffer contents will always be the
        # last one sent to the host (it just might lose one of the ones in the
        # middle).
        # last_time = time.ticks_ms()
        # while self.busy():
        #     machine.idle()
        #     if time.ticks_diff(time.ticks_ms(), last_time) > 200:
        #         return

        b = (self.bw << 4) + (self.fw << 3) + (self.b3 << 2) + (self.b2 << 1) + self.b1
        struct.pack_into("BBbbb", self.buf, 0, 1, b, self.x, self.y, self.w)
        return super().send_report(self.buf)

    def move(self, x, y):
        self.set_axes(x=x, y=y)
        self.set_wheel(w=0)
        self.send_report()

    def click(
        self, left=True, right=False, middle=False, forward=False, backward=False, release=True
    ):
        self.set_axes(x=0, y=0)
        self.set_wheel(w=0)
        self.set_buttons(b1=left, b2=right, b3=middle, fw=forward, bw=backward)
        self.send_report()
        if release:
            self.set_buttons(b1=False, b2=False, b3=False, fw=False, bw=False)
            self.send_report()

    def click_left(self, release=True):
        self.click(left=True, release=release)

    def click_right(self, release=True):
        self.click(right=True, release=release)

    def click_middle(self, release=True):
        self.click(middle=True, release=release)

    def click_forward(self, release=True):
        self.click(forward=True, release=release)

    def click_backward(self, release=True):
        self.click(backward=True, release=release)

    def scroll(self, w):
        self.set_axes(x=0, y=0)
        self.set_wheel(w=w)
        self.send_report()


# Basic 3-button mouse HID Report Descriptor.
# This is based on Appendix E.10 of the HID v1.11 document.
# fmt: off
_MOUSE_REPORT_DESC = bytes([ # Report Description: describes what we communicate.
            0x05, 0x01, # Uage Page (Generic Desktop)
            0x09, 0x02, # Usage (Mouse)
            0xa1, 0x01, # Collection (Application)
            0x85, 0x01, #     Report ID (1)
            0x09, 0x01, #     Usage (Pointer)
            0xa1, 0x00, #     Collection (Physical)
            0x05, 0x09, #         Uage Page (Buttons)
            0x19, 0x01, #             Usage Minimum (Button 1)
            0x29, 0x05, #             Usage Maximum (Button 5)
            0x15, 0x00, #             Logical Minimum (0)
            0x25, 0x01, #             Logical Maximum (1)
            0x95, 0x05, #             Report Count (5) - Now supports 5 buttons
            0x75, 0x01, #             Report Size (1)
            0x81, 0x02, #             Input (Data, Variable, Absolute) - 5 button bits (includes forward and backward buttons)
            0x95, 0x01, #             Report Count (1)
            0x75, 0x03, #             Report Size (3) - Padding for byte alignment
            0x81, 0x03, #             Input (Constant, Variable, Absolute) - 3 bit padding
            0x05, 0x01, #        Uage Page (Generic Desktop)
            0x09, 0x30, #             Usage (X)
            0x09, 0x31, #             Usage (Y)
            0x09, 0x38, #             Usage (Wheel)
            0x15, 0x81, #             Logical Minimum (-127)
            0x25, 0x7F, #             Logical Maximum (127)
            0x75, 0x08, #             Report Size (8)
            0x95, 0x03, #             Report Count (3)
            0x81, 0x06, #             Input (Data, Variable, Relative) - X, Y, Wheel
            0xc0,       #     End Collection
            0xc0        # End Collection
])
# fmt: on

# # Basic 3-button mouse HID Report Descriptor.
# # This is based on Appendix E.10 of the HID v1.11 document.
# # fmt: off
# _MOUSE_REPORT_DESC = bytes([ # Report Description: describes what we communicate.
#             0x05, 0x01, # Usage Page (Generic Desktop)
#             0x09, 0x02, #     Usage (Mouse)
#             0xa1, 0x01, # Collection (Application)
#             0x85, 0x01, # Report ID (1)
#             0x09, 0x01, #     Usage (Pointer)
#             0xa1, 0x00, #     Collection (Physical)
#             0x05, 0x09, #         Usage Page (Buttons)
#             0x19, 0x01, #             Usage Minimum (1)
#             0x29, 0x03, #             Usage Maximum (3)
#             0x15, 0x00, #             Logical Minimum (0)
#             0x25, 0x01, #             Logical Maximum (1)
#             0x95, 0x03, #             Report Count (3)
#             0x75, 0x01, #             Report Size (1)
#             0x81, 0x02, #             Input(Data, Variable, Absolute); 3 button bits
#             0x95, 0x01, #             Report Count(1)
#             0x75, 0x05, #             Report Size(5)
#             0x81, 0x03, #             Input(Constant);                 5 bit padding
#             0x05, 0x01, #         Usage Page (Generic Desktop)
#             0x09, 0x30, #             Usage (X)
#             0x09, 0x31, #             Usage (Y)
#             0x09, 0x38, #             Usage (Wheel)
#             0x15, 0x81, #             Logical Minimum (-127)
#             0x25, 0x7F, #             Logical Maximum (127)
#             0x75, 0x08, #             Report Size (8)
#             0x95, 0x03, #             Report Count (3)
#             0x81, 0x06, #             Input(Data, Variable, Relative); 3 position bytes (X,Y,Wheel)
#             0xc0,       #     End Collection
#             0xc0        # End Collection
#         ])
# # fmt: on
