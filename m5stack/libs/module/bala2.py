# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from micropython import const
from module.mbus import i2c1
import pid
import attitude_estimator
from driver import mpu6886
import machine


REG_MTR1_CTRL = const(0x00)  # motor 1 control register
REG_MTR2_CTRL = const(0x02)  # motor 2 control register
REG_ENCODER1 = const(0x10)  # recoder 1 register
REG_ENCODER2 = const(0x14)  # recoder 2 register
REG_SERVO_ANGLE = const(0x20)  # servo angle control register
REG_SERVO_PULSE = const(0x30)  # servo pulse control register


class Bala2Module:
    """Create an Bala2Module object.

    :param int timer_id: The Timer ID. Range: 0~3. Default is 0.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import Bala2Module

            module_bala2_0 = Bala2Module(timer_id = 0)
    """

    def __init__(self, timer_id: int = 0):
        self.i2c = i2c1
        self.bala2_addr = const(0x3A)
        # imu
        if 0x68 not in self.i2c.scan():
            raise RuntimeError("MPU6886 not found")
        self.sensor = mpu6886.MPU6886(
            self.i2c,
            accel_fs=mpu6886.ACCEL_FS_SEL_4G,
            gyro_fs=mpu6886.GYRO_FS_SEL_1000DPS,
            gyro_sf=mpu6886.SF_DEG_S,
        )
        self.imu = attitude_estimator.AttitudeEstimator()
        # PID controller
        self.pid_angle_kp = 30
        self.pid_angle_ki = 0
        self.pid_angle_kd = 108
        self.pid_angle_target = 0
        self.pid_speed_kp = 36
        self.pid_speed_ki = 0.18
        self.pid_speed_kd = 0
        self.pid_speed_target = 0
        self.pid_angle = pid.PIDController(
            kp=self.pid_angle_kp,
            ki=self.pid_angle_ki,
            kd=self.pid_angle_kd,
            setpoint=self.pid_angle_target,
            direction=1,
        )
        self.pid_angle.set_output_limits(-1023, 1023)
        self.pid_speed = pid.PIDController(
            kp=self.pid_speed_kp,
            ki=self.pid_speed_ki,
            kd=self.pid_speed_kd,
            setpoint=self.pid_speed_target,
            direction=-1,
        )
        self.pid_speed.set_integral_limits(-80, 80)
        self.pid_speed.set_output_limits(-1023, 1023)
        # others
        self.timer = machine.Timer(timer_id)
        self.dt = 0.01
        self.motor_speed = 0
        self.prev_enc = 0
        self.stop()
        self.angle = 0
        self.turn_speed = 0  # left and right motor speed offset
        self.start_cnt = 0

    def _limit_value(self, val, min_val, max_val) -> float:
        return max(min_val, min(max_val, val))

    def _map(self, x, in_min, in_max, out_min, out_max) -> float:
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def calibrate(self) -> None:
        """Calibrate sensor

        UiFlow2 Code Block:

            |calibrate.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.calibrate()
        """
        self.imu.calibrate_gyro(self.sensor.gyro)

    def set_motor_speed(self, left: int, right: int) -> None:
        """Set motor speed.

        :param int left: The speed of the left motor. Range: -1023 ~ 1023.
        :param int right: The speed of the right motor. Range: -1023 ~ 1023.

        UiFlow2 Code Block:

            |set_motor_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_motor_speed(left, right)
        """
        left_speed = self._limit_value(left, -1023, 1023)
        right_speed = self._limit_value(right, -1023, 1023)
        buf = struct.pack(">hh", int(-left_speed), int(-right_speed))
        self.i2c.writeto_mem(self.bala2_addr, REG_MTR1_CTRL, buf)

    def set_encoder_value(self, left: int, right: int) -> None:
        """Set encoder value.

        :param int left: The value of the left encoder. Range: -2^31 ~ 2^31.
        :param int right: The value of the right encoder. Range: -2^31 ~ 2^31.

        UiFlow2 Code Block:

            |set_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_encoder_value(left, right)
        """
        buf = struct.pack(">ii", left, right)
        self.i2c.writeto_mem(self.bala2_addr, REG_ENCODER1, buf)

    def get_encoder_value(self) -> tuple[int, int]:
        """The left, right encoder value returned in a 2-tuple

        :returns: left, right encoder value
        :rtype: tuple[int, int]

        The encoder count increases when rotating forward and decreases when rotating backward.
        A full rotation results in a value change of 420.

        UiFlow2 Code Block:

            |get_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_encoder_value()
        """
        buf = bytearray(8)
        self.i2c.readfrom_mem_into(self.bala2_addr, REG_ENCODER1, buf)
        tmp = struct.unpack(">ii", buf)
        return tmp[0], tmp[1]

    def set_servo_angle(self, pos: int, angle: int) -> None:
        """Set servo angle.

        :param int pos: The position of the output cahnnel. Range: 1 ~ 4.
        :param int angle: The value of the right encoder. Range: 0 ~ 180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_servo_angle(pos, angle)
        """
        pulse = self._map(angle, 0, 180, 500, 2500)
        self.set_servo_pulse(pos, pulse)

    def set_servo_pulse(self, pos: int, width: int) -> None:
        """Set pulse width for PWM signal.

        :param int pos: The position of the output cahnnel. Range: 1 ~ 4.
        :param int width: The value of the PWM signal witdh. Range: 500 ~ 2500, corresponds to 0.5ms ~ 2.5ms.

        The PWM frequency is fixed at 50Hz, with a period of 20ms.

        UiFlow2 Code Block:

            |set_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_servo_pulse(pos, width)
        """
        buf = struct.pack(">H", width)
        pos = self._limit_value(pos, 1, 8)
        pos = (pos - 1) << 1
        self.i2c.writeto_mem(self.bala2_addr, REG_SERVO_PULSE + pos, buf)

    def _balance_task(self, n) -> None:
        """
        get angle
        """
        accel_x, accel_y, accel_z = self.sensor.acceleration()  # m/s^2
        gyro_x, gyro_y, gyro_z = self.sensor.gyro()  # °/s
        self.imu.update_attitude(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, self.dt)
        self.angle = self.imu.get_angles()[0]

        """
         angle pid control
        """
        pid_angle_out = self.pid_angle.compute(self.angle)

        """
         read motor encoder 
        """
        enc1, enc2 = self.get_encoder_value()
        enc = enc1 + enc2
        self.motor_speed = 0.8 * self.motor_speed + 0.2 * (enc - self.prev_enc)  # speed filter
        self.prev_enc = enc

        """
         speed pid control
        """
        pid_speed_out = self.pid_speed.compute(self.motor_speed)

        """
         wait for the car to stabilize after startup
        """
        if self.start_cnt < 100:
            self.start_cnt += 1
            return

        """
         set motor speed
        """
        if self.angle > -65 and self.angle < 65:
            self.set_motor_speed(
                int(pid_angle_out + pid_speed_out + self.turn_speed),
                int(pid_angle_out + pid_speed_out - self.turn_speed),
            )
        else:
            self.set_motor_speed(0, 0)

    def start(self) -> None:
        """Start the balance control task.

        UiFlow2 Code Block:

            |start.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.start()
        """
        self.timer.init(
            period=int(self.dt * 1000), mode=machine.Timer.PERIODIC, callback=self._balance_task
        )

    def stop(self) -> None:
        """Stop the balance control task.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.stop()
        """
        self.set_motor_speed(0, 0)
        self.timer.deinit()
        self.start_cnt = 0
        self.motor_speed = 0
        self.prev_enc = 0

    def get_angle(self) -> float:
        """The angle of the car.

        :returns: The angle of the car
        :rtype: int

        UiFlow2 Code Block:

            |get_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle()
        """
        return self.angle

    def set_angle_pid(self, kp: float, ki: float, kd: float) -> None:
        """Set angle loop PID parameters.

        :param float kp: Proportional gain
        :param float ki: Integral gain
        :param float kd: Derivative gain

        UiFlow2 Code Block:

            |set_angle_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_angle_pid(kp, ki, kd)
        """
        self.pid_angle_kp, self.pid_angle_ki, self.pid_angle_kd = kp, ki, kd

    def get_angle_pid(self) -> tuple[float, float, float]:
        """The angle loop PID parameters returned in a 3-tuple

        :returns: kp, ki, kd parameters
        :rtype: tuple[float, float, float]

        UiFlow2 Code Block:

            |get_angle_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle_pid()
        """
        return self.pid_angle_kp, self.pid_angle_ki, self.pid_angle_kd

    def set_angle_pid_target(self, angle: float = 0) -> None:
        """Set angle loop PID control target.

        :param float angle: The angle of the angle loop PID control target. Default is 0.

        UiFlow2 Code Block:

            |set_angle_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_angle_pid_target(angle)
        """
        self.pid_angle_target = angle
        self.pid_angle.set_setpoint(self.pid_angle_target)

    def get_angle_pid_target(self) -> float:
        """Get angle loop PID control target

        :returns: The angle loop PID control target
        :rtype: float

        UiFlow2 Code Block:

            |get_angle_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle_pid_target()
        """
        return self.pid_angle_target

    def set_speed_pid(self, kp: float, ki: float, kd: float) -> None:
        """Set speed loop PID parameters.

        :param float kp: Proportional gain
        :param float ki: Integral gain
        :param float kd: Derivative gain

        UiFlow2 Code Block:

            |set_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_speed_pid(kp, ki, kd)
        """
        self.pid_speed_kp, self.pid_speed_ki, self.pid_speed_kd = kp, ki, kd

    def get_speed_pid(self) -> tuple[float, float, float]:
        """The speed loop PID parameters returned in a 3-tuple

        :returns: kp, ki, kd parameters
        :rtype: tuple[float, float, float]

        UiFlow2 Code Block:

            |get_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_speed_pid()
        """
        return self.pid_speed_kp, self.pid_speed_ki, self.pid_speed_kd

    def set_speed_pid_target(self, speed: float = 0) -> None:
        """Set speed loop PID control target.

        :param float speed: The speed of the speed loop PID control target. Default is 0.

        UiFlow2 Code Block:

            |set_speed_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_speed_pid_target(speed)
        """
        self.pid_speed_target = speed
        self.pid_speed.set_setpoint(self.pid_speed_target)

    def get_speed_pid_target(self) -> float:
        """Get speed loop PID control target

        :returns: The speed loop PID control target
        :rtype: float

        UiFlow2 Code Block:

            |get_speed_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_speed_pid_target()
        """
        return self.pid_speed_target

    def set_turn_speed(self, speed: float) -> None:
        """Set turn speed.

        :param float speed: The speed of the left and right motor offset

        UiFlow2 Code Block:

            |set_turn_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_turn_speed(speed)
        """
        self.turn_speed = speed
