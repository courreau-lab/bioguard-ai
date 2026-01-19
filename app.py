import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. LUXURY UI & BRANDING ---
st.set_page_config(page_title="Elite Performance Hub", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        label {{ color: #00ab4e !important; font-weight: 700 !important; }}
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: #000000 !important; color: #ffffff !important; border: 2px solid #00ab4e !important; border-radius: 12px !important;
        }}
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; color: white !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA SAFETY & LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# MASTER DATABASE INITIALIZATION: Standardized structure to prevent KeyError
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "7": {
            "first_name": "Vinícius", "last_name": "Júnior", "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low", "history": "ACL Rehab (2025)"},
            "roadmap": []
        }
    }

if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    u, p = st.text_input("Username", value="admin"), st.text_input("Password", type="password", placeholder="owner2026")
    if st.button("Access Portal"):
        if u == "admin" and p == "owner2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 3. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else: st.warning("⚠️ Secret missing: GEMINI_API_KEY")
except Exception as e: st.error(f"AI Failed: {e}")

# --- 4. NAVIGATION ---
tabs = st.tabs(["📊 Overview", "🏃 Squad Registry", "🩺 Medical Hub", "🤖 Virtual Coach", "🎥 Performance Audit", "📅 Roadmap"])

# PRE-CALCULATED SQUAD PICK-LIST
p_options = {uid: f"#{d['shirt_number']} {d['first_name']} {d['last_name']}" for uid, d in st.session_state.profiles.items()}

with tabs[0]: # OVERVIEW
    st.header("🏆 Squad Status Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'>Squad Size<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Injury Risk Score<br><span class='kpi-val'>Low</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>System Status<br><span class='kpi-val'>Paid Tier</span></div>", unsafe_allow_html=True)
    st.divider()
    st.subheader("📋 Athlete Readiness Status")
    # Using .get() to prevent KeyErrors
    st.table([{"Athlete": f"#{d['shirt_number']} {d['first_name']}", "Risk": d['medical'].get('risk', 'N/A'), "Age": d['medical'].get('age', 'N/A')} for d in st.session_state.profiles.values()])

with tabs[1]: # SQUAD REGISTRY
    st.header("🏃 Athlete Master Registry")
    with st.form("reg_form"):
        f_in, l_in, n_in = st.columns(3)
        f = f_in.text_input("First Name")
        l = l_in.text_input("Last Name")
        n = n_in.text_input("Shirt Number")
        if st.form_submit_button("Confirm Registration"):
            if f and l and n:
                st.session_state.profiles[n] = {
                    "first_name": f, "last_name": l, "shirt_number": n,
                    "medical": {"age": 0, "weight": 0.0, "risk": "Low", "history": ""},
                    "roadmap": []
                }
                st.success(f"Registered #{n}"); st.rerun()

with tabs[2]: # MEDICAL HUB
    st.header("🩺 Athlete Clinical Profile")
    p_uid = st.selectbox("Select Profile", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="med_sel")
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
        st.subheader(f"Biometrics: {st.session_state.profiles[p_uid]['first_name']}")
        w = st.number_input("Weight (kg)", value=float(st.session_state.profiles[p_uid]["medical"].get("weight", 0.0)))
        a = st.number_input("Age", value=int(st.session_state.profiles[p_uid]["medical"].get("age", 0)))
        r = st.selectbox("Injury Risk", ["Low", "Medium", "High"], key="risk_sel")
        hist = st.text_area("Medical History", value=st.session_state.profiles[p_uid]["medical"].get("history", ""))
        if st.button("Sync Data"):
            st.session_state.profiles[p_uid]["medical"].update({"weight": w, "age": a, "risk": r, "history": hist})
            st.success("Synced.")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_bin: b64 = base64.b64encode(f_bin.read()).decode()
            fig = go.Figure()
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64}", xref="x", yref="y", x=0, y=1000, sizex=1000, size_y=1000, sizing="contain", opacity=0.9, layer="below"))
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Risk", "Calf Strain"], textposition="middle right", marker=dict(size=45, color="#ff4b4b", line=dict(width=3, color='white'))))
            fig.update_layout(width=700, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]), margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]: # VIRTUAL COACH
    st.header("🤖 Virtual Coach Assistant")
    c_uid = st.selectbox("Select Player", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="coach_p")
    vid = st.file_uploader("Upload Session Video", type=['mp4', 'mov'], key="coach_vid")
    if vid and 'client' in locals():
        st.video(vid)
        if st.button("Analyze Technicals & Form"):
            with st.status("🤖 Analyzing performance..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    prompt = f"Target: shirt number {st.session_state.profiles[c_uid]['shirt_number']}. Analyze: 1. Technicals (touches, passes (good/bad)). 2. Tactical errors with MM:SS timestamps. 3. Body form efficiency."
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[c_uid]["roadmap"].append({"date": "2026-01-19", "type": "Coach Note", "note": resp.text})
                    st.success("Analysis Archived."); st.rerun()
                except Exception as e: st.error(f"Error: {e}")

with tabs[4]: # PERFORMANCE AUDIT
    st.header("🎥 Shirt-Color Targeted Audit")
    a_uid = st.selectbox("Assign Analysis", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="audit_p")
    shirt = st.text_input("Identify Kit Color", placeholder="e.g. Red with white trim")
    vid_audit = st.file_uploader("Upload Match Video", type=['mp4', 'mov'], key="audit_vid")
    if vid_audit and 'client' in locals():
        st.video(vid_audit)
        if st.button("Generate Performance Plan"):
            with st.status("🤖 AI Auditing..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid_audit.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    prompt = f"Target: {shirt}. Provide a 1-week tactical roadmap based on match movements."
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[a_uid]["roadmap"].append({"date": "2026-01-19", "type": "Audit", "note": resp.text})
                    st.success("Plan Delivered."); st.rerun()
                except Exception as e: st.error(f"Error: {e}")

with tabs[5]: # ROADMAP
    st.header("📅 Historical Clinical & Tactical Roadmap")
    r_uid = st.selectbox("View History", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="road_p")
    for entry in reversed(st.session_state.profiles[r_uid]["roadmap"]):
        st.markdown(f"<div class='roadmap-card'><strong>{entry['date']} - {entry['type']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)