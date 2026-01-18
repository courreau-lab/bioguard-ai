import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & TOTAL VISIBILITY ---
st.set_page_config(page_title="Elite Squad | BioGuard AI", layout="wide")

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
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION & AUTOMATIC PURGE ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # FORCE PURGE: Clears files immediately on boot to prevent "Resource Exhausted"
        for f in client.files.list(): client.files.delete(name=f.name)
    else:
        st.warning("⚠️ Secret missing. Add GEMINI_API_KEY to Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. PERSISTENT SQUAD DATA ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "profiles" not in st.session_state:
    st.session_state.profiles = {
        "Player 1": {"medical": {"age": 24, "weight": 78, "history": "ACL Reconstruction (2024)"}, "roadmap": []}
    }

# --- 4. NAVIGATION ---
tab_names = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tab_names += ["Medical Hub", "Analysis Engine", "Player Dashboard", "12-Week Roadmap"]
tabs = st.tabs(tab_names)

with tabs[0]: # LOGIN
    st.title("🛡️ ELITE SQUAD PORTAL")
    if not st.session_state.logged_in:
        u = st.text_input("Username", value="admin", key="u_log")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="p_log")
        if st.button("Unlock Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

if st.session_state.logged_in:
    with tabs[3]: # MEDICAL HUB
        st.header("🩺 Squad Medical Registry")
        
        # ADD NEW PLAYER PROFILE
        with st.expander("➕ Register New Athlete"):
            new_p = st.text_input("Full Name")
            if st.button("Add to Database"):
                if new_p and new_p not in st.session_state.profiles:
                    st.session_state.profiles[new_p] = {"medical": {"age": 0, "weight": 0, "history": "None"}, "roadmap": []}
                    st.success(f"Athlete {new_p} added."); st.rerun()

        p_id = st.selectbox("Select Athlete", options=list(st.session_state.profiles.keys()))
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
            w = st.number_input("Weight (kg)", value=float(st.session_state.profiles[p_id]["medical"]["weight"]))
            a = st.number_input("Age", value=int(st.session_state.profiles[p_id]["medical"]["age"]))
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
            hist = st.text_area("Injury History", value=st.session_state.profiles[p_id]["medical"]["history"])
            if st.button("Save Profile"):
                st.session_state.profiles[p_id]["medical"] = {"weight": w, "age": a, "history": hist}
                st.success("Clinical record updated.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[4]: # ANALYSIS ENGINE
        st.header("🎥 Shirt-Color Targeted Performance Audit")
        target_p = st.selectbox("Assign to Profile", options=list(st.session_state.profiles.keys()))
        color = st.text_input("Identify Player Shirt Color", placeholder="e.g., White shirt number 10")
        
        vid = st.file_uploader("Upload Match Video", type=['mp4', 'mov'])
        if vid and 'client' in locals():
            st.video(vid)
            if st.button("Run Targeted AI Analysis"):
                with st.status("🤖 Paid Tier: Analyzing specific target...") as status:
                    try:
                        for f in client.files.list(): client.files.delete(name=f.name)
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(vid.getvalue()); t_path = tmp.name
                        upf = client.files.upload(file=t_path)
                        while upf.state.name == "PROCESSING":
                            time.sleep(2); upf = client.files.get(name=upf.name)
                        
                        prompt = f"Focus ONLY on the player wearing: {color}. Provide: 1. Technical Summary, 2. Training Plan."
                        resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, upf])
                        
                        st.session_state.profiles[target_p]["roadmap"].append({"date": "2026-01-18", "category": "AI Performance Plan", "note": resp.text})
                        client.files.delete(name=upf.name); os.remove(t_path)
                        st.balloons(); st.success("Audit delivered to Roadmap.")
                    except Exception as e: st.error(f"Error: {e}")

    with tabs[5]: # DASHBOARD
        st.header("🩺 Digital Twin Alignment Fix")
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_b: b64 = base64.b64encode(f_b.read()).decode()
            fig = go.Figure()
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64}", xref="x", yref="y", x=0, y=1000, sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"))
            # RECALIBRATED: Midline Alignment (X=500) for portrait mannequin
            fig.add_trace(go.Scatter(x=[500, 500], y=[235, 125], mode='markers+text', text=["ACL Risk", "Calf Strain"], textposition="middle right", marker=dict(size=40, color="rgba(255, 75, 75, 0.7)", line=dict(width=3, color='white'))))
            fig.update_layout(width=800, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)

    with tabs[6]: # ROADMAP
        st.header("📅 Historical Clinical Roadmap")
        view_p = st.selectbox("View History for", options=list(st.session_state.profiles.keys()))
        for entry in reversed(st.session_state.profiles[view_p]["roadmap"]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']} - {entry['category']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)