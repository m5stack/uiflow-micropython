# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import time
import _thread
import cdriver
import micropython

if sys.platform != "esp32":
    from typing import Literal


class DMX512:
    """! DMX512 communication unit.
    @en DMX Unit is a communication unit specifically designed for DMX-512 data transmission scenarios. It integrates the CA-IS3092W isolated half-duplex RS-485 transceiver, providing up to 5kVrms electrical isolation protection.
    @cn DMX Unit 是一款专为 DMX-512 数据传输场景设计的通信单元。

    @color #0FEA97
    @link https://docs.m5stack.com/en/unit/UNIT-DMX
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/DMX/heart_01.webp
    @category unit

    @example
        from unit import HeartUnit
        from hardware import I2C
        i2c = I2C(1, scl=33, sda=32)
        heart = HeartUnit(i2c)
        heart.start()
        heart.get_heart_rate();heart.get_spo2()
    """

    DMX_MASTER = 1
    DMX_SLAVE = 2

    def __init__(
        self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, mode: int = DMX_MASTER
    ) -> None:
        """! Initializes the DMX512 unit with a specified UART ID and port pins.

        @param id UART device ID.
        @param port UART TX and RX pins.
        @param mode Operating mode (1 for Master, 2 for Slave).
        """
        self.port_id = id
        self.dmx_mode = mode
        self.dmx_tx = port[1]
        self.dmx_rx = port[0]
        self.dmx_ch = 1
        self.recv_running = False
        self.receive_callbacks = {}
        self._last_data = {}
        self.dmx_init(self.dmx_mode)

    def dmx_init(self, mode=DMX_MASTER) -> None:
        """! Initializes the DMX512 communication with the specified UART pins and mode.

        @param mode Operating mode (1 for Master, 2 for Slave).
        """
        self.dmx_mode = mode
        cdriver.esp_dmx.dmx_init(self.port_id, self.dmx_tx, self.dmx_rx, -1, self.dmx_mode)
        cdriver.esp_dmx.dmx_clear_buffer()
        time.sleep_ms(50)

    def write_data(self, channel, data) -> None:
        """! Updates the data for a specified DMX channel. Data is sent on the next update cycle.

        @param channel DMX channel number (1-512).
        @param data Data value to be sent (0-255).
        @raises ValueError if the channel number is out of range.
        """
        if not (1 <= channel <= 512):
            raise ValueError("Channel selection error")
        if self.dmx_mode == self.DMX_MASTER:
            self.dmx_ch = channel
            self.dmx_data = data
            cdriver.esp_dmx.dmx_write_data(self.dmx_ch, self.dmx_data)

    def read_data(self, channel) -> int:
        """! Reads data from a specified DMX channel in Slave mode.

        @param channel DMX channel number (1-512).
        @return Data value received from the DMX channel.
        @raises ValueError if the channel number is out of range.
        """
        if not (1 <= channel <= 512):
            raise ValueError("Channel selection error")
        self.dmx_ch = channel
        if self.dmx_mode == self.DMX_SLAVE:
            return cdriver.esp_dmx.dmx_read_data(channel)

    def clear_buffer(self) -> None:
        """! Clears the DMX buffer and resets the data."""
        self.dmx_data = 0
        cdriver.esp_dmx.dmx_clear_buffer()

    def deinit(self) -> None:
        """! Deinitializes the DMX512 unit and stops any ongoing operations."""
        if self.dmx_mode == self.DMX_MASTER:
            cdriver.esp_dmx.dmx_deinit()
        self.receive_callbacks.clear()
        self.clear_buffer()
        self.stop_receive()

    def _recv_task(self) -> None:
        """! Internal task that runs in a separate thread to handle non-blocking DMX data reception."""
        while self.recv_running:
            for channel in self.receive_callbacks.keys():
                data = self.read_data(channel)
                if self._last_data[channel] != data:
                    self._last_data[channel] = data
                    self.receive_callbacks[channel](data)

            time.sleep_ms(10)

    def receive_none_block(self) -> None:
        """! Starts non-blocking data reception for the specified channels with associated callbacks."""
        if not self.recv_running:
            self.recv_running = True
            _thread.start_new_thread(self._recv_task, ())

    def stop_receive(self) -> None:
        """! Stops the non-blocking data reception task."""
        self.recv_running = False
        time.sleep_ms(50)

    def attach_channel(self, channel, callback) -> None:
        """! Attaches a callback function to a specified DMX channel.

        @param channel DMX channel number (1-512) to attach the callback to.
        @param callback The function to be called when data changes on the specified channel.
        """
        self.receive_callbacks[channel] = callback
        self._last_data[channel] = 0

    def detach_channel(self, channel):
        """! Detaches the callback function from a specified DMX channel.

        @param channel DMX channel number (1-512) to detach the callback from.
        """
        self.receive_callbacks.pop(channel)
        self._last_data.pop(channel)
