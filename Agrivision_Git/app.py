# app.py
import streamlit as st
from auth.login import check_authentication
from components.sidebar import render_sidebar
from _pages.home import render_home
from _pages.weather import render_weather
from _pages.advisory import render_advisory
from _pages.analytics import render_analytics
from _pages.chatbot import render_chatbot

# Page Config
st.set_page_config(
    page_title="AgriVision — Climate-smart Farming",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check authentication
if not check_authentication():
    st.stop()

# Get page from sidebar
page = render_sidebar()

# Render selected page
if page == "Home":
    render_home()
elif page == "Weather":
    render_weather()
elif page == "Advisory":
    render_advisory()
elif page == "Analytics":
    render_analytics()
elif page == "Chatbot":
    render_chatbot()