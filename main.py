import streamlit as st
import time
from PIL import Image
import base64

# -------------------------
# Pixel UI (font + button)
# -------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Press Start 2P&display=swap');

html, body, [class*="css"]  {
    font-family: 'Press Start 2P', cursive;
}

button {
    background-color: #ff6b6b !important;
    color:white !important;
    border-radius:12px !important;
    padding:10px 20px !important;
}

button:hover {
    background-color:#ff4c4c !important;
}

div[data-testid="stProgressBar"] > div > div {
    background-color:#ff6b6b;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Pixel title
# -------------------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("title.png", use_container_width=True)

# -------------------------
# Session state
# -------------------------
if "cooking" not in st.session_state:
    st.session_state.cooking = False

selection_placeholder = st.empty()

# -------------------------
# Animation frames
# -------------------------
frames = [
    "steak_frames/frame1.png",
    "steak_frames/frame2.png",
    "steak_frames/frame3.png"
]

# -------------------------
# Alarm
# -------------------------
def play_alarm():
    with open("alarm.mp3", "rb") as f:
        audio_bytes = f.read()

    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)

# -------------------------
# Cooking times
# -------------------------
def get_base_time(doneness):
    times = {
        "Rare": 3,
        "Medium Rare": 4,
        "Medium": 5,
        "Medium Well": 6,
        "Well Done": 8
    }
    return times[doneness]

def thickness_multiplier(thickness):
    multipliers = {
        "Thin": 0.8,
        "Normal": 1,
        "Thick": 1.3
    }
    return multipliers[thickness]

# -------------------------
# Selection screen
# -------------------------
if not st.session_state.cooking:

    with selection_placeholder.container():

        st.header("Select steak thickness")

        thickness = st.selectbox(
            "Thickness",
            ["Thin", "Normal", "Thick"]
        )

        st.header("Select doneness")

        doneness = st.selectbox(
            "Doneness",
            ["Rare", "Medium Rare", "Medium", "Medium Well", "Well Done"]
        )

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            if st.button("Start Cooking"):
                st.session_state.cooking = True
                st.session_state.thickness = thickness
                st.session_state.doneness = doneness
                selection_placeholder.empty()
                st.rerun()

# -------------------------
# Cooking screen
# -------------------------
if st.session_state.cooking:

    thickness = st.session_state.thickness
    doneness = st.session_state.doneness

    base_time = get_base_time(doneness)
    multiplier = thickness_multiplier(thickness)

    total_minutes = base_time * multiplier
    total_seconds = int(total_minutes * 60)

    st.markdown(
    "<p style='text-align:center'>🔥 Cook at heat level: 7/10</p>",
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        image_placeholder = st.empty()
        timer_placeholder = st.empty()
        progress_bar = st.progress(0)

    frame_index = 0
    start_time = time.time()

    while True:

        elapsed = int(time.time() - start_time)
        remaining = total_seconds - elapsed

        if remaining <= 0:
            break

        mins = remaining // 60
        secs = remaining % 60

        timer_placeholder.markdown(
        f"<h1 style='text-align:center; font-size:50px'>{mins:02}:{secs:02}</h1>",
        unsafe_allow_html=True
        )

        progress = elapsed / total_seconds
        progress_bar.progress(min(progress, 1.0))

        img = Image.open(frames[frame_index])
        image_placeholder.image(img, width=320)

        frame_index = (frame_index + 1) % len(frames)

        time.sleep(0.2)

    # final timer
    timer_placeholder.markdown(
    "<h1 style='text-align:center; font-size:50px'>00:00</h1>",
    unsafe_allow_html=True
    )

    plate = Image.open("steak_frames/plate.png")
    image_placeholder.image(plate, width=320)

    progress_bar.progress(1.0)

    st.success("🥩 Your steak is ready!")

    play_alarm()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("Exit"):
            st.session_state.clear()
            st.rerun()