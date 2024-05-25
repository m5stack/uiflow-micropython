Glass2 Unit
===========

.. include:: ../refs/unit.glass2.ref


Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309
driver solution. It supports the I2C communication interface
(default address 0x3C) and has a built-in solder pad that allows changing the
communication address to 0x3D. It is suitable for home products and control
devices, and can be used for information display, status indicators, or user
interfaces, embedded into various home products or control devices to achieve
interaction with users.


Glass2 Unit has a glass area of 42x27.16mm, with a display area of 35.5x18mm
and a resolution of 128x64 pixels. It features 256-level brightness control,
allowing users to see the display content clearly with rich details and sharp
images. The excellent brightness and contrast ensure clear and readable display
effects in various lighting environments.


Glass2 Unit is compatible with M5Stack's development platform and rich product
ecosystem, allowing users to unleash their creativity and develop various
applications and functions. Whether it's developing small games, creating
personalized information display interfaces, or connecting with other M5Stack
devices, the Glass2 Unit provides strong support and endless possibilities.


Compared to Glass Unit, the Glass2 Unit does not include an STM32 MCU.
By changing the I2C address through the onboard solder pad, it can only control
two Glass2 Units simultaneously. If you need to control multiple Glass Units
simultaneously in a project, you will need to connect them using the PaHUB2
Unit. Additionally, by eliminating the intermediate processing step of the
STM32 MCU, the Glass2 Unit improves refresh efficiency, enabling faster content
updates or response to input signals, as well as providing smoother and more
fluid image or animation displays.


Supported products:

    |Glass2Unit|


Micropython example::

    import M5
    display = M5.addDisplay({"unit_glass2":{"enabled":True, "pin_scl": 33, "pin_sda": 32, "i2c_addr": 0x3C, "i2c_freq": 400000}}) # Add Glass unit
    display.clear(0xffffff) # Clear screen
