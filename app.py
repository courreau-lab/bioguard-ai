import streamlit as st
import plotly.graph_objects as go
from google import genai
import time

# --- 1. GLOBAL UI & LUXURY BRANDING ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    # Cinematic Stadium Background
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* Global Text & Font */
        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
            color: #ffffff !important;
        }}
        
        /* Fixed Background */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{bg_img}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* NAVIGATION: Force Menu Tabs to White */
        button[data-baseweb="tab"] {{
            color: white !important;
            font-weight: 600 !important;
        }}
        
        /* Luxury Metric & Roadmap Cards */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 15px;
        }}
        
        h1, h2, h3 {{ color: white !important; font-weight: 700; }}
        .stButton>button {{ border-radius: 50px; border: 1px solid #00ab4e; color: white; background: transparent; }}
        .stButton>button:hover {{ background: #00ab4e; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION ---
# Connects to your Streamlit Secret: GEMINI_API_KEY
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ AI Brain Offline: Please add GEMINI_API_KEY to Streamlit Secrets.")
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "2": [{"date": "2026-01-11", "category": "Health", "note": "Platform Initialized. System ready for AI Audit."}]
    }

# --- 4. NAVIGATION MENU ---
menu_options = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Console"]

current_tab = st.tabs(menu_options)

# --- 5. PUBLIC PAGES ---

with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    st.subheader("Bespoke AI Diagnostics & Performance Optimization")
    if not st.session_state.logged_in:
        st.divider()
        st.write("### Partner Access")
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="owner2026")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("⚽ Covered Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col_b:
        st.subheader("💎 Service Value")
        st.write("**Health:** AI-driven injury prevention and clinical gait analysis.")
        st.write("**Play:** Performance improvement through tactical intelligence audits.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>1 Player Analysis<br>Basic Health Metrics</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Integration<br>Interactive Body Map<br>Dual Health/Play Audits</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Custom 3D Scanning<br>Medical API Access<br>Full Club Management</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED MEMBER PAGES ---

if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        st.write("Upload raw footage for biomechanical and tactical extraction.")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Upload Match Highlight", type=['mp4', 'mov'])
        
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Run Multi-Modal Elite Analysis"):
                with st.status("🤖 AI analyzing movement and tactical patterns...", expanded=True):
                    # REAL AI INSTRUCTION
                    prompt = """
                    Analyze this sports footage as a Lead Biomechanist and Performance Coach. 
                    1. HEALTH: Identify any injury risks like knee valgus, gait asymmetry, or trunk lean.
                    2. PLAY: Identify performance improvement areas like scanning frequency or spatial positioning.
                    Provide two distinct clinical notes for a 12-week roadmap.
                    """
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.0-flash-exp",
                            contents=[prompt, video_file]
                        )
                        # Store the real AI result
                        st.session_state.roadmap[p_num].append({
                            "date": "2026-01-11", "category": "AI Audit", "note": response.text
                        })
                        st.success("Analysis Complete. Progress pushed to Roadmap.")
                    except Exception as e:
                        st.error(f"AI Analysis Failed: {e}")

    with current_tab[4]: # PLAYER DASHBOARD
        st.header("🩺 Biometric Body Map")
        p_sel = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        fig = go.Figure()
        fig.add_layout_image(dict(source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=25, color="red"), hovertext="Critical: Right Knee Stability Risk"))
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # 12-WEEK ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_id = st.selectbox("View History", list(st.session_state.roadmap.keys()), key="rd_view")
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)
        st.warning("⚠️ RECOVERY SUMMARY: Priority on ACL prevention drills and scanning awareness training.")

    with current_tab[6]: # ADMIN
        st.header("System Management")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()