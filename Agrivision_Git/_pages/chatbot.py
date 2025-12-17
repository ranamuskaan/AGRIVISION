# _pages/chatbot.py
import streamlit as st
from groq import Groq

# -----------------------------
# 🔧 Config
# -----------------------------
GROQ_API_KEY = "*****"  # 🔑 Replace with your Groq secret key
MODEL_NAME = "openai/gpt-oss-20b"           # Exact model from Groq playground
MAX_TOKENS = 512
TEMPERATURE = 0.7

# -----------------------------
# 🧠 Groq chat function
# -----------------------------
def groq_chat(prompt):
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_completion_tokens=MAX_TOKENS,
        stream=False
    )
    return completion.choices[0].message.content.strip()

# -----------------------------
# 🌿 Fallback
# -----------------------------
def get_fallback_response(prompt):
    return "⚠️ Sorry, I can't answer right now."

# -----------------------------
# 🌾 Streamlit Chat UI
# -----------------------------
def render_chatbot():
    st.markdown("""
    <style>
    body { background: linear-gradient(120deg, #e8f5e9 0%, #f1f8e9 100%); font-family:'Poppins',sans-serif; }
    .card { background:white; border-radius:14px; padding:22px; box-shadow:0 10px 30px rgba(46,125,50,0.12); max-width:900px; margin:auto; }
    .title { font-size:28px; font-weight:700; color:#1b5e20; margin-bottom:6px; }
    .subtitle { color:#4b6b47; margin-bottom:18px; }
    .chat-container { max-height:500px; overflow-y:auto; padding-right:10px; }
    .user-bubble { background:#c8e6c9; padding:12px 14px; border-radius:14px; margin:8px 0; color:#1b5e20; max-width:80%; align-self:flex-end; }
    .ai-bubble { background:#f1f8e9; padding:12px 14px; border-radius:14px; margin:8px 0; color:#2e7d32; max-width:80%; align-self:flex-start; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>🌾 AgriVision AI Chatbot</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Ask in English, हिन्दी  — I will respond naturally.</div>", unsafe_allow_html=True)

    # Initialize session state (prefixed keys)
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "chat_last_reply" not in st.session_state:
        st.session_state.chat_last_reply = ""

    # Scrollable chat container
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for m in st.session_state.chat_messages:
            if m["role"] == "user":
                st.markdown(f"<div class='user-bubble'>👩‍🌾 {m['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-bubble'>🤖 {m['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Chat input with instant reply
    # -----------------------------
    prompt = st.chat_input("Type your question about crops, weather, irrigation, or schemes...")

    if prompt:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        # Placeholder for AI response
        response_placeholder = st.empty()

        # Generate AI reply
        with st.spinner("Thinking... 🌿"):
            try:
                ai_text = groq_chat(prompt)
            except Exception:
                ai_text = get_fallback_response(prompt)

            # Append AI message
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_text})
            st.session_state.chat_last_reply = prompt

            # Display AI reply immediately
            response_placeholder.markdown(f"<div class='ai-bubble'>🤖 {ai_text}</div>", unsafe_allow_html=True)

        # Refresh all previous messages above
        with chat_container:
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for m in st.session_state.chat_messages[:-1]:
                if m["role"] == "user":
                    st.markdown(f"<div class='user-bubble'>👩‍🌾 {m['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='ai-bubble'>🤖 {m['content']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Quick Action Buttons
    # -----------------------------
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌧️ Weather Advice", use_container_width=True):
            question = "What's the weather advice for farming?"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            try:
                response = groq_chat(question)
            except Exception:
                response = get_fallback_response(question)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

    with col2:
        if st.button("🐛 Pest Control", use_container_width=True):
            question = "Tell me about pest control"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            try:
                response = groq_chat(question)
            except Exception:
                response = get_fallback_response(question)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

    with col3:
        if st.button("💰 Subsidy Info", use_container_width=True):
            question = "Government subsidies for farmers"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            try:
                response = groq_chat(question)
            except Exception:
                response = get_fallback_response(question)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

    # -----------------------------
    # Clear chat history
    # -----------------------------
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.chat_last_reply = ""
