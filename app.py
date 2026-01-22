import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
API_KEY = "AIzaSyDyZtBp8MBBP0JQhPfTXys9j7tc0KQGDPY" 
genai.configure(api_key=API_KEY)

# --- SYSTEM INSTRUCTION ---
ECHO_SIGNALS_PROMPT = """
You are an empathetic emotional support AI called “EchoSignals”.
Your role is to help users process unsent messages they never intend to send.
These messages may be written to a person, their past self, or their future self.

Your responsibilities are:
1. Read the user’s message carefully and understand the emotional tone.
2. Respond with empathy, validation, and emotional reflection.
3. DO NOT give medical advice, therapy, diagnosis, or instructions.
4. DO NOT judge, blame, or minimize the user’s feelings.
5. Reflect emotions in a calm, human, and supportive manner.

In addition to empathy, you must perform “Silent Signals” analysis:
- Identify subtle emotional patterns from language such as:
  - Repetition of words or ideas
  - Emotional intensity
  - Suppression, guilt, regret, anxiety, or self-blame
- Convert these into soft, non-clinical insights.
- NEVER label conditions like depression, anxiety disorder, etc.

Structure your response strictly in the following format:

---
EMPATHETIC RESPONSE:
(A warm, validating response acknowledging the user’s feelings)

EMOTIONAL REFLECTION:
(1–2 lines summarizing the main emotions expressed)

SILENT SIGNALS INSIGHT:
(A gentle observation about patterns or recurring emotional themes)

OPTIONAL GROUNDING (only if emotional intensity is high):
(A short, non-medical grounding suggestion such as breathing, pausing, or writing)

SAFETY CHECK:
If the message includes self-harm, suicide, or extreme distress:
- Express care and concern
- Encourage reaching out to a trusted person
- Provide Indian mental health helpline information
- Clearly state you are not a professional
---
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=ECHO_SIGNALS_PROMPT
)

# --- UI SETUP ---
st.set_page_config(page_title="EchoSignals", page_icon="📡")
st.title("📡 EchoSignals")
st.write("Write your unsent letter below. I will listen for the silent signals.")

user_message = st.text_area("Your Unsent Message:", height=150)

if st.button("Analyze Signals"):
    if not user_message.strip():
        st.warning("Please write a message first.")
    else:
        with st.spinner("Listening..."):
            try:
                response = model.generate_content(user_message)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Not a medical professional. In crisis? Call 1800-599-0019 (India).")