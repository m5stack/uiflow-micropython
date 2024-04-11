Weight I2C Unit
===============

.. include:: ../refs/unit.weight_i2c.ref

Weight I2C 单元是一个称重采集发射单元，它采用“STM32+HX711芯片”方案，通过I2C通信实现24位精度的重量测量，但不包括称重传感器。这个单元能够测量重量，并包含各种滤波器。

支持以下产品：


|WEIGHT I2C|              


Micropython Example::

	import os, sys, io
	import M5
	from M5 import *
	from hardware import *
	from unit import WEIGHT_I2CUnit
	import time

	i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
	weight_i2c0 = WEIGHT_I2CUnit(i2c0)
	print(weight_i2c_0.get_adc_raw)
  	print(weight_i2c_0.get_weight_float)
  	time.sleep_ms(100)


UIFLOW2 Example:

	|example.svg|


.. only:: builder_html


class WEIGHT_I2CUnit
--------------------

Constructors
---------------------------

.. class:: WEIGHT_I2CUnit(i2c0, 0x26)

	创建一个 WEIGHT_I2CUnit 对象。

	- ``I2C0`` is I2C Port.
	- ``0x26`` is default I2C address

 
	UIFLOW2:

		|init_i2c_address.svg|


Methods
----------------------

.. method:: WEIGHT_I2CUnit.get_adc_raw    


	获取原始的 ADC 值。

	UIFLOW2:

		|get_adc_raw.svg|

.. method:: WEIGHT_I2CUnit.get_weight_float


	获取以克为单位的重量浮点值。

	UIFLOW2:

		|get_weight_float.svg|

.. method:: WEIGHT_I2CUnit.get_weight_int


	获取以克为单位的重量整数值。 

	UIFLOW2:

		|get_weight_int.svg|

.. method:: WEIGHT_I2CUnit.get_weight_str


	获取以克为单位的重量字符串值。

	UIFLOW2:

		|get_weight_str.svg|

.. method:: WEIGHT_I2CUnit.set_reset_offset()

	重置偏移值(Tare).


	UIFLOW2:

		|set_reset_offset.svg|

.. method:: WEIGHT_I2CUnit.set_calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)

	
	校准称重传感器。

	- ``weight1_g``: Weight1 in grams.
	- ``weight1_adc``: Weight1 in ADC value.
	- ``weight2_g``: Weight2 in grams.
	- ``weight2_adc``: Weight2 in ADC value.

	calibration steps:

	1.Reset offset(Tare).
	2.Get the raw ADC value at no-load weight, this is the Raw ADC of zero weight in 0g.
	3.Put some weight on it, then get adc, this is the load weight adc value and the gram weight you put on it.


	UIFLOW2:

		|set_calibration.svg|

.. method:: WEIGHT_I2CUnit.set_lowpass_filter(Enable)

	启用或禁用低通滤波器。


	UIFLOW2:

		|set_lowpass_filter.svg|


.. method:: WEIGHT_I2CUnit.get_lowpass_filter

	返回低通滤波器的状态（启用或禁用）。


	UIFLOW2:

		|get_lowpass_filter.svg|

.. method:: WEIGHT_I2CUnit.set_average_filter_level(level)

	设置平均滤波器的级别。

	- ``level``: Level of the average filter (0 - 50). Larger value for smoother result but more latency

	UIFLOW2:

		|set_average_filter_level.svg|

.. method:: WEIGHT_I2CUnit.get_average_filter_level

	返回平均滤波器的级别。

	UIFLOW2:

		|get_average_filter_level.svg|

.. method:: WEIGHT_I2CUnit.set_ema_filter_alpha(alpha)

	设置EMA滤波器的alpha值。

	The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

	- ``alpha``: Alpha value for the EMA filter (0 - 99). Smaller value for smoother result but more latency

	UIFLOW2:

		|set_ema_filter_alpha.svg|

.. method:: WEIGHT_I2CUnit.get_ema_filter_alpha

	与平均滤波器相比，EMA（指数移动平均）滤波器对数据的变化更敏感。

	UIFLOW2:

		|get_ema_filter_alpha.svg|

.. method:: WEIGHT_I2CUnit.set_i2c_address(address)

	The i2c address can be changed by the user and this address should be between 0x01 and 0x7F.

	- ``address``: range of address(0x01 - 0x7F). 

	UIFLOW2:

		|set_i2c_address.svg|

.. method:: WEIGHT_I2CUnit.get_device_spec(info)

	获取此设备的固件版本详情和I2c地址。

	- ``info``: (0xFE, 0xFF)

	UIFLOW2:

		|get_device_spec.svg|