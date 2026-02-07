Atom DTU LoRaWAN-Series Base
============================

.. sku: K061/K062/K063

.. include:: ../refs/base.dtu_lorawan.ref

This is the driver library for the Atom DTU LoRaWAN-Series Base to accept and send data from the LoRaWAN module.

Support the following products:

    ===================== ===================== =====================
    |Atom DTU LoRaWAN470| |Atom DTU LoRaWAN868| |Atom DTU LoRaWAN915| 
    ===================== ===================== =====================

UiFlow2 Example
---------------

LoRaWAN communication
^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3r_dtu_lorawan_example.m5f2| project in UiFlow2.

This example shows how to receive and send data using the Atom DTU LoRaWAN Base.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

LoRaWAN communication
^^^^^^^^^^^^^^^^^^^^^^

This example shows how to receive and send data using the Atom DTU LoRaWAN Base.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_lorawan/atoms3r_dtu_lorawan_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

AtomDTULoRaWANBase
^^^^^^^^^^^^^^^^^^

.. autoclass:: base.dtu_lorawan.AtomDTULoRaWANBase
    :members:

.. autoclass:: driver.asr650x.LoRaWAN_470
    :members:
    :exclude-members: get_ABP_config, get_OTAA_config, config_OTAA, config_ABP

.. autoclass:: driver.asr650x.LoRaWAN_Asr650x
    :members:
    :member-order: bysource
    :exclude-members: enable_adaptive_datarate, get_APPSKEY, get_AppKey, get_AppEui, reset_module_to_default, get_device_address, get_DevAddr, set_device_address, set_DevAddr, get_device_eui, get_DevEui, set_device_eui, set_DevEui, get_product_serial_number, set_AppEui, set_AppKey, set_APPSKEY, get_NWKSKEY, set_NWKSKEY, get_join_mode, get_frequency_band_mask, get_uplink_downlink_mode, get_work_mode, get_class_mode, set_work_mode, get_status, receive_data, set_uplink_confirm_mode, set_datarate, set_report_mode, set_tx_power, enable_adaptive_datarate, set_rx1_delay_time