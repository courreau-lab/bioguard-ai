import streamlit as st
import plotly.graph_objects as go
import time, random, string

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
        
        /* Pricing & Metric Cards */
        .luxury-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }}
        
        /* 12-Week Roadmap Cards */
        .roadmap-card {{
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 5px solid #00ab4e;
        }}
        
        h1, h2, h3 {{ color: white !important; font-weight: 700; }}
        .stButton>button {{ border-radius: 50px; border: 1px solid #00ab4e; color: white; background: transparent; }}
        .stButton>button:hover {{ background: #00ab4e; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. DATA PERSISTENCE (Roadmap & Auth) ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    # Initial historical data for the demo
    st.session_state.roadmap = {
        "2": [
            {"date": "2026-01-11", "category": "Health", "note": "Gait asymmetry: 8% drift to right. Action: Glute activation protocol."},
            {"date": "2026-01-11", "category": "Play", "note": "Tactical: Low scanning frequency (0.4/s). Action: Shoulder-check drills."}
        ]
    }

# --- 3. NAVIGATION MENU ---
# Public pages are always visible. Private pages unlock after login.
menu_options = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Console"]

current_tab = st.tabs(menu_options)

# --- 4. PUBLIC FACING PAGES ---

with current_tab[0]: # --- HOME ---
    st.title("🛡️ ELITE PERFORMANCE")
    st.subheader("Bespoke AI Diagnostics & Performance Optimization")
    st.write("Democratizing elite medical and tactical standards for professional football, rugby, and basketball.")
    
    if not st.session_state.logged_in:
        st.divider()
        st.write("### Partner Access")
        col_u, col_p = st.columns(2)
        u = col_u.text_input("Username", placeholder="admin")
        p = col_p.text_input("Password", type="password", placeholder="owner2026")
        if st.button("Unlock Capabilities"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

with current_tab[1]: # --- BUSINESS OFFER ---
    st.header("Strategic Advantage")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("⚽ Covered Sports")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col_b:
        st.subheader("💎 Value Proposition")
        st.write("**Injury Prevention:** Detection of sub-clinical mechanical failure.")
        st.write("**Performance Improvement:** Auditing spatial intelligence and scanning.")

with current_tab[2]: # --- SUBSCRIPTION PLANS ---
    st.header("Strategic Partnership Tiers")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>1 Player Scan<br>Monthly Health Audit</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Squad (25 Players)<br>Interactive Body Map<br>Dual Health/Play Audits</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Club-wide Integration<br>3D Biometrics<br>Direct API Access</p></div>", unsafe_allow_html=True)

# --- 5. PROTECTED MEMBER PAGES ---

if st.session_state.logged_in:
    with current_tab[3]: # --- ANALYSIS ENGINE ---
        st.header("🎥 Video Analysis Engine")
        st.write("Upload match highlights to detect mechanical drift and tactical habits.")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Upload MP4/MOV Highlight", type=['mp4', 'mov'])
        
        if video_file:
            st.video(video_file)
            if st.button("Generate Dual-Track Audit"):
                with st.status("Analyzing Skeletal & Spatial Landmarks..."):
                    time.sleep(3)
                    # Append findings to roadmap without overwriting
                    st.session_state.roadmap[p_num].append({
                        "date": "2026-01-11", "category": "Health", 
                        "note": "Detected medial knee drift during deceleration. MRI scan advised if pain persists."
                    })
                    st.session_state.roadmap[p_num].append({
                        "date": "2026-01-11", "category": "Play", 
                        "note": "Improvement: Scanning frequency increased to 0.6/s. Continue vision drills."
                    })
                st.success("Audit Complete. Roadmap Updated.")

    with current_tab[4]: # --- PLAYER DASHBOARD / BODY MAP ---
        st.header("🩺 Biometric Body Map")
        p_select = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        
        # Interactive Plotly Body Map
        fig = go.Figure()
        fig.add_layout_image(dict(
            source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"
        ))
        # Add a red marker for knee issues
        fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=25, color="red", line=dict(width=2, color='white')), hovertext="Health Alert: Right Knee Stability"))
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # --- 12-WEEK ROADMAP ---
        st.header("📅 Cumulative 12-Week Roadmap")
        p_id = st.selectbox("View History for Player", list(st.session_state.roadmap.keys()), key="rd_select")
        
        for entry in reversed(st.session_state.roadmap[p_id]):
            # Color coding for Health (Red/Orange) vs Play (Green)
            border_color = "#ff4b4b" if entry['category'] == "Health" else "#00ab4e"
            st.markdown(f"""
            <div class='roadmap-card' style='border-left-color: {border_color}'>
                <strong>[{entry['category']}] {entry['date']}</strong><br>{entry['note']}
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.warning("⚠️ CLINICAL SUMMARY: Priority focus on right-knee stability and core anti-rotation to prevent non-contact ACL strain.")

    with current_tab[6]: # --- ADMIN CONSOLE ---
        st.header("System Management")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()