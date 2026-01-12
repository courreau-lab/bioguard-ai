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
        /* Prevents "white-on-white" text issues on all pages */
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
        # Initializing the 2026 Gemini 2.0 Brain
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ AI Brain Offline: Check Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {"22": [{"date": "2026-01-12", "category": "Health", "note": "System Active."}]}

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
        # Local variables for login to prevent global namespace errors
        login_u = st.text_input("Username", placeholder="admin", key="u_key")
        login_p = st.text_input("Password", type="password", placeholder="owner2026", key="p_key")
        if st.button("Unlock Elite Portal"):
            if login_u == "admin" and login_p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        st.success("Welcome, Admin.")

with tabs[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("### ⚽ Core Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col_r:
        st.write("### 💎 Value Strategy")
        st.write("**Health:** Clinical injury risk mitigation through AI scans.")
        st.write("**Play:** Technical and tactical audits for performance.")

with tabs[2]: # SUBSCRIPTION PLANS
    st.header("Strategic Partnership Tiers")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Digital Twin Mapping</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Clinical Integration</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with tabs[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        target_p = st.text_input("Target Player Number", "22", key="player_target")
        vid = st.file_uploader("Upload Match Clip", type=['mp4', 'mov'])
        if vid and 'client' in locals():
            st.video(vid)
            if st.button("Generate Dual-Track Analysis"):
                with st.status("🤖 AI Processing & Cleaning...", expanded=True):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as t:
                            t.write(vid.getvalue())
                            t_path = t.name
                        
                        up_file = client.files.upload(file=t_path)
                        prompt = "Analyze this sports video for health risk and tactical gains."
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, up_file])
                        
                        st.session_state.roadmap[target_p].append({"date": "2026-01-12", "category": "AI Audit", "note": response.text})
                        
                        # Auto-Cleanup
                        client.files.delete(name=up_file.name)
                        os.remove(t_path)
                        st.success("Audit Complete.")
                    except Exception as e:
                        if "429" in str(e): st.error("🚨 AI Busy. Wait 60s.")
                        else: st.error(f"Error: {e}")

    with tabs[4]: # PLAYER DASHBOARD (CLINICAL ALIGNMENT)
        st.header("🩺 Biometric Injury Mapping")
        
        if os.path.exists("digital_twin.png"):
            # Encoding for 100% reliable image loading
            with open("digital_twin.png", "rb") as f_img:
                b64_data = base64.b64encode(f_img.read()).decode()
            
            fig = go.Figure()
            # Scaling fix to prevent mannequin stretching
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{b64_data}",
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"
            ))
            
            # Clinical Circles & Call-outs aligned to mannequin limbs
            fig.add_trace(go.Scatter(
                x=[535, 530], y=[255, 165], # Aligned with Right Knee and Right Calf area
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
            st.warning("📸 Image 'digital_twin.png' missing.")

    with tabs[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id_view = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        for item in reversed(st.session_state.roadmap[p_id_view]):
            st.markdown(f"<div class='roadmap-card'><strong>{item['date']}</strong><br>{item['note']}</div>", unsafe_allow_html=True)

    with tabs[6]: # ADMIN HUB
        st.header("System Controls")
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()