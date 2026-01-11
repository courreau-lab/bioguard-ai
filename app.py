import streamlit as st
from google import genai
import plotly.graph_objects as go
import time, random, string

# --- 1. CONFIGURATION & PERSISTENCE ---
st.set_page_config(page_title="BioGuard AI | Squad Intelligence", layout="wide")

# Persistent State for Demo (In Prod, use a Database)
if "users" not in st.session_state:
    st.session_state.users = {"admin": {"pass": "owner2026", "role": "Owner", "name": "System Owner"}}
if "roadmaps" not in st.session_state:
    st.session_state.roadmaps = {
        "2": [{"date": "2025-11-30", "issue": "Right Knee", "severity": "High", "note": "12° Valgus detected"}]
    }
if "logged_in" not in st.session_state: st.session_state.logged_in = None

# --- 2. THEME & BRANDING ---
def apply_ui():
    bg_url = "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_url}"); background-size: cover; color: white; }}
        .pricing-card {{ background: rgba(22,27,34,0.9); padding: 25px; border-radius: 15px; border: 1px solid #004c97; text-align: center; }}
        .roadmap-card {{ background: rgba(0, 171, 78, 0.1); padding: 15px; border-radius: 8px; border-left: 5px solid #00ab4e; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

apply_ui()

# --- 3. COMPONENT: INTERACTIVE BODY MAP ---
def generate_body_map(issues):
    # Mapping points to a standard human anatomy diagram
    coords = {"Right Knee": [180, 550], "Left Knee": [320, 550], "Lower Back": [250, 320]}
    img_url = "https://i.imgur.com/9Yg0vVb.png" # Standard Medical Outline
    
    fig = go.Figure()
    fig.add_layout_image(dict(source=img_url, xref="x", yref="y", x=0, y=800, sizex=500, sizey=800, sizing="stretch", opacity=0.8, layer="below"))
    
    for issue in issues:
        if issue["issue"] in coords:
            pos = coords[issue["issue"]]
            fig.add_trace(go.Scatter(x=[pos[0]], y=[pos[1]], mode='markers', 
                                     marker=dict(size=20, color="red", line=dict(width=2, color='white')),
                                     hovertext=f"{issue['issue']}: {issue['note']}"))

    fig.update_layout(width=350, height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(visible=False, range=[0, 500]); fig.update_yaxes(visible=False, range=[0, 800])
    return fig

# --- 4. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.title("🛡️ BioGuard AI")
    tab1, tab2 = st.tabs(["Sign In", "About Our Business"])
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access Portal"):
            if u in st.session_state.users and st.session_state.users[u]["pass"] == p:
                st.session_state.logged_in = u; st.rerun()
    with tab2:
        st.write("BioGuard AI provides automated biomechanical audits for football, rugby, and basketball.")
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='pricing-card'><h3>Individual</h3><h2>£29/mo</h2></div>", unsafe_allow_html=True)
        c2.markdown("<div class='pricing-card' style='border-color:#00ab4e'><h3>Squad Pro</h3><h2>£199/mo</h2></div>", unsafe_allow_html=True)
        c3.markdown("<div class='pricing-card'><h3>Elite</h3><h2>£POA</h2></div>", unsafe_allow_html=True)
    st.stop()

# --- 5. MAIN NAVIGATION ---
user_role = st.session_state.users[st.session_state.logged_in]["role"]
menu = ["Analysis", "12-Week Roadmap", "Squad Dashboard"]
if user_role == "Owner": menu.insert(0, "🛡️ Admin Console")
choice = st.sidebar.radio("Navigation", menu)

# --- 6. PAGE: 12-WEEK ROADMAP ---
if choice == "12-Week Roadmap":
    st.header("📅 Player Recovery & Development Hub")
    p_id = st.selectbox("Select Player Number", list(st.session_state.roadmaps.keys()))
    
    col_map, col_details = st.columns([1, 2])
    with col_map:
        st.plotly_chart(generate_body_map(st.session_state.roadmaps[p_id]))
    with col_details:
        st.subheader(f"Current Plan for Player #{p_id}")
        for item in reversed(st.session_state.roadmaps[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{item['date']}</strong>: {item['note']}</div>", unsafe_allow_html=True)
        st.info("AI RECOMMENDATION: Perform Week 4 stability drills. Avoid high-velocity sprints until symmetry improves.")

# --- 7. PAGE: ADMIN CONSOLE (OWNER ONLY) ---
elif choice == "🛡️ Admin Console":
    st.header("System Owner Dashboard")
    new_team = st.text_input("New Team Username")
    if st.button("Create Team License"):
        temp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        st.session_state.users[new_team] = {"pass": temp_pass, "role": "Coach", "name": f"Coach {new_team}"}
        st.success(f"License Active. Password: {temp_pass}")