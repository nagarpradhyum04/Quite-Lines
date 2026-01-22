import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
import time
import os

# --- ASSETS & SETUP ---
st.set_page_config(page_title="Quiet Lines", page_icon="📝", layout="wide")

# --- CONFIGURATION ---
try:
    # Try getting the key from Streamlit secrets (for Cloud)
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # For Local Run: PASTE YOUR KEY BELOW inside the quotes
    API_KEY = "AIzaSyD2DueL2aUPymOZSC0LzqUbiDGgQpzFEcg" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations
lottie_signal = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_4kji20Y93r.json")

# --- SESSION STATE ---
if 'mood_hex' not in st.session_state:
    st.session_state.mood_hex = "#2c5364"

# --- CSS STYLING ---
def get_custom_css(hex_color):
    return f"""
    <style>
    /* Dynamic Background */
    .stApp {{
        background: linear-gradient(135deg, #0f2027, {hex_color}CC);
        transition: background 1.5s ease;
    }}
    
    /* Glass Cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }}
    
    /* Text Clarity */
    h1, h2, h3, p, .stMarkdown, li {{ color: #ffffff !important; }}
    
    /* Emoji & Meter */
    .big-emoji {{ font-size: 72px; text-align: center; }}
    .stProgress > div > div > div > div {{ background-color: #ffffff; }}
    
    /* Crisis Box */
    .crisis-box {{
        background-color: rgba(220, 53, 69, 0.2);
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        color: white;
        margin-top: 20px;
    }}
    </style>
    """

# Apply the default (or previous) color immediately
st.markdown(get_custom_css(st.session_state.mood_hex), unsafe_allow_html=True)

# --- SIDEBAR: SAFETY CENTER ---
with st.sidebar:
    st.title("📝 Quiet Lines")
    st.caption("A space for words unspoken.")
    
    st.markdown("---")
    
    st.error("🚨 *Emergency Contacts*")
    st.markdown("""
    *India:*
    - *Kiran (Mental Health):* 1800-599-0019
    - *Aasra (Suicide Prev):* 9820466726
    - *Vandrevala Fdn:* 1860-266-2345
    
    *Global:*
    - *US:* 988
    - *UK:* 111
    """)
    
    st.markdown("---")
    st.info("ℹ️ *How it works:*\n\n1. Write your unsent thoughts.\n2. AI analyzes emotional tone.\n3. The interface shifts color.\n4. You get a coping strategy.")

# --- HERO SECTION ---
col1, col2 = st.columns([1, 4])
with col1:
    if lottie_signal:
        st_lottie(lottie_signal, height=120, key="radar")
with col2:
    st.title("Quiet Lines")
    st.markdown("##### The safe space for words you cannot send.")

# --- INPUT AREA ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
user_message = st.text_area("Write freely. No one else will see this.", height=150, placeholder="Dear...")
col_act1, col_act2 = st.columns([1, 5])
with col_act1:
    analyze_clicked = st.button("📝 Transmit Lines")
st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYSIS LOGIC ---
if analyze_clicked:
    if not user_message.strip():
        st.warning("The page is blank. Please write something.")
    else:
        with st.spinner("Listening to the quiet..."):
            try:
                # --- PROMPT ---
                # UPDATED NAME HERE
                prompt = f"""
                Act as 'Quiet Lines', an empathetic emotional support AI. 
                Analyze this message: "{user_message}"

                Output strictly in this format:
                
                ### EMOJI_STATE
                [1 Emoji]
                
                ### STATE_NAME
                [1-3 words naming the state]
                
                ### COLOR_HEX
                [A HEX color code. Use #FF4B4B for high anger/danger, #4B4BFF for sadness, #FFD700 for joy, #7D3C98 for anxiety]
                
                ### INTENSITY
                [Integer 0-100]
                
                ### THE_SHIFT
                [1-sentence micro-action]
                
                ### EMPATHY
                [2 sentences of validation]
                
                ### SILENT_SIGNALS
                [Identify 2 hidden patterns]
                
                ### SAFETY_ALERT
                [TRUE or FALSE. Set TRUE only if self-harm or suicide is mentioned]
                """
                
                response = model.generate_content(prompt)
                text = response.text
                
                # --- PARSING ---
                parts = text.split("###")
                data = {
                    "emoji": "😐", "state": "Neutral", "color": "#2c5364", 
                    "intensity": 50, "shift": "Breathe.", "empathy": "Listening...", 
                    "signals": "None.", "safety": "FALSE"
                }

                for part in parts:
                    if "EMOJI_STATE" in part: data["emoji"] = part.replace("EMOJI_STATE", "").strip()
                    if "STATE_NAME" in part: data["state"] = part.replace("STATE_NAME", "").strip()
                    if "COLOR_HEX" in part: data["color"] = part.replace("COLOR_HEX", "").strip()
                    if "INTENSITY" in part: 
                        try: data["intensity"] = int(part.replace("INTENSITY", "").strip())
                        except: data["intensity"] = 50
                    if "THE_SHIFT" in part: data["shift"] = part.replace("THE_SHIFT", "").strip()
                    if "EMPATHY" in part: data["empathy"] = part.replace("EMPATHY", "").strip()
                    if "SILENT_SIGNALS" in part: data["signals"] = part.replace("SILENT_SIGNALS", "").strip()
                    if "SAFETY_ALERT" in part: data["safety"] = part.replace("SAFETY_ALERT", "").strip()

                # --- 1. UPDATE COLOR IMMEDIATELY ---
                st.markdown(get_custom_css(data["color"]), unsafe_allow_html=True)

                # --- 2. DISPLAY DASHBOARD ---
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h2 style="margin:0; text-shadow: 0 0 10px rgba(0,0,0,0.5);">{data["state"]}</h2>
                            <p style="opacity: 0.9;">Intensity Level: {data['intensity']}%</p>
                        </div>
                        <div class="big-emoji">{data["emoji"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(data["intensity"] / 100)
                
                # --- 3. SAFETY CHECK ---
                if "TRUE" in data["safety"].upper():
                    st.markdown("""
                    <div class="crisis-box">
                        <h3>🚨 Immediate Support Needed</h3>
                        <p>It sounds like you are going through a very difficult time. Please reach out to a human who can help.</p>
                        <ul>
                            <li><strong>Call:</strong> 1800-599-0019 (Kiran)</li>
                            <li><strong>Text:</strong> HOME to 741741</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # --- 4. DETAILED CARDS ---
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="glass-card" style="height:100%">', unsafe_allow_html=True)
                    st.markdown(f"*⚡ The Shift:*\n\n{data['shift']}")
                    st.markdown("---")
                    st.markdown(f"*💌 Quiet Lines Echo:*\n\n{data['empathy']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with c2:
                    st.markdown('<div class="glass-card" style="height:100%">', unsafe_allow_html=True)
                    st.markdown("### 🔍 Silent Signals")
                    st.write(data["signals"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # --- 5. BURN BUTTON ---
                if st.button("🔥 Burn This"):
                    st.balloons()
                    st.success("Lines released into the void.")

            except Exception as e:
                st.error(f"Signal Interference: {e}")
