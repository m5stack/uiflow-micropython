UHF-RFID Unit
=============

.. include:: ../refs/unit.uhf_rfid.ref

Support the following products:

    |UHFRFIDUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/uhf_rfid/cores3_uhf_rfid_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_uhf_rfid_example.m5f2|


class UHFRFIDUnit
-----------------

Constructors
------------

.. class:: UHFRFIDUnit(id: Literal[0, 1, 2], port: list | tuple, verbose: bool = False)

    Create a UHF-RFID unit.

    :param int id: The ID of the unit.
    :param list|tuple port: The port that the unit is connected to.
    :param bool verbose: Print the log information. Default is True.

    UIFLOW2:

        |init.png|


Methods
-------

Demodulator
^^^^^^^^^^^^

.. method:: UHFRFIDUnit.get_demodulator_mixer() -> int

    Get demodulator mixer value.

    :return int: demodulator mixer value.

    Options:
        - 0x00: 0dB
        - 0x01: 3dB
        - 0x02: 6dB
        - 0x03: 9dB
        - 0x04: 12dB
        - 0x05: 15dB
        - 0x06: 16dB

    UIFLOW2:

        |get_demodulator_mixer.png|


.. method:: UHFRFIDUnit.set_demodulator_mixer(value: int) -> bool

    Set demodulator mixer value.

    :param int value: demodulator mixer value. 

    Options:
        - 0x00: 0dB
        - 0x01: 3dB
        - 0x02: 6dB
        - 0x03: 9dB
        - 0x04: 12dB
        - 0x05: 15dB
        - 0x06: 16dB

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_demodulator_mixer.png|


.. method:: UHFRFIDUnit.get_demodulator_amplifier() -> int

    Get demodulator amplifier value.

    :return int: demodulator amplifier value.

    Options:
        - 0x00: 12dB
        - 0x01: 18dB
        - 0x02: 21dB
        - 0x03: 24dB
        - 0x04: 27dB
        - 0x05: 30dB
        - 0x06: 36dB
        - 0x07: 40dB

    UIFLOW2:

        |get_demodulator_amplifier.png|


.. method:: UHFRFIDUnit.set_demodulator_amplifier(value: int) -> bool

    Set demodulator amplifier value.

    :param int value: demodulator amplifier value.

    Options:
        - 0x00: 12dB
        - 0x01: 18dB
        - 0x02: 21dB
        - 0x03: 24dB
        - 0x04: 27dB
        - 0x05: 30dB
        - 0x06: 36dB
        - 0x07: 40dB

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_demodulator_amplifier.png|


.. method:: UHFRFIDUnit.get_demodulator_threshold() -> int

    Get demodulator threshold value.

    :return int: demodulator threshold value. the range is from 0x01B0 to 0xFFFF.

    UIFLOW2:

        |get_demodulator_threshold.png|


.. method:: UHFRFIDUnit.set_demodulator_threshold(value: int) -> bool

    Set demodulator threshold value.

    :param int value: demodulator threshold value. the range is from 0x01B0 to 0xFFFF.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_demodulator_threshold.png|


Working
^^^^^^^

.. method:: UHFRFIDUnit.get_working_region() -> int

    Get work region.

    :return int: work region.

    Options:
        - UHFRFIDUnit.CN_900MHZ: China 900MHz
        - UHFRFIDUnit.CN_800MHZ: China 800MHz
        - UHFRFIDUnit.USA: USA
        - UHFRFIDUnit.EUR: EUR
        - UHFRFIDUnit.KR: KR

    UIFLOW2:

        |get_working_region.png|


.. method:: UHFRFIDUnit.set_working_region(region: int) -> bool

    Set work region.

    :param int region: work region.

    Options:
        - UHFRFIDUnit.CN_900MHZ: China 900MHz
        - UHFRFIDUnit.CN_800MHZ: China 800MHz
        - UHFRFIDUnit.USA: USA
        - UHFRFIDUnit.EUR: EUR
        - UHFRFIDUnit.KR: KR

    :return int: True if success, False if failed.

    UIFLOW2:

        |set_working_region.png|


.. method:: UHFRFIDUnit.get_working_channel() -> int

    Get work channel.

    :return int: work channel. the range is from 0 to 19.

    UIFLOW2:

        |get_working_channel.png|


.. method:: UHFRFIDUnit.set_working_channel(channel: int) -> bool

    Set work channel.

    :param int channel: work channel. the range is from 0 to 19.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_working_channel.png|


.. method:: UHFRFIDUnit.insert_working_channel(channel: int) -> bool

    Insert work channel.

    :param int channel: work channel. the range is from 0 to 19.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |insert_working_channel.png|


