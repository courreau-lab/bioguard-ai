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
        
        /* 1. FORCE ALL TEXT TO WHITE EVERYWHERE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. THE BLACK BOX FIX: PERMANENT DARK BACKGROUND ON ALL INPUTS */
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

# --- 2. AI INITIALIZATION & AUTOMATIC PURGE ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # AUTOMATIC CLOUD PURGE: Clears files immediately on boot to prevent 429 errors
        for f in client.files.list():
            client.files.delete(name=f.name)
    else:
        st.warning("⚠️ AI Brain Offline: Please add GEMINI_API_KEY to Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {"22": [{"date": "2026-01-12", "category": "Health", "note": "System Ready."}]}

# --- 4. NAVIGATION ---
tab_labels = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tab_labels += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]
tabs = st.tabs(tab_labels)

# --- 5. PUBLIC PAGES (REINSTATED) ---
with tabs[0]: # HOME & LOGIN
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        st.markdown("### Partner Portal Access")
        u_login = st.text_input("Username", placeholder="admin", key="main_u_key")
        p_login = st.text_input("Password", type="password", placeholder="owner2026", key="main_p_key")
        if st.button("Unlock Elite Portal"):
            if u_login == "admin" and p_login == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with tabs[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### ⚽ Core Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.write("### 💎 Dual-Track Value")
        st.write("**Health:** Clinical injury risk mitigation through AI scans.")
        st.write("**Play:** Performance and tactical audits.")

with tabs[2]: # SUBSCRIPTION PLANS
    st.header("Strategic Partnership Tiers")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Digital Twin Mapping</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Clinical Integration</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with tabs[3]: # ANALYSIS ENGINE (WITH QUOTA PURGE)
        st.header("🎥 Live AI Technical Audit")
        target_p = st.text_input("Target Player Number", "22", key="final_analysis_target")
        vid_file = st.file_uploader("Upload Match Clip", type=['mp4', 'mov'])
        if vid_file and 'client' in locals():
            st.video(vid_file)
            if st.button("Generate Dual-Track Elite Analysis"):
                with st.status("🤖 AI Auditing (Purging Cloud First)...", expanded=True):
                    try:
                        # CLEAN QUOTA BEFORE EVERY UPLOAD
                        for f in client.files.list(): client.files.delete(name=f.name)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(vid_file.getvalue())
                            t_path = tmp.name
                        
                        up_file = client.files.upload(file=t_path)
                        prompt = "Analyze this sports video for health risk and technical gains."
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, up_file])
                        
                        st.session_state.roadmap[target_p].append({"date": "2026-01-12", "category": "AI Audit", "note": response.text})
                        client.files.delete(name=up_file.name)
                        os.remove(t_path)
                        st.success("Audit Complete. Analysis delivered.")
                    except Exception as e:
                        if "429" in str(e): st.error("🚨 AI Busy: Quota reached. Please wait 60s.")
                        else: st.error(f"Analysis Failed: {e}")

    with tabs[4]: # PLAYER DASHBOARD (PRECISION ALIGNMENT)
        st.header("🩺 Biometric Injury Mapping")
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_img:
                b64_data = base64.b64encode(f_img.read()).decode()
            
            fig = go.Figure()
            # Scaling fix to stop mannequin stretching
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{b64_data}",
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"
            ))
            
            # PIN ALIGNMENT: Shifts text and markers to center-right limbs
            fig.add_trace(go.Scatter(
                x=[465, 520], y=[280, 180], # Recalibrated for Knee and Calf on your new image
                mode='markers+text',
                text=["Knee ACL", "Calf Strain"],
                textposition="middle right",
                textfont=dict(color="white", size=15),
                marker=dict(size=35, color="rgba(255, 75, 75, 0.7)", 
                            symbol="circle", line=dict(width=3, color='white'))
            ))
            
            fig.update_layout(width=800, height=800, paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                              xaxis=dict(visible=False, range=[0, 1000]), 
                              yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("📸 Image 'digital_twin.png' missing in GitLab root folder.")

    with tabs[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id_view = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id_view]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)