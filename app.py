import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. THE VISIBILITY SHIELD & LUXURY STYLING ---
st.set_page_config(page_title="Elite Performance Hub", layout="wide")

def apply_titanium_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    # Using double curly braces {{ }} to escape CSS within the f-string
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* GLOBAL RESET: FORCE DARK THEME */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        
        /* LABEL VISIBILITY */
        label, .stWidget label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 8px !important; }}

        /* THE BRUTE-FORCE INPUT SHIELD (Fixes White-on-White) */
        input, textarea, select, 
        div[data-baseweb="input"], 
        div[data-baseweb="select"], 
        div[data-baseweb="base-input"],
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[role="combobox"],
        .stTextInput>div>div>input {{
            background-color: #0a0a0a !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 12px !important;
            -webkit-text-fill-color: #ffffff !important; /* Mobile/Safari visibility fix */
        }}

        /* APP BACKGROUND & NAVIGATION */
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}

        /* DATA CARDS */
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_titanium_styling()

# --- 2. DATA PERSISTENCE & LOGIN GATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# SAFE DATABASE INITIALIZATION
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "7": {
            "first_name": "Vinícius", "last_name": "Júnior", "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low", "history": "ACL Rehab (2025)"},
            "roadmap": []
        }
    }

if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    # FIXED LOGIN: Using a form ensures inputs are captured correctly on submit
    with st.form("login_form"):
        u = st.text_input("Username", placeholder="Enter username", key="auth_u")
        p = st.text_input("Password", type="password", placeholder="Enter password", key="auth_p")
        submitted = st.form_submit_button("Unlock Portal")
        if submitted:
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid credentials.")
    st.stop()

# --- 3. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception: pass

# --- 4. NAVIGATION & MASTER PICK-LIST [cite: 3.1