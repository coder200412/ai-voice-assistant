import streamlit as st
import pyttsx3
import os
import datetime
from assistant_backend import listen, get_current_city, get_current_location_weather, get_weather_by_coords,get_coordinates

st.set_page_config(page_title="Jarvis Voice Assistant", page_icon="🤖", layout="wide")


if "command_text" not in st.session_state:
    st.session_state.command_text = "Click to Start Listening"
if "spoken_greeting" not in st.session_state:
    st.session_state.spoken_greeting = False
if "city" not in st.session_state:
    st.session_state.city = get_current_city()
if "history" not in st.session_state:
    st.session_state.history = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if not st.session_state.spoken_greeting:
    speak("Hi, I am your assistant")
    st.session_state.spoken_greeting = True


bg_css = """
    background: radial-gradient(circle at center, rgba(20,40,80,0.9) 0%, rgba(10,20,40,0.9) 100%);
    color: white;
""" if st.session_state.dark_mode else "background: white; color: black;"

st.markdown(f"""
    <style>
    html, body {{
        height: 100%;
        margin: 0;
        {bg_css}
        overflow-x: hidden;
        font-family: 'Segoe UI', sans-serif;
    }}
    .glass-bg {{
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(0, 128, 255, 0.3);
        width: 280px;
        height: 280px;
        margin: auto;
        margin-top: 3%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: glow 3s infinite alternate;
    }}
    @keyframes glow {{
        0% {{ box-shadow: 0 0 30px rgba(0, 128, 255, 0.3); }}
        100% {{ box-shadow: 0 0 50px rgba(0, 255, 255, 0.6); }}
    }}
    .circle-text {{
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        animation: pulseText 1.8s infinite;
        padding: 10px;
    }}
    .stButton>button {{
        border-radius: 20px;
        background-color: #4A90E2;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.5);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }}
    .stButton>button:hover {{
        background-color: #7B61FF;
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)


st.sidebar.markdown("🌓 **Appearance**")
st.session_state.dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)


st.markdown('<div class="glass-bg">', unsafe_allow_html=True)
st.markdown(f'<div class="circle-text">{st.session_state.command_text}</div>', unsafe_allow_html=True)

if st.button("🎙️ Listen"):
    st.session_state.command_text = "Listening..."
    command = listen()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if command:
        st.session_state.command_text = command
        speak(f"You said: {command}")
        st.session_state.history.append(f"[{timestamp}] {command}")
    else:
        st.session_state.command_text = "Sorry, I didn't catch that."
        speak("Sorry, I didn't catch that.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🌦️ Weather Assistant")

with st.container():
    st.markdown("""
        <div style='padding: 15px; border-radius: 10px; background-color: rgba(255,255,255,0.07); box-shadow: 0 0 8px rgba(0,128,255,0.2);'>
    """, unsafe_allow_html=True)

    city_input = st.text_input("Enter city name", placeholder="e.g., Guntur, Delhi, Tokyo")
    if st.button("🔎 Check Weather"):
        if city_input.strip():
            speak(f"Fetching weather for {city_input}")
            get_weather_by_coords(city_input.strip())
        else:
            speak("Checking weather for your current location.")
            get_current_location_weather()

    st.markdown("</div>", unsafe_allow_html=True)




st.markdown("---")
st.subheader("🚀 Quick Launch")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌐 Open Chrome"):
        os.system("start chrome")

with col2:
    if st.button("📧 Open Mail"):
        os.system("start HxOutlook.exe")

with col3:
    if st.button("📁 Open File Explorer"):
        os.system("explorer.exe")


st.markdown("---")
st.subheader("🕒 Command History")

if st.session_state.history:
    for item in reversed(st.session_state.history[-10:]):
        st.markdown(f"• {item}")
    st.download_button("📥 Export History", data="\n".join(st.session_state.history), file_name="jarvis_history.txt")
else:
    st.info("No commands yet.")
