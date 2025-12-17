# components/video_section.py
import streamlit as st
from utils.assets import get_video_base64
import os


def render_video_section():
    st.markdown("""
    <div class="video-section">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        video_path = "assets/video/video.mp4"
        if os.path.exists(video_path):
            video_base64 = get_video_base64(video_path)
            if video_base64:
                st.markdown(f"""
                <div class="video-container-large">
                    <video width="100%" height="auto" autoplay loop muted playsinline style="border-radius: 12px;">
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="video-container-large" style="text-align: center; padding: 60px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">🎬</div>
                <h3 style="color: #0b2416;">Demo Video</h3>
                <p style="color: #2a3f33;">Place your video.mp4 file in assets/video/</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)