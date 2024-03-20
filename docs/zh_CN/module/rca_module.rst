RCA Module
==========

.. include:: ../refs/module.rca.ref

模块RCA是一个音视频复合信号扩展模块，使用常见的S端子RCA连接器，分为两个（左右声道）音频和一个视频输出。音频部分采用I2S功放芯片PCM5102APWR方案，能够实现32位立体声音频信号输出；在视频方面，应用了主控ESP32的DAC模拟视频信号功能，能够生成分辨率不超过864 x 576（PAL，PAL_M）的模拟视频信号；该模块包含一个直流插座和一个9-24V转5V的DCDC电路，以供应整机电力。该产品适用于驱动S端子接口的音视频设备。

支持以下产品：

|RCAModule|

Micropython 示例::

	import M5
	display = M5.addDisplay({"module_rca":{"enabled":True}}) # 添加RCA模块
	# or
	display = M5.addDisplay({
		"module_rca":{
			"enabled":True,
			"width": 216,
			"height": 144,
			"output_width": 0,
			"output_height": 0,
			"signal_type": 0, # NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4
			"use_psram": 0,
			"pin_dac": 26,
			"output_level": 0,
		}
	})
	display.clear(0xffffff) # 清屏

UIFLOW2 示例:

	|example.svg|

.. only:: builder_html
