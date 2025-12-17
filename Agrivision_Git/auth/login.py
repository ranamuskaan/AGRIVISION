# auth/login.py
import streamlit as st


def check_credentials(username, password):
    correct_username = "demo"
    correct_password = "agri123"
    return username == correct_username and password == correct_password


def render_login():
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 3rem 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(34,197,94,0.2);
        text-align: center;
    }
    .login-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #22c55e, #a3e635);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        color: #2a3f33;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .demo-box {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        margin: 1.5rem 0;
        text-align: left;
    }
    .demo-title {
        font-weight: 700;
        color: #166534;
        margin-bottom: 0.5rem;
    }
    .stTextInput>div>div>input {
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #22c55e, #a3e635) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-container">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🌾</div>
        <div class="login-title">AgriVision</div>
        <div class="login-subtitle">AI-Powered Climate Insights & Sustainable Farming</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        login_btn = st.button("🚀 Login to AgriVision", use_container_width=True)

        if login_btn:
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect username or password!")

    return False


def check_authentication():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login()
        return False
    return True