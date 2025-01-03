Atomic Echo Base
================

.. sku: A149

.. include:: ../refs/base.echo.ref

The following products are supported:

    |Atomic Echo Base|

Below is the detailed support for Speaker on the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+-------------------+
    |Controller       | Atomic Echo Base  |
    +=================+===================+
    | Atom Echo       | |O|               |
    +-----------------+-------------------+
    | Atom Lite       | |S|               |
    +-----------------+-------------------+
    | Atom Matrix     | |S|               |
    +-----------------+-------------------+
    | AtomS3          | |S|               |
    +-----------------+-------------------+
    | AtomS3 Lite     | |S|               |
    +-----------------+-------------------+
    | AtomS3R         | |S|               |
    +-----------------+-------------------+
    | AtomS3R-CAM     | |S|               |
    +-----------------+-------------------+
    | AtomS3R-Ext     | |S|               |
    +-----------------+-------------------+

.. |S| unicode:: U+2705
.. |O| unicode:: U+2B55


Micropython Example:

    .. literalinclude:: ../../../examples/base/echo/atoms3_echo_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |atoms3_echo_example.m5f2|


class ATOMEchoBase
------------------

Constructors
------------

.. class:: ATOMEchoBase(i2c, address: int = 0x18, i2s_port: int = 1, sample_rate: int = 44100, i2s_sck: int = -1, i2s_ws: int = -1, i2s_di: int = -1, i2s_do: int = -1)

    Create an ATOMEchoBase object.

    :param I2C i2c: I2C object
    :param int address: The I2C address of the ES8311. Default is 0x18.
    :param int i2s_port: The I2S port number. Default is 1.
    :param int sample_rate: The sample rate of the audio. Default is 44100.
    :param int i2s_sck: The I2S SCK pin. Default is -1.
    :param int i2s_ws: The I2S WS pin. Default is -1.
    :param int i2s_di: The I2S DI pin. Default is -1.
    :param int i2s_do: The I2S DO pin. Default is -1.

    UIFLOW2:

        |init.png|

    Micropython::

        from hardware import I2C
        from hardware import Pin
        from base import ATOMEchoBase

        # atom echo
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        echo = ATOMEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atom lite
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        echo = ATOMEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atom matrix
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        echo = ATOMEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atoms3 / atoms3 lite
        i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
        echo = ATOMEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

        # atoms3r / atoms3r-cam / atoms3-ext
        i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
        echo = ATOMEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

        echo.speaker.tone(2000, 1000)
        echo.speaker.playWavFile('res/audio/66.wav')


Attributes
----------

.. attribute:: ATOMEchoBase.speaker

    Objects of the Speaker class.

    See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details on how to use the ATOMEchoBase.speaker properties.

.. attribute:: ATOMEchoBase.microphone

    Objects of the Microphone class.

    See :ref:`hardware.Mic.Methods <hardware.Mic.Methods>` for more details on how to use the ATOMEchoBase.microphone properties.

    .. Note:: Microphone is not quite ready yet.
