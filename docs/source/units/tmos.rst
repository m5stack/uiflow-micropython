TMOS Unit
=========

.. include:: ../refs/unit.tmos.ref

The following products are supported:

    |TMOS|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import TMOSUnit
    from hardware import *


    title0 = None
    label0 = None
    title1 = None
    title2 = None
    TMOSTest = None
    label1 = None
    label2 = None
    label3 = None
    i2c0 = None
    tmos_0 = None


    def tmos_0_presence_detect_event(arg):
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
        label1.setText(str((str("Prescence Flag:") + str((tmos_0.get_presence_state())))))
        label0.setText(str((str("Prescence:") + str((tmos_0.get_presence_value())))))


    def tmos_0_motion_detect_event(arg):
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
        label3.setText(str((str("Motion Flag:") + str((tmos_0.get_motion_state())))))
        label2.setText(str((str("Motion:") + str((tmos_0.get_motion_value())))))


    def tmos_0_presence_not_detected_event(arg):
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
        label1.setText(str((str("Prescence Flag:") + str((tmos_0.get_presence_state())))))


    def tmos_0_motion_not_detected_event(arg):
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
        label3.setText(str((str("Motion Flag:") + str((tmos_0.get_motion_state())))))


    def setup():
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0

        M5.begin()
        Widgets.fillScreen(0x222222)
        title0 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
        label0 = Widgets.Label("Prescence:", 2, 65, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
        title1 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
        title2 = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
        TMOSTest = Widgets.Title("Title", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
        label1 = Widgets.Label(
            "Prescence Flag", 2, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
        )
        label2 = Widgets.Label("Motion:", 2, 130, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
        label3 = Widgets.Label("Motion Flag:", 2, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        title0.setText("TMOS Test")
        tmos_0 = TMOSUnit(i2c0, 0x5A)
        tmos_0.set_callback(tmos_0_presence_detect_event, tmos_0.PRESENCE_DETECT)
        tmos_0.set_callback(tmos_0_motion_detect_event, tmos_0.MOTION_DETECT)
        tmos_0.set_callback(tmos_0_presence_not_detected_event, tmos_0.PRESENCE_NOT_DETECTED)
        tmos_0.set_callback(tmos_0_motion_not_detected_event, tmos_0.MOTION_NOT_DETECTED)
        label0.setText(str("Prescence:"))
        label1.setText(str("Prescence Flag:"))
        label2.setText(str("Motion:"))
        label3.setText(str("Motion Flag:"))
        print(tmos_0.get_gain_mode())


    def loop():
        global title0, label0, title1, title2, TMOSTest, label1, label2, label3, i2c0, tmos_0
        M5.update()
        tmos_0.tick_callback()


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



UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |tmos_cores3_example.m5f2|


class TMOSUnit
--------------

Constructors
------------

.. class:: TMOSUnit(i2c0, address)

    Create a TMOSUnit object.

    :param i2c: I2C object

    :param address: I2C address, 0x5A by default

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: TMOSUnit.get_data_ready() -> bool

    Get data update status of TMOSUnit(TAMBIENT, TOBJECT, TAMB_SHOCK, TPRESENCE, TMOTION).

    :return: The data update status of TMOSUnit.

    UIFLOW2:

        |get_data_ready.png|

.. method:: TMOSUnit.get_motion_state() -> bool

    Get the motion status detected by TMOSUnit

    :return: The motion status.

    UIFLOW2:

        |get_motion_state.png|

.. method:: TMOSUnit.get_motion_value() -> int

    Get motion value(unit:cm^-1)

    :return: The motion value of TMOSUnit.

    UIFLOW2:

        |get_motion_value.png|

.. method:: TMOSUnit.get_presence_state() -> bool

    Get the presence status detected by TMOSUnit

    :return: The presence status.

    UIFLOW2:

        |get_presence_state.png|

.. method:: TMOSUnit.get_presence_value() -> int

    Get presence value(unit:cm^-1)

    :return: The presence value of TMOSUnit.

    UIFLOW2:

        |get_presence_value.png|

.. method:: TMOSUnit.get_tamb_shock_state() -> bool

    Get the ambient temperature shock status detected by TMOSUnit

    :return: The ambient temperature shock detection status.

    UIFLOW2:

        |get_tamb_shock_state.png|

.. method:: TMOSUnit.get_tambient_raw_value() -> int

    Get ambient temperature, represents the temperature of the environment in thermal coupling with the sensor.

    :return: The ambient temperature of TMOSUnit.

    UIFLOW2:

        |get_tambient_raw_value.png|

.. method:: TMOSUnit.get_temperature_data() -> float

    Get object temperature, represents the amount of infrared radiation emitted from the objects inside the field of view.

    :return: The object temperature of TMOSUnit.

    UIFLOW2:

        |get_temperature_data.png|

.. method:: TMOSUnit.set_callback(self, handler, trigger: Literal[0, 1, 2, 3, 4, 5])

    Set callback function for different triggers.

    :param handler: The callback function to be set.
    :param trigger: The event trigger to set the handler for:


        - ``ambient temperature``: 0
        - ``motion``: 1
        - ``presence``: 2
        - ``ambient temperature not``: 3
        - ``motion not``: 4
        - ``presence not``: 5

    UIFLOW2:

        |set_callback.png|

.. method:: TMOSUnit.tick_callback(self)

    Check the status of the TMOSUnit and execute the corresponding callback functions based on the event flags.

    This method should be called periodically to poll the sensor status and handle any detected events.

    It checks the following flags and triggers the associated callbacks if the flags are set:

    - ``ambient temperature`` (0): Indicates an ambient temperature shock event.
    - ``motion`` (1): Indicates a motion detection event.
    - ``presence`` (2): Indicates a presence detection event.
    - ``ambient temperature not`` (3): Indicates an ambient temperature shock event has not occurred.
    - ``motion not`` (4): Indicates a motion detection event has not occurred.
    - ``presence not`` (5): Indicates a presence detection event has not occurred.

    The callback functions associated with these events are set using the :meth:`set_callback` method.

    UIFLOW2:

        |tick_callback.png|


.. method:: TMOSUnit.get_gain_mode() -> int

    Get the gain mode configuration of TMOS.

    :return: Gain mode

    UIFLOW2:

        |get_gain_mode.png|

.. method:: TMOSUnit.get_tmos_sensitivity() -> int

    Get the sensitivity configuration of TMOS.

    :return: TMOS sensitivity

    UIFLOW2:

        |get_tmos_sensitivity.png|

.. method:: TMOSUnit.get_motion_threshold() -> int

   Get the motion threshold for motion detection algorithm.

    :return: The motion threshold of TMOSUnit.

    UIFLOW2:

        |get_motion_threshold.png|

.. method:: TMOSUnit.get_motion_hysteresis() -> int

   Get hysteresis value for motion detection algorithm.

    :return: The motion hysteresis of TMOSUnit.

    UIFLOW2:

        |get_motion_hysteresis.png|

.. method:: TMOSUnit.get_presence_threshold() -> int

    Get the presence threshold for presence detection algorithm.

    :return: The presence threshold of TMOSUnit.

    UIFLOW2:

        |get_presence_threshold.png|

.. method:: TMOSUnit.get_presence_hysteresis() -> int

   Get hysteresis value for presence detection algorithm.

    :return: The presence hysteresis of TMOSUnit.

    UIFLOW2:

        |get_presence_hysteresis.png|

.. method:: TMOSUnit.get_tambient_shock_threshold() -> int

   Get the ambient temperature shock threshold for Tambient shock detection algorithm.

    :return: The ambient temperature shock threshold of TMOSUnit.

    UIFLOW2:

        |get_tambient_shock_threshold.png|

.. method:: TMOSUnit.get_tambient_shock_hysteresis() -> int

   Get hysteresis value for ambient temperature shock detection algor.

    :return: The ambient temperature shock hysteresis of TMOSUnit.

    UIFLOW2:

        |get_tambient_shock_hysteresis.png|

.. method:: TMOSUnit.set_gain_mode(val) -> None

    Set the gain mode of TMOS (Note: DEFAULT mode has high sensitivity but easily leads to sensor oversaturation; WIDE mode has short detection distance but can avoid sensor saturation)

    :param int val: Gain mode

        Options:
            - ``GAIN_WIDE_MODE``: 0
            - ``GAIN_DEFAULT_MODE``: 7

    UIFLOW2:

        |set_gain_mode.png|

.. method:: TMOSUnit.set_tmos_sensitivity(val) -> None

    Set the sensitivity of TMOS

    :param int val: Sensitivity(0x00 ~ 0xFF)

    UIFLOW2:

        |set_tmos_sensitivity.png|


.. method:: TMOSUnit.set_motion_threshold(val)

    Set the the motion threshold for motion detection algorithm.

    :param int val: motion threshold(0x0~0x7FFF)

    :return: Is the setting successful?

    UIFLOW2:

        |set_motion_threshold.png|

.. method:: TMOSUnit.set_motion_hysteresis(val)

    Set hysteresis value for motion detection algorithm.

    :param int val: motion hysteresis(0x0~0xFF)

    UIFLOW2:

        |set_motion_hysteresis.png|


.. method:: TMOSUnit.set_presence_threshold(val) -> bool

    Set the presence threshold for presence detection algorithm.

    :param int val: presence threshold(0x0~0x7FFF)

    :return: Is the setting successful?

    UIFLOW2:

        |set_presence_threshold.png|

.. method:: TMOSUnit.set_presence_hysteresis(val)

    Set hysteresis value for presence detection algorithm.

    :param int val: presence hysteresis(0x0~0xFF)

    UIFLOW2:

        |set_presence_hysteresis.png|

.. method:: TMOSUnit.set_tambient_shock_threshold(val) -> bool

    Set ambient temperature shock threshold for Tambient shock detection algorithm.

    :param int val: ambient temperature shock threshold(0x0~0x7FFF)

    :return: Is the setting successful?

    UIFLOW2:

        |set_tambient_shock_threshold.png|

.. method:: TMOSUnit.set_tambient_shock_hysteresis(val)

    Set hysteresis value for ambient temperature shock detection algor.

    :param int val: ambient temperature shock hysteresis(0x0~0xFF)

    UIFLOW2:

        |set_tambient_shock_hysteresis.png|

.. method:: TMOSUnit.is_connected() -> None

    Check whether the TMOSUnit is connected to the device.

.. method:: TMOSUnit.begin() -> None

    Initialize TMOSUnit.

.. method:: TMOSUnit.reset() -> None

    Reset TMOSUnit (includes restarting OTP memory content, resetting algorithms).

.. method:: TMOSUnit.reset_algo() -> None

    Reset the algorithm (this function must be executed when modifying the threshold, hysteresis, absolute value in the selection of the presence detection algorithm, low-pass filter configuration).

.. method:: TMOSUnit.set_lpf_p_bandwidth(val) -> None

    Sets the low pass filter configuration for presence detection.

    :param int val: Configuration values ​​for the low pass filter.

        Options:
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_9``: ODR/9 , 0
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_20``: ODR/20, 1
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_50``: ODR/50, 2
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_100``: ODR/100, 3
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_200``: ODR/200, 4
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_400``: ODR/400, 5
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_800``: ODR/800, 6

.. method:: TMOSUnit.get_lpf_p_bandwidth() -> int

    Gets the low pass filter configuration used for presence detection.

    :return: Low pass filter bandwidth

.. method:: TMOSUnit.set_lpf_a_t_bandwidth(val) -> None

    Sets the low-pass filter configuration for ambient temperature shock detection.

    :param int val: Configuration values ​​for the low pass filter.

        Options:
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_9``: ODR/9 , 0
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_20``: ODR/20, 1
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_50``: ODR/50, 2
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_100``: ODR/100, 3
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_200``: ODR/200, 4
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_400``: ODR/400, 5
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_800``: ODR/800, 6

.. method:: TMOSUnit.get_lpf_a_t_bandwidth() -> int

    Gets the low pass filter configuration for ambient temperature shock detection.

    :return: Low pass filter bandwidth

.. method:: TMOSUnit.set_lpf_p_m_bandwidth(val) -> None

    Sets the low-pass filter configuration for presence and motion detection.

    :param int val: Configuration values ​​for the low pass filter.

        Options:
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_9``: ODR/9 , 0
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_20``: ODR/20, 1
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_50``: ODR/50, 2
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_100``: ODR/100, 3
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_200``: ODR/200, 4
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_400``: ODR/400, 5
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_800``: ODR/800, 6

.. method:: TMOSUnit.get_lpf_p_m_bandwidth() -> int

    Gets the low-pass filter configuration for presence and motion detection.

    :return: Low pass filter bandwidth

.. method:: TMOSUnit.set_lpf_m_bandwidth(val) -> None

    Sets the low-pass filter configuration for motion detection.

    :param int val: Configuration values ​​for the low pass filter.

        Options:
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_9``: ODR/9 , 0
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_20``: ODR/20, 1
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_50``: ODR/50, 2
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_100``: ODR/100, 3
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_200``: ODR/200, 4
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_400``: ODR/400, 5
            - ``TMOSUnit.STHS34PF80_LPF_ODR_DIV_800``: ODR/800, 6

.. method:: TMOSUnit.get_lpf_m_bandwidth() -> int

    Gets the low-pass filter configuration for motion detection.

    :return: Low pass filter bandwidth

.. method:: TMOSUnit.set_avg_tobj_num(val) -> None

    Sets the number of samples to average the object's temperature.

    :param int val: Configuration value for the number of samples to average.

        Options:
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_2``: RMS noise:90 , 0
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_8``: RMS noise:50, 1
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_32``: RMS noise:25, 2
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_128``: RMS noise:20, 3
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_256``: RMS noise:15, 4
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_512``: RMS noise:12, 5
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_1024``: RMS noise:11, 6
            - ``TMOSUnit.STHS34PF80_AVG_TMOS_2048``: RMS noise:10, 7

.. method:: TMOSUnit.get_avg_tobj_num() -> int

    Gets the number of samples to average the ambient temperature.

    :return: Average number of samples of object temperature

.. method:: TMOSUnit.set_avg_tamb_num(val) -> None

    Sets the number of samples to average the ambient temperature.

    :param int val: Configuration value for the number of samples to average.

        Options:
            - ``TMOSUnit.STHS34PF80_AVG_T_8``: 0
            - ``TMOSUnit.STHS34PF80_AVG_T_4``: 1
            - ``TMOSUnit.STHS34PF80_AVG_T_2``: 2
            - ``TMOSUnit.STHS34PF80_AVG_T_1``: 3


.. method:: TMOSUnit.get_avg_tamb_num() -> int

    Get the average number of samples of ambient temperature.

    :return: The number of samples for the average ambient temperature.

.. method:: TMOSUnit.set_tmos_odr(val) -> None

    Set the output data rate of TMOS

    :param int val: TMOS output data rate

        Options:
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_OFF``: ODR frequency(Hz):Power-down mode, 0
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_0Hz25``: ODR frequency(Hz):0.25, 1
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_0Hz50``: ODR frequency(Hz):0.5, 2
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_1Hz``: ODR frequency(Hz):1, 3
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_2Hz``: ODR frequency(Hz):2, 4
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_4Hz``: ODR frequency(Hz):4, 5
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_8Hz``: ODR frequency(Hz):8, 6
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_15Hz``: ODR frequency(Hz):15, 7
            - ``TMOSUnit.STHS34PF80_TMOS_ODR_AT_30Hz``: ODR frequency(Hz):30, 8

.. method:: TMOSUnit.get_tmos_odr() -> int

    Get the output data rate of TMOS

    :return: Output data rate

.. method:: TMOSUnit.set_block_data_update(val) -> None

    Enable/disable object temperature and ambient temperature register data update

    :param bool val: Enable or disable register data update

.. method:: TMOSUnit.get_block_data_update() -> bool

    Get the object temperature and ambient temperature storage data update enable status

    :return: Data register update enable status

.. method:: TMOSUnit.set_tmos_one_shot(val) -> None

    Set the state of one-time data collection

    :param bool val: One-time collection status

.. method:: TMOSUnit.get_tmos_one_shot() -> bool

    Get the status of triggering a one-time collection

    :return: Get the status of triggering a one-time collection

.. method:: TMOSUnit.refresh_state() -> self

    Retrieve the current status of the TMOSUnit, including presence detection, motion detection, and ambient temperature shock detection.

    :return: An instance of the TMOSUnit with updated status flags.

