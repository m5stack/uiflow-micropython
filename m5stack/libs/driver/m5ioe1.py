# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

# I2C address
I2C_ADDR = 0x6F

# Register addresses
REG_GPIO_MODE_L = 0x03
REG_GPIO_MODE_H = 0x04
REG_GPIO_OUT_L = 0x05
REG_GPIO_OUT_H = 0x06
REG_GPIO_IN_L = 0x07
REG_GPIO_IN_H = 0x08
REG_GPIO_PU_L = 0x09
REG_GPIO_PU_H = 0x0A
REG_GPIO_PD_L = 0x0B
REG_GPIO_PD_H = 0x0C
REG_GPIO_DRV_L = 0x13
REG_GPIO_DRV_H = 0x14

# PWM registers
REG_PWM1_DUTY_L = 0x1B
REG_PWM1_DUTY_H = 0x1C
REG_PWM2_DUTY_L = 0x1D
REG_PWM2_DUTY_H = 0x1E
REG_PWM3_DUTY_L = 0x1F
REG_PWM3_DUTY_H = 0x20
REG_PWM4_DUTY_L = 0x21
REG_PWM4_DUTY_H = 0x22
REG_PWM_FREQ_L = 0x25
REG_PWM_FREQ_H = 0x26

# LED registers
REG_LED_CFG = 0x24
REG_LED_RAM_START = 0x30

# Constants
IN = 0
OUT = 1
PULL_UP = 2
PULL_DOWN = 3

LOW = 0
HIGH = 1

LED_NUM_MASK = 0x3F
LED_REFRESH = 1 << 6

# 引脚编号说明：
# - 外部 API：使用 1-14（对应 G1-G14）
# - 内部硬件：P1=0, P2=1, ..., P8=7, P9=8, ..., P14=13
# 注意：IO 引脚最多支持 14 个（G1-G14）
PIN_COUNT = 14  # IO 引脚限制为 14
PWM_CHANNEL_COUNT = 4


