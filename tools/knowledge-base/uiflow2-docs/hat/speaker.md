# Speaker Hat

<!-- .. sku: U055 -->

<!-- .. include:: ../refs/hat.speaker.ref -->

The following products are supported:

    |Speaker Hat|

Below is the detailed support for Speaker on the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | Speaker Hat       |

###### | CoreInk         | |S|               |

###### | StickC          | |S|               |

###### | StickC PLUS     | |S|               |

###### | StickC PLUS2    | |S|               |

<!-- .. |S| unicode:: U+2705 -->
<!-- .. |N| unicode:: U+274C -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import SpeakerHat

hat_spk_0 = None

def setup():
    global hat_spk_0

    M5.begin()
    hat_spk_0 = SpeakerHat((26, 0))
    hat_spk_0.setVolumePercentage(1)
    hat_spk_0.tone(2000, 100)
    hat_spk_0.playWavFile("/flash/res/audio/poweron_2_5s.wav")

def loop():
    global hat_spk_0
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

    |stickc_plus2_speaker_example.m5f2|

    :download:`poweron_2_5s.wav <../../../examples/hardware/speaker/poweron_2_5s.wav>`

## class SpeakerHat

## Constructors

<!-- .. class:: SpeakerHat(*args, **kwargs) -->

    Create an SpeakerHat object.

    UIFLOW2:

    SpeakerHat class inherits M5.Speaker class, See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details.
