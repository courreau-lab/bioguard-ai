import streamlit as st
import plotly.graph_objects as go
from google import genai
import time
import tempfile
import os
import numpy as np

# --- 1. GLOBAL UI & LUXURY CONTRAST SHIELD ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* 1. GLOBAL TEXT VISIBILITY: FORCE WHITE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. THE BLACK BOX FIX: FORCES DARK BACKGROUND ON ALL INPUTS ACROSS ALL TABS */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 5px !important;
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
    st.session_state.roadmap = {"22": [{"date": "2026-01-11", "category": "Health", "note": "Initial baseline ready."}]}

# --- 4. NAVIGATION ---
tabs = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tabs += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]
current_tab = st.tabs(tabs)

# --- 5. PAGES ---
with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        st.markdown("### Partner Portal Access")
        u = st.text_input("Username", placeholder="admin", key="u_final")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="p_final")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[1]: # OFFER
    st.header("The Competitive Advantage")
    st.write("Clinical biomechanics and tactical audits for Tier 1 organizations.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Dual Health/Play Audits<br>3D Interactive Mapping</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Custom 3D Scanning</p></div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        p_num = st.text_input("Target Player Number", "22", key="analysis_p_input")
        video_file = st.file_uploader("Upload Match Clip", type=['mp4', 'mov'])
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Generate Dual-Track Analysis"):
                with st.status("🤖 AI Processing...", expanded=True):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(video_file.getvalue())
                            tmp_path = tmp.name
                        uploaded_file = client.files.upload(file=tmp_path)
                        prompt = "Analyze this sports video for injury risk and tactical play. Provide clinical notes."
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, uploaded_file])
                        st.session_state.roadmap[p_num].append({"date": "2026-01-11", "category": "AI Audit", "note": response.text})
                        os.remove(tmp_path)
                        st.success("Audit Complete.")
                    except Exception as e:
                        if "429" in str(e): st.error("🚨 AI Busy: Please wait 60 seconds.")
                        else: st.error(f"AI Failure: {e}")

    with current_tab[4]: # THE 3D ROTATABLE BODY MAP
        st.header("🩺 3D Biometric Injury Mapping")
        st.write("Rotate the model to view clinical alerts across the skeletal frame.")
        
        # GENERATING A PRO 3D MESH (No regional image blocks possible)
        # Coordinates for a 3D skeletal frame
        x, y, z = [0, 0, 0.5, -0.5, 0.5, -0.5, 0.3, -0.3], [0, 0, 0, 0, -1, -1, -2, -2], [0, 1, 0.5, 0.5, 0, 0, 0, 0]
        
        fig = go.Figure()

        # The 3D Skeletal Wireframe
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers+lines',
            line=dict(color='#00ab4e', width=8),
            marker=dict(size=5, color='white', opacity=0.8),
            name="Skeletal Frame"
        ))

        # THE CLINICAL PINPOINT (Red Star in 3D Space)
        fig.add_trace(go.Scatter3d(
            x=[0.3], y=[-2], z=[0], # Pinpointed on the Right Knee area
            mode='markers',
            marker=dict(size=15, color='#ff4b4b', symbol='diamond', line=dict(width=2, color='white')),
            hovertext="PLAYER #22: ACUTE MEDIAL KNEE VALGUS"
        ))

        fig.update_layout(
            width=800, height=800,
            scene=dict(
                xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 Use your mouse to rotate the 3D model and inspect the injury zone.")

    with current_tab[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id = st.selectbox("Player", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)