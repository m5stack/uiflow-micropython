使用代码审查skill检查下面的过程中的问题，输出中文报告在 ./tools/code-review 下

输入需求：
读取tab5上的所有传感器的信息，实时显示在屏幕上，并且要做一个炫酷富有科技感的ui界面


目前现象：
编译报错：
Traceback (most recent call last):
  File "<stdin>", line 216, in <module>
  File "<stdin>", line 29, in setup
  File "m5ui/__init__.py", line 43, in __getattr__
AttributeError: M5Screen

生成代码:
import os, sys, io
import M5
from M5 import *
import time
import m5ui
import lvgl as lv


page0 = None
title_label = None
time_label = None
accel_x_label = None
accel_y_label = None
accel_z_label = None
gyro_x_label = None
gyro_y_label = None
gyro_z_label = None
voltage_label = None
current_label = None
power_label = None


def setup():
    global page0, title_label, time_label
    global accel_x_label, accel_y_label, accel_z_label
    global gyro_x_label, gyro_y_label, gyro_z_label
    global voltage_label, current_label, power_label

    M5.begin()
    m5ui.init()

    # Set landscape orientation for 5-inch display
    M5.Lcd.setRotation(1)

    # Create main page with dark tech background
    page0 = m5ui.M5Screen(bg_c=0x0A0E27)

    # Title with cyan tech color
    title_label = m5ui.M5Label(
        "TAB5 SENSOR MONITOR",
        x=int(M5.Lcd.width() / 2 - 200),
        y=20,
        text_c=0x00FFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_28,
        parent=page0,
    )

    # Time display
    time_label = m5ui.M5Label(
        "TIME: --:--:--",
        x=int(M5.Lcd.width() / 2 - 150),
        y=70,
        text_c=0x00FF88,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_20,
        parent=page0,
    )

    # Accelerometer section (left column)
    accel_title = m5ui.M5Label(
        "ACCELEROMETER (g)",
        x=50,
        y=120,
        text_c=0xFF6B35,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    accel_x_label = m5ui.M5Label(
        "X: 0.000",
        x=50,
        y=160,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    accel_y_label = m5ui.M5Label(
        "Y: 0.000",
        x=50,
        y=200,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    accel_z_label = m5ui.M5Label(
        "Z: 0.000",
        x=50,
        y=240,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    # Gyroscope section (middle column)
    gyro_title = m5ui.M5Label(
        "GYROSCOPE (dps)",
        x=400,
        y=120,
        text_c=0x4ECDC4,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    gyro_x_label = m5ui.M5Label(
        "X: 0.000",
        x=400,
        y=160,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    gyro_y_label = m5ui.M5Label(
        "Y: 0.000",
        x=400,
        y=200,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    gyro_z_label = m5ui.M5Label(
        "Z: 0.000",
        x=400,
        y=240,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    # Power monitoring section (right column)
    power_title = m5ui.M5Label(
        "POWER MONITOR",
        x=750,
        y=120,
        text_c=0xF72585,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    voltage_label = m5ui.M5Label(
        "V: 0.00 V",
        x=750,
        y=160,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    current_label = m5ui.M5Label(
        "I: 0.00 mA",
        x=750,
        y=200,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    power_label = m5ui.M5Label(
        "P: 0.00 mW",
        x=750,
        y=240,
        text_c=0xFFFFFF,
        bg_c=0x0A0E27,
        bg_opa=0,
        font=lv.font_montserrat_22,
        parent=page0,
    )

    # Draw decorative tech lines
    M5.Lcd.drawLine(30, 110, M5.Lcd.width() - 30, 110, 0x1E3A8A)
    M5.Lcd.drawLine(30, 290, M5.Lcd.width() - 30, 290, 0x1E3A8A)
    M5.Lcd.drawRect(30, 110, 330, 190, 0x1E3A8A)
    M5.Lcd.drawRect(380, 110, 330, 190, 0x1E3A8A)
    M5.Lcd.drawRect(730, 110, 330, 190, 0x1E3A8A)

    page0.screen_load()


def loop():
    global page0, title_label, time_label
    global accel_x_label, accel_y_label, accel_z_label
    global gyro_x_label, gyro_y_label, gyro_z_label
    global voltage_label, current_label, power_label

    M5.update()

    # Read IMU data (BMI270)
    accel_data = Imu.getAccel()
    gyro_data = Imu.getGyro()

    # Update accelerometer labels
    accel_x_label.set_text("X: {:.3f}".format(accel_data[0]))
    accel_y_label.set_text("Y: {:.3f}".format(accel_data[1]))
    accel_z_label.set_text("Z: {:.3f}".format(accel_data[2]))

    # Update gyroscope labels
    gyro_x_label.set_text("X: {:.3f}".format(gyro_data[0]))
    gyro_y_label.set_text("Y: {:.3f}".format(gyro_data[1]))
    gyro_z_label.set_text("Z: {:.3f}".format(gyro_data[2]))

    # Read power data (INA226 via Power API)
    voltage = Power.getBatteryVoltage()
    current = Power.getBatteryCurrent()
    power = voltage * current

    # Update power labels
    voltage_label.set_text("V: {:.2f} V".format(voltage / 1000.0))
    current_label.set_text("I: {:.2f} mA".format(current))
    power_label.set_text("P: {:.2f} mW".format(power))

    # Read RTC time
    current_time = time.localtime()
    time_str = "TIME: {:02d}:{:02d}:{:02d}".format(
        current_time[3], current_time[4], current_time[5]
    )
    time_label.set_text(time_str)

    time.sleep_ms(100)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
