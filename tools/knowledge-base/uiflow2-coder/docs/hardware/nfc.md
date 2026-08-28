# NFC

The `NFC` class controls the onboard ST25R3916 NFC reader. It selects the I2C
bus, pins, and frequency for the detected controller automatically and supports
ISO14443 Type A tag detection, MIFARE Classic block access, and Type 2 page
access.

The following controllers provide an onboard NFC reader:

     Controller                        NFC     |
     PaperMono                         S     |
    | `StackChan <stackchan-nfc>`  S

## MicroPython Example

#### Detect a tag

This example detects a tag and prints its UID and resolved type name.

```python
from hardware import NFC

nfc = NFC()
card = nfc.detect()
if card:
    print(card.uid_str, card.type_name)
```
## API

#### NFC

### `class hardware.NFC()`

    Create an NFC reader for the onboard ST25R3916. The reader selects the
    controller's onboard NFC I2C bus, pins, and frequency; no bus or pin
    configuration is required.

    Except for initialization, this class provides the same reader API as
    `unit.nfc.NFCUnit`, which documents the shared methods and returned
    `driver.nfc.Card` object.
