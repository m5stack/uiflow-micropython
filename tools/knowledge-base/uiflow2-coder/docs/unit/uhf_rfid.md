# UHF-RFID Unit

Support the following products:

    UHFRFIDUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import UHFRFIDUnit

nbiot2_0 = None
uhfrfid_0 = None

epc = None

def setup():
    global nbiot2_0, uhfrfid_0, epc

    M5.begin()
    Widgets.fillScreen(0x222222)

    uhfrfid_0 = UHFRFIDUnit(2, port=(18, 17))
    epc = uhfrfid_0.inventory()
    print(epc)
    uhfrfid_0.select(UHFRFIDUnit.S0, 0b000, UHFRFIDUnit.RFU, 0x20, False, epc)
    uhfrfid_0.write_mem_bank(UHFRFIDUnit.RFU, 0x00, "12345678", "00000000")
    print(uhfrfid_0.read_mem_bank(UHFRFIDUnit.RFU, 0x00, 4, "00000000"))

def loop():
    global nbiot2_0, uhfrfid_0, epc
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## class UHFRFIDUnit

## Constructors

### `class UHFRFIDUnit(id: Literal[0, 1, 2], port: list | tuple, verbose: bool = False)`

    Create a UHF-RFID unit.

    - Parameter `id` (`int`): The ID of the unit.
    - Parameter `port` (`list|tuple`): The port that the unit is connected to.
    - Parameter `verbose` (`bool`): Print the log information. Default is True.

## Methods

#### Demodulator

### `UHFRFIDUnit.get_demodulator_mixer() -> int`

    Get demodulator mixer value.

    Options:
        - 0x00: 0dB
        - 0x01: 3dB
        - 0x02: 6dB
        - 0x03: 9dB
        - 0x04: 12dB
        - 0x05: 15dB
        - 0x06: 16dB

### `UHFRFIDUnit.set_demodulator_mixer(value: int) -> bool`

    Set demodulator mixer value.

    - Parameter `value` (`int`): demodulator mixer value.

    Options:
        - 0x00: 0dB
        - 0x01: 3dB
        - 0x02: 6dB
        - 0x03: 9dB
        - 0x04: 12dB
        - 0x05: 15dB
        - 0x06: 16dB

### `UHFRFIDUnit.get_demodulator_amplifier() -> int`

    Get demodulator amplifier value.

    Options:
        - 0x00: 12dB
        - 0x01: 18dB
        - 0x02: 21dB
        - 0x03: 24dB
        - 0x04: 27dB
        - 0x05: 30dB
        - 0x06: 36dB
        - 0x07: 40dB

### `UHFRFIDUnit.set_demodulator_amplifier(value: int) -> bool`

    Set demodulator amplifier value.

    - Parameter `value` (`int`): demodulator amplifier value.

    Options:
        - 0x00: 12dB
        - 0x01: 18dB
        - 0x02: 21dB
        - 0x03: 24dB
        - 0x04: 27dB
        - 0x05: 30dB
        - 0x06: 36dB
        - 0x07: 40dB

### `UHFRFIDUnit.get_demodulator_threshold() -> int`

    Get demodulator threshold value.

### `UHFRFIDUnit.set_demodulator_threshold(value: int) -> bool`

    Set demodulator threshold value.

    - Parameter `value` (`int`): demodulator threshold value. the range is from 0x01B0 to 0xFFFF.

#### Working

### `UHFRFIDUnit.get_working_region() -> int`

    Get work region.

    Options:
        - UHFRFIDUnit.CN_900MHZ: China 900MHz
        - UHFRFIDUnit.CN_800MHZ: China 800MHz
        - UHFRFIDUnit.USA: USA
        - UHFRFIDUnit.EUR: EUR
        - UHFRFIDUnit.KR: KR

### `UHFRFIDUnit.set_working_region(region: int) -> bool`

    Set work region.

    - Parameter `region` (`int`): work region.

    Options:
        - UHFRFIDUnit.CN_900MHZ: China 900MHz
        - UHFRFIDUnit.CN_800MHZ: China 800MHz
        - UHFRFIDUnit.USA: USA
        - UHFRFIDUnit.EUR: EUR
        - UHFRFIDUnit.KR: KR

