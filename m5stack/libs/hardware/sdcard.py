# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine, os


def create_sdcard_closure():
    sd = None

    def sdcard(
        slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000
    ):
        nonlocal sd
        try:
            os.umount("/sd")
            sd.deinit()
        except Exception as e:
            print(e)
        finally:
            sd = machine.SDCard(
                slot=slot,
                width=width,
                cd=cd,
                wp=wp,
                sck=sck,
                miso=miso,
                mosi=mosi,
                cs=cs,
                freq=freq,
            )
            sd.info()
            os.mount(sd, "/sd")

    return sdcard


SDCard = create_sdcard_closure()
