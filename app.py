import streamlit as st
import cv2
import pyautogui
from win32api import GetSystemMetrics
import numpy as np
import time
import os
import threading

# Streamlit UI
st.set_page_config(page_title="Screen Recorder", page_icon="📽️", layout="centered")


st.markdown("""
<style>
    * {
        font-family: 'Emblema One', cursive;       
    }
    
  
</style>
""", unsafe_allow_html=True)

st.markdown("<link href='https://fonts.googleapis.com/css2?family=Emblema+One&display=swap' rel='stylesheet'>", unsafe_allow_html=True)


# Initialize session state
if "recording" not in st.session_state:
    st.session_state.recording = False
if "thread" not in st.session_state:
    st.session_state.thread = None

# Function to start screen recording
def screen_record(duration, output_filename):
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    dim = (width, height)

    f = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(output_filename, f, 30.0, dim)

    st.session_state.recording = True
    st.toast("🎥 Recording started! Click 'Stop Recording' to stop.")

    start_time = time.time()
    progress_bar = st.progress(0)

    while st.session_state.recording and (time.time() - start_time) < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output.write(frame)

        # Update progress bar
        elapsed_time = time.time() - start_time
        progress = int((elapsed_time / duration) * 100)
        progress_bar.progress(progress)

    output.release()
    cv2.destroyAllWindows()

    if st.session_state.recording:
        st.toast(f"✅ Recording saved at: {output_filename}")
        st.video(output_filename)

    st.session_state.recording = False  # Reset the recording state



st.markdown(
    """
    <h1 style="text-align:center; color:#FF5733; font-family: 'Emblema One', cursive">📽️ Screen Recorder App</h1>
    <p style="text-align:center; font-size:18px;">Record your screen with ease using this modern and simple Streamlit app.</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# Input Fields (Save Location & File Name)
col1, col2 = st.columns(2)
with col1:
    save_folder = st.text_input("📂 Enter Save Location:", os.getcwd())

with col2:
    file_name = st.text_input("🎬 Enter File Name:", "recorded_video.mp4")

output_path = os.path.join(save_folder, file_name)

# Select Recording Duration
duration = st.slider("⏳ Select Recording Duration (seconds)", min_value=5, max_value=300, value=12)

# Buttons for Start and Stop
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Recording", use_container_width=True, disabled=st.session_state.recording):
        if os.path.exists(save_folder):
            st.session_state.recording = True
            st.session_state.thread = threading.Thread(target=screen_record, args=(duration, output_path))
            st.session_state.thread.start()
        else:
            st.error("❌ Invalid save location! Please enter a valid folder path.")

with col2:
    if st.button("⏹ Stop Recording", use_container_width=True, disabled=not st.session_state.recording):
        st.session_state.recording = False
        st.toast("🛑 Recording stopped!")

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    div[data-testid="stButton"] button {
        background-color: #FF5733;
        color: white;
        border-radius: 10px;
        padding: 8px;
    }
    div[data-testid="stButton"]:hover button {
        background-color: #C70039;
    }
    </style>
    """,
    unsafe_allow_html=True
)