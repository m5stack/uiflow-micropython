# Cardputer Adv

Support the following products:

    Cardputer Adv

Cardputer Adv provides a built-in I2C keyboard controller. In UiFlow2
MicroPython, use `MatrixKeyboard` as the high-level keyboard interface. It
automatically selects the correct keyboard backend for Cardputer and Cardputer
Adv.

## MicroPython Example

#### polling keyboard input

This example reads one key event at a time. `get_key()` and `get_string()`
both consume a pending key event, so use one of them for each read.

```python
import time
from hardware import MatrixKeyboard

kb = MatrixKeyboard()

while True:
    if kb.is_pressed():
        text = kb.get_string()
        print(text)
    time.sleep_ms(20)
```
#### callback keyboard input

This example registers a callback and then reads the pending key code from the
`MatrixKeyboard` instance.

```python
import time
from hardware import MatrixKeyboard

kb = MatrixKeyboard()

def key_event(_):
    key = kb.get_key()
    if key is not None:
        print(key, chr(key))

kb.set_callback(key_event)

while True:
    time.sleep_ms(20)
```
## **API**

#### MatrixKeyboard

### `class MatrixKeyboard()`

    Create the built-in keyboard interface for the current host. On Cardputer
    Adv, the keyboard is connected through the internal I2C keyboard controller.

### `MatrixKeyboard.get_key() -> int | None`

    Return the next pressed key code, or `None` when no key event is pending.

    Printable keys return ASCII key codes. Use this method for non-printable
    keys and navigation keys.

### `MatrixKeyboard.get_string() -> str | None`

    Return the next pressed key as a one-character string, or `None` when no
    key event is pending.

    This method converts the value returned by `get_key()` with `chr()`.
    Use `get_key()` instead when the key code is more useful than a string.

### `MatrixKeyboard.is_pressed() -> bool`

    Return `True` when at least one key event is waiting to be read.

### `MatrixKeyboard.is_key_pressed(keycode: int) -> bool`

    Return `True` when the specified key code is currently pressed.

    On Cardputer Adv, `FN` + ```` reports `ESC`` and can be checked with
    `0x1B`.

### `MatrixKeyboard.set_callback(handler) -> None`

    Register a callback for key press events.

    The callback receives the active keyboard object as its only argument. For
    portable Cardputer and Cardputer Adv code, read the pending event from your
    `MatrixKeyboard` instance inside the callback.

### `MatrixKeyboard.tick() -> None`

    Update the scanned keyboard state.

    Cardputer Adv receives key events from the I2C keyboard controller, so this
    method is not required for polling on Cardputer Adv. It can remain in shared
    Cardputer/Cardputer Adv loops.

### `MatrixKeyboard.deinit() -> None`

    Release the keyboard resources and clear pending key events.
