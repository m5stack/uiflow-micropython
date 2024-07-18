QRCode Unit
===========

.. include:: ../refs/unit.qrcode.ref

The ``QRCode Unit`` is an integrated one-dimensional/two-dimensional code scanning unit that combines a CMOS QR code capture engine with a resolution of 640x480 and a bus conversion MCU (STM32F030). It features a device-side toggle switch that allows for switching between I2C and UART communication interfaces.

Support the following products:

    |QRCodeUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import QRCodeUnit
    from hardware import *

    def qrcode_0_event(qrdata):
        print(qrdata)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    qrcode_0 = QRCodeUnit(0, i2c0, 0x21)
    qrcode_0.set_event_cb(qrcode_0_event)
    qrcode_0.set_trigger_mode(1)

    while True:
        qrcode_0.event_poll_loop()
        time.sleep_ms(25)

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |unit-qrcode-demo.m5f2|


class QRCodeUnit
----------------

Constructors
------------

.. class:: QRCodeUnit(mode, i2c, address, id, port)

    Create a QRCodeUnit object

    :param mode: 0: I2C, 1: UART mode.
    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x21.
    :param id: 1: UART1, 2: UART2.
    :param port: uart pin tuple, which contains: ``(tx_pin, rx_pin)``
    
    UIFLOW2:

        |init.png|


Methods
-------

.. method:: QRCodeUnit.get_qrcode_data_length()

    Scan the QR code and get the available data length. 

    - Return: ``int``:  available data length is int format

    UIFLOW2:

        |get_qrcode_data_length.png|


.. method:: QRCodeUnit.get_qrcode_data()

    Scan the QR code and get the data in the string. 

    - Return: ``string``:  scanned data output is string format

    UIFLOW2:

        |get_qrcode_data.png|


.. method:: QRCodeUnit.set_trigger_mode(mode)

    Set the trigger mode to Auto or Manual(Key). 

    The parameters is:
        - ``mode``:  auto: 0 or manual: 1

    UIFLOW2:

        |set_trigger_mode.png|


.. method:: QRCodeUnit.set_manual_scan(ctrl)

    Set the manual(use the key button) scanning control ON or OFF. 

    The parameters is:
        - ``ctrl``:  off: 0 or on: 1

    .. NOTE:: This command is only effective in manual trigger mode

    UIFLOW2:

        |set_manual_scan.png|


.. method:: QRCodeUnit.set_event_cb(qrcode_0_event)

    Set the callback event and callback function. 

    The callback function:
        - ``qrcode_0_event``

    An handler showing a message has been received::

        def qrcode_0_event(_qrdata):
            print(_qrdata)
            pass

    UIFLOW2:

        |callback.png|


.. method:: QRCodeUnit.event_poll_loop()

    The calling event poll block must be used inside a loop. 
    
    UIFLOW2:

        |event_poll_loop.png|


.. method:: QRCodeUnit.get_qrcode_data_status()

    Reading data scanned QR code after get the data status 

    - Return: ``int``:   0: not ready, 1: data available, 2: read again

    UIFLOW2:

        |get_qrcode_data_status.png|


.. method:: QRCodeUnit.get_trigger_mode()

    Get the auto or manual trigger mode status. 
    
    - Return: ``int``:   0: auto, 1: manual
    
    UIFLOW2:

        |get_trigger_mode.png|


.. method:: QRCodeUnit.get_trigger_button_status()

    Get the trigger button status 
    
    - Return: ``int``: 1: press, 0: not pressed
    
    UIFLOW2:

        |get_trigger_button_status.png|

    
.. method:: QRCodeUnit.get_device_info(info)

    Get the firmware version details and I2C address of this device.

    The parameters is:
	    - ``info``: 0xFE: firmware version, 0xFF: I2C address

    UIFLOW2:

        |get_device_info.png|


.. method:: QRCodeUnit.clear_qrcode_data_status()

    Clear the data status after reading the QR code scanned data.

    UIFLOW2:

        |clear_qrcode_data_status.png|
        

.. method:: QRCodeUnit.set_device_i2c_address(addr)

    The i2c address can be changed by the user and this address should be between 0x01 and 0x7F.

	- ``addr``: range of address(0x01 - 0x7F). 

    UIFLOW2:

        |set_device_i2c_address.png|

