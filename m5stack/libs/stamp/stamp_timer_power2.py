# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.m5pm1 import EVENT as _EVENT, M5PM1


class StampTimerPower2(M5PM1):
    """Configurable Stamp Timer Power 2 interface.

    The board wiring is intentionally supplied by the caller. This keeps
    the interface usable across board revisions and test fixtures without
    baking a board-specific I2C bus or GPIO mapping into the driver.

    ``EVENT`` exposes the event filters accepted by ``add_event_cb()``.
    Use ``StampTimerPower2.EVENT.GPIO4_CHANGE`` for a GPIO4 input event.
    Event callbacks require both ``pm1_int_gpio`` and ``mcu_int_gpio``;
    ordinary I2C access leaves both interrupt pins unconfigured.
    """

    # Event filters shared with the underlying driver; no duplicated values.
    EVENT = _EVENT

    def __init__(
        self,
        i2c,
        *,
        pm1_int_gpio=-1,
        mcu_int_gpio=-1,
    ):
        super().__init__(
            i2c,
            pm1_int_gpio=pm1_int_gpio,
            mcu_int_gpio=mcu_int_gpio,
        )
