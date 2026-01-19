import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. LUXURY INTERFACE & TOTAL VISIBILITY SHIELD ---
st.set_page_config(page_title="Elite Performance | Command Center", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    # Escaping CSS curly braces with {{ }} to prevent SyntaxErrors in f-strings
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* 1. FORCE GLOBAL DARK THEME & WHITE TEXT */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        
        /* 2. ELITE GREEN LABELS */
        label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 8px !important; }}

        /* 3. THE VISIBILITY SHIELD: FORCING BLACK BACKGROUNDS (Fixes 'White on White' bug) */
        input, textarea, select, 
        div[data-baseweb="input"], 
        div[data-baseweb="select"], 
        div[data-baseweb="base-input"],
        .stTextInput>div>div>input,
        .stSelectbox div[role="combobox"] {{
            background-color: #0c0c0c !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 12px !important;
            -webkit-text-fill-color: #ffffff !important;
        }}
        
        /* 4. CINEMATIC BACKGROUND */
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        /* 5. DATA CARDS */
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        
        /* 6. NAVIGATION TABS */
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}

        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. SESSION SECURITY & MASTER DATABASE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# MASTER REPOSITORY: Standardized structure prevents KeyErrors and TypeErrors
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "7": {
            "first_name": "Vinícius", "last_name": "Júnior", "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low", "history": "ACL Rehab (2025)"},
            "roadmap": []
        }
    }

# GLOBAL LOGIN GATE (Rebuilt with unique keys to prevent browser pre-fill issues)
if not st.session_state.logged_in:
    st.title("🛡️ ELITE COMMAND CENTER")
    # Added explicit keys and placeholder to ensure visibility
    u = st.text_input("Username", value="", placeholder="admin", key="auth_username_platinum")
    p = st.text_input("Password", type="password", value="", placeholder="owner2026", key="auth_password_platinum")
    if st.button("Unlock Command Center", key="login_btn"):
        if u == "admin" and p == "owner2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Access Denied: Please check credentials.")
    st.stop()

# --- 3. AI CONNECTION (Only runs if logged in) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception: pass

# --- 4. INTEGRATED NAVIGATION ---
tabs = st.tabs(["📊 Overview", "🏃 Squad Registry", "🩺 Medical Hub", "🤖 Virtual Coach", "🎥 Performance Audit", "📅 Roadmap"])

# MASTER PICK-LIST: Links all tabs together
p_options = {uid: f"#{d['shirt_number']} {d['first_name']} {d['last_name']}" for uid, d in st.session_state.profiles.items()}

with tabs[0]: # OVERVIEW (Safe from KeyErrors and Indentation errors)
    st.header("🏆 Squad Status Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'>Squad Size<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Injury Risk Score<br><span class='kpi-val'>Low</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>AI Analysis Tier<br><span class='kpi-val'>Paid</span></div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📋 Athlete Readiness Status")
    # Table logic with .get() fallbacks to prevent crashes
    overview_data = []
    for uid, data in st.session_state.profiles.items():
        med_info = data.get('medical', {})
        overview_data.append({
            "Athlete": f"#{data['shirt_number']} {data['first_name']}",
            "Risk": med_info.get('risk', 'N/A'),
            "Age": med_info.get('age', 'N/A')
        })
    st.table(overview_data)

with tabs[1]: # SQUAD REGISTRY (Master Entry Point)
    st.header("🏃 Athlete Master Registry")
    with st.form("registry_master_final", clear_on_submit=True):
        st.markdown("### Register New Elite Athlete")
        f_col, l_col, n_col = st.columns(3)
        f_reg = f_col.text_input("First Name", key="f_reg_in")
        l_reg = l_col.text_input("Last Name", key="l_reg_in")
        n_reg = n_col.text_input("Shirt Number", key="n_reg_in")
        if st.form_submit_button("Confirm Registration"):
            if f_reg and l_reg and n_reg:
                st.session_state.profiles[n_reg] = {
                    "first_name": f_reg, "last_name": l_reg, "shirt_number": n_reg,
                    "medical": {"age": 0, "weight": 0.0, "risk": "Low", "history": ""},
                    "roadmap": []
                }
                st.success(f"Registered #{n_reg} {f_reg} {l_reg}"); st.rerun()

with tabs[2]: # MEDICAL HUB (Anatomy Alignment)
    st.header("🩺 Athlete Clinical Profile")
    # Selection box for linked athlete profiles
    p_uid_med = st.selectbox("Select Profile", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="med_hub_sel")
    
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
        player_med = st.session_state.profiles[p_uid_med]
        st.subheader(f"Update: {player_med['first_name']}")
        w_up = st.number_input("Weight (kg)", value=float(player_med["medical"].get("weight", 0.0)), key="w_up_med")
        a_up = st.number_input("Age", value=int(player_med["medical"].get("age", 0)), key="a_up_med")
        r_up = st.selectbox("Injury Risk Status", ["Low", "Medium", "High"], key="r_up_med")
        if st.button("Sync Profile Data", key="sync_med_btn"):
            st.session_state.profiles[p_uid_med]["medical"].update({"weight": w_up, "age": a_up, "risk": r_up})
            st.success("Synchronized."); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_r:
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_bin: b64 = base64.b64encode(f_bin.read()).decode()
            fig = go.Figure()
            # Clean Plotly syntax to prevent ValueError
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{b64}", 
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"
            ))
            # Midline pins (X=500) for vertical mannequin alignment
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Risk", "Calf Strain"], textposition="middle right", marker=dict(size=45, color="#ff4b4b", line=dict(width=3, color='white'))))
            fig.update_layout(width=700, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]), margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]: # VIRTUAL COACH (MM:SS Timestamps)
    st.header("🤖 Virtual Coach AI Assistant")
    c_uid_v = st.selectbox("Target Player", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="coach_hub_sel")
    vid_v = st.file_uploader("Upload Session Video", type=['mp4', 'mov'], key="coach_vid_up")
    if vid_v and 'client' in locals():
        st.video(vid_v)
        if st.button("Generate Tactical Audit", key="gen_coach_btn"):
            with st.status("🤖 Analyzing metrics and timestamps..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid_v.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    
                    # PROMPT: Explicitly requests MM:SS timestamps for parent review
                    prompt = f"""
                    Target player shirt #{st.session_state.profiles[c_uid_v]['shirt_number']}.
                    Analyze for Parent/Coach review:
                    1. Technical KPIs: Touches, Good Passes, Bad Passes.
                    2. Tactical Errors: Provide bold MM:SS timestamps for bad passes or poor positioning.
                    3. Body Form: Monitor biomechanical efficiency and posture.
                    """
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[c_uid_v]["roadmap"].append({"date": "2026-01-19", "type": "Coach Session", "note": resp.text})
                    st.success("Audit Archived."); st.rerun()
                except Exception as e: st.error(f"Error: {e}")

with tabs[5]: # ROADMAP
    st.header("📅 Integrated Clinical & Tactical Roadmap")
    r_uid_view = st.selectbox("View History For", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="road_hub_sel")
    if not st.session_state.profiles[r_uid_view]["roadmap"]:
        st.info("No audit data yet. Add players and run a Coach or Performance Audit.")
    else:
        for entry in reversed(st.session_state.profiles[r_uid_view]["roadmap"]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']} - {entry['type']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)