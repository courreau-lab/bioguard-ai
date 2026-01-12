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
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; color: white !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
        .stButton>button:hover {{ background: #00ab4e !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION & QUOTA PURGE ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # FORCE PURGE: Deletes existing zombie files to clear quota
        for file in client.files.list():
            client.files.delete(name=file.name)
    else:
        st.warning("⚠️ AI Offline: Please add GEMINI_API_KEY to Streamlit Secrets.")
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

# --- 5. PUBLIC PAGES (RESTORED) ---
with tabs[0]: # LOGIN
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        u = st.text_input("Username", placeholder="admin", key="u_login_f")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="p_login_f")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with tabs[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### ⚽ Core Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.write("### 💎 Value Strategy")
        st.write("**Health:** Clinical injury risk mitigation.")
        st.write("**Play:** Technical tactical audits.")

with tabs[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Integration</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with tabs[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        target_p = st.text_input("Target Player Number", "22", key="p_target_final")
        vid_file = st.file_uploader("Upload Match Clip", type=['mp4', 'mov'])
        if vid_file and 'client' in locals():
            st.video(vid_file)
            if st.button("Generate Dual-Track Analysis"):
                with st.status("🤖 AI Auditing (Purging Storage First)...", expanded=True):
                    try:
                        # CLEAN QUOTA
                        for file in client.files.list(): client.files.delete(name=file.name)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(vid_file.getvalue())
                            t_path = tmp.name
                        
                        up_file = client.files.upload(file=t_path)
                        prompt = "Analyze this sports video for injury risk and performance."
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, up_file])
                        
                        st.session_state.roadmap[target_p].append({"date": "2026-01-12", "category": "AI Audit", "note": response.text})
                        client.files.delete(name=up_file.name)
                        os.remove(t_path)
                        st.success("Audit Complete.")
                    except Exception as e:
                        st.error(f"Quota issue or error: {e}. Please wait 60s.")

    with tabs[4]: # PLAYER DASHBOARD (RECALIBRATED ALIGNMENT)
        st.header("🩺 Biometric Injury Mapping")
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f: b64_img = base64.b64encode(f.read()).decode()
            fig = go.Figure()
            # Scaled exactly for the new mannequin
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64_img}", xref="x", yref="y", x=250, y=850, sizex=500, sizey=750, sizing="contain", opacity=0.9, layer="below"))
            
            # RECALIBRATED PIN LOCATIONS TO ALIGN WITH BODY
            fig.add_trace(go.Scatter(
                x=[500, 485], y=[330, 210], # Aligned exactly to Knee and Calf centers
                mode='markers+text', text=["Knee ACL", "Calf Strain"], textposition="middle right",
                textfont=dict(color="white", size=15),
                marker=dict(size=35, color="rgba(255, 75, 75, 0.7)", symbol="circle", line=dict(width=3, color='white'))
            ))
            
            fig.update_layout(width=700, height=800, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("📸 digital_twin.png not found.")

    with tabs[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id = st.selectbox("Player", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)