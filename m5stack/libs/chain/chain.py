# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time
import struct
import m5utils
import warnings
import _thread
import micropython

CMD_SET_RGB_VALUE = 0x20  # Set RGB value
CMD_GET_RGB_VALUE = 0x21  # Get RGB value
CMD_SET_RGB_BRIGHTNESS = 0x22  # Set RGB brightness
CMD_GET_RGB_BRIGHTNESS = 0x23  # Get RGB brightness
CMD_GET_BOOTLOADER_VERSION = 0xF9  # Get bootloader version
CMD_GET_FIRMWARE_VERSION = 0xFA  # Get firmware version
CMD_GET_DEVICE_TYPE = 0xFB  # Get device type
CMD_ENUM_REQUEST = 0xFC  # Enumeration request
CMD_HEARTBEAT = 0xFD  # Heartbeat command
CMD_ENUM_RESPONSE = 0xFE  # Enumeration response

STATUS_OK = 0x00  # Operation successful.
STATUS_PARAMETER_ERROR = 0x01  # Parameter error.
STATUS_RETURN_PACKET_ERROR = 0x02  # Return packet error.
STATUS_BUSY = 0x04  # Device is busy.
STATUS_TIMEOUT = 0x05  # Operation timeout.

CHAIN_DEVICE_TYPE_UNKNOWN = 0x0000  # Unknown device type
CHAIN_DEVICE_TYPE_ENCODER = 0x0001  # Encoder device type
CHAIN_DEVICE_TYPE_ANGLE = 0x0002  # Angle device type
CHAIN_DEVICE_TYPE_KEY = 0x0003  # Key device type
CHAIN_DEVICE_TYPE_JOYSTICK = 0x0004  # Joystick device type
CHAIN_DEVICE_TYPE_TOF = 0x0005  # ToF device type
CHAIN_DEVICE_TYPE_UART = 0x0006  # UART device type
CHAIN_DEVICE_TYPE_SWITCH = 0x0007  # Switch device type
CHAIN_DEVICE_TYPE_PEDAL = 0x0008  # Pedal device type
CHAIN_DEVICE_TYPE_PIR = 0x0009  # PIR device type
CHAIN_DEVICE_TYPE_MIC = 0x000A  # Microphone device type


class RecvData:
    def __init__(self, state, length, data, crc):
        self.recv_time = time.ticks_ms()
        self.state = state
        self.length = length
        self.device_id = 0
        self.cmd = 0
        self.payload = data
        self.crc = crc
        self.payload_len = 0


