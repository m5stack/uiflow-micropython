# main.py
import os, sys, io
import M5
import machine
from M5 import *
from hardware import *
from roller485 import Roller485Unit
from myenv import ENVUnit
import time

# i2c0 = None
roller485_0 = None


def setup():
    # global i2c0, roller485_0, start_time
    global roller485_0, start_time

    M5.begin()
    Widgets.fillScreen(0xFF6600)
    uart = UART(
        2,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=14,
        rx=13,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
    roller485_0 = Roller485Unit(uart, address=0x01, mode=Roller485Unit._RS485_TO_I2C_MODE)
    env2_0 = ENVUnit(i2c=roller485_0, type=2)
    print(f"roller485_0 instance: {roller485_0}")  # 打印实例信息
    Widgets.fillScreen(0xFF9900)

    print(env2_0.read_temperature())

    # roller485_0.scan()

    # roller485_0.set_motor_output_state(0)
    # I2C Communication
    # roller485_0.write_i2c_slave(bytes((0x2C, 0x06)),0)
    # read_buffer=roller485_0.read_i2c_slave(0x06)
    # print("hex: ", ' '.join(f'{byte:02x}' for byte in read_buffer))
    # temp = ((((read_buffer[0] * 256.0) + read_buffer[1]) * 175) / 65535.0) - 45;
    # print("Temperature: ", temp)
    # humidity=((((read_buffer[3] * 256.0) + read_buffer[4]) * 100) / 65535.0);
    # print("Humidity: ", humidity)

    # # #SYSTEM REGISTER
    # roller485_0.set_rgb_color(0x33ff33)
    # print(roller485_0.get_rgb_color())
    # roller485_0.set_rgb_color(0x11ff33)
    # print(roller485_0.get_rgb_color())

    # print(f"get_rgb_brightness:{roller485_0.get_rgb_brightness()}")
    # roller485_0.set_rgb_brightness(100)
    # print(f"get_rgb_brightness:{roller485_0.get_rgb_brightness()}")

    # roller485_0.set_rgb_mode(0)
    # print(roller485_0.get_rgb_mode())
    # roller485_0.set_rgb_mode(1)
    # print(roller485_0.get_rgb_mode())

    # # roller485_0.save_param_to_flash()

    # print(roller485_0.get_vin_voltage())

    # print(roller485_0.get_temperature_value())

    # roller485_0.set_motor_mode(4)
    # print(roller485_0.get_motor_mode())
    # print(roller485_0.get_encoder_value())
    # roller485_0.set_encoder_value(100)
    # print(roller485_0.get_encoder_value())
    # roller485_0.set_motor_mode(0)

    # # #MOTOR CONFIGURATION REGISTER
    # roller485_0.set_motor_output_state(1)
    # roller485_0.set_motor_output_state(0)

    # roller485_0.set_motor_mode(1)
    # print(roller485_0.get_motor_mode())
    # roller485_0.set_motor_mode(2)
    # print(roller485_0.get_motor_mode())
    # roller485_0.set_motor_mode(3)
    # print(roller485_0.get_motor_mode())
    # roller485_0.set_motor_mode(4)
    # print(roller485_0.get_motor_mode())

    # roller485_0.set_motor_over_range_protect_state(1)
    # roller485_0.set_motor_over_range_protect_state(0)

    # roller485_0.remove_motor_jam_protect()

    # print(f"get_motor_speed_pid:{roller485_0.get_motor_speed_pid()}")
    # roller485_0.set_motor_speed_pid(15,0.0001,400)
    # print(f"get_motor_speed_pid:{roller485_0.get_motor_speed_pid()}")

    # roller485_0.set_motor_jam_protect_state(1)

    # print(f"get_button_change_mode:{roller485_0.get_button_change_mode()}")
    # roller485_0.set_button_change_mode(1)
    # print(f"get_button_change_mode:{roller485_0.get_button_change_mode()}")

    # print(f"get_motor_id:{roller485_0.get_motor_id()}")
    # roller485_0.set_motor_id(0)
    # print(f"get_motor_id:{roller485_0.get_motor_id()}")

    # print(f"get_485_baudrate:{roller485_0.get_485_baudrate()}")
    # # roller485_0.set_485_baudrate(2)
    # # print(f"get_485_baudrate:{roller485_0.get_485_baudrate()}")
    # # roller485_0.set_485_baudrate(1)
    # # print(f"get_485_baudrate:{roller485_0.get_485_baudrate()}")
    # # roller485_0.set_485_baudrate(0)
    # # print(f"get_485_baudrate:{roller485_0.get_485_baudrate()}")

    # print(f"get_rgb_brightness:{roller485_0.get_rgb_brightness()}")
    # roller485_0.set_rgb_brightness(100)

    # # Speed Mode
    # roller485_0.set_motor_output_state(0)
    # roller485_0.set_motor_mode(1)
    # roller485_0.set_motor_speed(100)
    # roller485_0.set_speed_max_current(1200)
    # roller485_0.set_motor_output_state(1)
    # print(f"get_motor_status:{roller485_0.get_motor_status()}")
    # print(f"get_motor_error_code:{roller485_0.get_motor_error_code()}")
    # print(f"get_motor_speed_readback:{roller485_0.get_motor_speed_readback()}")

    # # Position Mode
    # roller485_0.set_motor_output_state(0)
    # roller485_0.set_motor_mode(2)
    # roller485_0.set_position_max_current(1000)
    # print(f"get_motor_position_readback:{roller485_0.get_motor_position_readback()}")
    # roller485_0.set_motor_position(360)
    # print(f"get_motor_position_readback:{roller485_0.get_motor_position_readback()}")
    # roller485_0.set_motor_output_state(1)

    # print(f"get_motor_position_pid:{roller485_0.get_motor_position_pid()}")
    # # roller485_0.set_motor_position_pid(15,0.000003,400)
    # roller485_0.set_motor_position_pid(20,0.000003,400)
    # print(f"get_motor_position_pid:{roller485_0.get_motor_position_pid()}")
    # roller485_0.set_motor_output_state(1)

    # #Current Mode
    # roller485_0.set_motor_output_state(0)
    # roller485_0.set_motor_mode(3)
    # roller485_0.set_motor_max_current(1000)
    # roller485_0.set_motor_output_state(1)

    # roller485_0.save_param_to_flash()

    # time.sleep(3)
    # roller485_0.set_motor_output_state(0)

    start_time = time.time()  # 获取当前时间


def loop():
    # global i2c0, roller485_0
    global roller485_0

    roller485_0.writeto(0x44, bytes((0x2C, 0x06)), False)
    read_buffer = roller485_0.readfrom(0x44, 0x06)
    print("hex: ", " ".join(f"{byte:02x}" for byte in read_buffer))
    temp = ((((read_buffer[0] * 256.0) + read_buffer[1]) * 175) / 65535.0) - 45
    print("Temperature: ", temp)
    humidity = (((read_buffer[3] * 256.0) + read_buffer[4]) * 100) / 65535.0
    print("Humidity: ", humidity)

    time.sleep(0.2)


if __name__ == "__main__":
    try:
        setup()
        # while True:
        #     elapsed_time = time.time() - start_time
        #     if elapsed_time > 10:
        #         print("超过10秒，循环终止")
        #         break
        #     loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
