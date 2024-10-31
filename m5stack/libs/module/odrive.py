# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from micropython import const
import time
import machine

READ_TIMEOUT = 1  # seconds


class ODriveModule:
    """

    note:
        cn: ODrive是M5Stack推出的高性能伺服电机驱动模块，基于开源运动控制解决方案ODrive。
        en: ODrive is a high-performance servo motor drive module launched by M5Stack, based on the open source motion control solution ODrive.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/module/odrive
        image: https://static-cdn.m5stack.com/resource/docs/products/module/odrive/odrive_01.webp
        category: Module

    example: |
        from module import ODriveModule
        drive = ODriveModule(port=(13,5))
        drive.get_vbus_voltage()
        drive.set_velocity(10)
        drive.set_current(5)
        drive.set_control_mode(ODriveModule.CONTROL_MODE_POSITION_CONTROL)
        drive.set_position(1000)


    """

    """
    constant: Axis states
    """
    AXIS_STATE_UNDEFINED = const(0)  # will fall through to idle
    AXIS_STATE_IDLE = const(1)  # disable PWM and do nothing
    AXIS_STATE_STARTUP_SEQUENCE = const(
        2
    )  # the actual sequence is defined by the config.startup_... flags
    AXIS_STATE_FULL_CALIBRATION_SEQUENCE = const(3)  # run all calibration procedures, then idle
    AXIS_STATE_MOTOR_CALIBRATION = const(4)  # run motor calibration
    AXIS_STATE_SENSORLESS_CONTROL = const(5)  # run sensorless control
    AXIS_STATE_ENCODER_INDEX_SEARCH = const(6)  # run encoder index search
    AXIS_STATE_ENCODER_OFFSET_CALIBRATION = const(7)  # run encoder offset calibration
    AXIS_STATE_CLOSED_LOOP_CONTROL = const(8)  # run closed loop control

    """
    constant: Control modes
    """
    CONTROL_MODE_VOLTAGE_CONTROL = const(0)
    CONTROL_MODE_TORQUE_CONTROL = const(1)
    CONTROL_MODE_VELOCITY_CONTROL = const(2)
    CONTROL_MODE_POSITION_CONTROL = const(3)

    def __init__(self, id=1, port=None):
        """
        note:
            en: Initialize the ODriveModule.
            cn: 初始化ODriveModule。
        """
        self.uart = machine.UART(id, tx=port[1], rx=port[0])
        self.uart.init(115200, bits=0, parity=None, stop=1, rxbuf=1024)

    def set_position(self, position, velocity_feedforward=0.0, current_feedforward=0.0):
        """
        note:
            en: Set the target position with optional feedforward values.
            cn: 设置目标位置，并可选地提供前馈值。

        params:
            position:
                note: The target position in counts or radians, depending on the configuration.
            velocity_feedforward:
                note: The feedforward velocity in counts/s or radians/s to assist the controller.
            current_feedforward:
                note: The feedforward current in amperes to assist the controller.
        """
        command = "p 0 {} {} {}\n".format(position, velocity_feedforward, current_feedforward)
        self.uart.write(command)

    def set_velocity(self, velocity, current_feedforward=0.0):
        """
        note:
            en: Set the target velocity with optional current feedforward.
            cn: 设置目标速度，并可选地提供电流前馈值。

        params:
            velocity:
                note: The target velocity in counts/s or radians/s.
            current_feedforward:
                note: The feedforward current in amperes to assist the controller.
        """
        command = "v 0 {} {}\n".format(velocity, current_feedforward)
        self.uart.write(command)

    def set_current(self, current):
        """
        note:
            en: Set the target current.
            cn: 设置目标电流。

        params:
            current:
                note: The target current in amperes for torque control.
        """
        command = "c 0 {}\n".format(current)
        self.uart.write(command)

    def set_gain(self, pos_gain, vel_gain, vel_integrator_gain):
        """
        note:
            en: Set the controller gains for position and velocity control.
            cn: 设置位置和速度控制的控制器增益。

        params:
            pos_gain:
                note: The proportional gain for position control (units: counts or radians).
            vel_gain:
                note: The proportional gain for velocity control (units: A/(counts/s) or A/(rad/s)).
            vel_integrator_gain:
                note: The integral gain for velocity control (units: A/(counts/s * s) or A/(rad/s * s)).
        """
        self.write_config("axis0.controller.config.pos_gain", pos_gain)
        self.write_config("axis0.controller.config.vel_gain", vel_gain)
        self.write_config("axis0.controller.config.vel_integrator_gain", vel_integrator_gain)

    def set_control_mode(self, mode):
        """
        note:
            en: Set the control mode of the controller.
            cn: 设置控制器的控制模式。

        params:
            mode:
                note: The control mode.
                options:
                    Voltage Control: ODriveModule.CONTROL_MODE_VOLTAGE_CONTROL
                    Torque Control: ODriveModule.CONTROL_MODE_TORQUE_CONTROL
                    Velocity Control: ODriveModule.CONTROL_MODE_VELOCITY_CONTROL
                    Position Control: ODriveModule.CONTROL_MODE_POSITION_CONTROL
        """
        self.write_config("axis0.controller.config.control_mode", mode)

    def set_control_input_pos(self, pos):
        """
        note:
            en: Set the control input position for the controller.
            cn: 设置控制器的输入位置。

        params:
            pos:
                note: The desired input position in counts or radians for position control.
        """
        self.write_config("axis0.controller.input_pos", pos)

    def trapezoidal_move(self, position):
        """
        note:
            en: Perform a trapezoidal move to the given position.
            cn: 执行到指定位置的梯形运动。

        params:
            position:
                note: The target position in counts or radians to move to using a trapezoidal velocity profile.
        """
        command = "t 0 {}\n".format(position)
        self.uart.write(command)

    def run_state(self, requested_state, timeout):
        """
        note:
            en: Run the axis to the requested state within a timeout period.
            cn: 在超时时间内将轴运行到请求的状态。

        params:
            requested_state:
                note: The desired axis state to transition to, using the AXIS_STATE_* constants.
                options:
                    Idle: ODriveModule.AXIS_STATE_UNDEFINED
                    Startup: ODriveModule.AXIS_STATE_STARTUP_SEQUENCE
                    Calibration: ODriveModule.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    Motor Calibration: ODriveModule.AXIS_STATE_MOTOR_CALIBRATION
                    Sensorless Control: ODriveModule.AXIS_STATE_SENSORLESS_CONTROL
                    Encoder Index Search: ODriveModule.AXIS_STATE_ENCODER_INDEX_SEARCH
                    Encoder Offset Calibration: ODriveModule.AXIS_STATE_ENCODER_OFFSET_CALIBRATION
                    Closed Loop Control: ODriveModule.AXIS_STATE_CLOSED_LOOP_CONTROL
            timeout:
                note: Timeout in milliseconds to wait for the axis to reach the requested state.
        returns:
            note: True if the axis reached the requested state within the timeout period, False otherwise.
        """
        self.write_config("axis0.requested_state", requested_state)
        time_start = time.ticks_ms()
        state = -1
        state = self.read_config_int("axis0.requested_state")
        while state != requested_state and time.ticks_diff(time.ticks_ms(), time_start) < timeout:
            time.sleep_ms(100)
            state = self.read_config_int("axis0.requested_state")
        return state == requested_state

    def get_velocity(self) -> float:
        """
        note:
            en: Get the estimated velocity of the motor.
            cn: 获取电机的估计速度。
        return:
            note: The estimated velocity in counts/s or radians/s.
        """
        return self.read_config_float("axis0.encoder.vel_estimate")

    def get_vbus_voltage(self) -> float:
        """
        note:
            en: Get the measured bus voltage.
            cn: 获取测量的母线电压。
        return:
            note: The bus voltage in volts.
        """
        return self.read_config_float("vbus_voltage")

    def get_phase_current(self) -> float:
        """
        note:
            en: Get the measured phase current of the motor.
            cn: 获取电机的测量相电流。
        return:
            note: The phase current in amperes.
        """
        return self.read_config_float("axis0.motor.current_control.Iq_measured")

    def get_bus_current(self) -> float:
        """
        note:
            en: Get the bus current drawn by the motor.
            cn: 获取电机消耗的母线电流。
        return:
            note: The bus current in amperes.
        """
        return self.read_config_float("axis0.motor.current_control.Ibus")

    def get_encoder_shadow_count(self) -> int:
        """
        note:
            en: Get the encoder's shadow count, which is an internal counter.
            cn: 获取编码器的影子计数，这是一个内部计数器。
        return:
            note: The shadow count as an integer value.
        """
        return self.read_config_int("axis0.encoder.shadow_count")

    def get_encoder_pos_estimate(self) -> float:
        """
        note:
            en: Get the estimated position from the encoder.
            cn: 获取编码器的估计位置。
        return:
            note: The estimated position in counts or radians.
        """
        return self.read_config_float("axis0.encoder.pos_estimate")

    def get_motor_temp(self) -> float:
        """
        note:
            en: Get the temperature of the motor thermistor.
            cn: 获取电机热敏电阻的温度。
        return:
            note: The motor temperature in degrees Celsius.
        """
        return self.read_config_float("axis0.motor_thermistor.temperature")

    def erase_config(self):
        """
        note:
            en: Erase the current configuration settings.
            cn: 擦除当前的配置设置。
        """
        self.write_to_device("se\n")

    def save_config(self):
        """
        note:
            en: Save the current configuration to non-volatile memory.
            cn: 将当前配置保存到非易失性存储器。
        """
        self.write_to_device("ss\n")

    def reboot(self):
        """
        note:
            en: Reboot the ODrive device.
            cn: 重启ODrive设备。
        """
        self.write_to_device("sr\n")

    def set_default_config(self):
        """
        note:
            en: Set the default configuration parameters.
            cn: 设置默认的配置参数。
        """
        default_config = (
            "w config.brake_resistance 0\n"
            "w config.dc_bus_undervoltage_trip_level 8\n"
            "w config.dc_bus_overvoltage_trip_level 34\n"
            "w config.dc_max_negative_current -5\n"
            "w config.max_regen_current 0\n"
            "w axis0.motor.config.pole_pairs 4\n"
            "w axis0.motor.config.calibration_current 5\n"
            "w axis0.motor.config.resistance_calib_max_voltage 4\n"
            "w axis0.motor.config.motor_type 0\n"
            "w axis0.motor.config.current_lim 5\n"
            "w axis0.motor.config.requested_current_range 20\n"
            "w axis0.encoder.config.mode 0\n"
            "w axis0.encoder.config.use_index 1\n"
            "w axis0.encoder.config.cpr 4000\n"
            "w axis0.controller.config.control_mode 3\n"
            "w axis0.controller.config.vel_limit 65536000\n"
            "w axis0.controller.config.pos_gain 20\n"
            "w axis0.motor_thermistor.config.poly_coefficient_0 551.8902587890625\n"
            "w axis0.motor_thermistor.config.poly_coefficient_1 -753.2103271484375\n"
            "w axis0.motor_thermistor.config.poly_coefficient_2 436.8048095703125\n"
            "w axis0.motor_thermistor.config.poly_coefficient_3 -42.3204460144043\n"
            "w axis0.motor_thermistor.config.temp_limit_lower 75\n"
            "w axis0.motor_thermistor.config.temp_limit_upper 90\n"
            "w axis0.motor_thermistor.config.enabled 1\n"
        )
        self.write_to_device("\n")
        self.write_to_device(default_config)
        self.save_config()

    def check_error(self) -> dict:
        """
        note:
            en: Check for any errors in the system components.
            cn: 检查系统组件中的任何错误。
        returns:
            note: A dictionary containing error codes for 'axis', 'motor_thermistor', 'encoder', and 'controller'. Zero indicates no error.
        """
        errors = {
            "axis": self.read_config_int("axis0.error"),
            "motor_thermistor": self.read_config_int("axis0.motor_thermistor.error"),
            "encoder": self.read_config_int("axis0.encoder.error"),
            "controller": self.read_config_int("axis0.controller.error"),
        }
        return errors

    def read_flush(self):
        """
        note:
            en: Flush the UART read buffer to clear any residual data.
            cn: 清空UART读取缓冲区，清除任何残留数据。
        """
        while self.uart.any():
            self.uart.read(1)

    def read_string(self) -> str:
        """
        note:
            en: Read a string terminated by a newline character from the device.
            cn: 从设备读取以换行符结尾的字符串。
        return:
            note: The string read from the device, excluding the newline character.
        """
        str_buffer = b""
        timeout_start = time.ticks_ms()
        while True:
            if self.uart.any():
                c = self.uart.read(1)
                if c == b"\n":
                    break
                str_buffer += c
            else:
                if time.ticks_diff(time.ticks_ms(), timeout_start) >= READ_TIMEOUT * 1000:
                    break
        return str_buffer.decode("utf-8")

    def read_float(self) -> float:
        """
        note:
            en: Read a floating-point value from the device.
            cn: 从设备读取浮点值。
        return:
            note: The float value read from the device; returns 0.0 if parsing fails.
        """
        response = self.read_string()
        try:
            return float(response)
        except ValueError:
            return 0.0

    def read_int(self) -> int:
        """
        note:
            en: Read an integer value from the device.
            cn: 从设备读取整数值。
        return:
            note: The integer value read from the device; returns 0 if parsing fails.
        """
        response = self.read_string()
        try:
            return int(response)
        except ValueError:
            return 0

    def write_to_device(self, data):
        """
        note:
            en: Write a command string to the device via UART.
            cn: 通过UART将命令字符串写入设备。

        params:
            data:
                note: The command string to send to the device, ending with a newline character.
        """
        if data:
            self.uart.write(data)

    def write_config(self, config, value):
        """
        note:
            en: Write a configuration parameter to the device.
            cn: 将配置参数写入设备。

        params:
            config:
                note: The configuration key as a string, e.g., 'axis0.controller.config.pos_gain'.
            value:
                note: The value to set for the configuration parameter; can be a float or integer.
        """
        command = "w {} {}\n".format(config, value)
        self.write_to_device(command)

    def read_config_int(self, config) -> int:
        """
        note:
            en: Read an integer configuration parameter from the device.
            cn: 从设备读取整数配置参数。

        params:
            config:
                note: The configuration key as a string, e.g., 'axis0.encoder.error'.
        return:
            note: The integer value of the specified configuration parameter; returns 0 if parsing fails.
        """
        self.read_flush()
        command = "r {}\n".format(config)
        self.write_to_device(command)
        return self.read_int()

    def read_config_float(self, config) -> float:
        """
        note:
            en: Read a floating-point configuration parameter from the device.
            cn: 从设备读取浮点配置参数。

        params:
            config:
                note: The configuration key as a string, e.g., 'axis0.motor_thermistor.temperature'.
        return:
            note: The float value of the specified configuration parameter; returns 0.0 if parsing fails.
        """
        self.read_flush()
        command = "r {}\n".format(config)
        self.write_to_device(command)
        return self.read_float()