class M5ioe1:
    """M5IOE1 IO expander driver class (low-level implementation)"""

    def __init__(self, i2c, addr=I2C_ADDR):
        self.i2c = i2c
        self.addr = addr

    def _read_reg8(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _write_reg8(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value & 0xFF]))
        return True

    def _read_reg16(self, reg_low):
        data = self.i2c.readfrom_mem(self.addr, reg_low, 2)
        return (data[1] << 8) | data[0]

    def _write_reg16(self, reg_low, value):
        self.i2c.writeto_mem(self.addr, reg_low, bytes([value & 0xFF, (value >> 8) & 0xFF]))
        return True

    def _write_bytes(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, bytes(data))
        return True

    def _get_pin_registers(self, pin):
        # M5IOE1 GPIO L/H registers are adjacent and are treated as one 14-bit bitmap.
        # External API keeps G1-G14 numbering, so convert to hardware bit 0-13 here.
        hw_pin = pin - 1
        return (
            REG_GPIO_MODE_L,
            REG_GPIO_OUT_L,
            REG_GPIO_IN_L,
            REG_GPIO_PU_L,
            REG_GPIO_PD_L,
            REG_GPIO_DRV_L,
            hw_pin,
        )

    def _pin_mode(self, pin, mode, pull=None):
        if pin < 1 or pin > PIN_COUNT:
            return False

        mode_reg, out_reg, in_reg, pu_reg, pd_reg, drv_reg, bit_pos = self._get_pin_registers(pin)

        mode_val = self._read_reg16(mode_reg)
        pu_val = self._read_reg16(pu_reg)
        pd_val = self._read_reg16(pd_reg)
        drv_val = self._read_reg16(drv_reg)

        if mode_val is None:
            return False

        mask = ~(1 << bit_pos)
        mode_val &= mask
        pu_val &= mask
        pd_val &= mask
        drv_val &= mask

        if mode == OUT:
            mode_val |= 1 << bit_pos
            if pull == PULL_UP:
                pu_val |= 1 << bit_pos
            elif pull == PULL_DOWN:
                pd_val |= 1 << bit_pos
        elif mode == IN:
            mode_val &= ~(1 << bit_pos)
            if pull == PULL_UP:
                pu_val |= 1 << bit_pos
            elif pull == PULL_DOWN:
                pd_val |= 1 << bit_pos
        else:
            return False

        self._write_reg16(pu_reg, pu_val)
        self._write_reg16(pd_reg, pd_val)
        self._write_reg16(drv_reg, drv_val)
        self._write_reg16(mode_reg, mode_val)

        return True

    def _pin_write(self, pin, value):
        if pin < 1 or pin > PIN_COUNT:
            return False

        mode_reg, out_reg, in_reg, pu_reg, pd_reg, drv_reg, bit_pos = self._get_pin_registers(pin)

        out_val = self._read_reg16(out_reg)
        if out_val is None:
            return False

        if value:
            out_val |= 1 << bit_pos
        else:
            out_val &= ~(1 << bit_pos)

        return self._write_reg16(out_reg, out_val)

    def _pin_read(self, pin):
        if pin < 1 or pin > PIN_COUNT:
            return None

        mode_reg, out_reg, in_reg, pu_reg, pd_reg, drv_reg, bit_pos = self._get_pin_registers(pin)

        in_val = self._read_reg16(in_reg)
        if in_val is None:
            return None

        return 1 if (in_val & (1 << bit_pos)) else 0

    def _pwm_write(self, channel, duty):
        if channel < 0 or channel >= PWM_CHANNEL_COUNT:
            return False

        duty = max(0, min(1000, duty))
        duty12 = duty * 0x0FFF // 1000
        pwm_data = duty12 & 0x0FFF
        if duty12:
            pwm_data |= 1 << 15  # EN bit in PWMx_DUTY_H
        pwm_reg_l = REG_PWM1_DUTY_L + (channel * 2)
        return self._write_reg16(pwm_reg_l, pwm_data)

    def _pwm_frequency(self, freq):
        freq = max(1, min(65535, freq))
        return self._write_reg16(REG_PWM_FREQ_L, freq)

    def _set_leds(self, colors, count=None, auto_refresh=True):
        if count is None:
            count = len(colors)

        if count == 0 or count > 32:
            return False

        cfg = count & LED_NUM_MASK
        if not self._write_reg8(REG_LED_CFG, cfg):
            return False

        for i in range(count):
            if i >= len(colors):
                r, g, b = (0, 0, 0)
            else:
                r, g, b = colors[i]

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            r5 = (r >> 3) & 0x1F
            g6 = (g >> 2) & 0x3F
            b5 = (b >> 3) & 0x1F
            rgb565 = (r5 << 11) | (g6 << 5) | b5

            reg_addr = REG_LED_RAM_START + (i * 2)
            data_low = rgb565 & 0xFF
            data_high = (rgb565 >> 8) & 0xFF

            if not self._write_bytes(reg_addr, (data_low, data_high)):
                return False

        if auto_refresh:
            cfg = self._read_reg8(REG_LED_CFG)
            if cfg is not None:
                cfg |= LED_REFRESH
                return self._write_reg8(REG_LED_CFG, cfg)

        return True


