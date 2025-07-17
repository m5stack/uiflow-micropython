.. currentmodule:: m5ui

M5Arc
========

.. include:: ../refs/m5ui.arc.ref

M5Arc is a widget that can be used to create arcs in the user interface. It can be used to display circular progress or other circular indicators.

UiFlow2 Example
---------------

event arc
^^^^^^^^^^^^

Open the |cores3_arc_event_example.m5f2| project in UiFlow2.

This example creates an arc that triggers an event when the value changes.

UiFlow2 Code Block:

    |cores3_arc_event_example.png|

Example output:

    None


MicroPython Example
-------------------

event arc
^^^^^^^^^^^^

This example creates an arc that triggers an event when the value changes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/arc/cores3_arc_event_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Arc
^^^^^^^^

.. autoclass:: m5ui.arc.M5Arc
    :members:
    :member-order: bysource

    .. py:method:: set_rotation(rotation)

        Set the rotation of the arc.

        :param int rotation: The rotation angle of the arc in degrees.

        UiFlow2 Code Block:

            |set_rotation.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_rotation(90)

    .. py:method:: set_value(value)

        Set the value of the arc.

        :param int value: The value of the arc.

        UiFlow2 Code Block:

            |set_value.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_value(90)

    .. py:method:: get_value()

        Get the value of the arc.

        :return: The value of the arc.
        :rtype: int

        UiFlow2 Code Block:

            |get_value.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.get_value()

    .. py:method:: set_range()

        Set the range of the arc.

        :param int min: The minimum value of the arc.
        :param int max: The maximum value of the arc.

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_range(0, 100)


    .. py:method:: set_mode()

        Set the mode of the arc.

        :param int mode: The mode of the arc.
    
            Option: 
                - lv.arc.MODE.NORMAL: Normal mode.
                - lv.arc.MODE.REVERSE: Reverse mode.
                - lv.arc.MODE.SYMMETRICAL: Symmetrical mode.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_mode(lv.ARC.MODE.NORMAL)

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_flag(lv.obj.FLAG.HIDDEN, True)


    .. py:method:: set_pos(x, y)

        Set the position of the arc.

        :param int x: The x-coordinate of the arc.
        :param int y: The y-coordinate of the arc.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the arc.

        :param int x: The x-coordinate of the arc.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the arc.

        :param int y: The y-coordinate of the arc.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the arc.

        :param int width: The width of the arc.
        :param int height: The height of the arc.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_size(100, 50)

    .. py:method:: set_width(width)

        Set the width of the arc.

        :param int width: The width of the arc.

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_width(100)

    .. py:method:: set_height(height)

        Set the height of the arc.

        :param int height: The height of the arc.

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.set_height(50)

    .. py:method:: align_to(obj, align, x, y)

        Align the arc to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                arc_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the arc. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def value_changed_event(event_struct):
                    global page0, arc_0
                    print("value changed:", arc_0.get_value())

                arc_0.add_event_cb(value_changed_event, lv.EVENT.VALUE_CHANGED, None)
