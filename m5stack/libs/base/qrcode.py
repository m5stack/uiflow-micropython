# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import machine
from micropython import const
from driver.qrcode import serial_cmd_helper


class AtomicQRCodeBase:
    """Create an AtomicQRCodeBase object.

    :param int id: UART id.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.
    :param int trig: the trigger pin.
    :param int done: the receive done pin.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicQRCodeBase

            base_qrcode = AtomicQRCodeBase(id = 1, tx = 6, rx = 5, trig = 7, done = 8)
    """

    # 触发解码模式
    TRIGGER_MODE_KEY = const(0)  # 按键模式：触发单次解码，解码成功后停止解码
    TRIGGER_MODE_HOST = const(
        8
    )  # 主机模式：指令控制开始/停止解码，触发解码后超时为识别或解码成功将停止解码。
    TRIGGER_MODE_AUTO = const(4)  # 自动模式：上电后连续解码
    TRIGGER_MODE_PULSE = const(
        2
    )  # 脉冲模式：Trig 引脚低电平触发解码，在识读成功或达到单次读码时长限制时结束读取。
    TRIGGER_MODE_MOTION_SENSING = const(
        9
    )  # 移动感应模式：图像识别，当检测到场景发送变化时，开始解码。
    # 补光灯模式
    FILL_LIGHT_ON_DECODE = const(0)  # 解码时亮
    FILL_LIGHT_ON = const(1)  # 常亮
    FILL_LIGHT_OFF = const(2)  # 常灭
    # 定位灯模式
    POS_LIGHT_ON_DECODE = const(0)  # 解码时亮
    POS_LIGHT_ON = const(1)  # 常亮
    POS_LIGHT_OFF = const(2)  # 常灭
    cmd_ack = bytes([0x04, 0xD0, 0x00, 0x00, 0xFF, 0x2C])

    def __init__(
        self, id: int = 1, tx: int = 5, rx: int = 6, trig: int = 7, done: int = 8
    ) -> None:
        self.serial = machine.UART(id, baudrate=9600, tx=rx, rx=tx, timeout=100)
        self.serial_handler = serial_cmd_helper.SerialCmdHelper(self.serial, False)
        self.trig = machine.Pin(trig, machine.Pin.OUT)
        self.done = machine.Pin(done, machine.Pin.IN)
        self.serial.write(b"\x00")  # 唤醒设备
        time.sleep_ms(100)
        self.serial.read()

    def set_trig(self, value: int) -> None:
        """Set trigger value.

        :param int value: ``0`` - Low level, ``1`` - High level.

        UiFlow2 Code Block:

            |set_trig.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_trig(value)
        """
        self.trig.value(value)

    def start_decode(self) -> None:
        """Start decode.

        UiFlow2 Code Block:

            |start_decode.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.start_decode()
        """
        cmd_start_decode = bytes([0x04, 0xE4, 0x04, 0x00, 0xFF, 0x14])
        self.serial_handler.cmd(cmd_start_decode, self.cmd_ack, timeout_ms=100)

    def stop_decode(self) -> None:
        """Stop decode.

        UiFlow2 Code Block:

            |stop_decode.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.stop_decode()
        """
        cmd_stop_decode = bytes([0x04, 0xE5, 0x04, 0x00, 0xFF, 0x13])
        self.serial_handler.cmd(cmd_stop_decode, self.cmd_ack, timeout_ms=100)

    def read(self) -> None | bytes:
        """Read decode data.

        :returns: qrcode data.
        :rtype: None | bytes

        UiFlow2 Code Block:

            |read.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.read()
        """
        data = bytearray()
        timeout_ms = 500  # 等待数据接收完成 (115200 波特率接收 200 字符传输耗时 17.3 ms)
        gap_timeout = 3
        start_time = time.ticks_ms()
        last_recv_time = 0
        if self.done.value():  # 解码成功
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
        """Set trigger mode.

        :param int mode: The trigger mode. Available options:

            - ``TRIGGER_MODE_KEY``: Key Mode, Triggers a single decode; decoding stops after a successful read.
            - ``TRIGGER_MODE_HOST``: Host Mode, The command controls the start/stop of decoding. Once triggered, decoding will stop either upon successful decoding or after a timeout of 5 seconds.
            - ``TRIGGER_MODE_AUTO``: Auto Mode, Performs continuous decoding upon power-up and cannot be stopped.
            - ``TRIGGER_MODE_PULSE``: Pulse Mode, The Trig pin's low-level signal triggers decoding, which stops after a successful read or when the single read time limit is reached.
            - ``TRIGGER_MODE_MOTION_SENSING``: Motion Sensing Mode, Uses image recognition; decoding starts when a scene change is detected.

        UiFlow2 Code Block:

            |set_trigger_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_trigger_mode(mode)
        """
        check = {
            TRIGGER_MODE_KEY: 0x9D,
            TRIGGER_MODE_HOST: 0x95,
            TRIGGER_MODE_AUTO: 0x99,
            TRIGGER_MODE_PULSE: 0x9B,
            TRIGGER_MODE_MOTION_SENSING: 0x94,
        }
        cmd_trigger_mode = bytes([0x07, 0xC6, 0x04, 0x08, 0x00, 0x8A, mode, 0xFE, check[mode]])
        self.serial_handler.cmd_retry(cmd_trigger_mode, self.cmd_ack, timeout_ms=300)

    def set_decode_continuous(self, delay_100ms: int) -> None:
        """Set continuous decode time.

        :param int delay_100ms: Continuous scanning time(unit: 100ms). Range: 099, i.e., 025,500 ms (0 means unlimited).

        UiFlow2 Code Block:

            |set_decode_continuous.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_decode_continuous(delay_100ms)
        """
        if delay_100ms > 255:
            delay_100ms = 255
        cmd = bytes([0x07, 0xC6, 0x04, 0x08, 0x00, 0x88, delay_100ms, 0xFE, 0x9F - delay_100ms])
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=150)

    def set_decode_interval(self, interval_100ms: int) -> None:
        """Set decode interval.

        :param int interval_100ms: Decode interval time(unit: 100ms). Range: 0~99, i.e., 0~9,900 ms.

        UiFlow2 Code Block:

            |set_decode_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_decode_interval(interval_100ms)
        """
        if interval_100ms > 99:
            interval_100ms = 99
        cmd = bytes(
            [0x07, 0xC6, 0x04, 0x08, 0x00, 0x89, interval_100ms, 0xFE, 0x9E - interval_100ms]
        )
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=250)

    def set_same_code_interval(self, interval_100ms: int) -> None:
        """Set same code interval.

        :param int interval_100ms: Decode interval for the same code(unit: 100ms). Range: 0~99, i.e., 0~9,900 ms.

        UiFlow2 Code Block:

            |set_same_code_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_same_code_interval(interval_100ms)
        """
        if interval_100ms > 99:
            interval_100ms = 99
        cmd = bytearray([0x08, 0xC6, 0x04, 0x08, 0x00, 0xF3, 0x03, interval_100ms, 0xFE, 0])
        check = ((sum(cmd[:-2]) % 256) ^ 0xFF) + 1  # 求和取低字节，计算补码
        cmd[-1] = check
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=250)

    # ============================================================================
    # System config
    # ============================================================================
    def set_fill_light_mode(self, mode: int) -> None:
        """Set fill light mode.

        :param int mode: The fill light mode. Available options:
            - ``FILL_LIGHT_OFF``: Light off.
            - ``FILL_LIGHT_ON``: Light on.
            - ``FILL_LIGHT_ON_DECODE``: Light on during decoding.

        UiFlow2 Code Block:

            |set_fill_light_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_fill_light_mode(mode)
        """
        cmd_fill_light = bytes([0x08, 0xC6, 0x04, 0x08, 0x00, 0xF2, 0x02, mode, 0xFE, 0x32 - mode])
        self.serial_handler.cmd(cmd_fill_light, self.cmd_ack, timeout_ms=150)

    def set_pos_light_mode(self, mode: int) -> None:
        """Set positioning light mode.

        :param int mode: The positioning light mode. Available options:
            - ``POS_LIGHT_OFF``: Light off.
            - ``POS_LIGHT_ON``: Light on.
            - ``POS_LIGHT_ON_DECODE``: Light flash during decoding.

        UiFlow2 Code Block:

            |set_pos_light_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_pos_light_mode(mode)
        """
        cmd_pos_light = bytes([0x08, 0xC6, 0x04, 0x08, 0x00, 0xF2, 0x03, mode, 0xFE, 0x31 - mode])
        self.serial_handler.cmd(cmd_pos_light, self.cmd_ack, timeout_ms=150)

    def set_startup_tone(self, enable: bool) -> None:
        """Set startup tone.

        :param bool enable: True - Enable startup tone, False - Disable startup tone.

        UiFlow2 Code Block:

            |set_startup_tone.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_startup_tone(enable)
        """
        s1 = 0x01 if enable else 0x00
        s2 = 0x26 if enable else 0x27
        cmd = bytes([0x08, 0xC6, 0x04, 0x08, 0x00, 0xF2, 0x0D, s1, 0xFE, s2])
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=150)

    def set_decode_success_tone(self, enable: bool) -> None:
        """Set decode success tone.

        :param bool enable: True - Enable decode success tone, False - Disable decode success tone.

        UiFlow2 Code Block:

            |set_decode_success_tone.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_decode_success_tone(enable)
        """
        s1 = 0x01 if enable else 0x00
        s2 = 0xEE if enable else 0xEF
        cmd = bytes([0x07, 0xC6, 0x04, 0x08, 0x00, 0x38, s1, 0xFE, s2])
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=150)

    def set_config_tone(self, enable: bool) -> None:
        """Set config tone.

        :param bool enable: True - Enable set config tone, False - Disable set config tone.

        UiFlow2 Code Block:

            |set_config_tone.png|

        MicroPython Code Block:

            .. code-block:: python

                base_qrcode.set_config_tone(enable)
        """
        s1 = 0x01 if enable else 0x00
        s2 = 0x25 if enable else 0x26
        cmd = bytes([0x08, 0xC6, 0x04, 0x08, 0x00, 0xF2, 0x0E, s1, 0xFE, s2])
        self.serial_handler.cmd(cmd, self.cmd_ack, timeout_ms=150)
