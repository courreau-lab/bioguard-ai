import streamlit as st
import plotly.graph_objects as go
import time, random, string

# --- 1. SETTINGS & LUXURY THEME ---
st.set_page_config(page_title="BioGuard AI | Elite Analytics", layout="wide")

def apply_luxury_styling():
    st.markdown("""
    <style>
        /* Modern Dark Luxury Theme */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #E0E0E0;
        }
        
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&q=80&w=2000");
            background-size: cover;
            background-attachment: fixed;
        }

        /* Top Navigation Bar Simulation */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 3rem;
        }

        /* Luxury Pricing Cards */
        .luxury-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .luxury-card:hover {
            border-color: #00ab4e;
            background: rgba(255, 255, 255, 0.07);
            transform: translateY(-5px);
        }

        /* Typography */
        h1 { font-weight: 700; letter-spacing: -1px; color: white; margin-bottom: 0.5rem; }
        .hero-sub { font-weight: 300; font-size: 1.5rem; color: #AAA; margin-bottom: 3rem; }
    </style>
    """, unsafe_allow_html=True)

apply_luxury_styling()

# --- 2. DATA STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmaps" not in st.session_state:
    st.session_state.roadmaps = {"2": [{"date": "2026-01-11", "issue": "Right Knee", "note": "Gait asymmetry detected"}]}

# --- 3. THE "LUXURY" HEADER ---
# This simulates the top-right icon navigation
col_title, col_nav = st.columns([3, 1])
with col_title:
    st.markdown("# 🛡️ BIOGUARD AI")
with col_nav:
    if not st.session_state.logged_in:
        if st.button("👤 Member Login", use_container_width=True):
            st.session_state.show_login = True
    else:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# --- 4. LOGIN OVERLAY (Only shows if clicked) ---
if hasattr(st.session_state, 'show_login') and st.session_state.show_login and not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("Partner Access")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Sign In"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.session_state.show_login = False
                st.rerun()
            else: st.error("Credentials not recognized.")
    if st.button("Close"): 
        st.session_state.show_login = False
        st.rerun()

# --- 5. CONDITIONAL CONTENT: PUBLIC vs PRIVATE ---

if not st.session_state.logged_in:
    # --- PUBLIC HOMEPAGE ---
    st.markdown("<p class='hero-sub'>Clinical Biomechanics for the 1%.</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Value Proposition Section
    st.header("The BioGuard Advantage")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 🛡️ Risk Mitigation")
        st.write("Detect sub-clinical fatigue markers and mechanical drift before they manifest as ACL or hamstring trauma.")
    with c2:
        st.write("### 📊 Tactical Synergy")
        st.write("AI-driven squad compactness metrics. Audit spacing, scanning frequency, and defensive transition speed.")
    with c3:
        st.write("### 💎 Value Retention")
        st.write("Generate verified 'Health Passports' for high-value players to protect market valuation during scouting.")

    st.divider()
    
    # Luxury Pricing Tiers
    st.header("Strategic Partnerships")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("<div class='luxury-card'><h4>Individual</h4><h1>£29<span style='font-size:1rem'>/mo</span></h1><p>Single Player Scan<br>Bi-Weekly Report</p></div>", unsafe_allow_html=True)
    with p2:
        st.markdown("<div class='luxury-card' style='border-color: #00ab4e'><h4>Squad Pro</h4><h1>£199<span style='font-size:1rem'>/mo</span></h1><p>Full Team (25 Players)<br>Interactive Roadmap<br>24/7 AI Audit</p></div>", unsafe_allow_html=True)
    with p3:
        st.markdown("<div class='luxury-card'><h4>Academy Elite</h4><h1>£POA</h1><p>Club-wide Integration<br>Custom 3D Mapping<br>Clinical Staff Portal</p></div>", unsafe_allow_html=True)

else:
    # --- PRIVATE MEMBER DASHBOARD ---
    st.sidebar.title("Elite Portal")
    choice = st.sidebar.radio("Navigation", ["Squad Analysis", "12-Week Roadmap", "Admin Hub"])
    
    if choice == "12-Week Roadmap":
        st.header("📅 Recovery & Development Roadmap")
        # Body map and roadmap logic goes here...
        st.info("Member content active. Welcome back, Owner.")