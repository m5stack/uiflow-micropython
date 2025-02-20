# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class PIDController:
    def __init__(self, kp, ki, kd, setpoint, direction):
        self._kp = abs(kp) * direction
        self._ki = abs(ki) * direction
        self._kd = abs(kd) * direction
        self._setpoint = setpoint
        self._dir = direction  # direction (1 or -1)
        self.output_min = -10000
        self.output_max = 10000
        self.integral_min = -10000
        self.integral_max = 10000
        self.error_integral = 0
        self._last_input = 0

    def compute(self, input_value):
        error = self._setpoint - input_value
        self.error_integral += self._ki * error
        if self.error_integral > self.integral_max:
            self.error_integral = self.integral_max
        elif self.error_integral < self.integral_min:
            self.error_integral = self.integral_min
        dinput = input_value - self._last_input
        output = self._kp * error + self.error_integral - self._kd * dinput
        if output > self.output_max:
            output = self.output_max
        elif output < self.output_min:
            output = self.output_min
        self._last_input = input_value
        return output

    def set_output_limits(self, min_out, max_out):
        self.output_min = min_out
        self.output_max = max_out

    def set_integral_limits(self, min_out, max_out):
        self.integral_min = min_out
        self.integral_max = max_out

    def set_direction(self, direction):
        self._dir = direction
        self._kp = abs(self._kp) * self._dir
        self._ki = abs(self._ki) * self._dir
        self._kd = abs(self._kd) * self._dir

    def set_params(self, kp, ki, kd):
        self._kp = abs(kp) * self._dir
        self._ki = abs(ki) * self._dir
        self._kd = abs(kd) * self._dir
        self.error_integral = 0
        self._last_input = 0

    def set_setpoint(self, setpoint):
        self._setpoint = setpoint
