import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

from app.system_info import get_system_info
from app.timer import render_timer
from app.weather import WeatherError, fetch_current_weather, load_weather_config

load_dotenv()

st.set_page_config(page_title="Smart Dashboard", layout="wide")



st.title("Smart Dashboard Raspberry Pi 5")
st.caption("Systeminfos Server * Wetter * Fokus-Timer")

st_autorefresh(interval=2000, key="dashboard_refresh")  # Refresh every 5 minutes

# System infos
st.header("System Informationen")
info = get_system_info()
col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Auslastung", f"{info['cpu_percentage']} %")
col2.metric("RAM Auslastung", f"{info['ram_percentage']} %", f"{info['ram_used_gb']:.2f} GB / {info['ram_total_gb']:.2f} GB")
col3.metric("Festplatten Auslastung", f"{info['disk_percentage']} %", f"{info['disk_used_gb']:.2f} GB / {info['disk_total_gb']:.2f} GB")
col4.metric("Uptime", str(info['uptime']).split('.')[0])  # Remove microseconds

st.divider()

# Weather
st.header("Wetter")
@st.cache_data(ttl=600)
def _cached_weather():
    config = load_weather_config()
    return fetch_current_weather(config)

try:
    weather = _cached_weather()
    wc1, wc2, wc3, wc4 = st.columns(4)
    temperature = weather.get("temperature")
    humidity = weather.get("humidity")
    pressure = weather.get("pressure")
    location = weather.get("location")
    description = weather.get("description", "–")
    wind_speed = weather.get("wind_speed")
    visibility = weather.get("visibility")
    observed_at = weather.get("observed_at")

    wc1.metric("Temperatur", f"{temperature:.1f} °C" if temperature is not None else "–")
    wc2.metric("Luftfeuchtigkeit", f"{humidity} %" if humidity is not None else "–")
    wc3.metric("Luftdruck", f"{pressure} hPa" if pressure is not None else "–")
    wc4.metric("Wetter", description.title() if isinstance(description, str) else "–")

    wind_text = f"{wind_speed} m/s" if wind_speed is not None else "–"
    visibility_text = (
        f"{visibility / 1000:.1f} km" if isinstance(visibility, (int, float)) else "–"
    )
    st.write(f"**Wind** {wind_text}, **Sichtweite** {visibility_text}")

    caption_parts = []
    if isinstance(location, str) and location:
        caption_parts.append(location)
    if observed_at is not None:
        caption_parts.append(observed_at.strftime("%d.%m.%Y %H:%M:%S %Z"))
    if caption_parts:
        st.caption(" • ".join(caption_parts))
except WeatherError as e:
    st.error(f"Wetterdaten konnten nicht geladen werden: {e}")
except Exception as e:
    st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

st.divider()

# Fokus-Timer
st.header("Fokus-Timer")
render_timer()

st.caption("Läuft im LAN")
    
        