import streamlit as st
from datetime import datetime, timedelta
import calendar
import json
from pathlib import Path

# ════════════════════════════════════════════════════════════════
# PAGE CONFIG & THEME
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Mood Weather Calendar 🌤",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ════════════════════════════════════════════════════════════════
# RESPONSIVE CSS STYLING
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    [data-testid="stMain"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    .main {
        padding: 2rem 1rem !important;
    }
    
    /* Title Styling */
    h1 {
        text-align: center;
        color: #ffffff;
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        letter-spacing: -1px;
    }
    
    h2 {
        text-align: center;
        color: rgba(255,255,255,0.95);
        font-size: clamp(1.3rem, 5vw, 2rem);
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: clamp(0.9rem, 3vw, 1.3rem);
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        max-width: 500px;
        display: block;
        margin: 0 auto 2rem auto;
        padding: 1.2rem 2rem;
        border-radius: 20px;
        background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%);
        color: black;
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        font-weight: 600;
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(47, 128, 237, 0.4);
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        text-transform: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(47, 128, 237, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-2px);
    }
    
    /* Weather Card */
    .weather-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: clamp(1.5rem, 5vw, 2.5rem);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        max-width: 600px;
        margin: 0 auto 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .weather-emoji {
        text-align: center;
        font-size: clamp(3rem, 15vw, 6rem);
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .weather-title {
        text-align: center;
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        color: #2D9CDB;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    .weather-description {
        text-align: center;
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        color: #333;
        line-height: 1.8;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .weather-action {
        text-align: center;
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: clamp(1rem, 3vw, 1.5rem);
        border-radius: 15px;
        font-size: clamp(0.95rem, 2.2vw, 1.1rem);
        font-weight: 600;
        font-style: italic;
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);
        margin-top: 1.5rem;
    }
    
    /* Calendar Styling */
    .calendar-container {
        padding: clamp(2rem, 5vw, 3rem);
        border-radius: 30px;
        max-width: 700px;
        margin: 0 auto 2rem auto;
    }
    
    .calendar-day-header {
        text-align: center;
        font-weight: 700;
        color: #ffffff;
        padding: 0.8rem;
        font-size: clamp(0.75rem, 2vw, 0.95rem);
    }
    
    .back-btn {
        text-align: center;
        margin-top: 2rem;
    }
    
    .message-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: clamp(2rem, 5vw, 3rem);
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        max-width: 600px;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .message-emoji {
        text-align: center;
        font-size: clamp(3rem, 15vw, 5rem);
        margin-bottom: 1.5rem;
    }
    
    .message-title {
        text-align: center;
        font-size: clamp(1.5rem, 4vw, 2rem);
        color: #2D9CDB;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .message-text {
        text-align: center;
        font-size: clamp(1rem, 2.5vw, 1.15rem);
        color: #333;
        line-height: 1.8;
        margin-bottom: 1.5rem;
    }
    
    .action-box {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: clamp(1rem, 3vw, 1.5rem);
        border-radius: 15px;
        text-align: center;
        font-size: clamp(0.95rem, 2.2vw, 1.1rem);
        font-weight: 600;
        font-style: italic;
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: clamp(0.75rem, 2vw, 0.95rem);
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 300;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #56CCF2;
    
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# MOODS DATA
# ════════════════════════════════════════════════════════════════
MOODS = {
    "☀️ Sunny": {
        "emoji": "☀️",
        "description": "You're glowing quietly, spreading warmth with your presence.",
        "action": "Share your light with someone who needs it today."
    },
    "🌧️ Rainy": {
        "emoji": "🌧️",
        "description": "Sometimes we all need to let our feelings pour out.",
        "action": "Allow yourself to feel, then watch the rainbow appear."
    },
    "☁️ Cloudy": {
        "emoji": "☁️",
        "description": "You're in a thoughtful mood, reflective and calm.",
        "action": "Take a moment to clear your mind with a quiet activity."
    },
    "🌪️ Stormy": {
        "emoji": "🌪️",
        "description": "Your emotions are intense right now, and that's okay.",
        "action": "Channel this energy into something creative or physical."
    },
    "🌈 Rainbow": {
        "emoji": "🌈",
        "description": "You're feeling blessed and full of hope.",
        "action": "Celebrate this moment and share your joy with others."
    },
    "💨 Windy": {
        "emoji": "💨",
        "description": "You're energetic and restless, ready for change.",
        "action": "Embrace this momentum and try something new today."
    }
}

# ════════════════════════════════════════════════════════════════
# DATA MANAGEMENT
# ════════════════════════════════════════════════════════════════
def load_mood_data():
    """Load mood data from JSON file"""
    mood_file = Path("mood_journal.json")
    if mood_file.exists():
        try:
            with open(mood_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_mood_data():
    """Save mood data to JSON file"""
    with open("mood_journal.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.mood_data, f, ensure_ascii=False, indent=2)

def get_mood_for_date(date_str):
    """Get mood for specific date"""
    return st.session_state.mood_data.get(date_str, None)

def save_mood_for_date(date_str, mood_key):
    """Save mood for specific date"""
    st.session_state.mood_data[date_str] = mood_key
    save_mood_data()

def delete_mood_for_date(date_str):
    """Delete mood for specific date"""
    if date_str in st.session_state.mood_data:
        del st.session_state.mood_data[date_str]
        save_mood_data()

def get_calendar_days(year, month):
    """Get calendar days for month (proper Monday-Sunday alignment)"""
    first_day_obj = datetime(year, month, 1)
    first_weekday = first_day_obj.weekday()  # 0=Monday

    # Get number of days in month
    if month == 12:
        last_day = 31
    else:
        last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day

    # Create calendar grid list
    days = []
    for _ in range(first_weekday):
        days.append(None)
    for day in range(1, last_day + 1):
        days.append(day)

    return days

# ════════════════════════════════════════════════════════════════
# INITIALIZE SESSION STATE
# ════════════════════════════════════════════════════════════════
if "current_page" not in st.session_state:
    st.session_state.current_page = "calendar"

if "selected_date" not in st.session_state:
    st.session_state.selected_date = None

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

if "current_month" not in st.session_state:
    st.session_state.current_month = datetime.now()

if "mood_data" not in st.session_state:
    st.session_state.mood_data = {}

# ════════════════════════════════════════════════════════════════
# PAGE: CALENDAR
# ════════════════════════════════════════════════════════════════
def show_calendar_page():
    st.markdown("""
        <h1>🌤️ MOOD WEATHER</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p class="subtitle">Track your mood by selecting a date 📅</p>
    """, unsafe_allow_html=True)
    
    # Load mood data once
    if "mood_data_loaded" not in st.session_state:
        st.session_state.mood_data = load_mood_data()
        st.session_state.mood_data_loaded = True
    
    # Month navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Prev", use_container_width=True, key="prev_month"):
            if st.session_state.current_month.month == 1:
                st.session_state.current_month = st.session_state.current_month.replace(year=st.session_state.current_month.year - 1, month=12)
            else:
                st.session_state.current_month = st.session_state.current_month.replace(month=st.session_state.current_month.month - 1)
            st.rerun()
    
    with col2:
        month_str = st.session_state.current_month.strftime("%B %Y")
        st.markdown(f"<h2 style='margin: 0;'>{month_str}</h2>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ▶", use_container_width=True, key="next_month"):
            if st.session_state.current_month.month == 12:
                st.session_state.current_month = st.session_state.current_month.replace(year=st.session_state.current_month.year + 1, month=1)
            else:
                st.session_state.current_month = st.session_state.current_month.replace(month=st.session_state.current_month.month + 1)
            st.rerun()
    
    # Calendar grid
    st.markdown("<div class='calendar-container'>", unsafe_allow_html=True)
    
    # Day headers (Monday to Sunday)
    day_headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, day in enumerate(day_headers):
        with cols[i]:
            st.markdown(f"<div class='calendar-day-header'>{day}</div>", unsafe_allow_html=True)
    
    # Get calendar days for current month
    year = st.session_state.current_month.year
    month = st.session_state.current_month.month
    days = get_calendar_days(year, month)
    today = datetime.now().date()
    
    # Display calendar grid (max 6 weeks)
    for week_idx in range(0, len(days), 7):
        week_days = days[week_idx:week_idx + 7]
        cols = st.columns(7)
        
        for day_idx, day in enumerate(week_days):
            with cols[day_idx]:
                if day is None:
                    # Empty cell
                    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
                else:
                    date_obj = datetime(year, month, day).date()
                    date_str = date_obj.strftime("%Y-%m-%d")
                    
                    # Get mood for this date
                    mood = get_mood_for_date(date_str)
                    mood_emoji = MOODS[mood]["emoji"] if mood else ""
                    
                    # Button styling
                    button_text = f"{day}\n{mood_emoji}" if mood_emoji else str(day)
                    
                    if st.button(button_text, key=f"date_{date_str}", use_container_width=True):
                        st.session_state.selected_date = date_str
                        st.session_state.current_page = "mood_selector"
                        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="footer">
            <p>Click on any date to record your mood ✨</p>
        </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE: MOOD SELECTOR
# ════════════════════════════════════════════════════════════════
def show_mood_selector_page():
    st.markdown("""
        <h1>🌤️ SELECT YOUR MOOD</h1>
    """, unsafe_allow_html=True)
    
    # Display selected date
    date_obj = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d")
    date_display = date_obj.strftime("%A, %B %d, %Y")
    st.markdown(f"""
        <p class="subtitle">How are you feeling on {date_display}?</p>
    """, unsafe_allow_html=True)
    
    # Mood selector grid
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    # Create mood selection buttons in grid
    cols = st.columns(3)
    mood_list = list(MOODS.keys())
    
    for idx, mood_key in enumerate(mood_list):
        mood_data = MOODS[mood_key]
        with cols[idx % 3]:
            if st.button(
                f"{mood_data['emoji']}\n{mood_key.split(' ')[0]}",
                key=f"mood_{mood_key}",
                use_container_width=True,
                help=mood_data['description']
            ):
                st.session_state.selected_mood = mood_key
                save_mood_for_date(st.session_state.selected_date, mood_key)
                st.session_state.current_page = "mood_result"
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Back button
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back to Calendar", use_container_width=True):
        st.session_state.current_page = "calendar"
        st.session_state.selected_date = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE: MOOD RESULT
# ════════════════════════════════════════════════════════════════
def show_mood_result_page():
    mood_key = st.session_state.selected_mood
    mood_info = MOODS[mood_key]
    
    st.markdown("""
        <h1>✨ YOUR MOOD FOR TODAY</h1>
    """, unsafe_allow_html=True)
    
    # Display date
    date_obj = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d")
    date_display = date_obj.strftime("%A, %B %d, %Y")
    st.markdown(f"""
        <p class="subtitle">{date_display}</p>
    """, unsafe_allow_html=True)
    
    # Display mood card
    st.markdown(f"""
    <div class="message-card">
        <div class="message-emoji">{mood_info['emoji']}</div>
        <div class="message-title">{mood_key}</div>
        <div class="message-text">{mood_info['description']}</div>
        <div class="action-box">→ Try: {mood_info['action']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_page = "mood_selector"
            st.rerun()
    
    with col2:
        if st.button("🗑️ Delete", use_container_width=True, help="Delete this mood entry"):
            delete_mood_for_date(st.session_state.selected_date)
            st.success("Mood entry deleted!")
            st.session_state.current_page = "calendar"
            st.session_state.selected_date = None
            st.session_state.selected_mood = None
            st.rerun()
    
    with col3:
        if st.button("Back to Calendar", use_container_width=True):
            st.session_state.current_page = "calendar"
            st.session_state.selected_date = None
            st.session_state.selected_mood = None
            st.rerun()

# ════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ════════════════════════════════════════════════════════════════
if st.session_state.current_page == "calendar":
    show_calendar_page()
elif st.session_state.current_page == "mood_selector":
    show_mood_selector_page()
elif st.session_state.current_page == "mood_result":
    show_mood_result_page()
