RCA Module
==========

.. include:: ../refs/module.rca.ref

模块RCA是一个音视频复合信号扩展模块，使用常见的S端子RCA连接器，分为两个（左右声道）音频和一个视频输出。音频部分采用I2S功放芯片PCM5102APWR方案，能够实现32位立体声音频信号输出；在视频方面，应用了主控ESP32的DAC模拟视频信号功能，能够生成分辨率不超过864 x 576（PAL，PAL_M）的模拟视频信号；该模块包含一个直流插座和一个9-24V转5V的DCDC电路，以供应整机电力。该产品适用于驱动S端子接口的音视频设备。

支持以下产品：

|RCAModule|

Micropython 示例::

	import M5
	M5.addDisplay({"module_rca":{"enabled":True}}) # 添加ModuleDisplay模块
	M5.getDisplayCount() # 获取显示数量
	M5.setPrimaryDisplay(1) # 设置主显示
	M5.Display.clear(0xffffff) # 清屏

UIFLOW2 示例:

	|example.svg|

.. only:: builder_html
