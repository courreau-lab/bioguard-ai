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
        
        /* 1. GLOBAL TEXT VISIBILITY: FORCE WHITE EVERYWHERE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. THE BLACK BOX FIX: PERMANENT DARK BACKGROUND ON ALL INPUTS */
        /* This prevents "white-on-white" text issues across all tabs */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 8px !important;
        }}

        /* 3. CINEMATIC BACKGROUND */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover; background-attachment: fixed;
        }}

        /* 4. NAVIGATION TABS: WHITE TEXT */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: white !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}
        
        /* 5. LUXURY CARDS */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important; padding: 25px !important; margin-bottom: 15px !important;
        }}
        
        /* 6. BUTTONS */
        .stButton>button {{ 
            border-radius: 50px !important; border: 2px solid #00ab4e !important; 
            color: white !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important;
        }}
        .stButton>button:hover {{ background: #00ab4e !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ AI Offline: Please add GEMINI_API_KEY to Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    # Ensuring history is preserved over time
    st.session_state.roadmap = {"22": [{"date": "2026-01-12", "category": "Health", "note": "Elite System Ready."}]}

# --- 4. NAVIGATION ---
tabs_labels = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tabs_labels += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]
current_tab = st.tabs(tabs_labels)

# --- 5. PUBLIC PAGES (Home, Offer, Pricing) ---
with current_tab[0]: # HOME & LOGIN
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        st.markdown("### Partner Portal Access")
        # Fixing the login interaction
        u = st.text_input("Username", placeholder="admin", key="login_user")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="login_pass")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied.")
    else:
        st.success("Elite Portal Unlocked. Welcome back, Admin.")

with current_tab[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### ⚽ Core Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.write("### 💎 Value Strategy")
        st.write("**Health:** Clinical injury risk mitigation through AI analysis.")
        st.write("**Play:** Performance and tactical audits for squad optimization.")

with current_tab[2]: # SUBSCRIPTION PLANS
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Digital Twin Mapping</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Clinical Integration</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        p