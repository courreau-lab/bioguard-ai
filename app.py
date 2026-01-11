import streamlit as st
import plotly.graph_objects as go
import time, random, string

# --- 1. SETTINGS & ELITE BRANDING ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600;800&display=swap');
        
        html, body, [class*="st-"] { font-family: 'Montserrat', sans-serif; color: #f0f0f0; }
        
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url("https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&q=80&w=2000");
            background-size: cover; background-attachment: fixed;
        }

        /* Top Menu Bar */
        .top-nav {
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 50px; background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(15px); border-bottom: 2px solid #00ab4e;
            position: fixed; top: 0; left: 0; right: 0; z-index: 999;
        }

        /* Luxury Cards */
        .tier-card {
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px; padding: 30px; text-align: center; height: 100%;
        }
        
        .stButton>button { border-radius: 50px; border: 1px solid #00ab4e; background: transparent; color: white; transition: 0.3s; }
        .stButton>button:hover { background: #00ab4e; border-color: #00ab4e; }
    </style>
    """, unsafe_allow_html=True)

apply_elite_theme()

# --- 2. SESSION & DATABASE STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmaps" not in st.session_state:
    st.session_state.roadmaps = {"2": [{"date": "2026-01-11", "issue": "Right Knee", "note": "Gait asymmetry"}]}

# --- 3. THE MENU BAR ---
# Using Streamlit columns to simulate a top navigation bar
st.markdown("<br><br>", unsafe_allow_html=True) # Spacer for fixed nav
col_logo, col_menu = st.columns([1, 2])

with col_logo:
    st.markdown("## 🛡️ ELITE PERFORMANCE")

with col_menu:
    # Navigation items
    nav_tabs = ["Home", "Solutions", "Subscription"]
    if st.session_state.logged_in:
        nav_tabs += ["Analysis", "12-Week Roadmap", "Admin"]
    
    current_page = st.tabs(nav_tabs)

# Login Trigger in Sidebar for a clean UI
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    if not st.session_state.logged_in:
        st.subheader("Partner Access")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Unlock Capabilities"):
            if user == "admin" and pw == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
    else:
        st.success(f"Connected: {user if 'user' in locals() else 'Admin'}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# --- 4. PAGE LOGIC ---

# 4A. HOME PAGE (Public)
with current_page[0]:
    st.markdown("<h1 style='text-align: center;'>The Future of Athlete Preservation</h1>", unsafe_allow_html=True)
    st.write("### Elite Performance provides proprietary AI diagnostics for Tier 1 organizations.")
    st.divider()
    st.header("Covered Disciplines")
    st.write("⚽ Football (Soccer) | 🏉 Rugby Union & League | 🏀 Basketball | 🏈 American Football")

# 4B. SOLUTIONS (Public)
with current_page[1]:
    st.header("Our Business Value")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Clinical Data vs. Video Evidence")
        st.write("We bridge the gap between physio-room data and pitch-side reality. Our AI audits biomechanics from standard match highlights.")
    with c2:
        st.subheader("ROI for Clubs")
        st.write("Reducing non-contact injuries by 15% saves a Premier League club an average of £4.2M per season in lost player availability.")

# 4C. SUBSCRIPTIONS (Public)
with current_page[2]:
    st.header("Elite Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='tier-card'><h3>Individual</h3><p>£29/mo</p><p>Standard AI Analytics</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='tier-card'><h3>Squad Pro</h3><p>£199/mo</p><p>Unlimited Analysis<br>Interactive Body Map</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='tier-card'><h3>Academy</h3><p>£POA</p><p>Custom 3D Scanning<br>Full Medical Integration</p></div>", unsafe_allow_html=True)

# 4D. PROTECTED PAGES (Only if logged in)
if st.session_state.logged_in:
    # ANALYSIS ENGINE
    with current_page[3]:
        st.header("Video Analysis Engine")
        st.write("Upload match highlights to detect mechanical drift.")
        player_num = st.text_input("Target Player #", placeholder="e.g. 10")
        uploaded_video = st.file_uploader("Upload MP4/MOV", type=['mp4', 'mov'])
        
        if uploaded_video:
            st.video(uploaded_video)
            if st.button("Generate Elite Audit"):
                with st.status("Analyzing Skeletal Landmarks..."):
                    time.sleep(3)
                    st.session_state.roadmaps["10"] = [{"date": "2026-01-11", "issue": "Lower Back", "note": "High lumbar stress"}]
                    st.success("Audit Complete. Data pushed to Roadmap.")

    # ROADMAP
    with current_page[4]:
        st.header("12-Week Roadmap")
        # Insert Body Map Logic here (from previous turn)
        st.write("Tracking history for all clinical alerts.")

    # ADMIN
    with current_page[5]:
        st.header("Admin Hub")
        st.write("Manage team licenses and global metrics.")