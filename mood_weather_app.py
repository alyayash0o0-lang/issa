import streamlit as st
from datetime import datetime, timedelta
import calendar
import json
import hashlib
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

# Add mobile viewport meta to help mobile browsers scale correctly
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# RESPONSIVE CSS STYLING
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        margin: 0;
    }

    [data-testid="stMain"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }

    .main { padding: 2rem 1rem !important; }

    /* Titles */
    h1 { text-align: center; color: #ffffff; font-size: clamp(1.6rem, 7vw, 3.2rem); font-weight:700; margin-bottom:0.5rem; text-shadow:0 4px 15px rgba(0,0,0,0.18); }
    h2 { text-align:center; color: rgba(255,255,255,0.95); font-size: clamp(1.05rem, 4.2vw, 1.9rem); font-weight:600; margin:1rem 0; }
    .subtitle { text-align:center; color: rgba(255,255,255,0.9); font-size: clamp(0.85rem, 3vw, 1.15rem); margin-bottom:1.5rem; font-weight:300; }

    /* Cards and containers should resize */
    .weather-card, .message-card { max-width: 720px; width: 96%; margin: 0.8rem auto; border-radius: 20px; }

    /* Button Styling - allow wrapping and scale down on mobile */
    .stButton > button {
        width: 100%; max-width: 520px; display:block; margin: 0.6rem auto; padding: 0.9rem 1rem; border-radius: 14px;
        background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%); font-size: 1rem; font-weight:600; border:none; cursor:pointer;
        box-shadow: 0 8px 25px rgba(47, 128, 237, 0.18); transition: all 0.2s ease; word-break: break-word; line-height:1.1;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(47,128,237,0.2); }

    /* Weather / message cards */
    .weather-card, .message-card { background: rgba(255,255,255,0.95); backdrop-filter: blur(8px); padding: 1.2rem; box-shadow: 0 18px 50px rgba(0,0,0,0.12); border: 1px solid rgba(255,255,255,0.12); }
    .weather-emoji, .message-emoji { font-size: clamp(2.4rem, 12vw, 4.5rem); text-align:center; margin-bottom:0.8rem; }
    .weather-title, .message-title { text-align:center; color:#2D9CDB; font-weight:700; margin-bottom:0.6rem; }
    .weather-description, .message-text { text-align:center; color:#333; line-height:1.6; margin-bottom:0.6rem; }
    .action-box { background: linear-gradient(90deg,#f093fb 0%,#f5576c 100%); color:white; padding:0.7rem; border-radius:12px; text-align:center; font-weight:600; }

    /* Calendar container - allow full width but keep spacing */
    .calendar-container { padding: 1rem; border-radius: 18px; max-width: 980px; width: 98%; margin: 0.6rem auto 1rem auto; }
    .calendar-day-header { text-align:center; font-weight:700; color:#ffffff; padding:0.35rem 0; font-size: clamp(0.6rem, 2.2vw, 0.9rem); }
    background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%);


    .back-btn { text-align:center; margin-top:1rem; }

    /* Smaller helpers */
    .footer { text-align:center; color: rgba(255,255,255,0.85); font-size: clamp(0.7rem, 1.9vw, 0.95rem); margin-top:2rem; padding-top:1rem; border-top: 1px solid rgba(255,255,255,0.08); }

    .info-box { background: rgba(255,255,255,0.06); border-left: 4px solid #56CCF2; padding:0.6rem 0.9rem; border-radius:8px; color: #fff; }

    /* Make calendar buttons compact and wrap content neatly */
    .stButton > button[title] { text-align:center; }

    /* Media queries for narrow screens */
    @media (max-width: 900px) {
        .main { padding: 1.4rem 0.6rem !important; }
        .calendar-container { padding: 0.6rem; }
        .stButton > button { padding: 0.7rem 0.6rem; font-size: 0.95rem; border-radius: 12px; }
    }

    @media (max-width: 600px) {
        h1 { font-size: clamp(1.2rem, 9vw, 2.2rem); }
        h2, .subtitle { font-size: 0.95rem; }
        .calendar-day-header { font-size: 0.7rem; }
        .stButton > button { padding: 0.6rem 0.5rem; font-size: 0.88rem; }
        .weather-card, .message-card { padding: 0.9rem; }
    }

    /* Very small phones - compress spacing */
    @media (max-width: 420px) {
        .stButton > button { padding: 0.5rem 0.45rem; font-size: 0.82rem; }
        .calendar-day-header { padding: 0.25rem 0; }
        .footer { margin-top:1rem; }
    }

</style>
""", unsafe_allow_html=True)
    
st.markdown("""
<style>
    /* Calendar HTML table styles for responsive touch on mobile */
    .calendar-table { width:100%; border-collapse: collapse; margin-top: 0.6rem; }
    .calendar-table thead th { padding: 6px 4px; font-weight:700; color:#ffffff; text-align:center; }
    .calendar-cell { width:14.2857%; padding:6px; vertical-align: top; }
    /* Date box: make visible rounded white cards so dates are tappable and readable */
    .background: linear-gradient{(90deg, #56CCF2 0%, #2F80ED 100%); font-size: 1rem; font-weight:600; border:none; cursor:pointer; }
    .box-shadow: 0 8px 25px rgba{(47, 128, 237, 0.18); transition: all 0.2s ease; word-break: break-word; line-height:1.1; }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(47,128,237,0.2); }
    .date-link { display:flex; flex-direction:column; align-items:center; justify-content:center; text-decoration:none; color:#061124; padding:10px 12px; border-radius:12px; background: rgba(255,255,255,0.98); min-height:64px; box-shadow: 0 8px 20px rgba(8,30,60,0.08); border: 1px solid rgba(0,0,0,0.04); text-decoration: none; }
    .date-link:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(8,30,60,0.10); }
    .date-num { font-weight:700; font-size:0.95rem; color: #061124; text-decoration: none}
    .date-emoji { font-size:1.15rem; margin-top:6px; }
    .calendar-cell.empty { background: transparent; }
    .calendar-cell.today .date-link { outline: 2px solid rgba(255,255,255,0.16); box-shadow: 0 6px 18px rgba(0,0,0,0.08); }

    @media (max-width: 600px) {
        .calendar-table { display:block; overflow-x:auto; white-space:nowrap; }
        .calendar-table thead, .calendar-table tbody, .calendar-table tr { display:inline-block; vertical-align:top; }
        .calendar-table tr { margin-right: 8px; }
        .calendar-cell { display:block; width: 100%; }
        .date-link { min-width: 72px; min-height:56px; padding:8px 10px; border-radius:10px; }
    }
</style>
""", unsafe_allow_html=True)
# ════════════════════════════════════════════════════════════════
# MOODS DATA
# ════════════════════════════════════════════════════════════════
MOODS = {
    "☀️ Sunny": {
        "emoji": "☀️",
            "description": "",
        "actions": [
            "Share your light with someone who needs it today.",
            "Write a short thank-you note to someone who made you smile.",
            "Take a five-minute walk and notice small beautiful things.",
            "Call a friend and spread some sunshine.",
            "Do one kind thing for yourself: make your favorite drink.",
            "Spend a moment noticing three things you're grateful for.",
            "Share a compliment with someone nearby.",
            "Start (or finish) a small creative task you've been postponing.",
            "Breathe deeply for two minutes and enjoy the warmth you feel.",
            "Take a photo of something that makes you happy and keep it."
        ]
    },
    "🌧️ Rainy": {
        "emoji": "🌧️",
            "description": "",
        "actions": [
            "Allow yourself to feel, then watch the rainbow appear.",
            "Make a warm drink and sit with your feelings for a moment.",
            "Write down one honest thought and then close the page.",
            "Listen to a song that matches your mood and let it move you.",
            "Draw or doodle how you're feeling for five minutes.",
            "Take a slow, mindful breath and notice how it changes you.",
            "Send a short message to someone you trust.",
            "Step outside briefly and feel the air on your face.",
            "Name three things you can control right now.",
            "Promise yourself one small gentle act before bed."
        ]
    },
    "☁️ Cloudy": {
        "emoji": "☁️",
            "description": "",
        "actions": [
            "Take a moment to clear your mind with a quiet activity.",
            "Write down one intent for the rest of today.",
            "Do a short breathing exercise to steady your thoughts.",
            "Read a paragraph from a book that calms you.",
            "Step outside and notice the clouds—let your mind drift.",
            "Organize one tiny area (desk, drawer) to feel clearer.",
            "Journal one small insight you've had recently.",
            "Try a 3-minute stretch to refresh your body and mind.",
            "Make a simple plan for a peaceful evening.",
            "Sit quietly and observe your breath for two minutes."
        ]
    },
    "🌪️ Stormy": {
        "emoji": "🌪️",
            "description": "",
        "actions": [
            "Channel this energy into something creative or physical.",
            "Do a short workout or move your body to release tension.",
            "Write a raw paragraph—no rules, just to let it out.",
            "Turn up music and dance for three songs.",
            "Squeeze a stress ball or do a grounding exercise.",
            "Take a brisk walk and focus on your surroundings.",
            "Sketch a quick comic to express how you feel.",
            "Practice 5 minutes of focused breathing to calm the storm.",
            "Make a list of actions you can take, then choose one.",
            "Tell yourself: 'This will pass' and breathe slowly."
        ]
    },
    "🌈 Rainbow": {
        "emoji": "🌈",
            "description": "",
        "actions": [
            "Celebrate this moment and share your joy with others.",
            "Write down something good that happened today.",
            "Send a quick 'thinking of you' to someone you care about.",
            "Take a photo of something beautiful and save it.",
            "Treat yourself to a tiny celebration (song, treat, dance).",
            "Share positive news with a friend.",
            "Make a short list of things you're hopeful about.",
            "Do one generous thing without expecting anything back.",
            "Pause and breathe in the good feeling for ten seconds.",
            "Write a one-line note to your future self about today."
        ]
    },
    "💨 Windy": {
        "emoji": "💨",
            "description": "",
        "actions": [
            "Embrace this momentum and try something new today.",
            "Start a small experiment—try a different route or recipe.",
            "Make a quick plan for a change you'd like to try.",
            "Take five minutes to brainstorm new ideas.",
            "Do a micro-task that moves you toward a goal.",
            "Reach out to someone and propose a short meetup.",
            "Switch tasks: do something hands-on to release energy.",
            "Try a short breathing or focus technique to harness energy.",
            "Write down one bold idea and one tiny next step.",
            "Celebrate a small win from today—no matter how small."
        ]
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


def get_daily_action(mood_key: str, date_str: str) -> str:
    """Return a deterministic 'action' string from the mood's actions list for the given date.

    The selection is deterministic per (mood_key, year, month) so each day in the same month
    will receive a shuffled, non-repeating ordering of available actions when possible.
    """
    mood = MOODS.get(mood_key, {})
    actions = mood.get("actions")
    # backward compatibility: if single 'action' exists, return it
    if actions is None:
        return mood.get("action", "")

    # parse date
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return actions[0] if actions else ""

    year = dt.year
    month = dt.month
    day = dt.day

    # deterministic seed per mood + year-month
    seed_str = f"{mood_key}|{year}-{month}"
    seed = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:16], 16)

    rng = __import__("random").Random(seed)
    n_actions = len(actions)

    # number of days in month
    if month == 12:
        days_in_month = 31
    else:
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day

    # create a shuffled list of indices and extend it if needed to cover all days
    indices = list(range(n_actions))
    order = []
    while len(order) < days_in_month:
        block = indices[:]  # copy
        rng.shuffle(block)
        order.extend(block)

    # pick index for this day (1-based day -> 0-based index)
    picked_idx = order[(day - 1) % len(order)]
    return actions[picked_idx]

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
    
    # Calendar grid (HTML table with links for mobile-friendly tapping)
    st.markdown("<div class='calendar-container'>", unsafe_allow_html=True)

    # If user clicked a date link (query param), navigate
    params = st.experimental_get_query_params()
    if 'date' in params and params['date']:
        try:
            selected = params['date'][0]
            st.session_state.selected_date = selected
            st.session_state.current_page = 'mood_selector'
            # clear query params to avoid repeat
            st.experimental_set_query_params()
            st.rerun()
        except Exception:
            pass

    # Day headers (Monday to Sunday)
    day_headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Get calendar days for current month
    year = st.session_state.current_month.year
    month = st.session_state.current_month.month
    days = get_calendar_days(year, month)
    today = datetime.now().date()

    # Build HTML table for the calendar (responsive and touch-friendly)
    table_html = ""
    table_html += "<table class='calendar-table'>"
    # headers
    table_html += "<thead><tr>"
    for d in day_headers:
        table_html += f"<th class='calendar-day-header'>{d}</th>"
    table_html += "</tr></thead>"

    # body rows
    table_html += "<tbody>"
    for week_idx in range(0, len(days), 7):
        week_days = days[week_idx:week_idx + 7]
        table_html += "<tr>"
        for day in week_days:
            if day is None:
                table_html += "<td class='calendar-cell empty'></td>"
            else:
                date_obj = datetime(year, month, day).date()
                date_str = date_obj.strftime("%Y-%m-%d")
                mood = get_mood_for_date(date_str)
                mood_emoji = MOODS[mood]["emoji"] if mood else ""
                today_class = " today" if date_obj == today else ""
                table_html += (
                    f"<td class='calendar-cell{today_class}'>"
                    f"<a class='date-link' href='?date={date_str}'>"
                    f"<div class='date-num'>{day}</div>"
                    f"<div class='date-emoji'>{mood_emoji}</div>"
                    f"</a></td>"
                )
        table_html += "</tr>"
    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="footer">
            <p>Click on any date to record your mood ✨</p>
        </div>
    """, unsafe_allow_html=True)
    # Small invisible marker to confirm deployed CSS/version
    st.markdown("""
        <div style='text-align:center; margin-top:6px; font-size:0.75rem; opacity:0.7'>CSS v2 — responsive</div>
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
    
    # Display mood card (use daily-varying action)
    daily_action = get_daily_action(mood_key, st.session_state.selected_date)
    st.markdown(f"""
    <div class="message-card">
        <div class="message-emoji">{mood_info['emoji']}</div>
        <div class="message-title">{mood_key}</div>
        <div class="message-text">{mood_info['description']}</div>
        <div class="action-box">→ Try: {daily_action}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_page = "mood_selector"
            st.rerun()
    
    with col2:
        if st.button("🗑️ Delete", use_container_width=True):
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











