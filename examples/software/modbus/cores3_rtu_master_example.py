# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import RS485Unit
import modbus
import time


label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label14 = None
label19 = None
label24 = None
label10 = None
label15 = None
label20 = None
label25 = None
label11 = None
label16 = None
label21 = None
label26 = None
label12 = None
label17 = None
label22 = None
label27 = None
label13 = None
label18 = None
label23 = None
label28 = None
modbusrtumaster_0 = None
rs485_0 = None


res = None
hr = None
coil = None


def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label14, \
        label19, \
        label24, \
        label10, \
        label15, \
        label20, \
        label25, \
        label11, \
        label16, \
        label21, \
        label26, \
        label12, \
        label17, \
        label22, \
        label27, \
        label13, \
        label18, \
        label23, \
        label28, \
        modbusrtumaster_0, \
        rs485_0, \
        res, \
        hr, \
        coil

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("co", 65, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("di", 135, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("hr", 205, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("ir", 275, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("1000", 4, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("1001", 4, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("1002", 4, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("1003", 4, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("1004", 4, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("a00", 65, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label14 = Widgets.Label("a01", 135, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label19 = Widgets.Label("a02", 205, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label24 = Widgets.Label("a03", 275, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("a10", 65, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label15 = Widgets.Label("a11", 135, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label20 = Widgets.Label("a12", 205, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label25 = Widgets.Label("a13", 275, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label11 = Widgets.Label("a20", 65, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label16 = Widgets.Label("a21", 135, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label21 = Widgets.Label("a22", 205, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label26 = Widgets.Label("a23", 275, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label12 = Widgets.Label("a30", 65, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label17 = Widgets.Label("a31", 135, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label22 = Widgets.Label("a32", 205, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label27 = Widgets.Label("a33", 275, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label13 = Widgets.Label("a40", 65, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label18 = Widgets.Label("a41", 135, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label23 = Widgets.Label("a42", 205, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label28 = Widgets.Label("a43", 275, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    rs485_0 = RS485Unit(2, port=(18, 17))
    rs485_0.init(
        tx_pin=None,
        rx_pin=None,
        baudrate=115200,
        data_bits=None,
        stop_bits=None,
        parity=None,
        ctrl_pin=None,
    )
    modbusrtumaster_0 = modbus.ModbusRTUMaster(uart=rs485_0, verbose=True)
    hr = 0
    res = modbusrtumaster_0.read_coils(1, 1000, 5, timeout=2000)
    label9.setText(str(res[0]))
    label10.setText(str(res[1]))
    label11.setText(str(res[2]))
    label12.setText(str(res[3]))
    label13.setText(str(res[4]))
    res = modbusrtumaster_0.read_discrete_inputs(1, 1000, 5, timeout=2000)
    label14.setText(str(res[0]))
    label15.setText(str(res[1]))
    label16.setText(str(res[2]))
    label17.setText(str(res[3]))
    label18.setText(str(res[4]))
    res = modbusrtumaster_0.read_holding_registers(1, 1000, 5, timeout=2000)
    label19.setText(str(res[0]))
    label20.setText(str(res[1]))
    label21.setText(str(res[2]))
    label22.setText(str(res[3]))
    label23.setText(str(res[4]))
    res = modbusrtumaster_0.read_input_registers(1, 1000, 5, timeout=2000)
    label24.setText(str(res[0]))
    label25.setText(str(res[1]))
    label26.setText(str(res[2]))
    label27.setText(str(res[3]))
    label28.setText(str(res[4]))


def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label14, \
        label19, \
        label24, \
        label10, \
        label15, \
        label20, \
        label25, \
        label11, \
        label16, \
        label21, \
        label26, \
        label12, \
        label17, \
        label22, \
        label27, \
        label13, \
        label18, \
        label23, \
        label28, \
        modbusrtumaster_0, \
        rs485_0, \
        res, \
        hr, \
        coil
    M5.update()
    hr = (hr + 1) % 65535
    coil = not coil
    modbusrtumaster_0.write_single_coil(1, 1000, coil, timeout=2000)
    modbusrtumaster_0.write_single_register(1, 1000, hr, timeout=2000)
    modbusrtumaster_0.write_multiple_coils(1, 1001, [coil, coil, coil], timeout=2000)
    label9.setText(str(coil))
    label10.setText(str(coil))
    label11.setText(str(coil))
    label12.setText(str(coil))
    modbusrtumaster_0.write_multiple_registers(1, 1001, [hr, hr, hr], timeout=2000)
    label19.setText(str(hr))
    label20.setText(str(hr))
    label21.setText(str(hr))
    label22.setText(str(hr))
    time.sleep(1)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
