NB-IoT Module
=============

.. include:: ../refs/module.nbiot.ref

The following products are supported:

    |NB-IoT Module|


class NBIOTModule
-----------------

Constructors
------------

.. class:: NBIOTModule(id: Literal[0, 1, 2], tx: int, rx: int)

    Create a NBIOTModule object

    :param id: UART ID.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.

    UIFLOW2:

        |init.png|


See :ref:`unit.NBIOTUnit.Methods <unit.NBIOTUnit.Methods>` for more details.
