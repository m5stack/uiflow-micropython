Miniscale Unit
==============

.. include:: ../refs/unit.miniscale.ref

``Miniscale`` 是为微型称重传感器设计的接口，其中包括一个HX711 22位ADC。此传感器能够测量重量，并且还包括其他功能，如LED控制和各种滤波器。

支持以下产品：


|MINISCALE|              



Micropython Example::

	import os, sys, io
	import M5
	from M5 import *
	import time
	from unit import MiniScaleUnit

	i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
	scale = MiniScaleUnit(i2c)
	scale.setLed(255, 0, 0)
	print(miniscale.weight)


UIFLOW2 Example:

	|example.svg|


.. only:: builder_html


class MiniScaleUnit
-------------------

Constructors
---------------------------

.. class:: MiniScaleUnit(i2c0)

	创建一个 MiniScaleUnit 对象。

	- ``I2C0`` is I2C Port.

 
	UIFLOW2:

		|init.svg|


Methods
----------------------

.. method:: MiniScaleUnit.adc


	获取原始的 ADC 读数。 

	UIFLOW2:

		|get_adc.svg|

.. method:: MiniScaleUnit.weight


	获取以克为单位的重量读数。  

	UIFLOW2:

		|get_weight.svg|


.. method:: MiniScaleUnit.button


	获取按钮状态。 

	UIFLOW2:

		|get_button.svg|

.. method:: MiniScaleUnit.setLed(r, g, b)

	设置 RGB LED 的颜色。

	- ``r``: Red value (0 - 255).
	- ``g``: Green value (0 - 255).
	- ``b``: Blue value (0 - 255).

	UIFLOW2:

		|setLed.svg|

.. method:: MiniScaleUnit.reset

	重置传感器。


	UIFLOW2:

		|reset.svg|

.. method:: MiniScaleUnit.calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)

	
	校准微型称重传感器。

	- ``weight1_g``: Weight1 in grams.
	- ``weight1_adc``: Weight1 in ADC value.
	- ``weight2_g``: Weight2 in grams.
	- ``weight2_adc``: Weight2 in ADC value.

	校准步骤:

	1. Reset sensor;
	2. Get adc, this is weight1_adc (should be zero). And weight1_g is also 0.
	3. Put some weight on it, then get adc, this is weight2_adc. And weight2_g is weight in gram you put on it.


	UIFLOW2:

		|calibration.svg|

.. method:: MiniScaleUnit.setLowPassFilter(enable)

	启用或禁用低通滤波器。


	UIFLOW2:

		|setLowPassFilter.svg|


.. method:: MiniScaleUnit.getLowPassFilter

	返回低通滤波器的状态（是否启用）。


	UIFLOW2:

		|getLowPassFilter.svg|

.. method:: MiniScaleUnit.setAverageFilterLevel(level)

	设置平均滤波器的级别。

	- ``level``: Level of the average filter (0 - 50). Larger value for smoother result but more latency

	UIFLOW2:

		|setAverageFilterLevel.svg|

.. method:: MiniScaleUnit.getAverageFilterLevel

	返回平均滤波器的级别。

	UIFLOW2:

		|getAverageFilterLevel.svg|

.. method:: MiniScaleUnit.setEMAFilterAlpha(alpha)

	设置EMA滤波器的alpha值。

	与平均滤波器相比，EMA（指数移动平均）滤波器对数据的变化更敏感。

	- ``alpha``: Alpha value for the EMA filter (0 - 99). Smaller value for smoother result but more latency

	UIFLOW2:

		|setEMAFilterAlpha.svg|

.. method:: MiniScaleUnit.getEMAFilterAlpha

	返回EMA滤波器的alpha值。

	UIFLOW2:

		|getEMAFilterAlpha.svg|

