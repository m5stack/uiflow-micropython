# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.sim7028 import SIM7028
from driver.m5ioe1 import M5IOE1, Pin
import sys
import machine
import time
import M5

if sys.platform != "esp32":
    from typing import Literal
    from typing import Optional


class AtomDTUNBIoT2V11(SIM7028):
    """Create an AtomDTUNBIoT2V11 object.

    :param machine.UART uart: The UART object to use.
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |nbiot_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTUNBIoT2V11
            from hardware import UART

            uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=19)
            base_nbiot2v11 = AtomDTUNBIoT2V11(uart2, verbose=False)
    """

    IOE1_VIN_ADC_PIN = 2
    IOE1_SIM_PWR_PIN = 9
    IOE1_SIM_RST_PIN = 11

    _pin_map = {
        M5.BOARD.M5AtomEcho: (21, 25),
        M5.BOARD.M5AtomEchoS3R: (39, 38),
        M5.BOARD.M5Atom: (21, 25),
        M5.BOARD.M5AtomMatrix: (21, 25),
        M5.BOARD.M5AtomS3: (39, 38),
        M5.BOARD.M5AtomS3Lite: (39, 38),
        M5.BOARD.M5AtomS3R: (39, 38),
        M5.BOARD.M5AtomS3R_CAM: (39, 38),
    }

    def __init__(self, uart, verbose=False):
        (scl, sda) = self._pin_map.get(M5.getBoard())
        self._i2c1 = machine.I2C(1, scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        self.m5ioe1 = M5IOE1(self._i2c1, addr=0x6F)
        self.vin_adc_pin = Pin(self.m5ioe1, self.IOE1_VIN_ADC_PIN, Pin.IN)
        self.sim_pwr_pin = Pin(self.m5ioe1, self.IOE1_SIM_PWR_PIN, Pin.OUT)
        self.sim_rst_pin = Pin(self.m5ioe1, self.IOE1_SIM_RST_PIN, Pin.OUT)

        # power on
        self.sim_pwr_pin.on()
        time.sleep(1)

        # reset
        self.sim_rst_pin.off()
        time.sleep(0.1)
        self.sim_rst_pin.on()

        time.sleep(3)

        SIM7028.__init__(self, uart=uart, verbose=verbose)

    def power_on(self):
        """Power on the DTU NB-IoT module.

        UiFlow2 Code Block:

            |nbiot_power_on.png|

        MicroPython Code Block:

            .. code-block:: python

                base_nbiot2v11.power_on()
        """
        self.sim_pwr_pin.on()
        time.sleep(1)
        self.sim_rst_pin.off()
        time.sleep(0.1)
        self.sim_rst_pin.on()

    def power_off(self):
        """Power off the DTU NB-IoT module.

        UiFlow2 Code Block:

            |nbiot_power_off.png|

        MicroPython Code Block:

            .. code-block:: python

                base_nbiot2v11.power_off()
        """
        self.sim_pwr_pin.off()

    def get_voltage(self) -> float:
        """Get the RS485 Port voltage in volts.

        UiFlow2 Code Block:

            |rs485_get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = base_nbiot2v11.get_voltage()
                print("Voltage:", voltage)
        """
        return self.m5ioe1.read_adc_mv(self.IOE1_VIN_ADC_PIN) / 1000.0 / 0.090909
