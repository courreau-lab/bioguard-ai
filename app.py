import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. PERFORMANCE CONFIGURATION ---
st.set_page_config(page_title="Elite Command Center", layout="wide")

def apply_platinum_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 8px !important; }}
        
        /* THE VISIBILITY SHIELD: FORCED DARK INPUTS */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], 
        .stTextInput>div>div>input, div[data-baseweb="base-input"] {{
            background-color: #0a0a0a !important; color: #ffffff !important;
            border: 2px solid #00ab4e !important; border-radius: 12px !important;
        }}
        
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_platinum_styling()

# --- 2. PERSISTENT DATA ENGINE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "profiles" not in st.session_state:
    st.session_state.profiles = {} # Storage for the full squad

# --- 3. PERSISTENT LOGIN GATE ---
if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    with st.form("persistent_login"):
        u = st.text_input("Username", value="", key="u_field")
        p = st.text_input("Password", type="password", value="", key="p_field")
        if st.form_submit_button("Unlock Command Center"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun() # Forces session state to lock in
            else: st.error("Access Denied.")
    st.stop()

# --- 4. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception: pass

# --- 5. NAVIGATION HUB ---
tabs = st.tabs(["📊 Overview", "🏃 Squad Registry", "🩺 Medical Hub", "🤖 Virtual Coach", "📅 Roadmap"])

with tabs[0]: # SQUAD OVERVIEW
    st.header("🏆 Full Squad Status")
    if not st.session_state.profiles:
        st.info("No athletes registered yet. Go to Squad Registry to add your first member.")
    else:
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='kpi-card'>Squad Size<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
        c2.markdown("<div class='kpi-card'>System Tier<br><span class='kpi-val'>Elite Paid</span></div>", unsafe_allow_html=True)
        st.divider()
        st.table([{"Name": f"{d['first']} {d['last']}", "Team": d['team'], "Shirt": d['num'], "Risk": d['medical']['risk']} for d in st.session_state.profiles.values()])

with tabs[1]: # SQUAD REGISTRY (Saves Data Permanently)
    st.header("🏃 Athlete & Team Registration")
    with st.form("squad_reg_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        f = col1.text_input("First Name")
        l = col2.text_input("Last Name")
        t = col1.text_input("Team Name (e.g. U15 Academy)")
        n = col2.text_input("Shirt Number")
        if st.form_submit_button("Save to My Squad"):
            if f and l and n and t:
                # Keyed by shirt number to prevent duplication
                st.session_state.profiles[n] = {
                    "first": f, "last": l, "num": n, "team": t,
                    "medical": {"age": 0, "weight": 0.0, "risk": "Low"},
                    "roadmap": []
                }
                st.success(f"Successfully saved {f} to {t} squad."); st.rerun()

with tabs[2]: # MEDICAL HUB
    st.header("🩺 Athlete Clinical Profile")
    if not st.session_state.profiles: st.warning("Please register a member first."); st.stop()
    
    # CHOOSE MEMBER FROM SQUAD
    p_choice = st.selectbox("Select Athlete", options=list(st.session_state.profiles.keys()), 
                            format_func=lambda x: f"#{st.session_state.profiles[x]['num']} {st.session_state.profiles[x]['first']} ({st.session_state.profiles[x]['team']})")
    
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        player = st.session_state.profiles[p_choice]
        st.subheader(f"Biometrics: {player['first']}")
        new_risk = st.selectbox("Current Risk Status", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(player['medical']['risk']))
        if st.button("Update Clinical Data"):
            st.session_state.profiles[p_choice]['medical']['risk'] = new_risk