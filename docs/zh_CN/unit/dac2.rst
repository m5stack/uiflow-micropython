DAC2 Unit
=========

.. include:: ../refs/unit.dac2.ref

`Dac2` 类控制GP8413 15位数字到模拟转换器（DAC），能够将数字信号转换为两个通道的模拟电压输出，范围可以为0-5V或0-10V。

支持以下产品：


|DAC2Unit|      

|DAC2Hat|    



Micropython示例::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import DAC2Unit

    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dac2_0 = DAC2Unit(i2c0, 0x59)
    dac2_0.setDACOutputVoltageRange(dac2_0.RANGE_10V)
    dac2_0.setVoltage(7.5, channel=dac2_0.CHANNEL_BOTH)


UIFLOW2示例:

    |example.svg|


.. only:: builder_html

DAC2Unit类
--------------

构造函数
---------------------------

.. class:: DAC2Unit(i2c0, addr)

    创建一个DAC2Unit对象。

    - ``I2C0`` 是I2C端口。
    - ``addr`` DAC的I2C地址（默认是`0x59`）。
 
    UIFLOW2:

        |init.svg|


方法
----------------------

.. method:: MiniScaleUnit.setDACOutputVoltageRange(_range)

    设置DAC的输出电压范围。

    - ``_range`` DAC输出电压范围，可以是`DAC2Unit.RANGE_5V`或`DAC2Unit.RANGE_10V`。

    UIFLOW2:

        |setDACOutputVoltageRange.svg|

.. method:: MiniScaleUnit.setVoltage(voltage, channel=Dac2.CHANNEL_BOTH)

    设置DAC的输出电压。

    - ``voltage`` 期望的输出电压，从0.0到范围最大值（5V或10V）。
    - ``channel`` 要设置的DAC通道。选项是`Dac2.CHANNEL_0`、`Dac2.CHANNEL_1`或`Dac2.CHANNEL_BOTH`。

    UIFLOW2:

        |setVoltage.svg|


.. method:: MiniScaleUnit.setVoltageBoth(voltage0, voltage1)

    为两个通道设置输出电压。

    - ``voltage0`` 期望的输出电压，从0.0到范围最大值（5V或10V）。
    - ``voltage1`` 期望的输出电压，从0.0到范围最大值（5V或10V）。

    UIFLOW2:

        |setVoltageBoth.svg|
