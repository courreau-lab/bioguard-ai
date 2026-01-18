import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & TOTAL VISIBILITY SHIELD ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #000000 !important; color: #ffffff !important; border: 2px solid #00ab4e !important; border-radius: 8px !important;
        }}
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: white !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}
        .luxury-card, .roadmap-card {{ background: rgba(255, 255, 255, 0.08) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 20px !important; padding: 25px !important; margin-bottom: 15px !important; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; color: white !important; background: rgba(0, 171, 78, 0.2) !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION & QUOTA PURGE ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # FORCE PURGE: Clears files immediately on boot
        for f in client.files.list(): client.files.delete(name=f.name)
    else:
        st.warning("⚠️ Secret missing. Add GEMINI_API_KEY to Streamlit Cloud Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {"22": [{"date": "2026-01-18", "category": "System", "note": "Elite Performance Engine Ready."}]}

# --- 4. NAVIGATION ---
tab_names = ["Home", "Business Offer", "Subscription Plans", "Analysis Engine", "Player Dashboard", "12-Week Roadmap"]
if not st.session_state.logged_in:
    tabs = st.tabs(tab_names[:3])