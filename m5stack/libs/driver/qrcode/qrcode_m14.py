# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import machine
from micropython import const
from driver.qrcode import serial_cmd_helper


class QRCodeM14:
    """
    此驱动适用于 M14 二维码识别模块
    """

    # 触发解码模式
    TRIGGER_MODE_KEY = const(0)  # 按键模式：触发单次解码，解码成功后停止解码
    TRIGGER_MODE_CONTINUOUS = const(
        1
    )  # 连续模式：触发连续解码，解码成功后继续解码，停止解码需要再次触发
    TRIGGER_MODE_AUTO = const(2)  # 自动模式：上电后连续解码，不可停止
    TRIGGER_MODE_PULSE = const(
        4
    )  # 脉冲模式：Trig 引脚低电平触发解码，在识读成功或达到单次读码时长限制时结束读取。
    TRIGGER_MODE_MOTION_SENSING = const(
        5
    )  # 移动感应模式：图像识别，当检测到场景发送变化时，开始解码。
    # 补光灯模式
    FILL_LIGHT_OFF = const(0)  # 常灭
    FILL_LIGHT_ON = const(3)  # 常亮
    FILL_LIGHT_ON_DECODE = const(2)  # 解码时亮
    # 定位灯模式
    POS_LIGHT_OFF = const(0)  # 常灭
    POS_LIGHT_ON_DECODE = const(2)  # 解码时亮
    POS_LIGHT_FLASH_ON_DECODE = const(1)  # 解码时闪烁

    def __init__(self, id: int = 1, tx: int = 5, rx: int = 6, trig: int = None, led=None) -> None:
        self.serial = machine.UART(id, baudrate=115200, tx=rx, rx=tx)  # 交叉
        self.serial_handler = serial_cmd_helper.SerialCmdHelper(self.serial, False)
        self.trig = None
        if trig is not None:
            self.trig = machine.Pin(trig, machine.Pin.OUT)
        self.led = led

    def set_trig(self, value: int) -> None:
        """Set trigger pin. 设置触发引脚。
        :param int value: ``0`` - 低电平，``1`` - 高电平。
        """
        if self.trig is not None:
            self.trig.value(value)
        else:
            raise RuntimeError("Trigger pin is not initialized.")

    def start_decode(self) -> None:
        """Start decode. 开始解码。"""
        cmd_start_decode = bytes([0x32, 0x75, 0x01])  # 开始解码
        self.serial_handler.cmd(cmd_start_decode)  # 此指令无返回

    def stop_decode(self) -> None:
        """Stop decode. 停止解码。"""
        cmd_stop_decode = bytes([0x32, 0x75, 0x02])
        cmd_stop_decode_ack = bytes([0x33, 0x75, 0x02, 0x00, 0x00])
        self.serial_handler.cmd(cmd_stop_decode, cmd_stop_decode_ack, timeout_ms=150)

    def read(self) -> None | bytes:
        """Read decode data. 读取解码数据。"""
        data = bytearray()
        timeout_ms = 50  # 等待数据接收完成 (115200 波特率接收 200 字符传输耗时 17.3 ms)
        gap_timeout = 3
        start_time = time.ticks_ms()
        last_recv_time = 0
        if self.serial.any() > 0:
            # 接收完整的一帧数据
            while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
                if self.serial.any() > 0:
                    chunk = self.serial.read()
                    if chunk:
                        data.extend(chunk)
                        last_recv_time = time.ticks_ms()
                elif time.ticks_diff(time.ticks_ms(), last_recv_time) > gap_timeout:
                    break
                time.sleep_ms(1)
            if data:
                return bytes(data)
        return None

    # ============================================================================
    # 识读模式
    # ============================================================================
    def set_trigger_mode(self, mode: int) -> None:
        """Set trigger mode. 设置触发解码模式。

        :param int mode: The decode trigger mode.
        """
        cmd_trigger_mode = bytes([0x21, 0x61, 0x41, mode])
        cmd_trigger_mode_ack = bytes([0x22, 0x61, 0x41, mode, 0x00])
        self.serial_handler.cmd(cmd_trigger_mode, cmd_trigger_mode_ack, timeout_ms=200)

    def set_decode_delay(self, delay_ms: int) -> None:
        """Set decode delay. 设置命令解码延迟 (按键模式)。

        :param int delay_ms: 解码延迟时间(单位：毫秒), 0 表示持续解码直到成功。
        """
        high_byte = (delay_ms >> 8) & 0xFF
        low_byte = delay_ms & 0xFF
        cmd = bytes([0x21, 0x61, 0x8A, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x61, 0x8A, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_trigger_timeout(self, timeout_ms: int) -> None:
        """Set trigger timeout. 设置触发超时。(脉冲模式)。

        :param int timeout_ms: 触发超时时间(单位：毫秒), 解码持续时间超过该值时自动停止。
        """
        high_byte = (timeout_ms >> 8) & 0xFF
        low_byte = timeout_ms & 0xFF
        cmd = bytes([0x21, 0x61, 0x82, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x61, 0x82, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_motion_sensitivity(self, level: int = 3) -> None:
        """Set motion detection sensitivity. 设置移动感应灵敏度。(感应模式中)

        :param int level: 灵敏度等级, 范围 1-5, 等级越高对场景变化越敏感, 默认等级为 3。
        """
        cmd = bytes([0x21, 0x61, 0x44, level])
        cmd_ack = bytes([0x22, 0x61, 0x44, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_continuous_decode_delay(self, delay_ms: int) -> None:
        """Set continuous decode delay. 设置持续解码延迟时间。(感应模式中)

        :param int delay_ms: 延迟时间，单位为 100 毫秒。值为 0 表示持续解码直到超时。
        """
        high_byte = (delay_ms >> 8) & 0xFF
        low_byte = delay_ms & 0xFF
        cmd = bytes([0x21, 0x61, 0x8C, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x61, 0x8C, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_trigger_decode_delay(self, delay_ms: int) -> None:
        """设置触发解码延迟时间(感应模式中)

        置触发解码延迟时间。当重新进入检测场景变化阶段，到检测到变化再次开始识读之间的延迟时长。

        :param int delay_ms: 触发解码延迟时间，单位为毫秒。
        """
        high_byte = (delay_ms >> 8) & 0xFF
        low_byte = delay_ms & 0xFF
        cmd = bytes([0x21, 0x61, 0x85, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x61, 0x85, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_same_code_interval(self, interval_ms: int) -> None:
        """Set same code interval. 设置同码间隔时间。

        :param interval_ms: 同一条码的重复识读间隔时间，单位为毫秒。
        """
        high_byte = (interval_ms >> 8) & 0xFF
        low_byte = interval_ms & 0xFF
        cmd = bytes([0x21, 0x64, 0x82, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x64, 0x82, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_diff_code_interval(self, interval_ms: int) -> None:
        """Set difference code interval. 设置异码间隔时间。

        :param int interval_ms: 不同条码的识读间隔时间，单位为毫秒。
        """
        high_byte = (interval_ms >> 8) & 0xFF
        low_byte = interval_ms & 0xFF
        cmd = bytes([0x21, 0x64, 0x81, high_byte, low_byte])
        cmd_ack = bytes([0x22, 0x64, 0x81, 0x00, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_same_code_no_delay(self, enable: bool) -> None:
        """Set same code no delay. 设置同码非延迟输出。

        :param bool enable: 是否开启同码非延迟输出, True 表示开启, False 表示关闭。
        """
        mode = 0x01 if enable else 0x00
        cmd = bytes([0x21, 0x64, 0x43, mode])
        cmd_ack = bytes([0x22, 0x64, 0x43, mode, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    # ============================================================================
    # 系统设置
    # ============================================================================
    def set_fill_light_mode(self, mode: int = FILL_LIGHT_ON_DECODE) -> None:
        """Set fill light mode. 设置补光灯模式。

        :param int mode: The fill light mode. Available options:
            - ``FILL_LIGHT_OFF``: Light off. 常灭
            - ``FILL_LIGHT_ON``: Light on. 常亮
            - ``FILL_LIGHT_ON_DECODE``: Light on during decoding. 解码时亮
        """
        cmd_fill_light = bytes([0x21, 0x62, 0x41, mode])
        cmd_fill_light_ack = bytes([0x22, 0x62, 0x41, mode, 0x00])
        self.serial_handler.cmd(cmd_fill_light, cmd_fill_light_ack, timeout_ms=100)

    def set_fill_light_brightness(self, brightness: int = 60) -> None:
        """Set fill light brightness. 设置补光灯亮度。

        :param int brightness: The fill light brightness. Range: 0~100.
        """
        brightness = max(0, min(100, brightness))
        cmd_light_brightness = bytes([0x21, 0x62, 0x48, brightness])
        cmd_light_brightness_ack = bytes([0x22, 0x62, 0x48, brightness, 0x00])
        self.serial_handler.cmd(cmd_light_brightness, cmd_light_brightness_ack, timeout_ms=100)

    def set_pos_light_mode(self, mode: int = POS_LIGHT_ON_DECODE) -> None:
        """Set positioning light mode. 设置定位灯模式。

        :param int mode: The positioning light mode. Available options:
            - ``POS_LIGHT_OFF``: Light off. 常灭
            - ``POS_LIGHT_ON_DECODE``: Light on during decoding. 解码时亮
            - ``POS_LIGHT_FLASH_ON_DECODE``: Light flash during decoding. 解码时闪烁
        """
        cmd_pos_light = bytes([0x21, 0x62, 0x42, mode])
        cmd_pos_light_ack = bytes([0x22, 0x62, 0x42, mode, 0x00])
        self.serial_handler.cmd(cmd_pos_light, cmd_pos_light_ack, timeout_ms=100)

    def set_startup_tone(self, mode: int) -> None:
        """Set startup tone. 设置启动提示音。

        :param mode: 0 - 关闭启动提示音
                     1 - 播放 4 声
                     2 - 播放 2 声
        """
        cmd_startup_tone = bytes([0x21, 0x63, 0x45, mode])
        cmd_startup_tone_ack = bytes([0x22, 0x63, 0x45, mode])
        self.serial_handler.cmd(cmd_startup_tone, cmd_startup_tone_ack, timeout_ms=150)

    def set_decode_success_beep(self, count: int) -> None:
        """Set decode success beep. 设置解码成功提示音次数。

        :param count: 0 - 无提示音
                      1 - 播放 1 次提示音
                      2 - 播放 2 次提示音
        """
        cmd_cfg_decode_beep = bytes([0x21, 0x63, 0x42, count])
        cmd_cfg_decode_beep_ack = bytes([0x22, 0x63, 0x42, count])
        self.serial_handler.cmd(cmd_cfg_decode_beep, cmd_cfg_decode_beep_ack, timeout_ms=150)

    # ============================================================================
    # 数据编辑
    # ============================================================================
    def set_case_conversion(self, mode: int = 0) -> None:
        """Set case conversion. 设置数据大小写转换模式。
        :param mode: 0x00 - 关闭（原始数据）
                     0x01 - 转大写（小写字母转换为大写）
                     0x02 - 转小写（大写字母转换为小写）
        """
        cmd = bytes([0x21, 0x51, 0x48, mode])
        cmd_ack = bytes([0x22, 0x51, 0x48, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def set_protocol_format(self, mode: int) -> None:
        """Set protocol format. 设置协议格式。
        :param mode: 0 - 无协议
                     1 - 格式 1: [0x03] + 数据长度(2bytes) + 数据
                     2 - 格式 2: [0x03] + 数据长度 + 条码个数 + 条码 1 数据长度 + 条码 1 数据 +... + CRC
                     3 - 格式 3: [0x03] + 数据长度 + 条码个数 + 条码 1ID 号 + 条码 1 数据长度 + 条码 1 数据 + ... + CRC
        """
        cmd = bytes([0x21, 0x51, 0x43, mode])
        cmd_ack = bytes([0x22, 0x51, 0x43, 0x00])
        self.serial_handler.cmd(cmd, cmd_ack, timeout_ms=200)

    def get_version(self, timeout_ms=500):
        self.serial.read()
        self.serial.write(b'\x43\x02\xc1') # 查询版本
        start = time.ticks_ms()
        rx = b''
        while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
            if self.serial.any():
                time.sleep_ms(5)
                rx += self.serial.read()
                data_len = (rx[3] << 8)  + rx[4]
                if len(rx) >= 4 + data_len:
                    if rx[0] == 0x44 and rx[1] == 0x02 and rx[2] == 0xC1:
                        total_len = 4 + data_len
                        if len(rx) >= total_len:
                            payload = rx[4:4 + data_len + 1]
                            try:
                                version_str = payload.decode('ascii')
                                return version_str[1:]
                            except:
                                return None
                    else:
                        return None
            time.sleep_ms(1)
        return None
