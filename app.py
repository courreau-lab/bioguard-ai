import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. LUXURY INTERFACE STYLING ---
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
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; background: rgba(0, 171, 78, 0.2) !important; color: white !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA SAFETY & LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# SAFE DATA INITIALIZATION: Prevents the KeyError seen in your screenshots
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "Player 1": {"medical": {"age": 24, "weight": 78.0, "risk": "Low"}, "roadmap": []}
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
        for f in client.files.list(): client.files.delete(name=f.name)
    else: st.warning("⚠️ Secret missing: GEMINI_API_KEY")
except Exception as e: st.error(f"AI Failed: {e}")

# --- 4. COMMAND CENTER NAVIGATION ---
tabs = st.tabs(["📊 Squad Overview", "🧬 Athlete Medical Hub", "🎥 AI Performance Audit", "📅 Performance Roadmap"])

with tabs[0]: # SQUAD OVERVIEW (ERROR-FREE VERSION)
    st.header("🏆 Squad Performance Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'>Active Athletes<br><span class='kpi-val'>{len(st.session_state.profiles)}</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='kpi-card'>Clinical System<br><span class='kpi-val'>Online</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='kpi-card'>AI Tier<br><span class='kpi-val'>Paid</span></div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📋 Athlete Readiness Status")
    # Table logic with safety defaults to prevent KeyErrors
    squad_data = []
    for name, data in st.session_state.profiles.items():
        squad_data.append({
            "Athlete": name,
            "Age": data["medical"].get("age", "N/A"),
            "Weight (kg)": data["medical"].get("weight", "N/A"),
            "Injury Risk": data["medical"].get("risk", "N/A")
        })
    st.table(squad_data)

with tabs[1]: # MEDICAL HUB & DIGITAL TWIN
    st.header("🧬 Clinical Biometrics")
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        p_id = st.selectbox("Select Athlete", options=list(st.session_state.profiles.keys()), key="med_sel")
        st.subheader(f"Update: {p_id}")
        new_w = st.number_input("Weight (kg)", value=float(st.session_state.profiles[p_id]["medical"]["weight"]))
        new_a = st.number_input("Age", value=int(st.session_state.profiles[p_id]["medical"]["age"]))
        new_r = st.selectbox("Injury Risk", ["Low", "Medium", "High"], index=0)
        if st.button("Sync Medical Data"):
            st.session_state.profiles[p_id]["medical"].update({"weight": new_w, "age": new_a, "risk": new_r})
            st.success("Synchronized.")

    with col_r:
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_b: b64 = base64.b64encode(f_b.read()).decode()
            fig = go.Figure()
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64}", xref="x", yref="y", x=0, y=1000, sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"))
            # CENTERED PINS (X=500) for your tall mannequin
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Stress", "Calf Fatigue"], textposition="middle right", marker=dict(size=40, color="#ff4b4b", line=dict(width=3, color='white'))))
            fig.update_layout(width=600, height=700, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]), margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # ANALYSIS ENGINE
    st.header("🎥 Shirt-Color Targeted Audit")
    target_p = st.selectbox("Analyze Profile", options=list(st.session_state.profiles.keys()))
    shirt = st.text_input("Shirt Color to Track", placeholder="e.g. Red shirt number 10")
    vid = st.file_uploader("Upload Clip", type=['mp4', 'mov'])
    
    if vid and 'client' in locals():
        st.video(vid)
        if st.button("Execute Targeted Analysis"):
            with st.status("🤖 Analyzing (Paid Tier)..."):
                try:
                    for f in client.files.list(): client.files.delete(name=f.name)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(vid.getvalue()); t_path = tmp.name
                    upf = client.files.upload(file=t_path)
                    while upf.state.name == "PROCESSING": time.sleep(2); upf = client.files.get(name=upf.name)
                    prompt = f"Target player in {shirt}. Summarize performance and provide a 1-week plan."
                    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                    st.session_state.profiles[target_p]["roadmap"].append({"date": "2026-01-18", "note": resp.text})
                    client.files.delete(name=upf.name); os.remove(t_path)
                    st.success("✅ Audit Complete.")
                except Exception as e: st.error(f"Failed: {e}")

with tabs[3]: # ROADMAP
    st.header("📅 Integrated Clinical Roadmap")
    view_p = st.selectbox("View Roadmap", options=list(st.session_state.profiles.keys()))
    for entry in reversed(st.session_state.profiles[view_p]["roadmap"]):
        st.markdown(f"<div style='background:rgba(255,255,255,0.08); padding:20px; border-radius:15px; border-left:5px solid #00ab4e; margin-bottom:10px;'><strong>{entry['date']} Audit</strong><br>{entry['note']}</div>", unsafe_allow_html=True)