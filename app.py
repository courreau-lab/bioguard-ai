import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & LUXURY STYLING ---
st.set_page_config(page_title="Elite Performance | Squad Management", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* THEMES & TEXT */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 5px !important; }}
        
        /* INPUT & INTERFACES */
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: #000000 !important; color: #ffffff !important; border: 2px solid #00ab4e !important; border-radius: 12px !important;
        }}
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        /* NAVIGATION & TABS */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}

        /* DATA CARDS */
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; padding: 10px 30px !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA PERSISTENCE & LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "Player 1": {"medical": {"age": 24, "weight": 78, "risk": "Low"}, "roadmap": []},
        "Player 2": {"medical": {"age": 21, "weight": 82, "risk": "Medium"}, "roadmap": []}
    }

if not st.session_state.logged_in:
    st.title("🛡️ ELITE PERFORMANCE HUB")
    u, p = st.text_input("Username", value="admin"), st.text_input("Password", type="password", placeholder="owner2026")
    if st.button("Access Command Center"):
        if u == "admin" and p == "owner2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 3. AI INITIALIZATION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        for f in client.files.list(): client.files.delete(name=f.name)
    else: st.warning("⚠️ Secret missing: GEMINI_API_KEY")
except Exception as e: st.error(f"AI Connectivity Failed: {e}")

# --- 4. NAVIGATION ---
tabs = st.tabs(["📊 Squad Overview", "🧬 Athlete Medical Hub", "🎥 AI Performance Audit", "📅 Performance Roadmap"])

with tabs[0]: # SQUAD OVERVIEW
    st.header("🏆 Squad Performance Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("<div class='kpi-card'>Total Athletes<br><span class='kpi-val'>2</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Injury Risk Score<br><span class='kpi-val'>12%</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>Technical Audits<br><span class='kpi-val'>48</span></div>", unsafe_allow_html=True)
    c4.markdown("<div class='kpi-card'>Avg Intensity<br><span class='kpi-val'>7.4</span></div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📋 Squad Readiness & Status")
    st.table([{"Athlete": name, "Age": d['medical']['age'], "Weight (kg)": d['medical']['weight'], "Status": d['medical']['risk']} 
              for name, d in st.session_state.profiles.items()])

with tabs[1]: # MEDICAL HUB & DASHBOARD
    st.header("🧬 Athlete Digital Twin & Clinical Hub")
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        p_id = st.selectbox("Select Profile", options=list(st.session_state.profiles.keys()), key="med_sel")
        st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
        st.subheader(f"Biometrics: {p_id}")
        st.session_state.profiles[p_id]["medical"]["weight"] = st.number_input("Weight (kg)", value=float(st.session_state.profiles[p_id]["medical"]["weight"]), key="w_in")
        st.session_state.profiles[p_id]["medical"]["risk"] = st.selectbox("Injury Risk Status", ["Low", "Medium", "High"], index=0, key="r_in")
        st.text_area("Clinical Notes", value="Previous ACL stress detected in week 4.", height=150)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_r:
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_b: b64 = base64.b64encode(f_b.read()).decode()
            fig = go.Figure()
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64}", xref="x", yref="y", x=0, y=1000, sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"))
            # RECALIBRATED: Midline Alignment (X=500) for centered portrait mannequin
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Stress", "Calf Fatigue"], textposition="middle right", marker=dict(size=45, color="rgba(255, 75, 75, 0.8)", line=dict(width=3, color='white'))))
            fig.update_layout(width=700, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]), margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # ANALYSIS ENGINE
    st.header("🎥 Targeted AI Performance Audit")
    target_p = st.selectbox("Assign to Profile", options=list(st.session_state.profiles.keys()), key="ana_sel")
    shirt = st.text_input("Shirt Color Targeting", placeholder="e.g., Target player in the Red Shirt number 10")
    
    vid = st.file_uploader("Upload Highlight (MP4/MOV)", type=['mp4', 'mov'])
    if vid and 'client' in locals():
        st.video(vid)
        if st.button("Execute Targeted Audit"):
            with st.status("🤖 Analyzing Player Biomechanics..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    
                    prompt = f"Target player in {shirt}. Summarize performance, technical gains, and provide 1-week plan."
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[target_p]["roadmap"].append({"date": "2026-01-18", "note": resp.text})
                    client.files.delete(name=upf.name); os.remove(t_path)
                    st.success(f"Audit Complete. Profile {target_p} updated.")
                except Exception as e: st.error(f"Audit Failed: {e}")

with tabs[3]: # ROADMAP
    st.header("📅 Integrated Clinical Roadmap")
    view_p = st.selectbox("Switch View", options=list(st.session_state.profiles.keys()), key="road_sel")
    for entry in reversed(st.session_state.profiles[view_p]["roadmap"]):
        st.markdown(f"<div class='roadmap-card'><strong>{entry['date']} - Performance Audit Result</strong><br>{entry['note']}</div>", unsafe_allow_html=True)