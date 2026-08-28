# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""Widgets weather example for a 135 x 240 display using Open-Meteo.

The existing UIFlow2 Wi-Fi connection is reused. Optional fallback credentials
and the location can be configured below. Button A refreshes immediately.
"""

import gc
import time

import M5
import network
import requests
from M5 import BtnA, Widgets


# User settings.
# An existing UiFlow2 Wi-Fi connection is always reused first. These optional
# credentials are used only when the device is not already connected.
WIFI_SSID = ""
WIFI_PASSWORD = ""
LOCATION_NAME = "Shenzhen"
LATITUDE = 22.5431
LONGITUDE = 114.0579
# Weather is refreshed every 15 minutes.
REFRESH_INTERVAL_MS = 15 * 60 * 1000
WIFI_TIMEOUT_MS = 15 * 1000
HTTP_TIMEOUT_SECONDS = 10


SCREEN_WIDTH = 135
SCREEN_HEIGHT = 240

COLOR_BACKGROUND = 0x0B0D0E
COLOR_SURFACE = 0x171B1D
COLOR_SURFACE_ALT = 0x202629
COLOR_BORDER = 0x394247
COLOR_TEXT = 0xF5F7F6
COLOR_MUTED = 0xA6B0B3
COLOR_ACCENT = 0x38C8E8
COLOR_SUCCESS = 0x5DD39E
COLOR_ERROR = 0xFF6B6B
COLOR_SUN = 0xFFC857
COLOR_CLOUD = 0xC9D1D4
COLOR_RAIN = 0x4DA3FF
COLOR_SNOW = 0xEAF7FF

FONT_SMALL = Widgets.FONTS.DejaVu12
FONT_BODY = Widgets.FONTS.DejaVu18
FONT_LARGE = Widgets.FONTS.DejaVu40

canvas = None
wlan = None
weather_data = None
refresh_requested = True
last_refresh_ms = None


def button_a_clicked(_state):
    global refresh_requested
    refresh_requested = True


def draw_text(text, x, y, font, color, background, align=0):
    canvas.setFont(font)
    canvas.setTextColor(color, background)
    if align < 0:
        canvas.drawRightString(str(text), x, y)
    elif align > 0:
        canvas.drawCenterString(str(text), x, y)
    else:
        canvas.drawString(str(text), x, y)


def draw_temperature(value):
    number = str(int(round(value)))
    canvas.setFont(FONT_LARGE)
    number_width = canvas.textWidth(number)
    unit_width = canvas.textWidth("C")
    degree_space = 8
    left = 128 - number_width - degree_space - unit_width

    draw_text(number, left, 47, FONT_LARGE, COLOR_TEXT, COLOR_BACKGROUND)
    unit_x = left + number_width + degree_space
    canvas.drawCircle(unit_x - 4, 54, 2, COLOR_TEXT)
    draw_text("C", unit_x, 47, FONT_LARGE, COLOR_TEXT, COLOR_BACKGROUND)


def draw_sun(cx, cy, scale):
    radius = 5 * scale
    canvas.fillCircle(cx, cy, radius, COLOR_SUN)
    inner = radius + 3 * scale
    outer = radius + 6 * scale
    canvas.drawLine(cx - outer, cy, cx - inner, cy, COLOR_SUN)
    canvas.drawLine(cx + inner, cy, cx + outer, cy, COLOR_SUN)
    canvas.drawLine(cx, cy - outer, cx, cy - inner, COLOR_SUN)
    canvas.drawLine(cx, cy + inner, cx, cy + outer, COLOR_SUN)
    diagonal_inner = radius + 2 * scale
    diagonal_outer = radius + 4 * scale
    canvas.drawLine(
        cx - diagonal_outer,
        cy - diagonal_outer,
        cx - diagonal_inner,
        cy - diagonal_inner,
        COLOR_SUN,
    )
    canvas.drawLine(
        cx + diagonal_inner,
        cy - diagonal_inner,
        cx + diagonal_outer,
        cy - diagonal_outer,
        COLOR_SUN,
    )
    canvas.drawLine(
        cx - diagonal_outer,
        cy + diagonal_outer,
        cx - diagonal_inner,
        cy + diagonal_inner,
        COLOR_SUN,
    )
    canvas.drawLine(
        cx + diagonal_inner,
        cy + diagonal_inner,
        cx + diagonal_outer,
        cy + diagonal_outer,
        COLOR_SUN,
    )


def draw_cloud(cx, cy, scale):
    canvas.fillCircle(cx - 6 * scale, cy, 5 * scale, COLOR_CLOUD)
    canvas.fillCircle(cx + 2 * scale, cy - 3 * scale, 7 * scale, COLOR_CLOUD)
    canvas.fillCircle(cx + 9 * scale, cy + scale, 5 * scale, COLOR_CLOUD)
    canvas.fillRoundRect(
        cx - 11 * scale,
        cy,
        22 * scale,
        7 * scale,
        3 * scale,
        COLOR_CLOUD,
    )


def draw_weather_icon(code, cx, cy, scale, is_day=True, background=COLOR_BACKGROUND):
    if code == 0:
        if is_day:
            draw_sun(cx, cy, scale)
        else:
            canvas.fillCircle(cx, cy, 7 * scale, COLOR_SNOW)
            canvas.fillCircle(cx + 4 * scale, cy - 3 * scale, 7 * scale, background)
        return

    if code in (1, 2):
        draw_sun(cx - 6 * scale, cy - 5 * scale, scale)
        draw_cloud(cx + 2 * scale, cy + 2 * scale, scale)
        return

    if code == 3:
        draw_cloud(cx, cy, scale)
        return

    if code in (45, 48):
        draw_cloud(cx, cy - 4 * scale, scale)
        for offset in (5, 9, 13):
            canvas.drawLine(
                cx - 10 * scale,
                cy + offset * scale,
                cx + 10 * scale,
                cy + offset * scale,
                COLOR_MUTED,
            )
        return

    draw_cloud(cx, cy - 4 * scale, scale)
    if 71 <= code <= 77 or 85 <= code <= 86:
        for offset in (-6, 0, 6):
            snow_x = cx + offset * scale
            snow_y = cy + 9 * scale
            canvas.drawLine(
                snow_x - 2 * scale,
                snow_y,
                snow_x + 2 * scale,
                snow_y,
                COLOR_SNOW,
            )
            canvas.drawLine(
                snow_x,
                snow_y - 2 * scale,
                snow_x,
                snow_y + 2 * scale,
                COLOR_SNOW,
            )
    elif 95 <= code <= 99:
        canvas.drawLine(
            cx + 2 * scale,
            cy + 4 * scale,
            cx - 3 * scale,
            cy + 11 * scale,
            COLOR_SUN,
        )
        canvas.drawLine(
            cx - 3 * scale,
            cy + 11 * scale,
            cx + scale,
            cy + 11 * scale,
            COLOR_SUN,
        )
        canvas.drawLine(
            cx + scale,
            cy + 11 * scale,
            cx - 3 * scale,
            cy + 17 * scale,
            COLOR_SUN,
        )
    else:
        for offset in (-7, 0, 7):
            canvas.drawLine(
                cx + offset * scale,
                cy + 5 * scale,
                cx + (offset - 2) * scale,
                cy + 12 * scale,
                COLOR_RAIN,
            )


def weather_name(code):
    if code == 0:
        return "Clear"
    if code in (1, 2):
        return "Part Cloudy"
    if code == 3:
        return "Cloudy"
    if code in (45, 48):
        return "Fog"
    if 51 <= code <= 57:
        return "Drizzle"
    if 61 <= code <= 67:
        return "Rain"
    if 71 <= code <= 77:
        return "Snow"
    if 80 <= code <= 82:
        return "Showers"
    if 85 <= code <= 86:
        return "Snow Shower"
    if 95 <= code <= 99:
        return "Storm"
    return "Unknown"


def draw_status(title, detail, color=COLOR_ACCENT):
    canvas.fillScreen(COLOR_BACKGROUND)
    draw_weather_icon(2, 67, 80, 2, True, COLOR_BACKGROUND)
    draw_text(title, 67, 116, FONT_BODY, color, COLOR_BACKGROUND, 1)
    draw_text(detail, 67, 143, FONT_SMALL, COLOR_MUTED, COLOR_BACKGROUND, 1)
    canvas.push(0, 0)


def draw_weather(data, offline=False):
    canvas.fillScreen(COLOR_BACKGROUND)

    location = LOCATION_NAME[:11]
    draw_text(location, 7, 5, FONT_BODY, COLOR_TEXT, COLOR_BACKGROUND)
    status_color = COLOR_ERROR if offline else COLOR_SUCCESS
    canvas.fillCircle(124, 13, 3, status_color)
    if offline:
        draw_text("OFFLINE", 128, 24, FONT_SMALL, COLOR_MUTED, COLOR_BACKGROUND, -1)
    canvas.drawLine(7, 38, 128, 38, COLOR_BORDER)

    draw_weather_icon(
        data["code"],
        31,
        77,
        2,
        data["is_day"],
        COLOR_BACKGROUND,
    )
    draw_temperature(data["temperature"])
    draw_text(
        weather_name(data["code"]),
        94,
        91,
        FONT_SMALL,
        COLOR_ACCENT,
        COLOR_BACKGROUND,
        1,
    )

    canvas.fillRect(0, 112, SCREEN_WIDTH, 41, COLOR_SURFACE)
    canvas.drawLine(67, 118, 67, 147, COLOR_BORDER)
    draw_text("HUM", 12, 117, FONT_SMALL, COLOR_MUTED, COLOR_SURFACE)
    draw_text(
        "%d%%" % int(round(data["humidity"])),
        12,
        134,
        FONT_SMALL,
        COLOR_TEXT,
        COLOR_SURFACE,
    )
    draw_text("WIND", 76, 117, FONT_SMALL, COLOR_MUTED, COLOR_SURFACE)
    draw_text(
        "%dkm/h" % int(round(data["wind"])),
        76,
        134,
        FONT_SMALL,
        COLOR_TEXT,
        COLOR_SURFACE,
    )

    row_top = 157
    for index, forecast in enumerate(data["daily"]):
        y = row_top + index * 27
        background = COLOR_SURFACE_ALT if index & 1 else COLOR_BACKGROUND
        canvas.fillRect(0, y, SCREEN_WIDTH, 27, background)
        if index:
            canvas.drawLine(7, y, 128, y, COLOR_BORDER)
        day = "TODAY" if index == 0 else forecast["date"][5:]
        draw_text(day, 7, y + 7, FONT_SMALL, COLOR_MUTED, background)
        draw_weather_icon(forecast["code"], 57, y + 9, 1, True, background)
        high = int(round(forecast["high"]))
        low = int(round(forecast["low"]))
        draw_text(
            "%d/%d" % (high, low),
            128,
            y + 7,
            FONT_SMALL,
            COLOR_TEXT,
            background,
            -1,
        )

    canvas.push(0, 0)


def ensure_wifi():
    if wlan.isconnected():
        return
    if not WIFI_SSID:
        raise RuntimeError("SET WIFI CONFIG")

    try:
        wlan.config(reconnects=3)
    except Exception:
        pass
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    started_ms = time.ticks_ms()
    while not wlan.isconnected():
        M5.update()
        if time.ticks_diff(time.ticks_ms(), started_ms) >= WIFI_TIMEOUT_MS:
            raise RuntimeError("WIFI TIMEOUT")
        time.sleep_ms(100)


def weather_url():
    return (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=%.4f&longitude=%.4f"
        "&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&timezone=auto&forecast_days=3"
    ) % (LATITUDE, LONGITUDE)


def fetch_weather():
    response = None
    try:
        response = requests.get(weather_url(), timeout=HTTP_TIMEOUT_SECONDS)
        if response.status_code != 200:
            raise RuntimeError("HTTP %d" % response.status_code)
        payload = response.json()
    finally:
        if response is not None:
            response.close()

    current = payload["current"]
    daily = payload["daily"]
    forecasts = []
    for index in range(3):
        forecasts.append(
            {
                "date": daily["time"][index],
                "code": daily["weather_code"][index],
                "high": daily["temperature_2m_max"][index],
                "low": daily["temperature_2m_min"][index],
            }
        )
    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "is_day": current["is_day"] == 1,
        "code": current["weather_code"],
        "daily": forecasts,
    }


def refresh_weather():
    global weather_data, last_refresh_ms
    draw_status("UPDATING", LOCATION_NAME)
    try:
        ensure_wifi()
        weather_data = fetch_weather()
        draw_weather(weather_data)
    except Exception as error:
        print("WEATHER_UPDATE_ERROR", error)
        if weather_data is not None:
            draw_weather(weather_data, offline=True)
        elif str(error) == "SET WIFI CONFIG":
            draw_status("NO WIFI", "SET WIFI CONFIG", COLOR_ERROR)
        elif str(error) == "WIFI TIMEOUT":
            draw_status("NO WIFI", "CHECK NETWORK", COLOR_ERROR)
        else:
            draw_status("NO WEATHER", "TRY AGAIN", COLOR_ERROR)
    finally:
        last_refresh_ms = time.ticks_ms()
        gc.collect()


def setup():
    global canvas, wlan
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(COLOR_BACKGROUND)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=button_a_clicked)
    gc.collect()

    canvas = M5.Lcd.newCanvas(SCREEN_WIDTH, SCREEN_HEIGHT, 8, True)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    draw_status("WEATHER", LOCATION_NAME)


def loop():
    global refresh_requested
    M5.update()
    now_ms = time.ticks_ms()
    refresh_due = (
        last_refresh_ms is None or time.ticks_diff(now_ms, last_refresh_ms) >= REFRESH_INTERVAL_MS
    )
    if refresh_requested or refresh_due:
        refresh_requested = False
        refresh_weather()
    time.sleep_ms(20)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as error:
        try:
            from utility import print_error_msg

            print_error_msg(error)
        except ImportError:
            print(error)
    finally:
        if canvas is not None:
            try:
                canvas.delete()
            except Exception:
                pass
            canvas = None
        weather_data = None
        gc.collect()
