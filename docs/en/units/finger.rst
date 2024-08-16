Finger Unit
===========

.. include:: ../refs/unit.finger.ref

The following products are supported:

    |FingerUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/finger/cores3_finger_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_finger_example.m5f2|


class FingerUnit
----------------

Constructors
------------

.. class:: FingerUnit(id: Literal[0, 1, 2] = 1, port: list | tuple = None)

    Create a FingerUnit object.

    :param id: The ID of the UART, 0 or 1 or 2.
    :param port: UART pin numbers.

    UIFLOW2:

        |init.png|


.. _unit.FingerUnit.Methods:

Methods
-------

.. method:: FingerUnit.sleep() -> bool

    After calling this method successfully, FPC1020A will not be able to respond to any messages.

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

        |sleep.png|


.. method:: FingerUnit.get_add_mode() -> int

    In the no-repeat mode, only one user can be added with the same finger,
    and an error message will be returned if the second round of adding is
    forced.

    :returns: mode (0: no-repeat mode, 1: repeat mode)

    UIFLOW2:

        |get_add_mode.png|


.. method:: FingerUnit.set_add_mode(mode: int) -> int

    In the no-repeat mode, only one user can be added with the same finger,
    and an error message will be returned if the second round of adding is
    forced.

    :param mode: mode (0: no-repeat mode, 1: repeat mode)

    :returns: mode (0: no-repeat mode, 1: repeat mode)

    UIFLOW2:

        |set_add_mode.png|


.. method:: FingerUnit.add_user(id: int, permission: Literal[1, 2, 3]) -> int

    add new user

    After calling this method, you need to put your finger on the fingerprint module.

    :param id: user id (0-149)
    :param permission: user permission (1: normal, 2: admin, 3: super admin)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

        |add_user.png|


.. method:: FingerUnit.delete_user(id: int) -> int

    Delete the user with the specified id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

        |delete_user.png|


.. method:: FingerUnit.delete_all_user() -> bool

    Delete all users.

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

        |delete_all_user.png|


.. method:: FingerUnit.get_user_count() -> int

    Get registered users count.

    :returns: -1 if the command was unsuccessful, otherwise the number of registered users.

    UIFLOW2:

        |get_user_count.png|


.. method:: FingerUnit.get_user_capacity() -> int

    Get the maximum number of users that can be registered.

    :returns: -1 if the command was unsuccessful, otherwise the maximum number of users that can be registered.

    UIFLOW2:

        |get_user_capacity.png|


.. method:: FingerUnit.compare_id(id: int, timeout: int=5000) -> bool

    Check whether the currently collected fingerprint matches the specified user id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

        |compare_id.png|


.. method:: FingerUnit.compare_finger(timeout: int=5000) -> int

    Detect whether the currently collected fingerprint is a registered user.

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

        |compare_finger.png|


.. method:: FingerUnit.get_user_list() -> list

    Get the list of registered users.

    :returns: list of registered users.

    UIFLOW2:

        |get_user_list.png|


.. method:: FingerUnit.get_user_info(id: int) -> Union[tuple, None]:

    Get the information of the user with the specified id.

    :param id: user id (0-149)

    :returns: tuple of (id, permission) if the command was successful, None otherwise.

    UIFLOW2:

        |get_user_info.png|


.. method:: FingerUnit.get_user_permission(id: int) -> int

    Get the permission of the user with the specified id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the permission of the user.

    UIFLOW2:

        |get_user_permission.png|


.. method:: FingerUnit.get_user_characteristics(id: int) -> Union[bytes, None]

    Get the characteristics of the user with the specified id.

    :param id: user id (0-149)

    :returns: bytes of the characteristics if the command was successful, None otherwise.

    UIFLOW2:

        |get_user_characteristic.png|


.. method:: FingerUnit.add_user_info(id, permissions, characteristic, timeout: int=5000) -> bool

    Register a new user with FPC1020A.

    :param id: user id (0-149)
    :param permissions: user permission (1: normal, 2: admin, 3: super admin)
    :param characteristic: user characteristics
    :param timeout: timeout in milliseconds

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

        |add_user_info.png|


.. method:: FingerUnit.capture_characteristic(timeout: int=5000) -> bytes

    Capture the characteristics of the fingerprint.

    :param timeout: timeout in milliseconds

    :returns: bytes of the characteristics if the command was successful, None otherwise.


.. method:: FingerUnit.get_match_level() -> int

    The comparison level ranges from 0 to 9, the larger the value, the stricter the comparison, and the default value is 5.

    :returns: match level (0-9)

    UIFLOW2:

        |get_match_level.png|


.. method:: FingerUnit.set_match_level(level: int) -> int

    The comparison level ranges from 0 to 9, the larger the value, the stricter the comparison, and the default value is 5.

    :param level: match level (0-9)

    :returns: match level (0-9)

    UIFLOW2:

        |set_match_level.png|


.. method:: FingerUnit.get_version() -> str

    Get the version information of FPC1020A.

    :returns: version information.
