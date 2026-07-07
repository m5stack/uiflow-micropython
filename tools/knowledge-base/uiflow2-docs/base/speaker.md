# Atomic Speaker Base

<!-- .. sku: A098 -->

<!-- .. include:: ../refs/base.speaker.ref -->

The following products are supported:

    |Atomic Speaker Base|

Below is the detailed support for Speaker on the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | NS4168  | SDCard  |

###### | Atom Echo       | |O|     | |O|     |

###### | Atom Lite       | |S|     | |S|     |

###### | Atom Matrix     | |O|     | |S|     |

###### | AtomS3          | |O|     | |S|     |

###### | AtomS3 Lite     | |S|     | |S|     |

###### | AtomS3R         | |S|     | |S|     |

###### | AtomS3R-CAM     | |S|     | |S|     |

###### | AtomS3R-Ext     | |S|     | |S|     |

<!-- .. |S| unicode:: U+2705 -->
<!-- .. |O| unicode:: U+2B55 -->

|S|: Supported.

|O|: Optional, It conflicts with some internal resource of the host.

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import SpeakerBase
from hardware import sdcard

base_spk = None

def setup():
    global base_spk

    M5.begin()
    base_spk = SpeakerBase(1, 5, 39, 38)
    sdcard.SDCard(slot=3, width=1, sck=7, miso=8, mosi=6, cs=None, freq=20000000)
    base_spk.playWavFile("/flash/res/audio/66.wav")
    base_spk.playWavFile("/sd/66.wav")

def loop():
    global base_spk
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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |atoms3_speaker_example.m5f2|

## class SpeakerBase

## Constructors

<!-- .. class:: SpeakerBase(_id, sck, ws, sd) -->

    Create an SpeakerBase object.

    :param int _id: The I2S port number.
    :param int sck: The I2S SCK pin.
    :param int ws: The I2S WS pin.
    :param int sd: The I2S DI pin.

    UIFLOW2:

    Micropython::

        from base import SpeakerBase

        # atoms3 lite / atoms3 / atoms3r / atoms3r-cam / atoms3-ext
        spk = SpeakerBase(1, 5, 39, 38)

        # atom lite / atom matrix / atom echo
        spk = SpeakerBase(1, 22, 21, 25)

    SpeakerBase class inherits M5.Speaker class, See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details.

## class SDCard

## Constructors

<!-- .. class:: SDCard(slot=2, width=1, sck=None, miso=None, mosi=None, cs=None, freq=20000000) -->

    Create an SDCard object.

    :param int slot: The slot number of the SD card. Default is 2.
    :param int width: width selects the bus width for the SD/MMC interface.
    :param int sck: sck can be used to specify an SPI clock pin.
    :param int miso: miso can be used to specify an SPI miso pin.
    :param int mosi: mosi can be used to specify an SPI mosi pin.
    :param int cs: cs can be used to specify an SPI chip select pin.
    :param int freq: freq selects the SD/MMC interface frequency in Hz.

    UIFLOW2:

    Micropython::

        from hardware import sdcard

        # atoms lite / atom martrix / atom echo: SPI2
        sd = sdcard.SDCard(slot=3, width=1, sck=23, miso=33, mosi=19, cs=None, freq=20000000)

        # atoms3 / atoms3 lite / atoms3r / atoms3r-cam / atoms3-ext: SPI2
        sd = SDCard(slot=3, width=1, sck=7, miso=8, mosi=6, cs=None, freq=20000000)
