import streamlit as st
import plotly.graph_objects as go
from google import genai
import time, tempfile, os, base64

# --- 1. GLOBAL UI & TOTAL VISIBILITY SHIELD ---
st.set_page_config(page_title="Elite Performance | BioGuard AI", layout="wide")

def apply_elite_styling():
    bg_img = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&q=80&w=2000"
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        html, body, [class*="st-"], .stMarkdown, p, div, h1, h2, h3, h4, h5, h6, span, label, li {{
            font-family: 'Inter', sans-serif !important; color: #ffffff !important;
        }}
        input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput>div>div>input {{
            background-color: #000000 !important; color: #ffffff !important; border: 2px solid #00ab4e !important; border-radius: 8px !important;
        }}
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
        button[data-baseweb="tab"] {{ background-color: transparent !important; border: none !important; }}
        button[data-baseweb="tab"] div {{ color: white !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ border-bottom: 3px solid #00ab4e !important; }}
        .luxury-card, .roadmap-card {{ background: rgba(255, 255, 255, 0.08) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 20px !important; padding: 25px !important; margin-bottom: 15px !important; }}
        .stButton>button {{ border-radius: 50px !important; border: 2px solid #00ab4e !important; color: white !important; background: rgba(0, 171, 78, 0.2) !important; font-weight: 700 !important; }}
        .stButton>button:hover {{ background: #00ab4e !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_elite_styling()

# --- 2. AI INITIALIZATION & QUOTA PURGE ---
if "last_ai_time" not in st.session_state: st.session_state.last_ai_time = 0

try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        # FORCE PURGE: Deletes zombie files on every boot to clear quota
        for f in client.files.list(): client.files.delete(name=f.name)
    else:
        st.warning("⚠️ Secret missing. Add GEMINI_API_KEY to Streamlit Secrets.")
except Exception as e:
    st.error(f"AI Connection Failed: {e}")

# --- 3. DATA & LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {"22": [{"date": "2026-01-18", "category": "System", "note": "Elite System Active."}]}

# --- 4. NAVIGATION ---
tab_labels = ["Home", "Business Offer", "Subscription Plans"]
if st.session_state.logged_in:
    tab_labels += ["Analysis Engine", "Player Dashboard", "12-Week Roadmap", "Admin Hub"]
tabs = st.tabs(tab_labels)

with tabs[0]: # HOME
    st.title("🛡️ ELITE PERFORMANCE")
    if not st.session_state.logged_in:
        u = st.text_input("Username", placeholder="admin", key="u_final")
        p = st.text_input("Password", type="password", placeholder="owner2026", key="p_final")
        if st.button("Unlock Elite Portal"):
            if u == "admin" and p == "owner2026":
                st.session_state.logged_in = True
                st.rerun()

if st.session_state.logged_in:
    with tabs[3]: # ANALYSIS ENGINE
        st.header("🎥 Technical Performance Audit")
        
        # PLAYER HIGHLIGHT INPUT
        target_desc = st.text_input("Player Description", placeholder="e.g., Player wearing red boots number 7")
        target_p = st.text_input("Store to Player ID", "22")
        
        vid = st.file_uploader("Upload Clip (12MB version)", type=['mp4', 'mov'])
        if vid and 'client' in locals():
            st.video(vid)
            elapsed = time.time() - st.session_state.last_ai_time
            if elapsed < 60:
                st.warning(f"🕒 AI Cooling Down: Wait {int(60 - elapsed)}s for next audit.")
            else:
                if st.button("Generate Performance Plan & Summary"):
                    with st.status("🤖 Auditing Player Performance..."):
                        try:
                            # Purge storage
                            for f in client.files.list(): client.files.delete(name=f.name)
                            
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                                tmp.write(vid.getvalue()); t_path = tmp.name
                            
                            up_f = client.files.upload(file=t_path)
                            
                            # DETAILED PROMPT FOR PLAN & SUMMARY
                            prompt = f"""
                            Act as an elite sports scientist. Focus on the player described as: {target_desc}.
                            1. Provide a detailed Performance Summary of their movements.
                            2. Identify specific Technical Gains to work on.
                            3. Create a 1-week Performance Plan to address clinical injury risks and tactical improvement.
                            """
                            
                            resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt, up_f])
                            
                            st.session_state.roadmap[target_p].append({
                                "date": "2026-01-18", 
                                "category": "AI Audit", 
                                "note": resp.text
                            })
                            st.session_state.last_ai_time = time.time()
                            client.files.delete(name=up_f.name); os.remove(t_path)
                            st.success("Analysis Delivered to Roadmap.")
                        except Exception as e:
                            st.error(f"Quota issue: Please wait 60s for Google reset.")

    with tabs[4]: # PLAYER DASHBOARD (ALIGNMENT FIX)
        st.header("🩺 Biometric Injury Mapping")
        if os.path.exists("digital_twin.png"):
            with open("digital_twin.png", "rb") as f_bin: b64 = base64.b64encode(f_bin.read()).decode()
            fig = go.Figure()
            # Scaling logic for portrait mannequin
            fig.add_layout_image(dict(
                source=f"data:image/png;base64,{b64}", 
                xref="x", yref="y", x=0, y=1000, 
                sizex=1000, sizey=1000, sizing="contain", opacity=0.9, layer="below"
            ))
            # RECALIBRATED: Midline Alignment (X=500) for centered mannequin
            fig.add_trace(go.Scatter(
                x=[500, 500], y=[235, 125], # Centered Knee and Calf
                mode='markers+text', text=["Knee ACL", "Calf Strain"], textposition="middle right",
                textfont=dict(color="white", size=15),
                marker=dict(size=40, color="rgba(255, 75, 75, 0.7)", symbol="circle", line=dict(width=3, color='white'))
            ))
            fig.update_layout(width=800, height=800, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False, range=[0, 1000]), yaxis=dict(visible=False, range=[0, 1000]))
            st.plotly_chart(fig, use_container_width=True)

    with tabs[5]: # ROADMAP
        st.header("📅 Performance Plan & Summary")
        p_id = st.selectbox("Select Player", list(st.session_state.roadmap.keys()))
        for entry in reversed(st.session_state.roadmap[p_id]):
            st.markdown(f"<div class='roadmap-card'><strong>{entry['date']} - {entry['category']}</strong><br>{entry['note']}</div>", unsafe_allow_html=True)