### `UHFRFIDUnit.get_working_channel() -> int`

    Get work channel.

### `UHFRFIDUnit.set_working_channel(channel: int) -> bool`

    Set work channel.

    - Parameter `channel` (`int`): work channel. the range is from 0 to 19.

### `UHFRFIDUnit.insert_working_channel(channel: int) -> bool`

    Insert work channel.

    - Parameter `channel` (`int`): work channel. the range is from 0 to 19.

### `UHFRFIDUnit.clear_working_channel() -> bool`

    Clear work channel.

### `UHFRFIDUnit.set_automatic_hopping(enable: bool) -> bool`

    Set automatic hopping.

    - Parameter `enable` (`bool`): enable automatic hopping.

#### RF Power

### `UHFRFIDUnit.get_channel_rssi(channel: int) -> int`

    Get channel RSSI value.

    - Parameter `channel` (`int`): work channel. the range is from 0 to 19.

### `UHFRFIDUnit.get_blocking_signal_strength(channel: int) -> int`

    Get blocking signal strength.

    - Parameter `channel` (`int`): work channel. the range is from 0 to 19.

### `UHFRFIDUnit.get_tx_power() -> int`

    Get TX power.

### `UHFRFIDUnit.set_tx_power(power: int) -> bool`

    Set TX power.

    - Parameter `power` (`int`): TX power. the range is from -7dBm to 30dBm.

### `UHFRFIDUnit.set_continuous_wave(enable: bool) -> bool`

    Set continuous wave.

    - Parameter `enable` (`bool`): enable continuous wave.

#### Module Information and Settings

### `UHFRFIDUnit.get_manufacturer_id() -> str`

    Get manufacturer ID.

### `UHFRFIDUnit.get_hardware_version() -> str`

    Get hardware version.

### `UHFRFIDUnit.get_firmware_version() -> str`

    Get firmware version.

### `UHFRFIDUnit.sleep() -> bool`

    Set sleep.

### `UHFRFIDUnit.wake() -> bool`

    Set wake up.

### `UHFRFIDUnit.set_automatic_sleep_time(min: int) -> bool`

    Set automatic sleep time.

    - Parameter `min` (`int`): automatic sleep time in minutes. the range is from 1 to 30.

### `UHFRFIDUnit.disable_automatic_sleep() -> bool`

    Disable automatic sleep.

#### Read and Write Tag

### `UHFRFIDUnit.inventory() -> str`

    Get tag epc code. if no tag is found, return empty string.

    - Returns: hexadecimal string of tag epc code.

### `UHFRFIDUnit.set_select_mode(mode: int) -> bool`

    Set select mode.

    - Parameter `mode` (`int`): select mode.

    Options:
        - 0x00: need select command
        - 0x01: no need select command
        - 0x02: part operation need select command

### `UHFRFIDUnit.select(target: int, action: int, membank: int, pointer: int, truncate: bool, mask: str) -> bool`

    Set select tag.

    - Parameter `target` (`int`): target.
    - Parameter `action` (`int`): action.
    - Parameter `membank` (`int`): memory bank.
    - Parameter `pointer` (`int`): pointer.
    - Parameter `truncate` (`bool`): truncate.
    - Parameter `mask` (`str`): EPC code. hexadecimal string.

### `UHFRFIDUnit.set_access_password(old_password: str, new_password: str) -> None`

    Set access password.

    - Parameter `old_password` (`str`): old access password. hexadecimal string.
    - Parameter `new_password` (`str`): new access password. hexadecimal string.

### `UHFRFIDUnit.set_kill_password(password) -> None`

    Set kill password.

    - Parameter `password` (`str`): kill password. hexadecimal string.

### `UHFRFIDUnit.kill(password: str) -> bool`

    Kill tag.

    - Parameter `password` (`str`): kill password. hexadecimal string.

### `UHFRFIDUnit.set_query_param(dr=0b0, m=0b00, tr_ext=0b1, sel=0b00, session=0b00, target=0b0, q=0b0100) -> bool`

    Set query parameter.

    - Parameter `dr` (`int`): dr. fixed to 0.
    - Parameter `m` (`int`): m. fixed to 0.
    - Parameter `tr_ext` (`int`): tr_ext. fixed to 1.
    - Parameter `sel` (`int`): sel. the range is from 0 to 3.
    - Parameter `session` (`int`): session. the range is from 0 to 3.
    - Parameter `target` (`int`): target. the range is from 0 to 1.
    - Parameter `q` (`int`): q. the range is from 0 to 8.