class ChainLinkLayer:
    RECV_STATE_HEAD1 = 0x01
    RECV_STATE_HEAD2 = 0x02
    RECV_STATE_LEN1 = 0x03
    RECV_STATE_LEN2 = 0x04
    RECV_STATE_DEVICE_ID = 0x05
    RECV_STATE_CMD = 0x06
    RECV_STATE_PAYLOAD = 0x07
    RECV_STATE_CRC = 0x08
    RECV_STATE_TAIL1 = 0x09
    RECV_STATE_TAIL2 = 0x0A

    def __init__(self, uart, verbose=False):
        self.uart = uart
        self._verbose = verbose
        self._recv_data = RecvData(self.RECV_STATE_HEAD1, 0, bytearray(), 0)
        self._packet_queue = []
        self._device_num = 0

    # CRC 校验算法：就是求和
    def _crc(self, indx, cmd, data):
        crc = 0
        crc += cmd
        crc += indx
        crc += sum(data)
        return crc & 0xFF

    # 发送完整数据包
    def _send_packet(self, index, cmd, data=b""):
        # 构建数据体: [长度低, 长度高, 索引, 命令] + 数据
        packet_len = 2 + 2 + 1 + 1 + len(data) + 1 + 2
        packet = bytearray(packet_len)

        # 帧头
        offset = 0
        struct.pack_into("<BB", packet, offset, 0xAA, 0x55)
        offset += 2

        # 数据长度
        # 长度字段包含 INDEX CMD DATA CRC (1 + 1 + len(data) + 1)
        struct.pack_into("<H", packet, offset, len(data) + 3)
        offset += 2

        # 索引
        struct.pack_into("<B", packet, offset, index)
        offset += 1

        # 命令
        struct.pack_into("<B", packet, offset, cmd)
        offset += 1

        # 数据
        if data:
            struct.pack_into(f"<{len(data)}s", packet, offset, data)
            offset += len(data)

        # CRC 校验
        crc = self._crc(cmd, index, data)
        struct.pack_into("<B", packet, offset, crc)
        offset += 1

        # 帧尾
        struct.pack_into("<BB", packet, offset, 0x55, 0xAA)
        offset += 2

        if self._verbose:
            print("[HOST] >>> [Chain]: ", end="")
            print(" ".join(["%02X" % b for b in packet]))

        self.uart.write(packet)

    # 接收并解析数据包
    def _decode_packet(self, buf: bytes, timeout_ms=None) -> bool:
        if self._verbose:
            print("[HOST] <<< [Chain]: ", end="")
            print(" ".join(["%02X" % b for b in buf]))

        decoded = False

        for b in buf:
            # if self._verbose:
            #     print("current state:", self._recv_data.state)
            if self._recv_data.state == self.RECV_STATE_HEAD1:
                # 查找帧头 0xAA
                if b == 0xAA:
                    # 初始化接收数据
                    self._recv_data.recv_time = time.ticks_ms()
                    self._recv_data.payload = bytearray()
                    self._recv_data.length = 0
                    self._recv_data.payload_len = 0
                    self._recv_data.crc = 0
                    # 转到下一个状态
                    self._recv_data.state = self.RECV_STATE_HEAD2
            elif self._recv_data.state == self.RECV_STATE_HEAD2:
                # 查找帧头 55
                if b == 0x55:
                    self._recv_data.state = self.RECV_STATE_LEN1
                else:
                    self._recv_data.state = self.RECV_STATE_HEAD1
            elif self._recv_data.state == self.RECV_STATE_LEN1:
                self._recv_data.length = b
                self._recv_data.state = self.RECV_STATE_LEN2
            elif self._recv_data.state == self.RECV_STATE_LEN2:
                self._recv_data.length = self._recv_data.length | (b << 8)
                self._recv_data.payload_len = 0
                self._recv_data.state = self.RECV_STATE_DEVICE_ID
            elif self._recv_data.state == self.RECV_STATE_DEVICE_ID:
                self._recv_data.device_id = b
                self._recv_data.state = self.RECV_STATE_CMD
            elif self._recv_data.state == self.RECV_STATE_CMD:
                self._recv_data.cmd = b
                if self._recv_data.length - 3 == 0:
                    self._recv_data.state = self.RECV_STATE_CRC
                else:
                    self._recv_data.state = self.RECV_STATE_PAYLOAD
            elif self._recv_data.state == self.RECV_STATE_PAYLOAD:
                self._recv_data.payload.append(b)
                self._recv_data.payload_len += 1
                if self._recv_data.payload_len == self._recv_data.length - 3:
                    self._recv_data.state = self.RECV_STATE_CRC
            elif self._recv_data.state == self.RECV_STATE_CRC:
                self._recv_data.crc = b
                self._recv_data.state = self.RECV_STATE_TAIL1
            elif self._recv_data.state == self.RECV_STATE_TAIL1:
                if b == 0x55:
                    self._recv_data.state = self.RECV_STATE_TAIL2
                else:
                    self._recv_data.state = self.RECV_STATE_HEAD1
            elif self._recv_data.state == self.RECV_STATE_TAIL2:
                self._recv_data.state = self.RECV_STATE_HEAD1
                if b == 0xAA:
                    crc = self._crc(
                        self._recv_data.cmd, self._recv_data.device_id, self._recv_data.payload
                    )
                    if crc != self._recv_data.crc:
                        warnings.warn("CRC check failed")
                    else:
                        if self._recv_data.cmd not in (CMD_HEARTBEAT, CMD_ENUM_REQUEST):
                            self._packet_queue.append(
                                (
                                    self._recv_data.recv_time,
                                    self._recv_data.device_id,
                                    self._recv_data.cmd,
                                    self._recv_data.payload,
                                )
                            )
                            if self._verbose:
                                print("[HOST] <<< [Chain]: ", end="")
                                print(
                                    "time=%d,device_id=%02X,cmd=%02X,payload=%s"
                                    % (
                                        self._recv_data.recv_time,
                                        self._recv_data.device_id,
                                        self._recv_data.cmd,
                                        " ".join(["%02X" % b for b in self._recv_data.payload]),
                                    )
                                )
                            decoded = True
        return decoded

    def _clear_old_packets(self):
        """清理队列中超过 5 秒的旧数据包。"""
        current_time = time.ticks_ms()
        for i in range(len(self._packet_queue) - 1, -1, -1):
            pkt_time = self._packet_queue[i][0]
            if time.ticks_diff(current_time, pkt_time) > 5000:
                del self._packet_queue[i]

    def _receive_packet(
        self, device_id, cmd, remove_repeated=False, timeout_ms=3000
    ) -> (bool, bytearray):
        """从队列中等待并获取匹配的数据包。

        - device_id/cmd: 目标设备与命令。
        - remove_repeated: 若为 True，则删除队列中所有与 (device_id, cmd) 匹配的重复项，
          并返回其中最新的一条；若为 False，则返回并移除遇到的第一条。
        - timeout_ms: 超时毫秒数。
        返回 (state, payload): state=True 表示获取成功，payload 为数据；否则返回 (False, 空 bytearray)。
        """
        start = time.ticks_ms()
        while True:
            if not remove_repeated:
                # 旧行为：命中第一条即返回
                for i, (_, dev_id, command, payload) in enumerate(self._packet_queue):
                    if dev_id == device_id and command == cmd:
                        del self._packet_queue[i]
                        return (True, payload)
            else:
                # 删除重复项：收集所有匹配项索引，删除并返回最新一条
                match_indices = [
                    i
                    for i, (_, dev_id, command, _) in enumerate(self._packet_queue)
                    if dev_id == device_id and command == cmd
                ]
                if match_indices:
                    last_idx = match_indices[-1]
                    payload = self._packet_queue[last_idx][2]
                    # 反向删除，避免索引移动
                    for idx in reversed(match_indices):
                        del self._packet_queue[idx]
                    return (True, payload)

            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                break
            time.sleep_ms(10)
        return (False, bytearray())

    def receive_packet(self, device_id, cmd, remove_repeated=False) -> (bool, bytearray):
        """从队列中等待并获取匹配的数据包。

        - device_id/cmd: 目标设备与命令。
        - remove_repeated: 若为 True，则删除队列中所有与 (device_id, cmd) 匹配的重复项，
          并返回其中最新的一条；若为 False，则返回并移除遇到的第一条。
        - timeout_ms: 超时毫秒数。
        返回 (state, payload): state=True 表示获取成功，payload 为数据；否则返回 (False, 空 bytearray)。
        """

        if not remove_repeated:
            # 旧行为：命中第一条即返回
            for i, (_, dev_id, command, payload) in enumerate(self._packet_queue):
                if dev_id == device_id and command == cmd:
                    del self._packet_queue[i]
                    return (True, payload)
        else:
            # 删除重复项：收集所有匹配项索引，删除并返回最新一条
            match_indices = [
                i
                for i, (_, dev_id, command, _) in enumerate(self._packet_queue)
                if dev_id == device_id and command == cmd
            ]
            if match_indices:
                last_idx = match_indices[-1]
                payload = self._packet_queue[last_idx][2]
                # 反向删除，避免索引移动
                for idx in reversed(match_indices):
                    del self._packet_queue[idx]
                return (True, payload)
        return (False, bytearray())

    def set_rgb_color(self, device_id: int, index: int, color: int) -> bool:
        """set RGB color.

        :param device_id: Device ID.
        :param index: Index of the RGB LED.
        :param color: RGB color value.
        """
        payload = struct.pack("BB3s", index & 0xFF, 1, color.to_bytes(3, "big"))
        state, response = self.send(device_id, CMD_SET_RGB_VALUE, payload)
        if state:
            return response[0] == 1
        return False

    def fill_rgb_color(self, device_id: int, index: int, num: int, color: int) -> bool:
        """fill RGB color.
        :param int device_id: Device ID.
        :param int index: Start index of the RGB LED.
        :param int num: Number of LEDs to fill.
        :param int color: RGB color value.
        """
        payload = struct.pack(
            "BB%ds" % (num * 3), index & 0xFF, num & 0xFF, color.to_bytes(3, "big") * num
        )
        state, response = self.send(device_id, CMD_SET_RGB_VALUE, payload)
        if state:
            if response[0] == 1:
                return True
        return False

    def get_rgb_color(self, device_id: int, index: int) -> int:
        """Get RGB color.

        :param int device_id: Device ID.
        :param int index: Index of the RGB LED.
        :return: RGB color value.
        """
        payload = struct.pack("BB", index & 0xFF, 1)
        state, response = self.send(device_id, CMD_GET_RGB_VALUE, payload)
        if state and response and len(response) == 4:
            if response[0] == 1:
                r = response[2]
                g = response[3]
                b = response[4]
                return (r << 16) | (g << 8) | b
        return -1

    def set_rgb_brightness(self, device_id: int, brightness: int, save: bool = False) -> bool:
        """Set rgb brightness.

        :param int device_id: Device ID.
        :param int brightness: Brightness value (0-100).
        :param bool save: Whether to save the brightness value to flash.
        """
        payload = struct.pack("BB", brightness & 0xFF, 1 if save else 0)
        state, response = self.send(device_id, CMD_SET_RGB_BRIGHTNESS, payload)
        if state and response:
            return response[0] == 1
        return False

    def get_rgb_brightness(self, device_id: int) -> int:
        """Get rgb brightness."""
        state, response = self.send(device_id, CMD_GET_RGB_BRIGHTNESS, bytes())
        if state and response:
            return response[0]
        return -1

    def get_bootloader_version(self, device_id: int) -> int:
        """Get bootloader version.

        :param int device_id: Device ID.
        :return: Bootloader version.
        """
        state, response = self.send(device_id, CMD_GET_BOOTLOADER_VERSION, bytes())
        if state and response:
            return response[0]
        return -1

    def get_firmware_version(self, device_id: int) -> int:
        """Get firmware version.

        :param int device_id: Device ID.
        :return: Firmware version.
        """
        state, response = self.send(device_id, CMD_GET_FIRMWARE_VERSION, bytes())
        if state and response:
            return response[0]
        return -1

    def get_device_type(self, device_id: int) -> int:
        """Get device type.

        :param int device_id: Device ID.
        :return: Device type.
        """
        state, response = self.send(device_id, CMD_GET_DEVICE_TYPE, bytes())
        if state and response:
            return struct.unpack("<H", response)[0]
        return -1

    def send_heartbeat(self):
        """Send heartbeat command."""
        state, _ = self.send(0xFD, CMD_HEARTBEAT, bytes())
        return state

    def get_device_num(self) -> int:
        """Get connected device number."""
        state, response = self.send(0xFF, CMD_ENUM_RESPONSE, b"\x00")
        if state and response:
            self._device_num = response[0]
            return self._device_num
        return 0

    def send(self, device_id: int, cmd: int, payload: bytes) -> (bool, bytes):
        """Send custom command to device.

        :param int device_id: Device ID.
        :param int cmd: Command.
        :param bytes payload: Data.
        :return: True if success, False otherwise.
        """
        if device_id != 0xFF and device_id > self._device_num:
            warnings.warn(f"Device ID {device_id} is disconnected.")
        for _ in range(3):
            self._send_packet(device_id, cmd, payload)
            time.sleep_ms(10)
            state, response = self._receive_packet(device_id, cmd)
            if state:
                return (state, response)
        return (False, b"")


