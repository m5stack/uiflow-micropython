# -*- encoding: utf-8 -*-
"""
@File    :   _dac2.py
@Time    :   2024/4/24
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin


class SSRUnit:
    """! UNIT SSR Solid-state relays are different from traditional electromagnetic relays

    @en UNIT SSR Solid-state relays are different from traditional electromagnetic relays in that their switching life are much longer than that of electromagnetic relays. With integrated MOC3043M optocoupler isolation and zero-crossing detection,It supports input 3.3-5V DC control signal, and control output single-phase 220-250V AC power.
    @cn UNIT SSR固态继电器与传统电磁继电器不同，其开关寿命远远大于电磁继电器。集成MOC3043M光耦隔离和零点检测，支持输入3.3-5V DC控制信号，控制输出单相220-250V AC电源。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/ssr
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/ssr/ssr_01.webp
    @category unit

    @example
        from unit import SSRUnit
        ssr = SSRUnit((33, 32))  # for core2
        ssr.on()
        ssr.off()
        ssr.set_state(1)
        ssr.set_state(0)

    """

    def __init__(self, port: tuple):
        """! Initialize the SSR.

        @param port The port to which the Fader is connected. port[1]: control pin
        """

        self.ssr = Pin(port[1])
        self.ssr.init(mode=Pin.OUT, pull=Pin.PULL_DOWN, value=0)

    def on(self):
        """! Turn on the SSR.

        @en %1 Turn on the SSR.
        @cn %1 打开SSR。

        """

        self.ssr.value(1)

    def off(self):
        """! Turn off the SSR.

        @en %1 Turn off the SSR.
        @cn %1 关闭SSR。

        """

        self.ssr.value(0)

    def set_state(self, state: int):
        """! Set the state of the SSR.

        @en %1 Set the state of the SSR to %2.
        @cn %1 设置SSR的状态为%2。

        @param state [field_switch] The state of the SSR.

        """

        self.ssr.value(state)
