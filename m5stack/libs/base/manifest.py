# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
package(
    "base",
    (
        "__init__.py",
        "atom_can.py",
        "atom_gps.py",
        "atom_socket.py",
        "display.py",
        "dtu_lorawan.py",
        "echo.py",
        "hdriver.py",
        "motion.py",
        "pwm.py",
        "rs232.py",
        "speaker.py",
        "stepmotor.py",
    ),
    base_path="..",
    opt=3,
)
