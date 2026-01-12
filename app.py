import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & VISIBILITY SHIELD ---
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

# --- 2. AI INITIALIZATION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ Key Missing: Add GEMINI_API_KEY to Streamlit Secrets.")
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

# --- 5. PUBLIC PAGES ---
with tabs[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        u = st.text_input("Username", placeholder="admin", key="u_log_final")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="p_log_final")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with tabs[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### ⚽ Core Disciplines\n- Football\n- Rugby\n- Basketball")
    with c2:
        st.write("### 💎 Value Strategy\n**Health:** AI Injury Prevention\n**Play:** Technical Tactical Audit")

with tabs[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2></div>", unsafe_allow_html=True)
    c2.markdown("<div class='luxury-card' style='border-color:#00ab4e!important;'><h3>Squad Pro</h3><h2>£199/mo</h2></div>", unsafe_allow_html=True)
    c3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2></div>", unsafe_allow_html=True)

# --- 6. PROTECTED PAGES ---
if st.session_state.logged_in:
    with tabs[3]: # ANALYSIS ENGINE (PURGE VERSION)
        st.header("🎥 Live AI Technical Audit")
        vf = st.file_uploader("Upload Match Clip", type=['mp4', 'mov'])
        if vf and 'client' in locals():
            st.video(vf)
            if st.button("Generate Dual-Track Analysis"):
                with st.status("🤖 FORCE PURGING CLOUD STORAGE..."):
                    try:
                        # Clear zombie files to fix the "taking forever" issue
                        for file in client.files.list():
                            client.files.delete(name=file.name)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                            tmp.write(vf.getvalue())
                            t_path = tmp.name
                        
                        upf = client.files.upload(file=t_path)
                        resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=["Identify injury risk and tactical play.", upf])
                        st.session_state.roadmap["22"].append({"date": "2026-01-12", "category": "AI", "note": resp.text})
                        client.files.delete(name=upf.name)
                        os.remove(t_path)
                        st.success("Analysis Complete.")
                    except Exception as e:
                        st.error(f"Quota Wait: Please wait 60s for Google to reset.")

    with tabs[4]: # PLAYER DASHBOARD (ALIGNMENT FIX)
        st.header("🩺 Biometric Injury Mapping")
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f: b64 = base64.b64encode(f.read()).decode()
            fig = go.Figure()
            # Scaling fix for holographic image
            fig.add_layout_image(dict(source=f"data:image/png;base64,{b64}", xref="x", yref="y", x=0, y=1000, sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"))
            
            # --- PIN COORDINATES (Move these to align with limbs) ---
            # X: 0 (Left) to 1000 (Right) | Y: 0 (Bottom) to 1000 (Top)
            fig.add_trace(go.Scatter(
                x=[480, 475], y=[330, 180], # Centered on leg joints of holographic mannequin
                mode='markers+text', text=["Knee ACL", "Calf Strain"], textposition="middle right",
                textfont=dict(color="white", size=15),
                marker=dict(size=40, color="rgba(255, 75, 75, 0.7)", symbol="circle", line=dict(width=3, color='white'))
            ))
            fig.update_layout(width=800, height=800, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("📸 digital_twin.png not found.")