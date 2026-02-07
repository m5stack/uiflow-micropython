LoRa868 Cap
===========

.. sku: U201

.. include:: ../refs/cap.lora868.ref

Cap LoRa868 is a high-performance LoRa communication and GNSS global navigation expansion module designed for the Cardputer-Adv.

Support the following products:

    |LoRa868Cap|

UiFlow2 Example
---------------

Sender
^^^^^^

Open the |cardputer_adv_lora868_cap_sender_example.m5f2| project in UiFlow2.

Use the keyboard to enter the text you want to send and press ENTER to send it.

UiFlow2 Code Block:

    |cardputer_adv_lora868_cap_sender_example.png|

Example output:

    None

Receiver
^^^^^^^^

Open the |cardputer_adv_lora868_cap_receiver_example.m5f2| project in UiFlow2.

This example receives and displays data.

UiFlow2 Code Block:

    |cardputer_adv_lora868_cap_receiver_example.png|

Example output:

    None

GPS Usage
^^^^^^^^^

Open the |cardputer_adv_lora868_cap_gps_example.m5f2| project in UiFlow2.

This example demonstrates how to use the GPS functionality of the LoRa868 Cap.

UiFlow2 Code Block:

    |cardputer_adv_lora868_cap_gps_example.png|

Example output:

    None


MicroPython Example
-------------------

Sender
^^^^^^

Use the keyboard to enter the text you want to send and press ENTER to send it.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/cap/lora868/cardputer_adv_lora868_cap_sender_example.py
        :language: python
        :linenos:

Example output:

    None

Receiver
^^^^^^^^

This example receives and displays data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/cap/lora868/cardputer_adv_lora868_cap_receiver_example.py
        :language: python
        :linenos:

Example output:

    None

GPS Usage
^^^^^^^^^

This example demonstrates how to use the GPS functionality of the LoRa868 Cap.

MicroPython Code Block:

   .. literalinclude:: ../../../examples/cap/lora868/cardputer_adv_lora868_cap_gps_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

class LoRa868Cap
^^^^^^^^^^^^^^^^

.. autoclass:: cap.lora868.LoRa868Cap
    :members:
    :member-order: bysource

class GPSCap
^^^^^^^^^^^^

.. autoclass:: cap.lora868.GPSCap
    :members:
    :member-order: bysource
