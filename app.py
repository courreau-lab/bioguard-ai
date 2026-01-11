import streamlit as st
import plotly.graph_objects as go
from google import genai
import time
import tempfile
import os

# --- 1. GLOBAL UI & LUXURY CONTRAST SHIELD ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* 1. GLOBAL TEXT VISIBILITY */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. FORCE DARK BACKGROUND FOR INPUT BOXES (Fixes White-on-White) */
        input, textarea, [data-baseweb="input"], [data-baseweb="select"] {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: #ffffff !important;
            border: 1px solid #00ab4e !important;
        }}
        
        /* 3. INPUT LABELS */
        label, [data-testid="stWidgetLabel"] p {{
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}

        /* 4. CINEMATIC BACKGROUND */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover; background-attachment: fixed;
        }}

        /* 5. NAVIGATION TABS */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: white !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}
        
        /* 6. CARDS & BUTTONS */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important; padding: 25px !important; margin-bottom: 15px !important;
        }}
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
        st.warning("⚠️ AI Brain Offline: GEMINI_API_KEY missing from Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {"2": [{"date": "2026-01-11", "category": "Health", "note": "System ready."}]}

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
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="owner2026")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Dual Health/Play Audits<br>Interactive Body Map</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Custom 3D Scanning</p></div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Upload Match Clip (MP4/MOV)", type=['mp4', 'mov'])
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Generate Dual-Track Elite Analysis"):
                with st.status("🤖 AI Processing Video...", expanded=True):
                    try:
                        # FIX: Save file temporarily to provide a real path for the API
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(video_file.getvalue())
                            tmp_path = tmp.name
                        
                        st.write("Securely Uploading to Cloud...")
                        # Use the correct 'file' parameter for the SDK
                        uploaded_file = client.files.upload(file=tmp_path)
                        
                        prompt = "Analyze this sports video. 1. HEALTH (injury risk markers like knee valgus). 2. PLAY (tactical improvements like scanning frequency)."
                        response = client.models.generate_content(
                            model="gemini-2.0-flash-exp", 
                            contents=[prompt, uploaded_file]
                        )
                        
                        st.session_state.roadmap[p_num].append({"date": "2026-01-11", "category": "AI Audit", "note": response.text})
                        os.remove(tmp_path) # Clean up
                        st.success("Audit Complete. Data pushed to Roadmap.")
                    except Exception as e:
                        st.error(f"AI Failure: {e}")

    with current_tab[4]: # BODY MAP
        st.header("🩺 Biometric Body Map")
        fig = go.Figure()
        fig.add_layout_image(dict(source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=30, color="#ff4b4b", line=dict(width=2, color='white')), hovertext="Knee Alert"))
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id = st.selectbox("View Player History", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)