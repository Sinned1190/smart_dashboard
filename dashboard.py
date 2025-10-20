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




        
    
        