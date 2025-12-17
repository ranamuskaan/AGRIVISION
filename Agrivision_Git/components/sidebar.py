# components/sidebar.py
import streamlit as st
import base64
import os


def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return None
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def render_sidebar():
    with st.sidebar:
        # Logo with image
        try:
            logo_path = "assets/images/logo.png"
            if os.path.exists(logo_path):
                logo_base64 = get_base64_of_bin_file(logo_path)
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="data:image/png;base64,{logo_base64}" width="80%" style="border-radius: 10px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Fallback if logo not found
                st.markdown("""
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="font-size: 32px;">🌾</div>
                    <div style="font-weight: bold; font-size: 20px; color: white;">AgriVision</div>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 32px;">🌾</div>
                <div style="font-weight: bold; font-size: 20px; color: white;">AgriVision</div>
            </div>
            """, unsafe_allow_html=True)

        # Language Section
        st.markdown('<div style="color: white; font-weight: bold; margin-bottom: 10px;">🌐 Select Language</div>',
                    unsafe_allow_html=True)

        lang = st.radio(
            "Language",
            options=["English", "Hindi"],
            key="lang_radio",
            label_visibility="collapsed"
        )

        # Navigation Section
        st.markdown(
            '<div style="color: white; font-weight: bold; margin-bottom: 10px; margin-top: 20px;">📱 Navigation</div>',
            unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            options=["🏠 Home", "🌤️ Weather", "🌱 Advisory", "📊 Analytics", "💬 Chatbot"],
            key="page_radio",
            label_visibility="collapsed"
        )

        # Clean page name
        page_clean = page.split(" ")[-1]

        st.markdown("---")
        st.caption("v1.1 • Enhanced UI/UX")

        # Store language
        lang_code = "EN" if lang == "English" else "HI"
        st.session_state.lang = lang_code

        return page_clean