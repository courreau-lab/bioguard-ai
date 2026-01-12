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
        
        /* FORCE ALL TEXT TO WHITE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* THE BLACK BOX FIX: ENSURES READABLE INPUTS (NO WHITE-ON-WHITE) */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 8px !important;
        }}

        /* CINEMATIC STADIUM BACKGROUND */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover; background-attachment: fixed;
        }}

        /* NAVIGATION TABS: WHITE TEXT */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: white !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}
        
        /* LUXURY CARDS */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important; padding: 25px !important; margin-bottom: 15px !important;
        }}
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
    st.session_state.roadmap = {"22": [{"date": "2026-01-12", "category": "Health", "note": "System Ready."}]}

# --- 4. NAVIGATION ---
tabs = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tabs += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]
current_tab = st.tabs(tabs)

# --- 5. PUBLIC PAGES (RESTORED) ---
with current_tab[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### ⚽ Core Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.write("### 💎 Dual-Track Value")
        st.write("**Health:** Clinical injury risk mitigation.")
        st.write("**Play:** Performance and tactical audits.")

with current_tab[2]: # SUBSCRIPTION PLANS
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Digital Twin Mapping</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Clinical Integration</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with current_tab[4]: # PLAYER DASHBOARD (ANATOMICAL ALIGNMENT FIX)
        st.header("🩺 Biometric Injury Mapping")
        
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode()
            
            fig = go.Figure()
            
            # Locked Aspect Ratio for proper alignment
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{encoded_img}",
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000,
                sizing="contain", opacity=0.9, layer="below"
            ))
            
            # PRECISE CLINICAL PINS
            # X=500 is center. Y=250 is leg level.
            fig.add_trace(go.Scatter(
                x=[465, 520], y=[280, 180], # Aligned with Knee and Calf on your mannequin
                mode='markers+text',
                text=["Knee ACL", "Calf Strain"],
                textposition="middle right",
                textfont=dict(color="white", size=15),
                marker=dict(size=35, color="rgba(255, 75, 75, 0.7)", 
                            symbol="circle", line=dict(width=3, color='white')),
                hovertext=["RIGHT KNEE: CRITICAL", "LEFT CALF: MODERATE"]
            ))
            
            fig.update_layout(width=800, height=800, paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                              xaxis=dict(visible=False, range=[0, 1000]), 
                              yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("📸 Digital Twin Image Missing in GitLab root folder.")

    with current_tab[5]: # ROADMAP (RESTORED)
        st.header("📅 Integrated 12-Week Roadmap")
        p_id = st.selectbox("View Player History", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)