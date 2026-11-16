# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time
from chain import ChainBus
from chain import ENVChain


title = None
pressure_caption = None
label_pressure = None
pressure_unit = None
temperature_caption = None
label_temperature = None
temperature_unit = None
humidity_caption = None
label_humidity = None
humidity_unit = None
altitude_caption = None
label_altitude = None
altitude_unit = None
sea_level_caption = None
bus2 = None
chain_env_0 = None


SEA_LEVEL_PRESSURE_PA = None
UPDATE_INTERVAL_MS = None
last_time = None


def setup():
    global \
        title, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        humidity_caption, \
        label_humidity, \
        humidity_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        sea_level_caption, \
        bus2, \
        chain_env_0, \
        SEA_LEVEL_PRESSURE_PA, \
        UPDATE_INTERVAL_MS, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label("Chain ENV", 111, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18)
    pressure_caption = Widgets.Label(
        "Pressure", 12, 44, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_pressure = Widgets.Label(
        "----.-", 12, 62, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    pressure_unit = Widgets.Label(
        "hPa", 170, 84, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    temperature_caption = Widgets.Label(
        "Temperature", 12, 118, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_temperature = Widgets.Label(
        "--.-", 12, 137, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat24
    )
    temperature_unit = Widgets.Label(
        "C", 80, 144, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat18
    )
    humidity_caption = Widgets.Label(
        "Humidity", 170, 118, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_humidity = Widgets.Label(
        "--.-", 170, 137, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat24
    )
    humidity_unit = Widgets.Label(
        "%", 225, 144, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat18
    )
    altitude_caption = Widgets.Label(
        "Altitude", 12, 180, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_altitude = Widgets.Label(
        "----.-", 100, 173, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat24
    )
    altitude_unit = Widgets.Label(
        "m", 200, 180, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat18
    )
    sea_level_caption = Widgets.Label(
        "Sea level / Shenzhen: -- hPa",
        12,
        215,
        1.0,
        0x8FA1AD,
        0x10171D,
        Widgets.FONTS.Montserrat14,
    )

    title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain ENV", Widgets.FONTS.Montserrat18))) / 2)), y=8
    )
    SEA_LEVEL_PRESSURE_PA = 101330
    UPDATE_INTERVAL_MS = 500
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_env_0 = ENVChain(bus2, 1)
    chain_env_0.set_sea_level_pressure(SEA_LEVEL_PRESSURE_PA)
    sea_level_caption.setText(
        str(
            (
                str((str("Sea level / Shenzhen: ") + str((SEA_LEVEL_PRESSURE_PA / 100))))
                + str(" hPa")
            )
        )
    )
    label_pressure.setText(str(round((chain_env_0.read_pressure()) / 100, 1)))
    label_temperature.setText(
        str(round(chain_env_0.read_temperature(sensor=ENVChain.SENSOR_AHT20), 1))
    )
    label_humidity.setText(str(round(chain_env_0.read_humidity(), 1)))
    label_altitude.setText(str(round(chain_env_0.read_altitude(), 1)))
    last_time = time.ticks_ms()


def loop():
    global \
        title, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        humidity_caption, \
        label_humidity, \
        humidity_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        sea_level_caption, \
        bus2, \
        chain_env_0, \
        SEA_LEVEL_PRESSURE_PA, \
        UPDATE_INTERVAL_MS, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_INTERVAL_MS:
        label_pressure.setText(str(round((chain_env_0.read_pressure()) / 100, 1)))
        label_temperature.setText(
            str(round(chain_env_0.read_temperature(sensor=ENVChain.SENSOR_AHT20), 1))
        )
        label_humidity.setText(str(round(chain_env_0.read_humidity(), 1)))
        label_altitude.setText(str(round(chain_env_0.read_altitude(), 1)))
        last_time = time.ticks_ms()
    time.sleep_ms(20)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
