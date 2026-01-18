import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. LUXURY INTERFACE STYLING ---
st.set_page_config(page_title="Elite Performance Hub", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        label {{ color: #00ab4e !important; font-weight: 700 !important; }}
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: #000000 !important; color: #ffffff !important; border: 2px solid #00ab4e !important; border-radius: 12px !important;
        }}
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; color: white !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA SAFETY & LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# SAFE SQUAD INITIALIZATION
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "22": {
            "first_name": "Vinícius", 
            "last_name": "Júnior", 
            "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low"},
            "roadmap": []
        }
    }

if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    u, p = st.text_input("Username", value="admin"), st.text_input("Password", type="password", placeholder="owner2026")
    if st.button("Access Portal"):
        if u == "admin" and p == "owner2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 3. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        for f in client.files.list(): client.files.delete(name=f.name)
    else: st.warning("⚠️ Secret missing: GEMINI_API_KEY")
except Exception as e: st.error(f"AI Failed: {e}")

# --- 4. NAVIGATION ---
# Added 'Squad' as the first management tab
tabs = st.tabs(["📊 Squad Overview", "🏃 Squad Registry", "🧬 Athlete Medical Hub", "🎥 AI Performance Audit", "📅 Performance Roadmap"])

with tabs[0]: # SQUAD OVERVIEW
    st.header("🏆 Squad Performance Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'>Active Athletes<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Clinical System<br><span class='kpi-val'>Online</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>AI Tier<br><span class='kpi-val'>Paid</span></div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📋 Athlete Readiness Status")
    squad_summary = []
    for uid, data in st.session_state.profiles.items():
        squad_summary.append({
            "Shirt