#############
Chain Captain
#############

.. include:: ../refs/controllers.chain_captain.ref

Support the following products:

    |Chain Captain|

.. NOTE::
   Chain Captain has a 240 x 240 display and three physical buttons. Its UI
   supports **M5.Lcd** and **M5.Widgets**. **M5UI** is not supported.

UiFlow2 Example
---------------

Button Counter
^^^^^^^^^^^^^^

Open the |chain_captain_button_example.m5f2| project in UiFlow2.

This example registers click callbacks for all three physical buttons. Press
**BtnA**, **BtnB**, or **BtnC** to increment the corresponding counter on the
display. Each event is also written to the serial console.

UiFlow2 Code Block:

    |chain_captain_button_example.png|

Example output:

    The display shows independent counters for BtnA, BtnB, and BtnC.

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |chain_captain_audio_example.m5f2| project in UiFlow2.

This example configures the recorder for 8 kHz, 16-bit audio and stores a
five-second recording as ``/flash/res/audio/test.amr``. Press **BtnA** to start
recording. The display shows a countdown, and playback starts automatically
when recording finishes.

UiFlow2 Code Block:

    |chain_captain_audio_example.png|

Example output:

    The display changes between Stop, Recording, countdown, and Playing states.

IMU and Magnetometer
^^^^^^^^^^^^^^^^^^^^

Open the |chain_captain_imu_example.m5f2| project in UiFlow2.

This example reads the accelerometer, gyroscope, and magnetometer every 100 ms.
It converts acceleration to ``m/s^2`` and displays the X, Y, and Z values for
all three sensors.

UiFlow2 Code Block:

    |chain_captain_imu_example.png|

Example output:

    The display shows live Acc, Gyro, and Mag readings on the 240 x 240 screen.

Infrared Transmission and Reception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |chain_captain_ir_rx_tx_example.m5f2| project in UiFlow2.

This example receives infrared frames continuously and displays the received
address, data, and frame count. Press **BtnA** to increment the transmit data
value and send it using address ``8``. A short speaker tone confirms startup
and each received frame.

UiFlow2 Code Block:

    |chain_captain_ir_rx_tx_example.png|

Example output:

    The display shows the current TX address/data and the latest RX values.

Power Management
^^^^^^^^^^^^^^^^

Open the |chain_captain_power_example.m5f2| project in UiFlow2.

This example updates USB, battery, and external-output voltage once per second.
The battery value is green while charging, and the output state is shown as
ON or OFF.

* **BtnA** enables or disables the external 5 V output.
* **BtnB** enables or disables battery charging.

UiFlow2 Code Block:

    |chain_captain_power_example.png|

Example output:

    The display shows USB, battery, and output voltage together with charging
    and output state.

Speaker Tone
^^^^^^^^^^^^

Open the |chain_captain_speaker_example.m5f2| project in UiFlow2.

This example starts at 600 Hz with speaker volume set to 90 percent. Press
**BtnA** to play the current frequency for 200 ms. A new random frequency from
600 Hz to 1600 Hz is then selected and displayed for the next press.

UiFlow2 Code Block:

    |chain_captain_speaker_example.png|

Example output:

    The display shows the frequency that will be played on the next BtnA click.

MicroPython Example
-------------------

Button Counter
^^^^^^^^^^^^^^

This example registers click callbacks for BtnA, BtnB, and BtnC and maintains
an independent display counter for each button.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_button_example.py
        :language: python
        :linenos:

Example output:

    The display shows independent counters for all three buttons.

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example records five seconds of 8 kHz, 16-bit audio to
``/flash/res/audio/test.amr`` and automatically plays the file when recording
finishes. Press BtnA to start recording.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_audio_example.py
        :language: python
        :linenos:

Example output:

    The display shows the recording countdown and playback state.

IMU and Magnetometer
^^^^^^^^^^^^^^^^^^^^

This example reads accelerometer, gyroscope, and magnetometer data every
100 ms and updates the nine displayed axis values in place.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_imu_example.py
        :language: python
        :linenos:

Example output:

    The display shows live acceleration, angular velocity, and magnetic field
    values for the X, Y, and Z axes.

Infrared Transmission and Reception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example registers an infrared receive callback and tracks received
address, data, and frame count. Press BtnA to increment and send the transmit
data value using address ``8``.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_ir_rx_tx_example.py
        :language: python
        :linenos:

Example output:

    The display shows live TX and RX values, and the speaker confirms received
    frames with a short tone.

Power Management
^^^^^^^^^^^^^^^^

This example monitors USB, battery, and external-output voltage. BtnA toggles
the external 5 V output, while BtnB toggles battery charging.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_power_example.py
        :language: python
        :linenos:

Example output:

    The display shows voltage, charging state, and external-output state.

Speaker Tone
^^^^^^^^^^^^

This example plays a 200 ms speaker tone when BtnA is clicked, then selects and
displays a new random frequency between 600 Hz and 1600 Hz.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/chaincaptain/chain_captain_speaker_example.py
        :language: python
        :linenos:

Example output:

    The display shows the next tone frequency.
