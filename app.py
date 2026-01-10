import streamlit as st
from google import genai
import time, random, string

# --- 1. SQUAD REGISTRY (Persistent Database Simulation) ---
if "squad_data" not in st.session_state:
    st.session_state.squad_data = {
        "2": {"name": "Right Back", "risk": "Medium", "plan": ["Wk1: Glute Activation", "Wk2: Proprioception Training"]},
        "8": {"name": "Central Mid", "risk": "Low", "plan": ["Wk1: Scanning Drills"]}
    }
if "users" not in st.session_state:
    st.session_state.users = {"admin": {"pass": "owner2026", "role": "Owner"}}
if "logged_in" not in st.session_state: st.session_state.logged_in = None

# --- 2. THEME & NAVIGATION ---
st.set_page_config(page_title="BioGuard AI", layout="wide")
st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

# Navigation Menu
if not st.session_state.logged_in:
    st.title("🛡️ BioGuard AI: Sign In")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u in st.session_state.users and st.session_state.users[u]["pass"] == p:
            st.session_state.logged_in = u
            st.rerun()
    st.stop()

menu = st.sidebar.radio("Menu", ["Dashboard", "Analysis", "12-Week Roadmap", "Admin Console"])

# --- 3. PAGE: ANALYSIS (THE ENGINE) ---
if menu == "Analysis":
    st.header("Upload Squad Highlights")
    p_num = st.text_input("Player Number", placeholder="Blank = All Green Shirts")
    file = st.file_uploader("Upload Video", type=['mp4', 'mov'])
    
    if file and st.button("Run AI Audit"):
        with st.status("Analyzing Biomechanics..."):
            time.sleep(3) # AI Inference Simulation
            new_issue = "Detected 12° Knee Valgus. MRI Scan Recommended."
            # Automated Plan Update Logic
            target = p_num if p_num else "2" # Defaulting to known player for demo
            st.session_state.squad_data[target]["plan"].append(f"Wk{len(st.session_state.squad_data[target]['plan'])+1}: {new_issue}")
            st.success("Analysis Complete. 12-Week Roadmap Updated.")

# --- 4. PAGE: 12-WEEK ROADMAP (RECOVERY HUB) ---
elif menu == "12-Week Roadmap":
    st.header("📅 Squad Recovery & Development")
    target_p = st.selectbox("Select Player", list(st.session_state.squad_data.keys()))
    
    player = st.session_state.squad_data[target_p]
    st.subheader(f"Player #{target_p} - {player['name']}")
    
    st.write("### Active Program (Cumulative)")
    for step in player["plan"]:
        st.markdown(f"- ✅ {step}")
    
    st.divider()
    if "MRI" in str(player["plan"]):
        st.error("⚠️ CLINICAL ALERT: Cumulative mechanical stress requires a medical scan before Matchday.")

# --- 5. PAGE: ADMIN CONSOLE (OWNER ONLY) ---
elif menu == "Admin Console":
    st.header("Owner Admin Console")
    st.write("Generate credentials for new teams.")
    new_team = st.text_input("New Team Name")
    if st.button("Generate License"):
        temp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        st.code(f"Username: {new_team} | Temp Password: {temp_pass}")