### `UHFRFIDUnit.lock_mem_bank( kill_lock: int = 0b00, access_lock: int = 0b00, epc_lock: int = 0b00, tid_lock: int = 0b00, user_lock: int = 0b00, access: str = "00000000",) -> bool`

    Lock memory bank.

    - Parameter `kill_lock` (`int`): kill lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    - Parameter `access_lock` (`int`): access lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    - Parameter `epc_lock` (`int`): epc lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    - Parameter `tid_lock` (`int`): tid lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    - Parameter `user_lock` (`int`): user lock.

        Options:
            - UHFRFIDUnit.OPEN: open
            - UHFRFIDUnit.LOCK: lock
            - UHFRFIDUnit.PERMA_OPEN: perma open
            - UHFRFIDUnit.PERMA_LOCK: perma lock

    - Parameter `access` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.read_mem_bank(bank: int, offset: int, length: int, access_password: str = "00000000") -> str`

    Read memory bank.

    - Parameter `bank` (`int`): memory bank.

        Options:
            - UHFRFIDUnit.RFU: reserved
            - UHFRFIDUnit.EPC: epc
            - UHFRFIDUnit.TID: tid
            - UHFRFIDUnit.USER: user

    - Parameter `offset` (`int`): offset.
    - Parameter `length` (`int`): length.
    - Parameter `access_password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.write_mem_bank(bank: int, offset: int, data: str, access_password: str = "00000000")`

    Write memory bank.

    - Parameter `bank` (`int`): memory bank.

        Options:
            - UHFRFIDUnit.RFU: reserved
            - UHFRFIDUnit.EPC: epc
            - UHFRFIDUnit.TID: tid
            - UHFRFIDUnit.USER: user

    - Parameter `offset` (`int`): offset.
    - Parameter `data` (`str`): data. hexadecimal string.
    - Parameter `access_password` (`str`): access password. hexadecimal string.

#### Impinj Monza

### `UHFRFIDUnit.get_impinj_monza_qt_sr(persistence, password: str = "00000000") -> bool`

    Get Impinj Monza QT_SR.

    - Parameter `persistence` (`int`): persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.set_impinj_monza_qt_sr(qt_sr: bool, persistence: int, password: str = "00000000") -> bool`

    Set Impinj Monza QT_SR.

    - Parameter `qt_sr` (`bool`): QT_SR status.
    - Parameter `persistence` (`int`): persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.get_impinj_monza_qt_mem(persistence, password: str = "00000000") -> bool`

    Set Impinj Monza QT_MEM.

    - Parameter `persistence` (`int`): persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.set_impinj_monza_qt_mem(qt_mem: bool, persistence: int, password: str = "00000000") -> bool`

    Set Impinj Monza QT_MEM.

    - Parameter `qt_mem` (`bool`): QT_MEM status.
    - Parameter `persistence` (`int`): persistence. 0x00 is volatile memory, 0x01 is non-volatile memory.
    - Parameter `password` (`str`): access password. hexadecimal string.

#### NXP

### `UHFRFIDUnit.nxp_eas_alarm() -> str`

    Get NXP EAS alarm code.

### `UHFRFIDUnit.get_nxp_config_word(password: str = "00000000") -> int`

    Get NXP config word.

    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.set_nxp_config_word(config_word: int, password: str = "00000000") -> bool`

    Set NXP config word.

    - Parameter `config_word` (`int`): NXP config word.
    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.nxp_read_protect(set: int, password: str = "00000000") -> bool`

    Set NXP read protect.

    - Parameter `set` (`int`): set read protect. 0x00 is set read protect, 0x01 is reset read protect.
    - Parameter `password` (`str`): access password. hexadecimal string.

### `UHFRFIDUnit.nxp_change_eas(set: int, password: str = "00000000") -> bool`

    Change NXP EAS.

    - Parameter `set` (`int`): set EAS. 0x00 is set EAS, 0x01 is reset EAS.
    - Parameter `password` (`str`): access password. hexadecimal string.