class ChainBus:
    """Create a Chain bus instance.

    :param int id: UART ID.
    :param int tx: TX pin.
    :param int rx: RX pin.
    :param bool verbose: Enable verbose mode. Default is False.

    UiFlow2 Code Block:

        |get_device_num.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, id, tx, rx, verbose=False):
        if self._initialized:
            return
        self.uart = machine.UART(id, baudrate=115200, tx=tx, rx=rx, rxbuf=2048)
        if self.uart.any() > 0:
            self.uart.read()  # flush rx buffer
        self._verbose = verbose

        self._device = []
        self._event = []
        self.chainll = ChainLinkLayer(self.uart, verbose=self._verbose)
        # self.timer = m5utils.Timer(
        #     0, mode=m5utils.Timer.ONE_SHOT, period=3000, callback=self._device_connect_task
        # )
        self.new_device_handler = None
        self.disconnect_device_handler = None
        self._running = True
        _thread.start_new_thread(self._recv_task, ())
        self.device_num = self.chainll.get_device_num()
        self._initialized = True

    def register_device(self, device):
        """Register a Chain device.

        :param ChainDevice device: Chain device instance.
        """
        self._device.append(device)

    def register_event(self, device, cmd, payload, callback):
        self._event.append((device, cmd, payload, callback))

    def send(self, device_id: int, cmd: int, payload: bytes, timeout_ms: int) -> bytes:
        """Send custom command to device.

        :param int device_id: Device ID.
        :param int cmd: Command.
        :param bytes payload: Data.
        :param int timeout_ms: receive timeout in milliseconds.

        :return: Response data.
        :rtype: bytes

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                chainbus_0.send(1, 0x20, b"\x00\x01\xFF\x00\x00", 3000)
        """
        for _ in range(3):
            self.chainll._send_packet(device_id, cmd, payload)
            state, response = self.chainll._receive_packet(device_id, cmd, timeout_ms=timeout_ms)
            if state:
                return response
        return b""

    def get_device_num(self) -> int:
        """Get connected device number.

        :return: Number of connected devices.
        :rtype: int

        UiFlow2 Code Block:

            |get_device_num.png|

        MicroPython Code Block:

            .. code-block:: python

                num = chainbus_0.get_device_num()
        """
        return self.chainll.get_device_num()

    def set_device_connected_handler(self, handler):
        """Set new device connection handler callback.

        :param function handler: Callback function.
        """
        self.new_device_handler = handler

    def set_device_disconnected_handler(self, handler):
        """Set device disconnection handler callback.

        :param function handler: Callback function.
        """
        self.disconnect_device_handler = handler

    def _recv_task(self):
        decoded = False
        last_clear_time = time.ticks_ms()
        while self._running:
            # recv data
            if self.uart.any() > 0:
                decoded = self.chainll._decode_packet(self.uart.read())

            # handle registered events
            if decoded:
                for device, cmd, payload, callback in self._event:
                    state, response = self.chainll.receive_packet(device.device_id, cmd)
                    if state and response == bytearray(payload) and callback:
                        micropython.schedule(callback, None)

            # 5s clear old packets in queue
            if time.ticks_ms() - last_clear_time > 5000:
                self.chainll._clear_old_packets()
                last_clear_time = time.ticks_ms()

            time.sleep_ms(10)

    def _device_connect_task(self, timer):
        new_device_num = self.chainll.get_device_num()
        if new_device_num < self.device_num:
            # device disconnected
            if self.disconnect_device_handler:
                for device_id in range(new_device_num + 1, self.device_num + 1):
                    micropython.schedule(self.disconnect_device_handler, (device_id,))
        elif new_device_num > self.device_num:
            # new device connected
            if self.new_device_handler:
                for device_id in range(self.device_num + 1, new_device_num + 1):
                    device_type = self.chainll.get_device_type(device_id)
                    micropython.schedule(self.new_device_handler, (device_id, device_type))
        self.device_num = new_device_num
        self.timer.init(
            period=3000, mode=m5utils.Timer.ONE_SHOT, callback=self._device_connect_task
        )

    def deinit(self):
        """Deinitialize the Chain bus."""
        if hasattr(self, "timer"):
            self.timer.deinit()
        self._running = False
        ChainBus._instance = None
        self._initialized = False
