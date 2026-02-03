# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import modbus
import network


label0 = None
label1 = None
label3 = None
label2 = None
wlan_sta = None
modbustcpserver_0 = None


starting_register4 = None
slave_list4 = None
starting_register1 = None
slave_list1 = None
starting_register2 = None
slave_list2 = None
register2 = None
slave_value2 = None
starting_register3 = None
slave_list3 = None
starting_register6 = None
slave_list6 = None
register1 = None
slave_value1 = None
starting_register5 = None
slave_list5 = None


def modbus_read_input_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register4, slave_list4 = args
    label0.setText(str("read input register"))
    label1.setText(str(starting_register4))
    label2.setText(str(slave_list4))


def modbus_read_coils_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register1, slave_list1 = args
    label0.setText(str("read coils"))
    label1.setText(str(starting_register1))
    label2.setText(str(slave_list1))


def modbus_read_discrete_inputs_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register2, slave_list2 = args
    label0.setText(str("read  discrete input"))
    label1.setText(str(starting_register2))
    label2.setText(str(slave_list2))


def modbus_write_single_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, register2, slave_value2 = args
    label0.setText(str("write single registers"))
    label1.setText(str(register2))
    label2.setText(str(slave_value2))


def modbus_read_holding_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register3, slave_list3 = args
    label0.setText(str("read holding register"))
    label1.setText(str(starting_register3))
    label2.setText(str(slave_list3))


def modbus_write_multiple_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register6, slave_list6 = args
    label0.setText(str("write multiple registers"))
    label1.setText(str(slave_list6))
    label2.setText(str(slave_list6))


def modbus_write_single_coil_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, register1, slave_value1 = args
    label0.setText(str("write single coil"))
    label1.setText(str(register1))
    label2.setText(str(slave_value1))


def modbus_write_multiple_coils_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register5, slave_list5 = args
    label0.setText(str("write multiple coils"))
    label0.setText(str(slave_list5))
    label0.setText(str(slave_list5))


def setup():
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 61, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 58, 94, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 53, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 58, 133, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan_sta = network.WLAN(network.STA_IF)
    while not (wlan_sta.isconnected()):
        pass
    label3.setText(str(wlan_sta.ifconfig()[0]))
    modbustcpserver_0 = modbus.ModbusTCPServer("0.0.0.0", 5000, device_address=1, verbose=False)
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_INPUT_REGISTERS_EVENT, modbus_read_input_registers_cb
    )
    modbustcpserver_0.set_callback(modbustcpserver_0.READ_COILS_EVENT, modbus_read_coils_cb)
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_DISCRETE_INPUTS_EVENT, modbus_read_discrete_inputs_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_SINGLE_REGISTER_EVENT, modbus_write_single_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_HOLDING_REGISTERS_EVENT, modbus_read_holding_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_MULTIPLE_REGISTERS_EVENT, modbus_write_multiple_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_SINGLE_COIL_EVENT, modbus_write_single_coil_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_MULTIPLE_COILS_EVENT, modbus_write_multiple_coils_cb
    )
    modbustcpserver_0.add_coil(1000, True)
    modbustcpserver_0.add_coil(1001, False)
    modbustcpserver_0.add_coil(1002, True)
    modbustcpserver_0.add_coil(1003, False)
    modbustcpserver_0.add_coil(1004, True)
    modbustcpserver_0.add_discrete_input(1000, True)
    modbustcpserver_0.add_discrete_input(1001, False)
    modbustcpserver_0.add_discrete_input(1002, True)
    modbustcpserver_0.add_discrete_input(1003, False)
    modbustcpserver_0.add_discrete_input(1004, True)
    modbustcpserver_0.add_holding_register(1000, 0x0102)
    modbustcpserver_0.add_holding_register(1001, 0x0304)
    modbustcpserver_0.add_holding_register(1002, 0x0506)
    modbustcpserver_0.add_holding_register(1003, 0x0708)
    modbustcpserver_0.add_holding_register(1004, 0x090A)
    modbustcpserver_0.add_input_register(1000, 0x0102)
    modbustcpserver_0.add_input_register(1001, 0x0304)
    modbustcpserver_0.add_input_register(1002, 0x0506)
    modbustcpserver_0.add_input_register(1003, 0x0708)
    modbustcpserver_0.add_input_register(1004, 0x090A)
    modbustcpserver_0.start()


def loop():
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    M5.update()
    modbustcpserver_0.tick()


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