.. method:: UHFRFIDUnit.clear_working_channel() -> bool

    Clear work channel.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |clear_working_channel.png|


.. method:: UHFRFIDUnit.set_automatic_hopping(enable: bool) -> bool

    Set automatic hopping.

    :param bool enable: enable automatic hopping.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_automatic_hopping.png|


RF Power
^^^^^^^^

.. method:: UHFRFIDUnit.get_channel_rssi(channel: int) -> int

    Get channel RSSI value.

    :param int channel: work channel. the range is from 0 to 19.

    :return int: channel RSSI value. the unit is dBm.

    UIFLOW2:

        |get_channel_rssi.png|


.. method:: UHFRFIDUnit.get_blocking_signal_strength(channel: int) -> int

    Get blocking signal strength.

    :param int channel: work channel. the range is from 0 to 19.

    :return int: blocking signal strength. the unit is dBm.

    UIFLOW2:

        |get_blocking_signal_strength.png|


.. method:: UHFRFIDUnit.get_tx_power() -> int

    Get TX power.

    :return int: TX power. the unit is dBm. the range is from -7dBm to 30dBm.

    UIFLOW2:

        |get_tx_power.png|


.. method:: UHFRFIDUnit.set_tx_power(power: int) -> bool

    Set TX power.

    :param int power: TX power. the range is from -7dBm to 30dBm.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_tx_power.png|


.. method:: UHFRFIDUnit.set_continuous_wave(enable: bool) -> bool

    Set continuous wave.

    :param bool enable: enable continuous wave.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_continuous_wave.png|


Module Information and Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: UHFRFIDUnit.get_manufacturer_id() -> str

    Get manufacturer ID.

    :return str: manufacturer ID.

    UIFLOW2:

        |get_manufacturer_id.png|


.. method:: UHFRFIDUnit.get_hardware_version() -> str

    Get hardware version.

    :return str: hardware version.

    UIFLOW2:

        |get_hardware_version.png|


.. method:: UHFRFIDUnit.get_firmware_version() -> str

    Get firmware version.

    :return str: firmware version.

    UIFLOW2:

        |get_firmware_version.png|


.. method:: UHFRFIDUnit.sleep() -> bool

    Set sleep.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |sleep.png|


.. method:: UHFRFIDUnit.wake() -> bool

    Set wake up.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |wake.png|


.. method:: UHFRFIDUnit.set_automatic_sleep_time(min: int) -> bool

    Set automatic sleep time.

    :param int min: automatic sleep time in minutes. the range is from 1 to 30.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_automatic_sleep_time.png|


.. method:: UHFRFIDUnit.disable_automatic_sleep() -> bool

    Disable automatic sleep.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |disable_automatic_sleep.png|


Read and Write Tag
^^^^^^^^^^^^^^^^^^

.. method:: UHFRFIDUnit.inventory() -> str

    Get tag epc code. if no tag is found, return empty string.

    :return: hexadecimal string of tag epc code.

    UIFLOW2:

        |inventory.png|


.. method:: UHFRFIDUnit.set_select_mode(mode: int) -> bool

    Set select mode.

    :param int mode: select mode.

    Options:
        - 0x00: need select command
        - 0x01: no need select command
        - 0x02: part operation need select command

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_select_mode.png|


.. method:: UHFRFIDUnit.select(target: int, action: int, membank: int, pointer: int, truncate: bool, mask: str) -> bool

    Set select tag.

    :param int target: target.
    :param int action: action.
    :param int membank: memory bank.
    :param int pointer: pointer.
    :param bool truncate: truncate.
    :param str mask: EPC code. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |select.png|


.. method:: UHFRFIDUnit.set_access_password(old_password: str, new_password: str) -> None

    Set access password.

    :param str old_password: old access password. hexadecimal string.
    :param str new_password: new access password. hexadecimal string.

    UIFLOW2:

        |set_access_password.png|


.. method:: UHFRFIDUnit.set_kill_password(password) -> None

    Set kill password.

    :param str password: kill password. hexadecimal string.

    UIFLOW2:

        |set_kill_password.png|


.. method:: UHFRFIDUnit.kill(password: str) -> bool

    Kill tag.

    :param str password: kill password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |kill.png|

.. method:: UHFRFIDUnit.set_query_param(dr=0b0, m=0b00, tr_ext=0b1, sel=0b00, session=0b00, target=0b0, q=0b0100) -> bool

    Set query parameter.

    :param int dr: dr. fixed to 0.
    :param int m: m. fixed to 0.
    :param int tr_ext: tr_ext. fixed to 1.
    :param int sel: sel. the range is from 0 to 3.
    :param int session: session. the range is from 0 to 3.
    :param int target: target. the range is from 0 to 1.
    :param int q: q. the range is from 0 to 8.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_query_param.png|


