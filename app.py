import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. THE VISIBILITY SHIELD & LUXURY STYLING ---
st.set_page_config(page_title="Elite Performance Hub", layout="wide")

def apply_platinum_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    # Note: Double curly braces {{ }} are used for CSS inside an f-string to prevent SyntaxErrors
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        
        label, .stWidget label {{ color: #00ab4e !important; font-weight: 700 !important; margin-bottom: 8px !important; }}

        /* THE BRUTE-FORCE INPUT SHIELD (High Contrast Visibility) */
        input, textarea, select, 
        div[data-baseweb="input"], 
        div[data-baseweb="select"], 
        div[data-baseweb="base-input"],
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[role="combobox"],
        .stTextInput>div>div>input {{
            background-color: #0a0a0a !important;
            color: #ffffff !important;
            border: 2px solid #00ab4e !important;
            border-radius: 12px !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        
        .kpi-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; }}
        .kpi-val {{ color: #00ab4e; font-size: 2rem; font-weight: 700; }}
        .roadmap-card {{ background: rgba(255, 255, 255, 0.08); border-left: 5px solid #00ab4e; border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}

        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_platinum_styling()

# --- 2. DATA PERSISTENCE & MANUAL LOGIN GATE ---
if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False

if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "7": {
            "first_name": "Vinícius", "last_name": "Júnior", "shirt_number": "7",
            "medical": {"age": 25, "weight": 73.0, "risk": "Low", "history": "ACL Rehab complete (2025)"},
            "roadmap": []
        }
    }

# FIXED LOGIN: Using st.form + unique keys to prevent auto-fill and "Access Denied" bugs
if not st.session_state.logged_in:
    st.title("🛡️ ELITE HUB LOGIN")
    with st.form("manual_auth_gate"):
        # Unique keys stop browser pre-fill; value="" ensures empty start
        u_input = st.text_input("Username", value="", key="u_manual_gate")
        p_input = st.text_input("Password", type="password", value="", key="p_manual_gate")
        submit = st.form_submit_button("Unlock Command Center")
        
        if submit:
            if u_input == "admin" and p_input == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied: Please check your manual entries.")
    st.stop()

# --- 3. AI CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception: pass

# --- 4. NAVIGATION ---
tabs = st.tabs(["📊 Overview", "🏃 Squad Registry", "🩺 Medical Hub", "🤖 Virtual Coach", "🎥 Performance Audit", "📅 Roadmap"])
p_options = {uid: f"#{d['shirt_number']} {d['first_name']} {d['last_name']}" for uid, d in st.session_state.profiles.items()}

# FIXED INDENTATION: Correcting the errors from image_08a5db.png
with tabs[0]: 
    st.header("🏆 Squad Status Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'>Squad Size<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Injury Risk Score<br><span class='kpi-val'>Low</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>AI Analysis Tier<br><span class='kpi-val'>Paid</span></div>", unsafe_allow_html=True)
    st.divider()
    st.subheader("📋 Athlete Readiness Status")
    status_list = []
    for uid, d in st.session_state.profiles.items():
        med = d.get('medical', {})
        status_list.append({
            "Athlete": f"#{d['shirt_number']} {d['first_name']}",
            "Risk": med.get('risk', 'N/A'),
            "Age": med.get('age', 'N/A')
        })
    st.table(status_list)

with tabs[1]: # SQUAD REGISTRY
    st.header("🏃 Athlete Master Registry")
    with st.form("reg_final", clear_on_submit=True):
        f_in, l_in, n_in = st.columns(3)
        f_new = f_in.text_input("First Name")
        l_new = l_in.text_input("Last Name")
        n_new = n_in.text_input("Shirt Number")
        if st.form_submit_button("Confirm Registration"):
            if f_new and l_new and n_new:
                st.session_state.profiles[n_new] = {
                    "first_name": f_new, "last_name": l_new, "shirt_number": n_new,
                    "medical": {"age": 0, "weight": 0.0, "risk": "Low", "history": ""},
                    "roadmap": []
                }
                st.success(f"Registered #{n_new}"); st.rerun()

with tabs[2]: # MEDICAL HUB
    st.header("🩺 Athlete Clinical Profile")
    p_uid_med = st.selectbox("Select Profile", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="med_p_sel")
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
        player_med = st.session_state.profiles[p_uid_med]
        st.subheader(f"Update: {player_med['first_name']}")
        w_up = st.number_input("Weight (kg)", value=float(player_med["medical"].get("weight", 0.0)))
        a_up = st.number_input("Age", value=int(player_med["medical"].get("age", 0)))
        r_up = st.selectbox("Injury Risk Status", ["Low", "Medium", "High"])
        if st.button("Sync Profile Data"):
            st.session_state.profiles[p_uid_med]["medical"].update({"weight": w_up, "age": a_up, "risk": r_up})
            st.success("Synchronized."); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_bin: b64 = base64.b64encode(f_bin.read()).decode()
            fig = go.Figure()
            # FIXED PLOTLY SYNTAX: sizey corrected to prevent ValueErrors
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{b64}", 
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"
            ))
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Risk", "Calf Strain"], textposition="middle right", marker=dict(size=45, color="#ff4b4b", line=dict(width=3, color='white'))))
            fig.update_layout(width=700, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]), margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]: # VIRTUAL COACH (MM:SS Timestamps)
    st.header("🤖 Virtual Coach AI Assistant")
    c_uid_v = st.selectbox("Target Player", options=list(p_options.keys()), format_func=lambda x: p_options[x], key="coach_p_sel")
    vid_v = st.file_uploader("Upload Session Video", type=['mp4', 'mov'], key="coach_vid_up")
    if vid_v and 'client' in locals():
        st.video(vid_v)
        if st.button("Generate Technical Audit"):
            with st.status("🤖 Analyzing metrics and timestamps..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid_v.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    prompt = f"Target shirt #{st.session_state.profiles[c_uid_v]['shirt_number']}. Analyze: 1. Technical KPIs. 2. Tactical errors with bold MM:SS timestamps. 3. Body form efficiency."
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[c_uid_v]["roadmap"].append({"date": "2026-01-19", "type": "Coach Session", "note": resp.text})
                    st.success("Audit Archived."); st.rerun()
                except Exception as e