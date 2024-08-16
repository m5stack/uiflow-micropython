:mod:`bleuart` --- UART/Serial Port Emulation over BLE
======================================================

The Nordic UART Service (NUS) Application is an example that emulates a serial port over BLE.

The application includes one service: the Nordic UART Service. The 128-bit vendor-specific UUID of the Nordic UART Service is 6E400001-B5A3-F393-E0A9-E50E24DCCA9E (16-bit offset: 0x0001).

This service exposes two characteristics: one for transmitting and one for receiving (as seen from the peer).


Classes
-------

.. toctree::
    :maxdepth: 1

    bleuart.server.rst
    bleuart.client.rst
