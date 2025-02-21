
ASR Unit
=========
.. sku:U194
.. include:: ../refs/unit.asr.ref

**Unit ASR** is an **AI** offline speech recognition unit, featuring the built-in AI smart offline speech module **CI-03T**. This unit offers powerful functions such as speech recognition, voiceprint recognition, speech enhancement, and speech detection. It supports AEC (Acoustic Echo Cancellation) to effectively eliminate echoes and noise interference, improving the accuracy of speech recognition. Additionally, it supports mid-speech interruption, allowing for flexible interruption during the recognition process and quick response to new commands. The product is pre-configured with wake-up words and feedback commands at the factory. The device uses **UART** serial communication for data transmission and also supports waking up the device via UART or voice keywords. This unit supports user customization of the **wake-up** recognition word and can recognize up to 300 command words. It is equipped with a **microphone** for clear audio capture and includes a **speaker** for high-quality audio feedback. This product is widely used in AI assistants, smart homes, security monitoring, automotive systems, robotics, smart hardware, healthcare, and other fields, making it an ideal choice for realizing smart voice interactions.

Support the following products:

|ASRUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/asr/asr_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |asr_cores3_example.m5f2|

class ASRUnit
-------------

Constructors
------------

.. class:: ASRUnit(id, port)

    Initialize the ASRUnit object with UART configuration and set up the command handler.

    :param int id: The UART port ID for communication, default is 1.
    :param  port: A list or tuple containing the TX and RX pins for UART communication.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ASRUnit.get_received_status()

    Get the status of the received message.

        :returns: True if a message is received, False otherwise.

    UIFLOW2:

        |get_received_status.png|

.. method:: ASRUnit.send_message(command_num)

    Send a message with a specified command number via UART.

    :param int command_num: The command number to send in the message.

    UIFLOW2:

        |send_message.png|

.. method:: ASRUnit.get_current_raw_message()

    Get the raw message received in hexadecimal format.


    :returns: The raw message as a string in hexadecimal format.

    UIFLOW2:

        |get_current_raw_message.png|

.. method:: ASRUnit.get_current_command_word()

    Get the command word corresponding to the current command number.


    :returns: The command word as a string.

    UIFLOW2:

        |get_current_command_word.png|

.. method:: ASRUnit.get_current_command_num()

    Get the current command number.

    :returns: The command number.

    UIFLOW2:

        |get_current_command_num.png|

.. method:: ASRUnit.get_command_handler()

    Check if the current command has an associated handler.

    :returns: True if a handler exists for the current command, 

    UIFLOW2:

        |get_command_handler.png|

.. method:: ASRUnit.add_command_word(command_num, command_word, event_handler)

    Add a new command word and its handler to the command list.

    :param int command_num: The command number (must be between 0 and 255).
    :param str command_word: The command word to associate with the command number.
    :param  event_handler: An optional event handler function to be called for the command.

    UIFLOW2:

        |add_command_word.png|
        
        |event.png|

.. method:: ASRUnit.remove_command_word(command_word)

    Remove a command word from the command list by its word.

    :param str command_word: The command word to remove.

    UIFLOW2:

        |remove_command_word.png|

.. method:: ASRUnit.search_command_num(command_word)

    Search for the command number associated with a command word.

    :param str command_word: The command word to search for.

    :returns: The command number if found, otherwise -1.

    UIFLOW2:

        |search_command_num.png|

.. method:: ASRUnit.search_command_word(command_num)

    Search for the command word associated with a command number.

    :param int command_num: The command number to search for.

    :returns: The command word if found, otherwise "Unknown command 

    UIFLOW2:

        |search_command_word.png|

.. method:: ASRUnit.get_command_list()

    Get the list of all commands and their associated handlers.

    :returns: A dictionary of command numbers and their corresponding command words and handlers.

    UIFLOW2:

        |get_command_list.png|

.. method:: ASRUnit.check_tick_callback()

    Check if a handler is defined for the current command and schedule its execution.