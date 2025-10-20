import streamlit as st
import datetime
import psutil
import os
import streamlit as st
from dotenv import load_dotenv

from app.system_info import get_system_info
from app.weather import load_weather_config, fetch_current_weather, WeatherError
from app.timer import render_timer

load_dotenv()

st.set_page_config(page_title="Smart Dashboard", layout="wide")

st.title("Smart Dashboard Raspberry Pi 5")
st.caption("Systeminfos Server * Wetter * Fokus-Timer")

# System infos
st.header("System Informationen")
info = get_system_info()
col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Auslastung", f"{info['cpu_percentage']} %")
col2.metric("RAM Auslastung", f"{info['ram_percentage']} %", f"{info['ram_used_gb']:.2f} GB / {info['ram_total_gb']:.2f} GB")
col3.metric("Festplatten Auslastung", f"{info['disk_percentage']} %", f"{info['disk_used_gb']:.2f} GB / {info['disk_total_gb']:.2f} GB")
col4.metric("Uptime", str(info['uptime']).split('.')[0])  # Remove microseconds

st.divider()

#Weather
st.header("Wetter")
@st.cache_data(ttl=600)
def _cached_weather():
    api_key, city, country, lang, units, = load_weather_config()
    return fetch_current_weather(api_key, city, country, lang, units)

try:
    weather = _cached_weather()
    wc1, wc2, wc3, wc4 = st.columns(4)
    wc1.metric("Temperatur", f"{weather['temperature']} °C")
    wc2.metric("Luftfeuchtigkeit", f"{weather['humidity']} %")
    wc3.metric("Luftdruck", f"{weather['pressure']} hPa")
    wc4.metric("Wetter", weather['description'].title())
    st.write(f"**Wind** {weather['wind_speed']} m/s, **Sichtweite** {weather['visibility']} m")
except WeatherError as e:
    st.error(f"Wetterdaten konnten nicht geladen werden: {e}")
except Exception as e:
    st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

st.divider()

# Fokus-Timer
st.header("Fokus-Timer")
render_timer()

st.caption("Läuft im LAN")
    
        