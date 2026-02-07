
ASR Unit
=========
.. sku:U194
.. include:: ../refs/unit.asr.ref

**Unit ASR** is an **AI** offline speech recognition unit, featuring the built-in AI smart offline speech module **CI-03T**. This unit offers powerful functions such as speech recognition, voiceprint recognition, speech enhancement, and speech detection. It supports AEC (Acoustic Echo Cancellation) to effectively eliminate echoes and noise interference, improving the accuracy of speech recognition. Additionally, it supports mid-speech interruption, allowing for flexible interruption during the recognition process and quick response to new commands. The product is pre-configured with wake-up words and feedback commands at the factory. The device uses **UART** serial communication for data transmission and also supports waking up the device via UART or voice keywords. This unit supports user customization of the **wake-up** recognition word and can recognize up to 300 command words. It is equipped with a **microphone** for clear audio capture and includes a **speaker** for high-quality audio feedback. This product is widely used in AI assistants, smart homes, security monitoring, automotive systems, robotics, smart hardware, healthcare, and other fields, making it an ideal choice for realizing smart voice interactions.

Support the following products:

|ASRUnit|


UiFlow2 Example
---------------

ASR Example
^^^^^^^^^^^^^

Open the |asr_cores3_example.m5f2| project in UiFlow2.

This example shows how to use Unit ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

ASR Example
^^^^^^^^^^^^^

This example shows how to use Unit ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/asr/asr_cores3_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

ASRUnit
^^^^^^^^^

.. autoclass:: unit.asr.ASRUnit
    :members:
    :member-order: bysource