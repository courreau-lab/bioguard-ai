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
        
        /* FORCE ALL TEXT TO WHITE FOR LUXURY CONTRAST */
        html, body, [class*="st-"], .stMarkdown, p, div {{
            font-family: 'Inter', sans-serif;
            color: #ffffff !important;
        }}
        
        /* FIXED BACKGROUND */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* NAVIGATION TABS: STRICT WHITE ON DARK */
        button[data-baseweb="tab"] {{
            background-color: transparent !important;
        }}
        button[data-baseweb="tab"] div {{
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            border-bottom: 3px solid #00ab4e !important;
        }}
        
        /* CARDS & CONTAINERS */
        .luxury-card, .roadmap-card {{
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 15px;
        }}
        
        /* INPUT FIELDS VISIBILITY */
        input {{ color: white !important; background-color: rgba(255,255,255,0.1) !important; }}
        
        .stButton>button {{ 
            border-radius: 50px; 
            border: 1px solid #00ab4e; 
            color: white !important; 
            background: transparent; 
            padding: 10px 25px;
        }}
        .stButton>button:hover {{ background: #00ab4e; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        # Standard 2026 GenAI Integration
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ AI Brain Offline: GEMINI_API_KEY missing from Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Link Failed: {e}")

# --- 3. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "2": [{"date": "2026-01-11", "category": "Health", "note": "Initial baseline established."}]
    }

# --- 4. NAVIGATION MENU ---
# Tabs remain white-on-dark due to the CSS inject above
menu_options = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]

current_tab = st.tabs(menu_options)

# --- 5. PUBLIC PAGES ---
with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    st.subheader("Bespoke AI Diagnostics & Performance Optimization")
    if not st.session_state.logged_in:
        st.divider()
        st.write("### Partner Portal Access")
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="owner2026")
        if st.button("Unlock Elite Capabilities"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[1]: # OFFER
    st.header("The Competitive Advantage")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("### ⚽ Disciplines")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball")
    with c_b:
        st.write("### 💎 Value Strategy")
        st.write("**Health:** Injury prevention via clinical gait analysis.")
        st.write("**Play:** Performance gains via tactical scanning audits.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad Dual Audits<br>Interactive Body Map</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Custom 3D Scanning<br>Medical API Access</p></div>", unsafe_allow_html=True)

# --- 6. PROTECTED MEMBER PAGES ---
if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Live AI Technical Audit")
        st.write("Upload video highlights for biomechanical and tactical extraction.")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Select MP4/MOV Clip", type=['mp4', 'mov'])
        
        if video_file and 'client' in locals():
            st.video(video_file)
            if st.button("Generate Dual-Track Elite Analysis"):
                with st.status("🤖 AI Engine analyzing video...", expanded=True):
                    prompt = """Analyze this video as a Lead Sports Scientist. 
                               1. HEALTH: Injury risks (knee valgus, gait). 
                               2. PLAY: Performance (scanning/tactics). 
                               Provide two clinical notes."""
                    try:
                        # Direct Google Gemini 2.0 Integration
                        response = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, video_file])
                        st.session_state.roadmap[p_num].append({"date": "2026-01-11", "category": "AI Audit", "note": response.text})
                        st.success("Analysis Complete.")
                    except Exception as e:
                        st.error(f"AI Failure: {e}")

    with current_tab[4]: # PLAYER DASHBOARD
        st.header("🩺 Biometric Body Map")
        p_id = st.selectbox("Select Player Profile", list(st.session_state.roadmap.keys()))
        # Interactive Plotly Body Map
        fig = go.Figure()
        fig.add_layout_image(dict(source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=30, color="red"), hovertext="Critical Alert: Knee Stability"))
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # ROADMAP
        st.header("📅 Integrated 12-Week Roadmap")
        p_sel = st.selectbox("View History", list(st.session_state.roadmap.keys()), key="rd_view")
        for entry in reversed(st.session_state.roadmap[p_sel]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)
        st.warning("⚠️ RECOVERY FOCUS: ACL risk mitigation and transition scanning drills.")

    with current_tab[6]: # ADMIN
        st.header("Elite Management Hub")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()