.. method:: UHFRFIDUnit.lock_mem_bank( kill_lock: int = 0b00, access_lock: int = 0b00, epc_lock: int = 0b00, tid_lock: int = 0b00, user_lock: int = 0b00, access: str = "00000000",) -> bool

    Lock memory bank.

    :param int kill_lock: kill lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    :param int access_lock: access lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    :param int epc_lock: epc lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    :param int tid_lock: tid lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    :param int user_lock: user lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    :param str access: access password. hexadecimal string.

    UIFLOW2:

        |lock_mem_bank.png|


.. method:: UHFRFIDUnit.read_mem_bank(bank: int, offset: int, length: int, access_password: str = "00000000") -> str

    Read memory bank.

    :param int bank: memory bank.

        Options:
            - UHFRFIDUnit.RFU: reserved
            - UHFRFIDUnit.EPC: epc
            - UHFRFIDUnit.TID: tid
            - UHFRFIDUnit.USER: user

    :param int offset: offset.
    :param int length: length.
    :param str access_password: access password. hexadecimal string.

    :return str: data. hexadecimal string.

    UIFLOW2:

        |read_mem_bank.png|


.. method:: UHFRFIDUnit.write_mem_bank(bank: int, offset: int, data: str, access_password: str = "00000000")

    Write memory bank.

    :param int bank: memory bank.

        Options:
            - UHFRFIDUnit.RFU: reserved
            - UHFRFIDUnit.EPC: epc
            - UHFRFIDUnit.TID: tid
            - UHFRFIDUnit.USER: user

    :param int offset: offset.
    :param str data: data. hexadecimal string.
    :param str access_password: access password. hexadecimal string.

    UIFLOW2:

        |write_mem_bank.png|


Impinj Monza
^^^^^^^^^^^^^

.. method:: UHFRFIDUnit.get_impinj_monza_qt_sr(persistence, password: str = "00000000") -> bool

    Get Impinj Monza QT_SR.

    :param int persistence: persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    :param str password: access password. hexadecimal string.

    :return bool: QT_SR status.

    UIFLOW2:

        |get_impinj_monza_qt_sr.png|


.. method:: UHFRFIDUnit.set_impinj_monza_qt_sr(qt_sr: bool, persistence: int, password: str = "00000000") -> bool

    Set Impinj Monza QT_SR.

    :param bool qt_sr: QT_SR status.
    :param int persistence: persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    :param str password: access password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_impinj_monza_qt_sr.png|


.. method:: UHFRFIDUnit.get_impinj_monza_qt_mem(persistence, password: str = "00000000") -> bool

    Set Impinj Monza QT_MEM.

    :param int persistence: persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    :param str password: access password. hexadecimal string.

    :return bool: QT_MEM status.

    UIFLOW2:

        |get_impinj_monza_qt_mem.png|


.. method:: UHFRFIDUnit.set_impinj_monza_qt_mem(qt_mem: bool, persistence: int, password: str = "00000000") -> bool

    Set Impinj Monza QT_MEM.

    :param bool qt_mem: QT_MEM status.
    :param int persistence: persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    :param str password: access password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_impinj_monza_qt_mem.png|


NXP
^^^

.. method:: UHFRFIDUnit.nxp_eas_alarm() -> str

    Get NXP EAS alarm code.

    :return str: NXP EAS alarm code. hexadecimal string.

    UIFLOW2:

        |nxp_eas_alarm.png|


.. method:: UHFRFIDUnit.get_nxp_config_word(password: str = "00000000") -> int

    Get NXP config word.

    :param str password: access password. hexadecimal string.

    :return int: NXP config word.

    UIFLOW2:

        |get_nxp_config_word.png|


.. method:: UHFRFIDUnit.set_nxp_config_word(config_word: int, password: str = "00000000") -> bool

    Set NXP config word.

    :param int config_word: NXP config word.
    :param str password: access password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |set_nxp_config_word.png|


.. method:: UHFRFIDUnit.nxp_read_protect(set: int, password: str = "00000000") -> bool

    Set NXP read protect.

    :param int set: set read protect. 0x00 is set read protect, 0x01 is reset read protect.
    :param str password: access password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |nxp_read_protect.png|

        |nxp_read_protect1.png|


.. method:: UHFRFIDUnit.nxp_change_eas(set: int, password: str = "00000000") -> bool

    Change NXP EAS.

    :param int set: set EAS. 0x00 is set EAS, 0x01 is reset EAS.
    :param str password: access password. hexadecimal string.

    :return bool: True if success, False if failed.

    UIFLOW2:

        |nxp_change_eas.png|

        |nxp_change_eas1.png|
