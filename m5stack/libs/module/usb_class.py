# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class EP_RECORD:
    epAddr = bytes
    Attr = bytes
    MaxPktSize = int
    Interval = bytes
    bmSndToggle = bytes
    bmRcvToggle = bytes


class DEV_RECORD:
    epinfo = EP_RECORD()
    devclass = bytes


class SETUP_PKT:
    bmRequestType = bytes
    bRequest = bytes
    wValueLo = bytes
    wValueHi = bytes
    wIndex = int
    wLength = int


class USB_DEVICE_DESCRIPTOR:
    bLength = bytes
    bDescriptorType = bytes
    bcdUSB = int
    bDeviceClass = bytes
    bDeviceSubClass = bytes
    bDeviceProtocol = bytes
    bMaxPacketSize0 = bytes
    idVendor = int
    idProduct = int
    bcdDevice = int
    iManufacturer = bytes
    iProduct = bytes
    iSerialNumber = bytes
    bNumConfigurations = bytes
