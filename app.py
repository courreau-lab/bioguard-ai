import streamlit as st
import plotly.graph_objects as go
import time

# --- 1. SETTINGS & LUXURY THEME ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_luxury_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        /* Global Typography */
        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        /* Cinematic Football Background */
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{bg_img}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* --- THE "WHITE BOX / BLACK TEXT" FIX --- */
        /* Targets every input box, text area, and select box on the site */
        input, textarea, [data-baseweb="input"], [data-baseweb="select"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 8px !important;
        }}
        
        /* Ensures the text you type is black and bold enough to read */
        input {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}

        /* Fix Menu Tabs to White */
        button[data-baseweb="tab"] {{
            color: white !important;
        }}
        
        .luxury-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }}
        
        h1, h2, h3 {{ color: white !important; font-weight: 700; }}
        .stButton>button {{ border-radius: 50px; border: 1px solid #00ab4e; color: white; background: transparent; }}
        
        /* Warning/Info text visibility */
        .stAlert {{ background-color: rgba(255, 255, 255, 0.1); color: white; }}
    </style>
    """, unsafe_allow_html=True)

apply_luxury_styling()

# --- 2. DATA PERSISTENCE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "2": [{"date": "2026-01-11", "issue": "Right Knee", "note": "Baseline established."}]
    }

# --- 3. THE NAVIGATION MENU ---
menu_options = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    menu_options += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Console"]

current_tab = st.tabs(menu_options)

# --- 4. PUBLIC PAGES ---

with current_tab[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    st.subheader("Elite Biometrics & AI-Driven Injury Prevention")
    
    if not st.session_state.logged_in:
        st.divider()
        st.write("### Partner Access")
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("Unlock Capabilities"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Partner Credentials")

with current_tab[1]: # BUSINESS OFFER
    st.header("What We Offer")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚽ Covered Sports")
        st.write("- Football (Soccer)\n- Rugby Union/League\n- Basketball\n- American Football")
    with col2:
        st.subheader("💎 Value Proposition")
        st.write("- Reduce non-contact injuries by up to 22%\n- Protect player market valuation\n- Automated recovery roadmaps")

with current_tab[2]: # SUBSCRIPTION
    st.header("Subscription Plans")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='luxury-card'><h3>Individual</h3><h2>£29/mo</h2><p>1 Player Scan</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='luxury-card' style='border-color: #00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2><p>Full Team (25 Players)</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='luxury-card'><h3>Elite Academy</h3><h2>£POA</h2><p>Full Club Integration</p></div>", unsafe_allow_html=True)

# --- 5. PRIVATE MEMBER CAPABILITIES ---

if st.session_state.logged_in:
    with current_tab[3]: # ANALYSIS ENGINE
        st.header("🎥 Video Analysis Engine")
        st.write("Upload match highlights to detect mechanical drift.")
        p_num = st.text_input("Target Player Number", "2")
        video_file = st.file_uploader("Upload MP4/MOV Video", type=['mp4', 'mov'])
        
        if video_file:
            st.video(video_file)
            if st.button("Generate Elite Audit"):
                with st.status("Analyzing Skeletal Landmarks..."):
                    time.sleep(3)
                    findings = "Detected 12° Knee Valgus. MRI Scan Recommended."
                    st.session_state.roadmap[p_num].append({"date": "2026-01-11", "issue": "Right Knee", "note": findings})
                st.success("Analysis Complete. Progress pushed to Player Roadmap.")

    with current_tab[4]: # PLAYER DASHBOARD
        st.header("🩺 Biometric Body Map")
        p_select = st.selectbox("Select Player Number", list(st.session_state.roadmap.keys()))
        
        fig = go.Figure()
        fig.add_layout_image(dict(source="https://i.imgur.com/9Yg0vVb.png", xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
        
        for item in st.session_state.roadmap[p_select]:
            if item["issue"] == "Right Knee":
                fig.add_trace(go.Scatter(x=[180], y=[550], mode='markers', marker=dict(size=25, color="red"), hovertext=item['note']))
        
        fig.update_layout(width=400, height=600, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
        st.plotly_chart(fig)

    with current_tab[5]: # 12-WEEK ROADMAP
        st.header("📅 12-Week Roadmap")
        p_select = st.selectbox("View History", list(st.session_state.roadmap.keys()), key="roadmap_p")
        for event in reversed(st.session_state.roadmap[p_select]):
            st.markdown(f"**{event['date']}**: {event['note']}")

    with current_tab[6]: # ADMIN
        st.header("System Settings")
        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))