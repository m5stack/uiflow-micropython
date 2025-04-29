ALS
===

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.als.ref

ALS is used to read the built-in ambient light sensor inside the host device.

The following are the details of the host's support for ALS:

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+
    |                 |   ALS   |
    +=================+=========+
    | CoreS3          | |S|     |
    +-----------------+---------+
    | CoreS3 SE       |         |
    +-----------------+---------+


.. |S| unicode:: U+2714


Micropython Example:

    .. literalinclude:: ../../../examples/hardware/als/als_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |als_cores3_example.m5f2|


class ALS
---------

.. important::

    Methods of the ALS Class heavily rely on ``M5.begin()`` |M5.begin.png| and ``M5.update()`` |M5.update.png|.

    All calls to methods of ALS objects should be placed after ``M5.begin()`` |M5.begin.png|, and ``M5.update()`` |M5.update.png| should be called in the main loop.


Methods
-------

.. method:: ALS.getLightSensorData() -> int

    Read the ambient light sensor value built into the host device.

    UIFLOW2:

        |getLightSensorData.png|
