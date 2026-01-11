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
        
        /* 1. GLOBAL TEXT OVERRIDE - FORCES WHITE ON EVERY PAGE */
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, label, .stTabs {{
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* 2. FIXED BACKGROUND */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* 3. NAVIGATION TABS: WHITE TEXT & DARK BACKDROP */
        button[data-baseweb="tab"] {{
            background-color: transparent !important;
            border: none !important;
        }}
        button[data-baseweb="tab"] div {{
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            border-bottom: 3px solid #00ab4e !important;
        }}
        
        /* 4. LUXURY CARDS & ROADMAP CARDS */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.07) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 20px !important;
            padding: 25px !important;
            margin-bottom: 15px !important;
            color: white !important;
        }}
        
        /* 5. INPUT FIELDS & BUTTONS */
        input {{ 
            color: white !important; 
            background-color: rgba(255,255,255,0.1) !important; 
            border: 1px solid rgba(255,255,255,0.2) !important;
        }}
        
        .stButton>button {{ 
            border-radius: 50px !important; 
            border: 2px solid #00ab4e !important; 
            color: white !important; 
            background: rgba(0, 171, 78, 0.1) !important; 
            padding: 10px 30px !important;
            font-weight: 700 !important;
        }}
        .stButton>button:hover {{ 
            background: #00ab4e !important; 
            color: white !important;
        }}

        /* 6. SIDEBAR FIX */
        [data-testid="stSidebar"] {{
            background-color: rgba(0,0,0,0.9) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ AI Offline: GEMINI_API_KEY not found in Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Link Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "2": [{"date": "2026-01-11", "category": "Health", "note": "Baseline scan ready for AI audit."}]
    }

# --- 4. NAVIGATION MENU ---
# Logic: Always show public tabs; unlock private tabs on login.
menu_options = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]

current_tab = st.tabs(menu_options)

# --- 5. PUBLIC PAGES (Home, Offer, Pricing) ---
with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    st.markdown("### Bespoke AI Diagnostics & Performance Optimization")
    if not st.session_state.logged_in:
        st.divider()
        st.markdown("### Partner Portal Access")
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="owner2026")
        if st.button("Unlock Elite Capabilities"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[1]: # BUSINESS OFFER
    st.header("The Competitive Advantage")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚽ Core Disciplines")
        st.markdown("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.markdown("### 💎 Value Strategy")
        st.markdown("**Injury Prevention:** Clinical biomechanics for non-contact risk mitigation.")
        st.markdown("**Performance Gain:** Tactical intelligence and spatial awareness audits.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit<br>Injury Risk Baseline</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e !important;'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Interactive Body Map<br>12-Week Roadmap</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Custom 3D Scanning<br>Medical API Access<br>Multi-Team Management</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED MEMBER PAGES ---
if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE (Video Loader)
        st.header("🎥 Live AI Technical Audit")
        st.markdown("Upload video highlights for biomechanical and tactical extraction.")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Select Match Clip (MP4/MOV)", type=['mp4', 'mov'])
        
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Generate Dual-Track Elite Analysis"):
                with st.status("🤖 AI Engine analyzing video...", expanded=True):
                    prompt = "Analyze this sports video. 1. HEALTH (injury risk). 2. PLAY (tactical improvement). Return two clinical notes."
                    try:
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, video_file])
                        st.session_state.roadmap[p_num].append({"date": "2026-01-11", "category": "AI Audit", "note": response.text})
                        st.success("Analysis Complete. Progress pushed to Roadmap.")
                    except Exception as e:
                        st.error(f"AI Failure: {e}")

    with current_tab[4]: # PLAYER DASHBOARD (Body Map)
        st.header("🩺 Biometric Body Map")
        p_sel = st.selectbox("Select Player Profile", list(st.session_state.roadmap.keys()))
        
        # Interactive Body Map
        fig = go.Figure()
        fig.add_layout_image(dict(source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=30, color="#ff4b4b", line=dict(width=2, color='white')), hovertext="Critical Alert: Knee Stability"))
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_view = st.selectbox("View Player History", list(st.session_state.roadmap.keys()), key="rd_view")
        for entry in reversed(st.session_state.roadmap[p_view]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)
        st.warning("⚠️ RECOVERY FOCUS: ACL risk mitigation and transition scanning drills.")

    with current_tab[6]: # ADMIN HUB
        st.header("Elite Management Hub")
        st.markdown("### System Owner Tools")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()