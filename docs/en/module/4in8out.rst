
4In8OutModule
=============

.. include:: ../refs/module.module_4in8out.ref

Support the following products:

|Module4In8Out|

Micropython Example:

    .. literalinclude:: ../../../examples/module/4in8out/module4in8out_fire_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |module4in8out_fire_example.m5f2|

class Module4In8Out
-------------------

Constructors
------------

.. class:: Module4In8Out(address)

    Init I2C Module 4In8Out I2C Address.

    :param int|list|tuple address: I2C address of the 4In8OutModule.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Module4In8Out.get_switch_value(switch_num) -> bool

    Get the current value of the rotary.

    :param int switch_num: Switch number (1 to 4).

    UIFLOW2:

        |get_switch_value.png|

.. method:: Module4In8Out.get_load_state(load_num) -> bool

    Get the state of a specific LED.

    :param int load_num: Load number (1 to 8).

    UIFLOW2:

        |get_load_state.png|

.. method:: Module4In8Out.set_load_state(load_num, state) -> None

    Set the state of a specific Load.

    :param int load_num: Load number (1 to 8).
    :param int state: The state to set for the Load.

    UIFLOW2:

        |set_load_state.png|

.. method:: Module4In8Out.get_firmware_version() -> int

    Get the firmware version of the 4In8Out module.


    UIFLOW2:

        |get_firmware_version.png|

.. method:: Module4In8Out.get_i2c_address() -> int

    Get the current I2C address of the 4In8Out module.


    UIFLOW2:

        |get_i2c_address.png|

.. method:: Module4In8Out.set_i2c_address(addr) -> None

    Set a new I2C address for the 4In8Out module.

    :param int addr: The new I2C address to set.

    UIFLOW2:

        |set_i2c_address.png|
