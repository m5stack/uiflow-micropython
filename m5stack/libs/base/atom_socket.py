# -*- encoding: utf-8 -*-
"""
@File    :   atom_socket.py
@Time    :   2024/3/29
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

import sys

if sys.platform != "esp32":
    from typing import Literal
from micropython import const

import machine
import time
import _thread
import struct


class ATOMSocketBase:
    """! ATOM Socket is a smart power socket adapted to ATOM main control.

    @en ATOM Socket is a smart power socket adapted to ATOM main control. Built-in HLW8032 high-precision energy metering IC. It can measure the voltage, current, power, and energy of the load. It can also be used as a smart socket to control the power on and off of the load. It can be used in various scenarios such as smart home, industrial control, and energy management.
    @cn ATOM Socket 是集成了M5 ATOM作为控制器的智能电源插座。内置HLW8032高精度电能表IC，可以测量负载的电压、电流、功率和能量。同时也可以作为智能插座控制负载的开关，可以应用于智能家居、工业控制、能源管理等各种场景。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/atom/atom_socket
    @image https://static-cdn.m5stack.com/resource/docs/products/atom/atom_socket/atom_socket_01.webp
    @category Base

    @init
        from base import ATOMSocketBase
        atomsocket = ATOMSocketBase(1,(22,33),23) # for atom lite

    @test
        atomsocket.get_data() # got (230.4192, 0.02074951, 0.8106091, 0.0)
        atomsocket.set_relay(True)
        atomsocket.set_relay(False)
        atomsocket.get_voltage() # got 230.4192
        atomsocket.get_current() # got 0.02074951
        atomsocket.get_power() # got 0.8106091
        atomsocket.get_pf()
        atomsocket.get_inspecting_power() # got 4.774
        atomsocket.get_power_factor() # got 5.88235
        atomsocket.get_kwh() # got 0.0
        def f(voltage, current, power, kwh): print(voltage, current, power, kwh)
        atomsocket.receive_none_block(f)
        atomsocket.stop_receive_data()

    """

    def __init__(self, _id: Literal[0, 1, 2], port: list | tuple, relay: int = 23):
        """! Initialize the ATOM Socket.

        @param id serial id, no actual use for this base.
        @param port UART pin number.
        @param relay The relay pin number.
        """
        self.uart = machine.UART(_id, tx=port[1], rx=port[0])
        self.uart.init(4800, bits=8, parity=None, stop=1, rxbuf=256)
        self.relay = machine.Pin(relay, machine.Pin.OUT)
        self.recv_running = False
        self.receive_callback = None
        self.voltage = 0
        self.current = 0
        self.power = 0
        self.pf = 0
        self.pf_data = 0
        self.kwh = 0

    def set_relay(self, state: bool) -> None:
        """! Set the relay state of the ATOM Socket.

        @param state The state of the relay.
        """
        self.relay.value(state)

    def get_data(self, timeout=3000) -> tuple:
        """! Get the data from the ATOM Socket.

        @param timeout The timeout of the function.

        @return The data of the ATOM Socket: Voltage (V), Current (A), Power (W), Total Energy (KWh). None if the timeout.

        """
        start = time.ticks_ms()
        while True:
            if time.ticks_ms() - start > timeout:
                return None

            if not self.uart.any():
                time.sleep_ms(1)
                continue

            time.sleep_ms(55)

            if self.uart.any() != 24:
                _ = self.uart.read()
                continue

            data = self.uart.read()

            if data[1] != 0x5A:
                _ = self.uart.read()
                continue

            vol_par = int.from_bytes(data[2:5], "big")
            vol_data = int.from_bytes(data[5:8], "big")
            self.voltage = (vol_par / vol_data) * 1.8
            current_par = int.from_bytes(data[8:11], "big")
            current_data = int.from_bytes(data[11:14], "big")
            self.current = (current_par / current_data) - 0.06
            power_par = int.from_bytes(data[14:17], "big")
            power_data = int.from_bytes(data[17:20], "big")
            self.power = (power_par / power_data) * 1.8
            self.pf = int.from_bytes(data[21:23], "big")
            if (data[20] & 0x80) == 0x80:
                self.pf_data += 1

            inspecting_pwr = self.get_inspecting_power()
            pf_cnt = (1 / power_par) * (1 / inspecting_pwr) * 1000000000 * 3600
            self.kwh = (self.pf_data * self.pf) / pf_cnt

            break

        return self.voltage, self.current, self.power, self.kwh

    def get_voltage(self) -> float:
        """! Get the voltage of the ATOM Socket."""
        return self.voltage

    def get_current(self) -> float:
        """! Get the current of the ATOM Socket."""
        return self.current

    def get_power(self) -> float:
        """! Get the power of the ATOM Socket."""
        return self.power

    def get_pf(self) -> int:
        """! Get the power factor of the ATOM Socket."""
        return self.pf

    def get_inspecting_power(self) -> float:
        """! Get the inspecting power of the ATOM Socket."""
        return self.get_voltage() * self.get_current()

    def get_power_factor(self) -> float:
        """! Get the power factor of the ATOM Socket."""
        return self.get_inspecting_power() / self.get_power()

    def get_kwh(self) -> float:
        """! Get the KWh of the ATOM Socket."""
        return self.kwh

    def stop_receive_data(self) -> None:
        """! Stop receiving data from the ATOM Socket."""
        self.recv_running = False
        time.sleep_ms(100)
        self.receive_callback = None

    def _recv_task(self) -> None:
        """! Thread to receive the data from the ATOM Socket."""

        _ = self.uart.read()
        while self.recv_running:
            if self.get_data() is not None:
                self.receive_callback(self.voltage, self.current, self.power, self.kwh)
            time.sleep_ms(10)

    def receive_none_block(self, receive_callback) -> None:
        """! Receive data from the ATOM Socket.  in none block mode."""

        if not self.recv_running:
            self.recv_running = True
            self.receive_callback = receive_callback
            # FIXME: Threads cannot be automatically destroyed when the
            # application is interrupted.
            _thread.start_new_thread(self._recv_task, ())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """! Stop receiving data from the ATOM Socket."""
        self.stop_receive_data()
