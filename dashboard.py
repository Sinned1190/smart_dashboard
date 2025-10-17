import streamlit as st
import datetime
import psutil

st.set_page_config(page_title="Smart Dashboard", layout="wide")



st.title("Smart Dashboard")
st.caption(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

while True:
    if st.button("Refresh", key="refresh"):
        st.experimental_rerun()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
        with col2:
            st.metric("RAM", f"{psutil.virtual_memory().percent}%")

        if st.button("Exit", key="exit"):
            st.stop()
        st.info("Alles läuft rund! Als nächstes: Wetter, Fokus Timer, Kalender, News, ToDo-Liste, uvm.")




        
    
        