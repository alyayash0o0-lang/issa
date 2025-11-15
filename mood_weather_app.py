# forecast_shuffle_final.py
import random
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Forecast Shuffle ☁", page_icon="⛅", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .main {
        text-align: center;
        padding-top: 2em;
    }
    button[kind="primary"] {
        border-radius: 12px;
        background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%);
        color: white;
        font-size: 1.1em;
        font-weight: 600;
        transition: 0.2s;
    }
    button[kind="primary"]:hover {
        transform: scale(1.03);
    }
    .forecast-card {
        background: #f9fbff;
        padding: 1.8em;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        display: inline-block;
        margin-top: 20px;
        max-width: 420px;
        width: 85%;
    }
    @media (max-width: 600px) {
        .forecast-card { width: 95%; padding: 1.2em; }
        h1 { font-size: 1.6em !important; }
        h2 { font-size: 1.4em !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("""
<h1 style='color:#2D9CDB;'>☁ Forecast Shuffle ☁</h1>
<p style='color:#555; font-size:1em;'>Tap to reveal today’s mood in the sky.</p>
""", unsafe_allow_html=True)

# --- WEATHER OPTIONS ---
weathers = {
    "☀️ Sunny": {
        "desc": "You’re glowing quietly — let it stay that way.",
        "action": "Send a kind message to someone random."
    },
    "🌧 Rainy": {
        "desc": "It’s okay to slow down. Even rain makes things grow.",
        "action": "Play your favorite comfort song."
    },
    "☁️ Cloudy": {
        "desc": "You might not see the sun yet — but it’s still there.",
        "action": "Write one thing you’re grateful for today."
    },
    "🌪 Stormy": {
        "desc": "Emotions swirling? They’ll pass, like all storms do.",
        "action": "Take 3 deep breaths before checking your phone."
    },
    "🌈 Rainbow": {
        "desc": "You made it through something, didn’t you?",
        "action": "Smile about it — just a little."
    },
    "💨 Windy": {
        "desc": "Change is in the air — don’t resist it.",
        "action": "Do one thing differently today, just for fun."
    }
}

# --- MAIN BUTTON ---
if st.button("🌤 Spin the Sky"):
    choice = random.choice(list(weathers.keys()))
    forecast = weathers[choice]
    
    st.markdown(f"""
    <div class='forecast-card'>
        <h2>{choice}</h2>
        <p style='font-size:1.05em; color:#333;'>{forecast['desc']}</p>
        <p style='font-style:italic; color:#2D9CDB;'>→ Try: {forecast['action']}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888;'>Press the button to shuffle your sky ☁</p>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<br><hr style='opacity:0.3;'>
<p style='font-size:0.8em; color:#777;'>
Made for someone special — because every sky tells a story 🌦
</p>
""", unsafe_allow_html=True)

