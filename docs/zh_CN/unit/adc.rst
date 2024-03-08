ADC Unit
========

.. include:: ../refs/unit.adc.ref

支持以下产品：

    |ADC|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import *

    adc_0 = None

    def setup():
    global adc_0

    print(adc_0.get_voltage())
    time.sleep(1)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |adc_core_example.m5f2|


class ADCUnit
-------------

Constructors
------------

.. class:: ADCUnit(i2c0)

    创建一个ADCUnit对象.

    参数是:
        - ``I2C0`` 是I2C端口.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ADCUnit.get_value()

    获取adc读取的原始值。

    UIFLOW2:

        |get_value.svg|


.. method:: ADCUnit.get_voltage()

    获取电压值。

    UIFLOW2:

        |get_voltage.svg|


.. method:: ADCUnit.get_raw_value()

    读取原始数值。

    UIFLOW2:

        |get_raw_value.svg|


.. method:: ADCUnit.get_operating_mode()

    获取工作模式。（单次读取还是连续读取）

    UIFLOW2:

        |get_operating_mode.svg|


.. method:: ADCUnit.get_data_rate()

    获取数据的读取速率。

    UIFLOW2:

        |get_data_rate.svg|


.. method:: ADCUnit.get_gain()

    获取数据的增益倍数。

    UIFLOW2:

        |get_gain.svg|


.. method:: ADCUnit.operating_mode()

    设置工作模式（单次读取还是连续读取）

    UIFLOW2:

        |set_operating_mode.svg|


.. method:: ADCUnit.data_rate()

    设置获取数据的速率。

    UIFLOW2:

        |set_data_rate.svg|


.. method:: ADCUnit.gain()

    设置读取数据的增益倍数。

    UIFLOW2:

        |set_gain.svg|
