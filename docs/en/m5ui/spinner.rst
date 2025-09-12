.. currentmodule:: m5ui

M5Spinner
==========

.. include:: ../refs/m5ui.spinner.ref

M5Spinner is a spinning arc over a ring, typically used to show some type of activity is in progress.

UiFlow2 Example
---------------

spinner
^^^^^^^^^^^^^^

Open the |core2_spinner_example.m5f2| project in UiFlow2.

This example shows a spinning arc over a ring.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

spinner
^^^^^^^^^^^^^

This example shows a spinning arc over a ring.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/spinner/core2_spinner_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Spinner
^^^^^^^^^

.. autoclass:: m5ui.spinner.M5Spinner
    :members:
    :member-order: bysource

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: set_pos(x, y)

        Set the position of the spinner.

        :param int x: The x-coordinate of the spinner.
        :param int y: The y-coordinate of the spinner.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the spinner.

        :param int x: The x-coordinate of the spinner.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the spinner.

        :param int y: The y-coordinate of the spinner.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the spinner.

        :param int width: The width of the spinner.
        :param int height: The height of the spinner.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_size(100, 50)

    .. py:method:: align_to(obj, align, x, y)

        Align the spinner to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_anim_params(anim_t, angle)

        Set the animation parameters of the spinner.

        :param int anim_t: The animation time in milliseconds.
        :param int angle: The angle of the spinner in degrees.

        UiFlow2 Code Block:

            |set_anim_params.png|

        MicroPython Code Block:

            .. code-block:: python

                spinner_0.set_anim_params(1000, 180)