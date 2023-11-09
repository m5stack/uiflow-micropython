from machine import I2C, Pin
from unit.color import ColorUnit
import time

i2c0 = None
sensor = None


def setup():
    global i2c0, sensor
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    sensor = ColorUnit(i2c0)


def loop():
    global i2c0, sensor
    color = sensor.get_color()
    color_rgb = sensor.get_color_rgb_bytes()
    print("RGB888: #{0:02X} or as 3-tuple: {1}".format(color, color_rgb))

    color565 = sensor.get_color565()
    color_rgb = sensor.get_color_rgb_bytes()
    print("RGB666: #{0:02X} or as 3-tuple: {1}".format(color565, color_rgb))

    # Read the color temperature and lux of the sensor too.
    temp = sensor.get_color_temperature()
    lux = sensor.get_lux()
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(1.0)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except Exception as ex:
        # error handler
        raise ex
