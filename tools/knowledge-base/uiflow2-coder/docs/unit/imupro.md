# IMU Pro Unit

The `IMU Pro Unit` is a versatile and integrated inertial motion unit. It incorporates advanced six-axis attitude sensors (BMI270), a three-axis geomagnetic sensor (BMM150), and an atmospheric pressure sensor (BMP280) to provide comprehensive measurement and detection capabilities for users. Whether it is measuring acceleration and angular velocity, detecting the direction and intensity of the geomagnetic field, or measuring atmospheric pressure.

Support the following products:

    IMUProUnit

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import IMUProUnit
import time

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
imupro_0 = IMUProUnit(i2c0)

while True:
    print((str('Acc:') + str((imupro_0.get_accelerometer()))))
    print((str('Gryo:') + str((imupro_0.get_gyroscope()))))
    print((str('Magneto:') + str((imupro_0.get_magnetometer()))))
    print((str('Compass:') + str((imupro_0.get_compass()))))
    print((str('Attitude') + str((imupro_0.get_attitude()))))
    print((str('Temperature') + str((imupro_0.get_temperature()))))
    print((str('Pressure:') + str((imupro_0.get_pressure()))))
    time.sleep_ms(100)
```

## class IMUProUnit

## Constructors

### `class IMUProUnit(i2c)`

    Create a IMUProUnit object

    - Parameter `i2c`: the I2C object.

## Methods

### `IMUProUnit.get_accelerometer()`

    Get the tuple of x, y, and z values of the accelerometer and acceleration vector in gravity units (9.81m/s^2).

    - Return: `tuple`:  (float, float, float)

### `IMUProUnit.get_gyroscope()`

    Get the tuple of x, y, and z values of the gyroscope and gyroscope vector in rad/sec.

    - Return: `tuple`:  (float, float, float)

### `IMUProUnit.get_magnetometer()`

    Get the tuple of x, y, and z values of the magnetometer and magnetometer vector in uT.

    - Return: `tuple`:  (float, float, float)

### `IMUProUnit.get_compass()`

    Get the compass heading value is in range of 0º ~ 360º.

    - Return: `float`:  0 ~ 360

### `IMUProUnit.get_attitude()`

    Get the attitude angles as yaw, pitch, and roll in degrees.

    - Return: `tuple`:  (float, float, float)

### `IMUProUnit.get_temperature()`

    Get the temperature value in degrees celsius from the BMP280 sensor.

    - Return: `float`:  -40 ~ +85 °C

### `IMUProUnit.get_pressure()`

    Get the pressure value in pascals from the BMP280 sensor.

    - Return: `float`:  300 ~ 1100 hPa

### `IMUProUnit.set_accel_gyro_odr(accel_odr, gyro_odr)`

    Set the accelerometer and gyroscope output data rate(ODR): 0.78 Hz … 1.6 kHz (accelerometer) and 25 Hz … 6.4 kHz (gyroscope).

    - Parameter `accel_odr`: range of 0.78 Hz … 1.6 kHz.
    - Type of `unit`: float
    - Parameter `gyro_odr`: range of 25 Hz … 6.4 kHz.
    - Type of `unit`: float

### `IMUProUnit.set_magnet_odr(magnet_odr)`

    Set the magnetometer output data rate(ODR): 2, 6, 8, 10(default), 15, 20, 25, 30Hz.

    - Parameter `magnet_odr`: range of 2Hz … 30Hz.
    - Type of `unit`: int

### `IMUProUnit.set_accel_range(accel_scale)`

    Set the accelerometer scale range.

    - Parameter `accel_scale`: scale range of ±2g, ±4g, ±8g and ±16g.
    - Type of `unit`: int

### `IMUProUnit.set_gyro_range(gyro_scale)`

    Set the gyroscope scale range.

    - Parameter `gyro_scale`: scale range of ±125 dps, ±250 dps, ±500 dps, ±1000 dps, and ±2000 dps.
    - Type of `unit`: int

### `IMUProUnit.set_gyro_offsets(x, y, z)`

    Set the manual gyro calibrations offsets value

    - Parameter `x`: 0.0
    - Type of `unit`: float
    - Parameter `y`: 0.0
    - Type of `unit`: float
    - Parameter `z`: 0.0
    - Type of `unit`: float
