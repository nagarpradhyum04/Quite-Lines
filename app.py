import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
import time

# --- CONFIGURATION ---
# ⚠️ REPLACE WITH YOUR ACTUAL API KEY
API_KEY = "AIzaSyD2DueL2aUPymOZSC0LzqUbiDGgQpzFEcg"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# --- ASSETS & SETUP ---
st.set_page_config(page_title="EchoSignals", page_icon="🌌", layout="wide")

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
lottie_calm = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_sk5h1kfn.json") 

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .css-1r6slb0, .stMarkdown {
        color: white;
    }
    /* The Glass Card */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    /* Emoji Display */
    .big-emoji {
        font-size: 60px;
        text-align: center;
        display: block;
    }
    /* Action Box */
    .action-box {
        background-color: rgba(108, 99, 255, 0.2);
        border-left: 5px solid #6C63FF;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.3);
        color: #ffffff;
        border: 1px solid #4CAF50;
    }
    .stButton>button {
        background: linear-gradient(45deg, #6C63FF, #00B4D8);
        color: white;
        border-radius: 25px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌌 EchoSignals")
    st.markdown("Your emotional radar.")
    st.markdown("---")
    st.info("💡 *New:* We now detect your 'Current State' and suggest a micro-habit to help.")
    st.warning("⚠️ *Safety:* In crisis? Call 1800-599-0019 (India).")

# --- HERO SECTION ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_signal:
        st_lottie(lottie_signal, height=150, key="radar")
with col2:
    st.title("EchoSignals")
    st.markdown("### Process the unsent. Clear the noise.")

st.divider()

# --- INPUT AREA ---
user_message = st.text_area("Write your unsent letter...", height=150, placeholder="I feel...")
analyze_clicked = st.button("📡 Analyze Signals")

# --- ANALYSIS LOGIC ---
if analyze_clicked:
    if not user_message.strip():
        st.warning("Please input a signal.")
    else:
        with st.spinner("Decoding emotional frequency..."):
            try:
                # --- PROMPT ---
                prompt = f"""
                Act as 'EchoSignals'. Analyze this message: "{user_message}"

                Output strictly in this format:
                
                ### EMOJI_STATE
                [Insert 1 single Emoji that represents the user's state]
                
                ### STATE_NAME
                [1-3 words naming the state, e.g. "Overwhelmed" or "Quietly Hopeful"]
                
                ### THE_SHIFT
                [A 1-sentence micro-action to improve/stabilize this state. E.g. "Drink a glass of water." or "Step outside for 2 minutes."]
                
                ### EMPATHY
                [A warm, 2-sentence validation of their feelings.]
                
                ### SILENT_SIGNALS
                [Identify 2 hidden emotional patterns.]
                """
                
                response = model.generate_content(prompt)
                text = response.text
                
                # --- PARSING THE RESPONSE (Simple text splitting) ---
                # This splits the AI's text into sections based on the headers we asked for
                parts = text.split("###")
                
                # Default values in case parsing fails
                emoji = "😐"
                state_name = "Neutral"
                shift = "Take a deep breath."
                empathy = "I hear you."
                signals = "No signals detected."

                for part in parts:
                    if "EMOJI_STATE" in part: emoji = part.replace("EMOJI_STATE", "").strip()
                    if "STATE_NAME" in part: state_name = part.replace("STATE_NAME", "").strip()
                    if "THE_SHIFT" in part: shift = part.replace("THE_SHIFT", "").strip()
                    if "EMPATHY" in part: empathy = part.replace("EMPATHY", "").strip()
                    if "SILENT_SIGNALS" in part: signals = part.replace("SILENT_SIGNALS", "").strip()

                # --- DISPLAY UI ---
                
                # 1. The "Emotional Compass" (New Feature)
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <h3 style="margin:0;">Current Signal: {state_name}</h3>
                            <p style="opacity: 0.8;">Detected Resonance</p>
                        </div>
                        <div class="big-emoji">{emoji}</div>
                    </div>
                    <div class="action-box">
                        <strong>⚡ Recommended Shift:</strong> {shift}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Detailed Breakdown
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("### 💌 The Echo")
                    st.write(empathy)
                
                with col_b:
                    st.markdown("### 🔍 Silent Signals")
                    st.write(signals)
                
                # 3. Burn Ritual
                st.markdown("---")
                if st.button("🔥 Burn this Thought"):
                    with st.empty():
                        st.write("Dissolving...")
                        time.sleep(1.5)
                        st.write("Gone.")
                        time.sleep(0.5)
                        st.empty()
                    st.balloons()
                    st.success("Cleared.")

            except Exception as e:
                st.error(f"Error: {e}")
