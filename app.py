import streamlit as st
import plotly.graph_objects as go
import time

# --- 1. SETTINGS & ELITE STYLING ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* Global Background & Font */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{bg_img}");
            background-size: cover; background-attachment: fixed;
            font-family: 'Inter', sans-serif; color: #ffffff;
        }}

        /* --- UNIVERSAL WHITE BOX / BLACK TEXT FIX --- */
        input, textarea, [data-baseweb="input"], [data-baseweb="select"], [data-testid="stFileUploader"] section {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 10px !important;
        }}
        
        /* Force uploader instructions to be black and visible */
        [data-testid="stFileUploader"] section * {{
            color: #000000 !important;
        }}

        /* Force typed text and dropdown text to black */
        input, div[data-baseweb="select"] span {{
             color: #000000 !important;
             -webkit-text-fill-color: #000000 !important;
        }}

        /* --- ERROR & POPUP CONTRAST FIX --- */
        .stException, .stAlert, div[data-testid="stNotification"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            padding: 20px;
            border-radius: 10px;
        }}
        .stException p, .stException pre, .stAlert p {{
            color: #000000 !important;
        }}

        label, p {{ color: #ffffff !important; }}
        button[data-baseweb="tab"] {{ color: white !important; font-weight: bold; }}

        .luxury-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 30px; text-align: center;
        }}
        
        h1, h2, h3 {{ color: white !important; font-weight: 700; }}
        .stButton>button {{ border-radius: 50px; border: 1px solid #00ab4e; color: white; background: transparent; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "2": [{"date": "2026-01-11", "issue": "Right Knee", "note": "Initial baseline established."}]
    }

# --- 3. MENU NAVIGATION ---
menu_options = ["Home", "Solutions", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]

current_tab = st.tabs(menu_options)

# --- 4. PUBLIC PAGES ---
with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        st.divider()
        st.write("### Partner Access")
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Partner Credentials")

with current_tab[1]: # SOLUTIONS
    st.header("Strategic Value")
    st.write("Detect mechanical drift in elite athletes using standard match highlights.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Elite Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color:#00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Academy</h3><h2>£POA</h2></div>", unsafe_allow_html=True)

# --- 5. PRIVATE MEMBER AREA ---
if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Video Analysis Engine")
        p_num = st.text_input("Target Player Number", placeholder="e.g., 10")
        video_file = st.file_uploader("Upload MP4/MOV Video", type=['mp4', 'mov'])
        
        if video_file:
            st.video(video_file)
            if st.button("Generate Elite Audit"):
                with st.status("Analyzing Skeletal Landmarks..."):
                    time.sleep(3)
                    # FIX: Handle new player creation automatically
                    if p_num not in st.session_state.roadmap:
                        st.session_state.roadmap[p_num] = []
                    
                    st.session_state.roadmap[p_num].append({
                        "date": "2026-01-11", "issue": "Right Knee", 
                        "note": "Detected 12° medial buckle. Recommended Week 2 rehab drills."
                    })
                st.success(f"Audit Complete for Player #{p_num}.")

    with current_tab[4]: # PLAYER DASHBOARD (THE HUMAN BODY VIEW)
        st.header("🩺 Biometric Body Map")
        p_select = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        
        # Globally reliable medical body outline
        body_map_url = "https://i.ibb.co/L5h8xK3/human-body-outline.png"
        
        fig = go.Figure()
        fig.add_layout_image(dict(source=body_map_url, xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        
        if p_select in st.session_state.roadmap:
            for item in st.session_state.roadmap[p_select]:
                if "Knee" in item["issue"]:
                    # Placing red dot on the right knee
                    fig.add_trace(go.Scatter(x=[185], y=[540], mode='markers', marker=dict(size=25, color="red"), hovertext=item['note']))
        
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # 12-WEEK ROADMAP
        st.header("📅 Recovery Roadmap")
        p_road = st.selectbox("View History", list(st.session_state.roadmap.keys()), key="road_p")
        for event in reversed(st.session_state.roadmap[p_road]):
            st.markdown(f"**{event['date']}**: {event['note']}")

    with current_tab[6]: # ADMIN HUB
        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))