.. currentmodule:: Widgets

class Label -- display text
===========================

Label 是用于显示文本的基本对象类型。

.. include:: ../refs/widgets.label.ref

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 38, 47, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

    label0.setText('Label')
    label0.setFont(Widgets.FONTS.DejaVu12)

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    :download:`example.m5f2 <../../_static/widgets/label/example.m5f2>`

Constructors
------------

.. class:: Widgets.Label(text: str, x: int, y: int, text_sz: float, text_c: int=0xFFFFFF, bg_c: int=0x000000, font=None, parent=None)

    创建一个 Label 对象。它接受以下参数：

        - ``text`` 是要显示的文本。
        - ``x`` 是显示的起始x轴坐标。
        - ``y`` 是显示的起始y轴坐标。
        - ``text_sz`` 是显示文本的字体大小，一般使用1.0。
        - ``text_c`` 是显示文本的字体颜色，默认是白色。
        - ``bg_c`` 是显示文本的背景颜色，默认是黑色。
        - ``font`` 是显示文本使用的字体集，内置的字体，请参考 ``Widgets.FONTS``。
        - ``parent`` 是 Label 对象的输出目标，默认是输出到LCD，也可以是输出到 Canvas 对象。

Methods
-------

.. method:: Label.setColor(text_c:int, bg_c: int=-1)

    设置 Label 对象的文本字体颜色。接受以下参数：

        - ``text_c`` 是显示文本的字体颜色。
        - ``bg_c`` 是显示文本的背景颜色，默认是黑色。

    UIFLOW2:

        |setColor.svg|


.. method:: Label.setCursor(x: int, y: int)

    设置 Label 对象的起始坐标。接受以下参数：

        - ``x`` 是显示的起始x轴坐标。
        - ``y`` 是显示的起始y轴坐标。

    UIFLOW2:

        |setCursor.svg|

.. method:: Label.setFont(font)

    设置 Label 对象的字体集。``font`` 是显示文本使用的字体集，内置的字体，请参考 ``Widgets.FONTS``。

    UIFLOW2:

        |setFont.svg|

.. method:: Label.setSize(text_sz: float)

    设置 Label 对象的文本字体大小，``text_sz`` 是显示文本的字体大小。

    UIFLOW2:

        |setSize.svg|

.. method:: Label.setText(text: str)

    设置 Label 对象的文本内容。

    UIFLOW2:

        |setText.svg|

.. method:: Label.setVisible(visible: bool)

    设置 Label 对象的可见属性，``visible`` 是 True时，Label 对象内容将会可见，否则不可见。

    UIFLOW2:

        |setVisible.svg|
