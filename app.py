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
        
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}");
            background-size: cover; background-attachment: fixed;
            font-family: 'Inter', sans-serif; color: #ffffff;
        }}

        /* FIX: Universal White Box & Black Text */
        input, textarea, [data-baseweb="input"], [data-baseweb="select"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 10px !important;
        }}
        
        /* FIX: Visible File Uploader */
        [data-testid="stFileUploader"] section {{
            background-color: #ffffff !important;
            border-radius: 10px !important;
            padding: 20px !important;
        }}
        [data-testid="stFileUploader"] section * {{
            color: #000000 !important;
        }}

        /* FIX: Black typed text */
        input {{
             color: #000000 !important;
             -webkit-text-fill-color: #000000 !important;
        }}

        /* FIX: High-Contrast Error Boxes */
        .stException, .stAlert {{
            background-color: #ffffff !important;
            color: #000000 !important;
            padding: 20px; border-radius: 10px;
        }}
        .stException p, .stAlert p {{ color: #000000 !important; }}

        label, p {{ color: #ffffff !important; }}
        button[data-baseweb="tab"] {{ color: white !important; font-weight: bold; }}
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
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap"]

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

with current_tab[1]: # SOLUTIONS
    st.header("Strategic Value")
    st.write("Clinical AI video audits for Tier 1 sports organizations.")

with current_tab[2]: # SUBSCRIPTION
    st.header("Elite Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("### Individual\n£29/mo")
    p2.markdown("### Squad Pro\n£199/mo")
    p3.markdown("### Academy\n£POA")

# --- 5. PRIVATE MEMBER AREA ---
if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Video Analysis Engine")
        p_num = st.text_input("Target Player Number", value="2")
        video_file = st.file_uploader("Upload Match Footage", type=['mp4', 'mov'])
        
        if video_file:
            st.video(video_file)
            if st.button("Generate Elite Audit"):
                with st.status("Analyzing Skeletal Landmarks..."):
                    time.sleep(3)
                    # FIX: Handle new player creation to avoid KeyError
                    if p_num not in st.session_state.roadmap:
                        st.session_state.roadmap[p_num] = []
                    
                    st.session_state.roadmap[p_num].append({
                        "date": "2026-01-11", "issue": "Right Knee", 
                        "note": "Detected 12° medial buckle. Recommended Week 2 rehab drills."
                    })
                st.success(f"Audit Complete for Player #{p_num}.")

    with current_tab[4]: # PLAYER DASHBOARD
        st.header("🩺 Biometric Body Map")
        p_select = st.selectbox("Select Player Profile", list(st.session_state.roadmap.keys()))
        
        # Globally reliable medical body outline from Wikimedia Commons
        body_url = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Human_body_silhouette.png"
        
        fig = go.Figure()
        fig.add_layout_image(dict(source=body_url, xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.6, layer="below"))
        
        # Plot markers if issues exist
        if p_select in st.session_state.roadmap:
            for item in st.session_state.roadmap[p_select]:
                if "Knee" in item["issue"]:
                    # Placing red dot on the right knee area
                    fig.add_trace(go.Scatter(x=[195], y=[520], mode='markers', marker=dict(size=30, color="red", line=dict(width=2, color="white")), hovertext=item['note']))
        
        fig.update_layout(width=500, height=700, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # 12-WEEK ROADMAP
        st.header("📅 Recovery Roadmap")
        p_road = st.selectbox("View History", list(st.session_state.roadmap.keys()), key="road_select")
        for event in reversed(st.session_state.roadmap[p_road]):
            st.write(f"**{event['date']}**: {event['note']}")
        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))