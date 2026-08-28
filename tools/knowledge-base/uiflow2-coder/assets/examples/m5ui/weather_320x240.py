# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""M5UI/LVGL weather example for a 320 x 240 display.

The example first reuses an existing UiFlow2 Wi-Fi connection. Optional Wi-Fi
credentials are only used when no network is already connected.
"""

import gc
import time

import M5
import lvgl as lv
import m5ui
import network
import requests
from M5 import Widgets


# User settings.
# Leave both strings empty to only use a Wi-Fi connection made by UiFlow2.
WIFI_SSID = ""
WIFI_PASSWORD = ""

# IP location is approximate. If it is disabled or unavailable, the fixed
# location below is used instead.
AUTO_LOCATION_BY_IP = True
FALLBACK_LOCATION_NAME = "Shenzhen"
FALLBACK_LATITUDE = 22.5431
FALLBACK_LONGITUDE = 114.0579

# Weather is refreshed every 15 minutes.
REFRESH_INTERVAL_MS = 15 * 60 * 1000
WIFI_TIMEOUT_MS = 15 * 1000
HTTP_TIMEOUT_SECONDS = 10


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
CANVAS_HEIGHT = 184

COLOR_BACKGROUND = 0x091113
COLOR_SURFACE = 0x172024
COLOR_SURFACE_ALT = 0x202B30
COLOR_BORDER = 0x39494F
COLOR_TEXT = 0xF4F7F7
COLOR_MUTED = 0x9BA9AE
COLOR_ACCENT = 0x31B7C9
COLOR_SUCCESS = 0x52C88B
COLOR_ERROR = 0xEB6656
COLOR_SUN = 0xF6C94C
COLOR_CLOUD = 0xC7D1D4
COLOR_RAIN = 0x55A5E8
COLOR_SNOW = 0xE8F7FA

page = None
canvas = None
status_label = None
refresh_button = None
wlan = None
weather_data = None
location_data = None
ip_location_resolved = False
refresh_requested = True
last_refresh_ms = None


def ascii_text(value):
    # Built-in Montserrat fonts cover ASCII; keep API-provided city names safe.
    return "".join(character for character in str(value) if ord(character) < 128)


def set_status(text, color=COLOR_MUTED):
    status_label.set_text(text)
    status_label.set_style_text_color(lv.color_hex(color), lv.PART.MAIN)


def refresh_clicked(_event):
    global refresh_requested
    refresh_requested = True


def text_width(text, font):
    size = lv.point_t()
    lv.text_get_size(size, str(text), font, 0, 0, lv.COORD.MAX, lv.TEXT_FLAG.NONE)
    return size.x


def fill_circle(cx, cy, radius, color):
    radius_squared = radius * radius
    for offset_y in range(-radius, radius + 1):
        half_width = int((radius_squared - offset_y * offset_y) ** 0.5)
        canvas.draw_line(
            cx - half_width,
            cy + offset_y,
            cx + half_width,
            cy + offset_y,
            color,
        )


def draw_sun(cx, cy, scale):
    radius = 6 * scale
    fill_circle(cx, cy, radius, COLOR_SUN)
    inner = radius + 3 * scale
    outer = radius + 7 * scale
    canvas.draw_line(cx - outer, cy, cx - inner, cy, COLOR_SUN, width=2)
    canvas.draw_line(cx + inner, cy, cx + outer, cy, COLOR_SUN, width=2)
    canvas.draw_line(cx, cy - outer, cx, cy - inner, COLOR_SUN, width=2)
    canvas.draw_line(cx, cy + inner, cx, cy + outer, COLOR_SUN, width=2)
    canvas.draw_line(
        cx - outer + 2,
        cy - outer + 2,
        cx - inner + 2,
        cy - inner + 2,
        COLOR_SUN,
        width=2,
    )
    canvas.draw_line(
        cx + inner - 2,
        cy - inner + 2,
        cx + outer - 2,
        cy - outer + 2,
        COLOR_SUN,
        width=2,
    )


def draw_cloud(cx, cy, scale):
    fill_circle(cx - 7 * scale, cy, 6 * scale, COLOR_CLOUD)
    fill_circle(cx + 2 * scale, cy - 4 * scale, 8 * scale, COLOR_CLOUD)
    fill_circle(cx + 11 * scale, cy + scale, 6 * scale, COLOR_CLOUD)
    canvas.draw_rect(
        cx - 13 * scale,
        cy,
        27 * scale,
        8 * scale,
        radius=3 * scale,
        bg_c=COLOR_CLOUD,
    )


def draw_weather_icon(code, cx, cy, scale, is_day=True, background=COLOR_BACKGROUND):
    if code == 0:
        if is_day:
            draw_sun(cx, cy, scale)
        else:
            fill_circle(cx, cy, 9 * scale, COLOR_SNOW)
            fill_circle(cx + 5 * scale, cy - 4 * scale, 9 * scale, background)
        return

    if code in (1, 2):
        draw_sun(cx - 7 * scale, cy - 6 * scale, scale)
        draw_cloud(cx + 3 * scale, cy + 2 * scale, scale)
        return

    if code == 3:
        draw_cloud(cx, cy, scale)
        return

    if code in (45, 48):
        draw_cloud(cx, cy - 5 * scale, scale)
        for offset in (6, 11, 16):
            canvas.draw_line(
                cx - 12 * scale,
                cy + offset * scale,
                cx + 13 * scale,
                cy + offset * scale,
                COLOR_MUTED,
            )
        return

    draw_cloud(cx, cy - 5 * scale, scale)
    if 71 <= code <= 77 or 85 <= code <= 86:
        for offset in (-7, 0, 7):
            snow_x = cx + offset * scale
            snow_y = cy + 9 * scale
            canvas.draw_line(snow_x - 2 * scale, snow_y, snow_x + 2 * scale, snow_y, COLOR_SNOW)
            canvas.draw_line(snow_x, snow_y - 2 * scale, snow_x, snow_y + 2 * scale, COLOR_SNOW)
    elif 95 <= code <= 99:
        canvas.draw_line(
            cx + 3 * scale, cy + 4 * scale, cx - 3 * scale, cy + 12 * scale, COLOR_SUN, width=2
        )
        canvas.draw_line(
            cx - 3 * scale, cy + 12 * scale, cx + scale, cy + 12 * scale, COLOR_SUN, width=2
        )
        canvas.draw_line(
            cx + scale, cy + 12 * scale, cx - 4 * scale, cy + 19 * scale, COLOR_SUN, width=2
        )
    else:
        for offset in (-8, 0, 8):
            canvas.draw_line(
                cx + offset * scale,
                cy + 5 * scale,
                cx + (offset - 3) * scale,
                cy + 14 * scale,
                COLOR_RAIN,
                width=2,
            )


def weather_name(code):
    if code == 0:
        return "Clear"
    if code in (1, 2):
        return "Partly cloudy"
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
        return "Snow shower"
    if 95 <= code <= 99:
        return "Storm"
    return "Unknown"


def draw_temperature(value):
    number = str(int(round(value)))
    number_font = lv.font_montserrat_48
    unit_font = lv.font_montserrat_24
    number_x = 14
    number_y = 44
    unit_x = number_x + text_width(number, number_font) + 5

    canvas.draw_label(number, number_x, number_y, font=number_font, color=COLOR_TEXT)
    # Draw the degree mark as a real circle at the upper-left of C.
    canvas.draw_arc(unit_x + 3, number_y + 7, 3, COLOR_TEXT, width=1, start_angle=0, end_angle=360)
    canvas.draw_label("C", unit_x + 10, number_y + 4, font=unit_font, color=COLOR_TEXT)


def draw_status_screen(title, detail, color=COLOR_ACCENT):
    canvas.begin_draw()
    canvas.fill_bg(COLOR_BACKGROUND, 255)
    draw_weather_icon(2, 160, 64, 2, True, COLOR_BACKGROUND)
    title_x = (SCREEN_WIDTH - text_width(title, lv.font_montserrat_24)) // 2
    detail_x = (SCREEN_WIDTH - text_width(detail, lv.font_montserrat_14)) // 2
    canvas.draw_label(title, title_x, 110, font=lv.font_montserrat_24, color=color)
    canvas.draw_label(detail, detail_x, 142, font=lv.font_montserrat_14, color=COLOR_MUTED)
    canvas.end_draw()


def draw_weather(data, offline=False):
    location = data["location"][:20]
    status_text = "OFFLINE" if offline else "ONLINE"
    status_color = COLOR_ERROR if offline else COLOR_SUCCESS

    canvas.begin_draw()
    canvas.fill_bg(COLOR_BACKGROUND, 255)

    canvas.draw_label(location, 10, 8, font=lv.font_montserrat_18, color=COLOR_TEXT)
    fill_circle(245, 17, 4, status_color)
    canvas.draw_label(status_text, 256, 10, font=lv.font_montserrat_14, color=status_color)
    canvas.draw_line(10, 34, 310, 34, COLOR_BORDER)

    # Current conditions occupy the left half.
    draw_temperature(data["temperature"])
    draw_weather_icon(data["code"], 137, 108, 1, data["is_day"], COLOR_BACKGROUND)
    canvas.draw_label(
        weather_name(data["code"]),
        14,
        111,
        font=lv.font_montserrat_16,
        color=COLOR_ACCENT,
    )
    canvas.draw_rect(10, 139, 146, 35, radius=4, bg_c=COLOR_SURFACE)
    canvas.draw_label("HUM", 18, 145, font=lv.font_montserrat_14, color=COLOR_MUTED)
    canvas.draw_label(
        "%d%%" % int(round(data["humidity"])),
        18,
        160,
        font=lv.font_montserrat_14,
        color=COLOR_TEXT,
    )
    canvas.draw_line(82, 145, 82, 168, COLOR_BORDER)
    canvas.draw_label("WIND", 92, 145, font=lv.font_montserrat_14, color=COLOR_MUTED)
    canvas.draw_label(
        "%dkm/h" % int(round(data["wind"])),
        92,
        160,
        font=lv.font_montserrat_14,
        color=COLOR_TEXT,
    )

    # Three-day forecast occupies the right half.
    canvas.draw_label("FORECAST", 172, 43, font=lv.font_montserrat_14, color=COLOR_MUTED)
    for index, forecast in enumerate(data["daily"]):
        y = 64 + index * 37
        background = COLOR_SURFACE_ALT if index & 1 else COLOR_SURFACE
        canvas.draw_rect(168, y, 142, 34, radius=3, bg_c=background)
        day = "TODAY" if index == 0 else forecast["date"][5:]
        canvas.draw_label(day, 176, y + 10, font=lv.font_montserrat_14, color=COLOR_MUTED)
        draw_weather_icon(forecast["code"], 239, y + 15, 1, True, background)
        temperatures = "%d/%d" % (
            int(round(forecast["high"])),
            int(round(forecast["low"])),
        )
        text_x = 302 - text_width(temperatures, lv.font_montserrat_14)
        canvas.draw_label(
            temperatures, text_x, y + 10, font=lv.font_montserrat_14, color=COLOR_TEXT
        )

    canvas.end_draw()


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


def fetch_json(url):
    response = None
    try:
        response = requests.get(url, timeout=HTTP_TIMEOUT_SECONDS)
        if response.status_code != 200:
            raise RuntimeError("HTTP %d" % response.status_code)
        return response.json()
    finally:
        if response is not None:
            response.close()


def fallback_location():
    return {
        "name": FALLBACK_LOCATION_NAME,
        "latitude": FALLBACK_LATITUDE,
        "longitude": FALLBACK_LONGITUDE,
    }


def resolve_location():
    global ip_location_resolved
    if not AUTO_LOCATION_BY_IP:
        return fallback_location()

    try:
        payload = fetch_json("https://ipwho.is/")
        if payload.get("success", True) is False:
            raise RuntimeError("IP LOCATION REJECTED")
        city = ascii_text(payload.get("city", ""))
        latitude = payload["latitude"]
        longitude = payload["longitude"]
        if not city:
            city = FALLBACK_LOCATION_NAME
        ip_location_resolved = True
        return {"name": city, "latitude": latitude, "longitude": longitude}
    except Exception as error:
        print("IP_LOCATION_ERROR", error)
        return fallback_location()


def weather_url(location):
    return (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=%.4f&longitude=%.4f"
        "&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&timezone=auto&forecast_days=3"
    ) % (location["latitude"], location["longitude"])


def fetch_weather(location):
    payload = fetch_json(weather_url(location))
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
        "location": location["name"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "is_day": current["is_day"] == 1,
        "code": current["weather_code"],
        "daily": forecasts,
    }


def refresh_weather():
    global weather_data, location_data, last_refresh_ms
    set_status("UPDATING", COLOR_ACCENT)
    draw_status_screen("UPDATING", "GETTING WEATHER")
    try:
        ensure_wifi()
        if location_data is None or (AUTO_LOCATION_BY_IP and not ip_location_resolved):
            location_data = resolve_location()
        weather_data = fetch_weather(location_data)
        draw_weather(weather_data)
        set_status("UPDATED", COLOR_SUCCESS)
    except Exception as error:
        print("WEATHER_UPDATE_ERROR", error)
        if weather_data is not None:
            draw_weather(weather_data, offline=True)
            set_status("OFFLINE - SAVED DATA", COLOR_ERROR)
        elif str(error) == "SET WIFI CONFIG":
            draw_status_screen("NO WIFI", "SET WIFI CONFIG", COLOR_ERROR)
            set_status("NO NETWORK", COLOR_ERROR)
        elif str(error) == "WIFI TIMEOUT":
            draw_status_screen("NO WIFI", "CHECK NETWORK", COLOR_ERROR)
            set_status("CONNECTION TIMEOUT", COLOR_ERROR)
        else:
            draw_status_screen("NO WEATHER", "TOUCH REFRESH", COLOR_ERROR)
            set_status("UPDATE FAILED", COLOR_ERROR)
    finally:
        last_refresh_ms = time.ticks_ms()
        gc.collect()


def setup():
    global page, canvas, status_label, refresh_button, wlan

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page = m5ui.M5Page(bg_c=COLOR_SURFACE)
    canvas = m5ui.M5Canvas(
        x=0,
        y=0,
        w=SCREEN_WIDTH,
        h=CANVAS_HEIGHT,
        color_format=lv.COLOR_FORMAT.RGB565,
        bg_c=COLOR_BACKGROUND,
        bg_opa=255,
        parent=page,
    )
    status_label = m5ui.M5Label(
        "READY",
        x=10,
        y=204,
        text_c=COLOR_MUTED,
        bg_c=COLOR_SURFACE,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page,
    )
    refresh_button = m5ui.M5Button(
        text="REFRESH",
        x=222,
        y=190,
        w=90,
        h=44,
        bg_c=COLOR_ACCENT,
        text_c=COLOR_TEXT,
        font=lv.font_montserrat_14,
        parent=page,
    )
    refresh_button.set_style_radius(6, lv.PART.MAIN)
    refresh_button.add_event_cb(refresh_clicked, lv.EVENT.CLICKED, None)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    page.screen_load()
    draw_status_screen("WEATHER", FALLBACK_LOCATION_NAME)


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
        try:
            m5ui.deinit()
        except Exception:
            pass
        page = None
        canvas = None
        weather_data = None
        gc.collect()
