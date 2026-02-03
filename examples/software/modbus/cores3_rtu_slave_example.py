# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import modbus
from unit import ISO485Unit


label0 = None
label1 = None
label2 = None
modbusrtuslave_0 = None
iso485_0 = None


starting_register1 = None
slave_list1 = None
register1 = None
slave_value1 = None
starting_register4 = None
slave_list4 = None
register2 = None
slave_value2 = None
starting_register2 = None
slave_list2 = None
starting_register6 = None
slave_list6 = None
starting_register5 = None
slave_list5 = None
starting_register3 = None
slave_list3 = None


def modbus_read_coils_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register1, slave_list1 = args
    label0.setText(str("read coils"))
    label1.setText(str(starting_register1))
    label2.setText(str(slave_list1))


def modbus_write_single_coil_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, register1, slave_value1 = args
    label0.setText(str("write single coil"))
    label1.setText(str(register1))
    label2.setText(str(slave_value1))


def modbus_read_input_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register4, slave_list4 = args
    label0.setText(str("read input register"))
    label1.setText(str(starting_register4))
    label2.setText(str(slave_list4))


def modbus_write_single_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, register2, slave_value2 = args
    label0.setText(str("write single registers"))
    label1.setText(str(register2))
    label2.setText(str(slave_value2))


def modbus_read_discrete_inputs_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register2, slave_list2 = args
    label0.setText(str("read  discrete input"))
    label1.setText(str(starting_register2))
    label2.setText(str(slave_list2))


def modbus_write_multiple_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register6, slave_list6 = args
    label0.setText(str("write multiple registers"))
    label1.setText(str(slave_list6))
    label2.setText(str(slave_list6))


def modbus_write_multiple_coils_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register5, slave_list5 = args
    label0.setText(str("write multiple coils"))
    label1.setText(str(slave_list5))
    label2.setText(str(slave_list5))


def modbus_read_holding_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register3, slave_list3 = args
    label0.setText(str("read holding register"))
    label1.setText(str(starting_register3))
    label2.setText(str(slave_list3))


def setup():
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 79, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 73, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 67, 135, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    iso485_0 = ISO485Unit(2, port=(1, 2))
    iso485_0.init(
        tx_pin=None,
        rx_pin=None,
        baudrate=115200,
        data_bits=None,
        stop_bits=None,
        parity=None,
        ctrl_pin=None,
    )
    modbusrtuslave_0 = modbus.ModbusRTUSlave(iso485_0, device_address=1, verbose=True)
    modbusrtuslave_0.set_callback(modbusrtuslave_0.READ_COILS_EVENT, modbus_read_coils_cb)
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_SINGLE_COIL_EVENT, modbus_write_single_coil_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_INPUT_REGISTERS_EVENT, modbus_read_input_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_SINGLE_REGISTER_EVENT, modbus_write_single_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_DISCRETE_INPUTS_EVENT, modbus_read_discrete_inputs_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_MULTIPLE_REGISTERS_EVENT, modbus_write_multiple_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_MULTIPLE_COILS_EVENT, modbus_write_multiple_coils_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_HOLDING_REGISTERS_EVENT, modbus_read_holding_registers_cb
    )
    modbusrtuslave_0.add_coil(1000, True)
    modbusrtuslave_0.add_coil(1001, False)
    modbusrtuslave_0.add_coil(1002, True)
    modbusrtuslave_0.add_coil(1003, False)
    modbusrtuslave_0.add_coil(1004, True)
    modbusrtuslave_0.add_discrete_input(1000, True)
    modbusrtuslave_0.add_discrete_input(1001, False)
    modbusrtuslave_0.add_discrete_input(1002, True)
    modbusrtuslave_0.add_discrete_input(1003, False)
    modbusrtuslave_0.add_discrete_input(1004, True)
    modbusrtuslave_0.add_holding_register(1000, 0x0102)
    modbusrtuslave_0.add_holding_register(1001, 0x0304)
    modbusrtuslave_0.add_holding_register(1002, 0x0304)
    modbusrtuslave_0.add_holding_register(1003, 0x0304)
    modbusrtuslave_0.add_holding_register(1004, 0x0304)
    modbusrtuslave_0.add_input_register(1000, 0x0102)
    modbusrtuslave_0.add_input_register(1001, 0x0304)
    modbusrtuslave_0.add_input_register(1002, 0x0304)
    modbusrtuslave_0.add_input_register(1003, 0x0304)
    modbusrtuslave_0.add_input_register(1004, 0x0304)


def loop():
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    M5.update()
    modbusrtuslave_0.tick()


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
