Atomic Display Base
===================

.. sku: A115 K115 K115-B

.. include:: ../refs/base.display.ref

The is the class of the Atomic Display Base, which is used to display images and text on the screen.

Support the following products:

    ====================== ====================== ======================
    |Atomic Display Base|  |Atom Display|         |Atom Display-Lite|
    ====================== ====================== ======================

Below is the detailed support for Atomic Display Base on the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+
    |Controller       | Status  |
    +=================+=========+
    | Atom Echo       | |O|     |
    +-----------------+---------+
    | Atom Lite       | |S|     |
    +-----------------+---------+
    | Atom Matrix     | |S|     |
    +-----------------+---------+
    | AtomS3          | |S|     |
    +-----------------+---------+
    | AtomS3 Lite     | |S|     |
    +-----------------+---------+
    | AtomS3R         | |S|     |
    +-----------------+---------+
    | AtomS3R-CAM     | |S|     |
    +-----------------+---------+
    | AtomS3R-Ext     | |S|     |
    +-----------------+---------+

.. |S| unicode:: U+2705
.. |O| unicode:: U+2B55

- |S|: Supported.

- |O|: Optional, It conflicts with some internal resource of the host.


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^^^^^^^

Open the |atoms3_draw_text_example.m5f2| project in UiFlow2.

This example displays the text "M5Stack" on the screen.

UiFlow2 Code Block:

    |example_draw_text.png|

Example output:

    None


Draw Image
^^^^^^^^^^^^^^^

Open the |atoms3_draw_text_example.m5f2| project in UiFlow2.

This example displays the image on the screen.

UiFlow2 Code Block:

    |example_draw_image.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^^^^^^^

This example displays the text "M5Stack" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/display/atoms3_draw_text_example.py
        :language: python
        :linenos:

Example output:

    None


Draw Image
^^^^^^^^^^^^^^^

This example displays the image on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/display/atoms3_draw_image_example.py

Example output:

    None


**API**
-------

AtomicDisplayBase
^^^^^^^^^^^^^^^^^^

.. autoclass:: base.display.AtomicDisplayBase
    :members:
