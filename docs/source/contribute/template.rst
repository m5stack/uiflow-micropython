**************************
API Documentation Template
**************************

.. note::

    1. Please follow the template below to write your API documentation;
    2. Strict use of reStructuredText syntax;
    3. Write strictly according to the various tags of the template
    4. When you are finished, delete all instructions (similar to this one) and any extra header information.

.. Write your overview and delete this line when you are finished.

.. List the supported devices and provide links to product documentation. Delete this line when you are done.

Support the following products:

    ================== ==================
    xxx Unit           xxx Unit
    ================== ==================

.. Compatibility list, if there are compatibility issues, please list the table. Below is a complete example, delete this line when you are done.

Below is the detailed support for Speaker on the host:

.. table::
    :widths: auto

    +-----------------+-------------------+
    |Controller       | Atomic Echo Base  |
    +=================+===================+
    | Atom Echo       | |O|               |
    +-----------------+-------------------+
    | Atom Lite       | |S|               |
    +-----------------+-------------------+

- |S|: Supported.
- |O|: Optional, It conflicts with some internal resource of the host.

.. |S| unicode:: U+2705
.. |O| unicode:: U+2B55


UiFlow2 Example
===============

.. note::

    Prepare one or more examples that fully demonstrate the functionality of the API. Delete this part of the description when you are done.


Example1
--------

.. Source code link of the example. Click the link to open the project directly on uiflow2. Delete this line after completion.

.. Write a detailed description of the example. A good description allows the reader to fully understand the example. Delete this line when you are finished.

.. Place a picture of your example and delete this line when you are finished.

.. Display the output of the example, which can be a picture or log text. Delete this line when you are done.


MicroPython Example
===================

Example1
--------

.. The source code link of the example. Click this link to download the source code. Delete this line when you are done.

.. Write a detailed description of the example. A good description allows the reader to fully understand the example. Delete this line when you are finished.

.. Display the output of the example, which can be a picture or log text. Delete this line when you are done.


API
===

Function
--------

.. All functions can be put under this heading.

.. function:: func1(arg1:int, arg2:int) -> int

    Function 1, please write a detailed description of the function.

    :param arg1: Parameter 1.
    :type arg1: int
    :param int arg2: Parameter 2.
    :type arg2: int
    :return: Return value.
    :rtype: int

    .. Please note that the return value type of the function needs to be specified

    UiFlow2 Code Block:

        .. Please place the Blockly image of the function and delete this line when you are done.

    MicroPython Code Block:

        .. code-block:: python

            pass # Please put the MicroPython code of the function, and delete this line when you are done


Class1
-------

.. Add a title to each class.

.. class:: Class1(arg1:int)

    Constructor.

    :param arg1: Parameter 1.
    :type arg1: int

    .. Please note that the type of the parameter needs to be specified


    .. method:: Class1.method1(arg1:int, arg2:int) -> int

        Method 1, please write a detailed description of the method.

        :param arg1: Parameter 1.
        :type arg1: int
        :param int arg2: Parameter 2.
        :type arg2: int
        :return: Return value.
        :rtype: int

        .. Please note that the return value type of the method needs to be specified.

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.


    .. property:: Class1.property1
        :type: int

        Property 1, please write a detailed description of the property.

        .. Please note that the type of the property needs to be specified.

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.


    .. staticmethod:: Class1.staticmethod1(arg1:int, arg2:int) -> int

        Static method 1, please write a detailed description of the static method.

        :param arg1: Parameter 1.
        :type arg1: int
        :param int arg2: Parameter 2.
        :type arg2: int
        :return: Return value.
        :rtype: int

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.


    .. classmethod:: Class1.classmethod1(arg1:int, arg2:int) -> int

        Class method 1, please write a detailed description of the class method.

        :param arg1: Parameter 1.
        :type arg1: int
        :param int arg2: Parameter 2.
        :type arg2: int
        :return: Return value.
        :rtype: int

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.


    .. attribute:: Class1.b
       :type: int

        Attribute b, please write a detailed description of the attribute.

        .. Please note that the type of the attribute needs to be specified.

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.


    .. data:: Class1.CONSTANT1
       :type: int

        Constant 1, Please write a detailed description of the constant. Constants are named using uppercase letters.

        UiFlow2 Code Block:

            .. Please place the Blockly image of the function and delete this line when you are done.

        MicroPython Code Block:

            .. code-block:: python

                pass # Please put the MicroPython code of the function, and delete this line when you are done.

Class2
-------

.. class:: Class2()

    Constructor.
