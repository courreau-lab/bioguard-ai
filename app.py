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

        /* --- THE WHITE BOX / BLACK TEXT FIX --- */
        
        /* 1. Standard Inputs & Select Boxes */
        input, textarea, [data-baseweb="input"], [data-baseweb="select"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 8px !important;
        }}
        
        /* 2. The File Uploader Container */
        [data-testid="stFileUploader"] section {{
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 2px dashed #ccc !important;
        }}

        /* 3. Force ALL text inside inputs, dropdowns, and uploader to be BLACK */
        [data-testid="stFileUploader"] section *, 
        input, 
        div[data-baseweb="select"] span,
        .stSelectbox div {{
             color: #000000 !important;
             -webkit-text-fill-color: #000000 !important;
        }}

        /* --- FIX FOR ERROR BOXES (White on White fix) --- */
        /* This ensures error messages and popups are readable */
        .stException, .stAlert, div[data-testid="stNotification"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        .stException p, .stException pre, .stAlert p {{
            color: #000000 !important;