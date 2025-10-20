import streamlit as st
import time

def init_state():
    st.session_state.setdefault('timer_running', False)
    st.session_state.setdefault("timer_end_ts", 0)
    st.session_state.setdefault("timer_label", "Fokus")


def start_timer(minutes: int, label: str = "Fokus"):
    st.session_state.timer_running = True
    st.session_state.timer_end_ts = time.time() + minutes * 60
    st.session_state.timer_label = label

def reset_timer():
    st.session_state.timer_running = False
    st.session_state.timer_end_ts = 0

def render_timer():
    init_state()
    st.subheader("Fokus Timer(Pomodoro)")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        minutes = st.number_input("Dauer (Minuten)", min_value=1, max_value=120, value=25, step=1)
    with col2:
        if st.button("Start", key="start_timer"):
            start_timer(minutes)
    with col3:
        if st.button("Reset", key="reset_timer"):
            reset_timer()

    if st.session_state.timer_running:
        remaining = int(st.session_state.timer_end_ts - time.time())
        if remaining <= 0:
            st.success(f"{st.session_state.timer_label} Zeit ist um!")
            reset_timer()
        else:
            mm, ss = divmod(remaining, 60)
            st.metric(st.session_state.timer_label, f"Timer läuft: {mm:02}:{ss:02} verbleibend")