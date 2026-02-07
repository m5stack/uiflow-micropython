Atom DTU LoRaWAN-Series(RAK3172) Base
======================================

.. sku:U184-CN470,U184-AS923,U184-EU868,U184-US915

.. include:: ../refs/base.lorawan_rui3.ref

SKU: A152-CN470, A152-US915, A152-EU868

The Atom DTU LoRaWAN-Series is a LoRaWAN programmable data transfer unit (DTU) based on the STM32WLE5 chip. The module supports long-range communication, low-power operation, and high sensitivity characteristics, making it suitable for IoT communication needs in a variety of complex environments.

- **Frequency band support**: CN470 (470MHz), EU868 (868MHz), US915 (915MHz)
- **Communication protocol**:
  
  - Supports LoRaWAN Class A, Class B, Class C modes
  - Supports LoRa Point-to-Point (P2P) communication mode.

- **Communication Interface**:
  
  - UART interface: Used to send AT commands to control LoRaWAN network access, data sending/receiving, P2P mode communication, etc.
  - RS485 interface: supports wired communication of industrial equipment with high reliability.

- **Internet access method**:
  
  - OTAA (Over-The-Air Activation)
  - ABP (Activation By Personalization)

Support the following products:

================== ================== ==================
|LoRaWAN-CN470|       |LoRaWAN-EU868| |LoRaWAN-US915|
================== ================== ==================


Micropython LoRaWAN-EU868 LoRaWAN OTAA Mode Example:

    .. literalinclude:: ../../../examples/base/dtu_lorawan_rui3/base_lorawan868_otaa_atom_lite_example.py
        :language: python
        :linenos:

Micropython LoRaWAN-EU868 P2P Mode TX Example:

    .. literalinclude:: ../../../examples/base/dtu_lorawan_rui3/base_lorawan868_p2p_tx_atom_lite_example.py
        :language: python
        :linenos:

Micropython LoRaWAN-EU868 P2P Mode RX Example:

    .. literalinclude:: ../../../examples/base/dtu_lorawan_rui3/base_lorawan868_p2p_tx_atom_lite_example.py
        :language: python
        :linenos:

UIFLOW2 LoRaWAN-EU868 LoRaWAN OTAA Mode Example:

    |lorawan_otaa_cores3_example.png|

    |base_lorawan868_otaa_atom_lite_example.m5f2|

UIFLOW2 LoRaWAN-EU868 P2P Mode TX Example:

    |lorawan_p2p_cores3_example.png|

    |base_lorawan868_p2p_tx_atom_lite_example.m5f2|

UIFLOW2 LoRaWAN-EU868 P2P Mode RX Example:

    |lorawan_p2p_rec_cores3_example.png|

    |base_lorawan868_p2p_rx_atom_lite_example.m5f2|

**API**
-------

AtomDTULoRaWANRUI3Base
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: base.dtu_lorawan_rui3.AtomDTULoRaWANRUI3Base
    :members:

.. autoclass:: driver.rui3.RUI3
    :members:
    :member-order: bysource
