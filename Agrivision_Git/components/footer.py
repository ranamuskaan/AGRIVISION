# components/footer.py
import streamlit as st

def render_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-text">
                <p>© 2025 AgriVision. All rights reserved.</p>
                <p>Made with ❤️ for sustainable farming</p>
            </div>
            <div class="footer-links">
                <span>🌾</span>
                <span>🌱</span>
                <span>💧</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)