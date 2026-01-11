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
        
        /* 1. FORCE ALL TEXT TO WHITE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. THE BLACK BOX FIX: FORCES DEEP BLACK BACKGROUND ON ALL INPUTS */
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
    st.session_state.roadmap = {"22": [{"date": "2026-01-11", "category": "Health", "note": "System Ready."}]}

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

if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE (With Auto-Cleanup)
        st.header("🎥 Live AI Technical Audit")
        p_num = st.text_input("Target Player Number", "22", key="analysis_p")
        video_file = st.file_uploader("Upload Match Clip (MP4/MOV)", type=['mp4', 'mov'])
        
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Generate Dual-Track Elite Analysis"):
                with st.status("🤖 AI Processing & Cleaning Storage...", expanded=True):
                    try:
                        # 1. Save to temporary local file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(video_file.getvalue())
                            tmp_path = tmp.name
                        
                        # 2. Upload to Google Cloud
                        uploaded_file = client.files.upload(file=tmp_path)
                        
                        # 3. Perform Analysis
                        prompt = "Analyze this sports video for injury risk and tactical play. Provide clinical notes."
                        response = client.models.generate_content(
                            model="gemini-2.0-flash-exp", contents=[prompt, uploaded_file]
                        )
                        
                        # 4. Save result to roadmap
                        st.session_state.roadmap[p_num].append({
                            "date": "2026-01-11", "category": "AI Audit", "note": response.text
                        })
                        
                        # 5. IMMEDIATELY DELETE FILE FROM CLOUD TO FREE SPACE
                        client.files.delete(name=uploaded_file.name)
                        
                        # 6. Delete temporary local file
                        os.remove(tmp_path)
                        
                        st.success("Audit Complete. Cloud storage cleared.")
                    except Exception as e:
                        if "429" in str(e):
                            st.error("🚨 QUOTA EXCEEDED: The AI is busy. Please wait 60 seconds.")
                        else:
                            st.error(f"AI Failure: {e}")

    with current_tab[4]: # THE 3D ROTATABLE DIGITAL TWIN
        st.header("🩺 3D Biometric Injury Mapping")
        
        # PRO MEDICAL MESH (Glass Effect)
        def create_body_mesh():
            def ellipsoid(x_c, y_c, z_c, rx, ry, rz):
                u = np.linspace(0, 2 * np.pi, 20); v = np.linspace(0, np.pi, 20)
                x = x_c + rx * np.outer(np.cos(u), np.sin(v))
                y = y_c + ry * np.outer(np.sin(u), np.sin(v))
                z = z_c + rz * np.outer(np.ones_like(u), np.cos(v))
                return x.flatten(), y.flatten(), z.flatten()
            tx, ty, tz = ellipsoid(0, 0, 4, 1.2, 0.8, 2)   # Torso
            hx, hy, hz = ellipsoid(0, 0, 7, 0.6, 0.6, 0.7) # Head
            lx, ly, lz = ellipsoid(0.7, 0, 1.5, 0.4, 0.4, 1.5) # Left Leg
            rx, ry, rz = ellipsoid(-0.7, 0, 1.5, 0.4, 0.4, 1.5) # Right Leg
            return np.concatenate([tx, hx, lx, rx]), np.concatenate([ty, hy, ly, ry]), np.concatenate([tz, hz, lz, rz])

        bx, by, bz = create_body_mesh()
        fig = go.Figure()
        fig.add_trace(go.Mesh3d(x=bx, y=by, z=bz, alphahull=7, color='lightgray', opacity=0.2, name="Digital Twin"))
        fig.add_trace(go.Scatter3d(x=[-0.7], y=[0], z=[1.5], mode='markers', marker=dict(size=18, color='#ff4b4b', symbol='diamond', line=dict(width=3, color='white'))))
        fig.update_layout(width=800, height=800, scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)', camera=dict(eye=dict(x=1.8, y=1.8, z=0.8))), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)