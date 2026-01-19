import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & VISIBILITY SHIELD ---
st.set_page_config(page_title="Elite Performance | Command Center", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* 1. FORCE DARK THEME & WHITE TEXT */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        
        /* 2. ELITE GREEN LABELS (High visibility) */
        label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 8px !important; }}

        /* 3. INPUT BOXES: FORCE BLACK BACKGROUND (Fixes 'White on White' bug) */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #0c0c0c !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 12px !important;
            -webkit-text-fill-color: #ffffff !important;
        }}
        
        /* 4. CINEMATIC BACKGROUND */
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        /* 5. LUXURY CARDS */
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        
        /* 6. NAVIGATION TABS */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}

        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. SESSION SECURITY & MASTER DATABASE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# SAFE MASTER DATABASE INITIALIZATION
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "7": {
            "first_name": "Vinícius", "last_name": "Júnior", "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low", "history": "ACL Rehab (2025)"},
            "roadmap": []
        }
    }

# --- 3. LOGIN GATE (REBUILT TO PREVENT PRE-FILL) ---
if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    # Added random seed to key to prevent browser autocomplete issues
    u = st.text_input("Username", value="", placeholder="Enter admin username", key="auth_user_sec")
    p = st.text_input("Password", type="password", value="", placeholder="Enter system password", key="auth_pass_sec")
    
    if st.button("Access Portal"):
        if u == "admin" and p == "owner2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please type carefully.")
    st.stop()

# --- 4. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception: pass

# --- 5. NAVIGATION & MASTER PICK-LIST ---
tabs = st.tabs(["📊 Overview", "🏃 Squad Registry", "🩺 Medical Hub", "🤖 Virtual Coach", "🎥 Performance Audit", "📅 Roadmap"])
p_options = {uid: f"#{d['shirt_number']} {d['first_name']} {d['last_name']}" for uid, d in st.session_state.profiles.items()}

with tabs[0]: # OVERVIEW (No-