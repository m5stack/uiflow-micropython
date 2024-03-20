Display Module
==============

.. include:: ../refs/module.display.ref

显示模块13.2是一个扩展模块，用于高清音视频，采用高云GW1NR系列FPGA芯片输出显示信号，并使用LT8618S芯片作为信号输出调节，能够实现24位色深的显示信号和多达8通道的音频信号输出，分辨率高达1080P，其中FPGA内部实现了I2S音频生成功能。该模块包含直流电源输入插座及相应的直流-直流电路，能够实现整机的供电。该产品适用于各种可编程高清音视频输出及其他场合。


支持以下产品：

|DisplayModule|

Micropython 示例::

	import M5
    display = M5.addDisplay({"module_display":{"enabled":True}}) # 添加Display模块
	# or
    display = M5.addDisplay({
        "module_display":{
            "enabled":True,
            "width": 1280,
            "height": 720,
            "refresh_rate": 60,
            "output_width": 0, # 0 default
            "output_height": 0,
            "scale_w": 0, # intger
            "scale_h": 0,
            "pixel_clock": 74250000,
        }
    })
	display.clear(0xffffff) # 清屏

UIFLOW2 示例:

	|example.svg|

.. only:: builder_html