class Pin:
    """
    M5IOE1 pin class

    使用示例：
        from driver.m5ioe1 import M5ioe1, Pin
        from machine import I2C, Pin as MPin

        i2c = I2C(0, scl=MPin(11), sda=MPin(12))
        ioe1 = M5ioe1(i2c)

        # 创建引脚对象（引脚编号 1-14，对应 G1-G14）
        pin1 = Pin(ioe1, 1, Pin.OUT)  # G1 输出
        pin1.on()                     # 设置为 HIGH
        pin1.off()                    # 设置为 LOW
        pin1.value(1)                 # 设置为 HIGH
        value = pin1.value()          # 读取值
    """

    IN = IN
    OUT = OUT
    PULL_UP = PULL_UP
    PULL_DOWN = PULL_DOWN
    LOW = LOW
    HIGH = HIGH

    def __init__(self, ioe1, pin, mode=None, pull=None):
        """初始化引脚

        :param ioe1: M5ioe1 实例
        :type ioe1: M5ioe1
        :param pin: 引脚编号 (1-14，对应 G1-G14)
        :type pin: int
        :param mode: 模式 (Pin.IN, Pin.OUT)
        :type mode: int or None
        :param pull: 上拉/下拉 (Pin.PULL_UP, Pin.PULL_DOWN, None)
        :type pull: int or None
        """
        self.ioe1 = ioe1
        self.pin = pin
        self.mode = mode
        self.pull = pull
        if mode is not None:
            self.ioe1._pin_mode(self.pin, mode, pull)

    def init(self, mode=None, pull=None):
        """初始化引脚（重新配置）

        :param mode: 模式
        :type mode: int or None
        :param pull: 上拉/下拉
        :type pull: int or None
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        if mode is not None:
            self.mode = mode
        if pull is not None:
            self.pull = pull
        return self.ioe1._pin_mode(self.pin, self.mode, self.pull)

    def value(self, val=None):
        """读取或设置引脚值（参考 machine.Pin.value）

        :param val: 如果为 None，读取引脚值；否则设置引脚值 (0/1)
        :type val: int or None
        :return: 读取时返回 0 或 1，设置时返回 None
        :rtype: int or None
        """
        if val is None:
            return self.ioe1._pin_read(self.pin)
        else:
            self.ioe1._pin_write(self.pin, 1 if val else 0)
            return None

    def on(self):
        """设置引脚为 HIGH"""
        self.ioe1._pin_write(self.pin, 1)

    def off(self):
        """设置引脚为 LOW"""
        self.ioe1._pin_write(self.pin, 0)

    def __call__(self, val=None):
        """支持函数调用方式：pin() 读取，pin(1) 设置

        :param val: 如果为 None，读取引脚值；否则设置引脚值 (0/1)
        :type val: int or None
        :return: 读取时返回 0 或 1，设置时返回 None
        :rtype: int or None
        """
        return self.value(val)


class PWM:
    """
    M5IOE1 PWM 类（参考 machine.PWM 风格）

    使用示例：
        from driver.m5ioe1 import M5ioe1, PWM

        ioe1 = M5ioe1(i2c)
        pwm = PWM(ioe1, 0)  # 通道 0
        pwm.freq(1000)      # 设置频率 1kHz
        pwm.duty(500)       # 设置占空比 50%
    """

    def __init__(self, ioe1, channel, freq=1000, duty=0):
        """初始化 PWM

        :param ioe1: M5ioe1 实例
        :type ioe1: M5ioe1
        :param channel: PWM 通道 (0-3)
        :type channel: int
        :param freq: 频率 (Hz)
        :type freq: int
        :param duty: 占空比 (0-1000)
        :type duty: int
        """
        self.ioe1 = ioe1
        self.channel = channel
        self._freq = freq
        self._duty = duty

        if freq:
            self.freq(freq)
        if duty:
            self.duty(duty)

    def freq(self, f=None):
        """获取或设置频率

        :param f: 频率值 (Hz)，如果为 None 则返回当前频率
        :type f: int or None
        :return: 频率值
        :rtype: int or None
        """
        if f is None:
            return self._freq
        else:
            self._freq = f
            self.ioe1._pwm_frequency(f)
            return None

    def duty(self, d=None):
        """获取或设置占空比

        :param d: 占空比 (0-1000)，如果为 None 则返回当前占空比
        :type d: int or None
        :return: 占空比值
        :rtype: int or None
        """
        if d is None:
            return self._duty
        else:
            self._duty = max(0, min(1000, d))
            self.ioe1._pwm_write(self.channel, self._duty)
            return None

    def deinit(self):
        """取消初始化（停止 PWM）"""
        self.duty(0)


class RGB:
    """
    M5IOE1 RGB LED 控制类

    使用示例：
        from driver.m5ioe1 import M5ioe1, RGB, Pin

        ioe1 = M5ioe1(i2c)
        rgb = RGB(ioe1, io=14, n=12)   # 12 个 LED，使用 G14 引脚
        rgb.set_color(0, 0xFF0000)     # 设置第 0 个 LED 为红色
        rgb.fill_color(0x00FF00)       # 填充所有 LED 为绿色
    """

    def __init__(self, ioe1, io, n=12):
        """初始化 RGB LED 控制器

        :param ioe1: M5ioe1 实例
        :type ioe1: M5ioe1
        :param io: RGB LED 控制引脚号 (1-14，对应 G1-G14)
        :type io: int
        :param n: LED 数量（默认 12，最多 32）
        :type n: int
        :raises ValueError: 如果 LED 数量超过 32 或引脚号无效
        """
        if n < 1 or n > 32:
            raise ValueError(f"LED count must be between 1 and 32, got {n}")
        if io < 1 or io > PIN_COUNT:
            raise ValueError(f"Pin number must be between 1 and {PIN_COUNT}, got {io}")

        self.ioe1 = ioe1
        self.io = io
        self.n = n
        self._colors = [(0, 0, 0)] * n  # 内部颜色缓存
        self._pin = Pin(ioe1, io, Pin.OUT)

        # 初始化 LED 配置（设置 LED 数量）
        cfg = n & LED_NUM_MASK
        self.ioe1._write_reg8(REG_LED_CFG, cfg)

    def set_color(self, i, color, refresh=True):
        """设置单个 LED 的颜色

        :param i: LED 索引 (0 到 n-1)
        :type i: int
        :param color: 颜色 RGB888 格式 (int)，例如 0xFF0000 表示红色
        :type color: int
        :param refresh: 是否立即刷新显示
        :type refresh: bool
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        if i < 0 or i >= self.n:
            return False

        # 从 RGB888 格式提取 r, g, b
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF

        # 更新内部缓存
        self._colors[i] = (r, g, b)

        # 转换为 RGB565
        r5 = (r >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        b5 = (b >> 3) & 0x1F
        rgb565 = (r5 << 11) | (g6 << 5) | b5

        # 写入到芯片寄存器
        reg_addr = REG_LED_RAM_START + (i * 2)
        data_low = rgb565 & 0xFF
        data_high = (rgb565 >> 8) & 0xFF

        if not self.ioe1._write_bytes(reg_addr, (data_low, data_high)):
            return False

        # 如果需要刷新，触发显示更新
        if refresh:
            return self.refresh()

        return True

    def fill_color(self, color, refresh=True):
        """填充所有 LED 为同一颜色

        :param color: 颜色 RGB888 格式 (int)，例如 0xFF0000 表示红色
        :type color: int
        :param refresh: 是否立即刷新显示
        :type refresh: bool
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        # 从 RGB888 格式提取 r, g, b
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF

        # 更新所有 LED 的颜色缓存
        for i in range(self.n):
            self._colors[i] = (r, g, b)

        # 批量写入
        if refresh:
            return self.ioe1._set_leds(self._colors, self.n, True)
        else:
            # 逐个写入但不刷新
            for i in range(self.n):
                if not self.set_color(i, color, refresh=False):
                    return False
            return True

    def refresh(self):
        """手动刷新 LED 显示

        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        cfg = self.ioe1._read_reg8(REG_LED_CFG)
        if cfg is not None:
            cfg |= LED_REFRESH
            return self.ioe1._write_reg8(REG_LED_CFG, cfg)
        return False

    def clear(self, refresh=True):
        """清除所有 LED（设置为黑色）

        :param refresh: 是否立即刷新显示
        :type refresh: bool
        :return: 成功返回 True，失败返回 False
        :rtype: bool
        """
        return self.fill_color(0x000000, refresh)
