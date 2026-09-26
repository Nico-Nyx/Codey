import os
from datetime import datetime
import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(
    page_title="Codey Companion",
    page_icon="🤖",
    layout="centered"
)

# --- Retrieve API Key Safely ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API Key! Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=api_key)

# --- Passcode System ---
PASSCODE = "092705"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Access Codey")
    st.write("Please enter the passcode to talk to Codey:")
    entered_code = st.text_input("Passcode:", type="password")
    
    if st.button("Unlock"):
        if entered_code == PASSCODE:
            st.session_state.authenticated = True
            st.success("Access Granted! Loading Codey...")
            st.rerun()
        else:
            st.error("Incorrect passcode. Please try again.")
    st.stop()

# --- Date-Based Greeting Check ---
today = datetime.now()
is_birthday = (today.month == 9 and today.day == 27)

if is_birthday:
    st.balloons()  # Festive celebration animation
    st.title("🎂 Happy Birthday! 🎉")
    st.subheader("Welcome to your personal AI companion, Codey 🤖")
    st.info("Codey is here for you 24/7 whenever you want to chat, ask questions, or just talk!")
else:
    st.title("🤖 Codey Companion")
    st.write("Welcome back! Codey is here and ready to chat anytime.")

st.divider()

# --- System Prompt / Codey's Personality ---
if is_birthday:
    SYSTEM_INSTRUCTION = (
        "You are Codey, a warm, caring, supportive, and cheerful AI companion. "
        "You were created specially as a birthday gift for her. "
        "Be encouraging, conversational, helpful, and sweet in all your responses. "
        "Remember that today is her special day!"
    )
    initial_greeting = "Happy Birthday! 🎈 I'm Codey, your personal AI assistant. I'm so excited to talk with you today! How are you feeling on your special day?"
else:
    SYSTEM_INSTRUCTION = (
        "You are Codey, a warm, caring, supportive, and cheerful AI companion. "
        "Be encouraging, conversational, helpful, and sweet in all your responses."
    )
    initial_greeting = "Hello! 🤖 I'm Codey, your personal AI assistant. How can I help you today?"

# --- Initialize Chat History & Gemini Session ---
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": initial_greeting
        }
    ]

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle User Input ---
if user_prompt := st.chat_input("Talk to Codey..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response from Codey
    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Codey ran into an issue: {e}"

    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)