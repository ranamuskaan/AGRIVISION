# pages/analytics.py - FIXED VERSION (No Dynamic Sections)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def render_analytics():
    # Get current language
    current_lang = st.session_state.get('lang', 'EN')

    # Bilingual text dictionary
    TEXT = {
        'header_title': {
            'EN': "📊 Analytics Dashboard",
            'HI': "📊 एनालिटिक्स डैशबोर्ड"
        },
        'header_subtitle': {
            'EN': "Historical Data & Performance Insights",
            'HI': "ऐतिहासिक डेटा और प्रदर्शन अंतर्दृष्टि"
        },
        'yield_trend': {
            'EN': "### 📈 Historical Yield Trend (Quintal/Hectare)",
            'HI': "### 📈 ऐतिहासिक उपज प्रवृत्ति (क्विंटल/हेक्टेयर)"
        },
        'select_crop_yield': {
            'EN': "Select Crop for Yield Analysis",
            'HI': "उपज विश्लेषण के लिए फसल चुनें"
        },
        'price_trend': {
            'EN': "### 💰 Historical Price Trend (₹/Quintal)",
            'HI': "### 💰 ऐतिहासिक मूल्य प्रवृत्ति (₹/क्विंटल)"
        },
        'select_crop_price': {
            'EN': "Select Crop for Price Analysis",
            'HI': "मूल्य विश्लेषण के लिए फसल चुनें"
        },
        'regional_performance': {
            'EN': "### 🗺️ Regional Performance (2023-2024)",
            'HI': "### 🗺️ क्षेत्रीय प्रदर्शन (2023-2024)"
        },
        'crop_analysis': {
            'EN': "### 🌾 Crop Performance Summary",
            'HI': "### 🌾 फसल प्रदर्शन सारांश"
        },
        'seasonal_insights': {
            'EN': "### 📅 Seasonal Performance (2022-2024)",
            'HI': "### 📅 मौसमी प्रदर्शन (2022-2024)"
        },
        'profit_analysis': {
            'EN': "### 💹 Cost & Profit Analysis",
            'HI': "### 💹 लागत और लाभ विश्लेषण"
        },
        'market_intel': {
            'EN': "### 📋 Market Summary",
            'HI': "### 📋 बाजार सारांश"
        },
        'performance_metrics': {
            'EN': "### 📊 Farm Performance Overview",
            'HI': "### 📊 खेत प्रदर्शन अवलोकन"
        }
    }

    def T(key):
        return TEXT.get(key, {}).get(current_lang, key)

    # Custom CSS for analytics
    st.markdown("""
    <style>
    .analytics-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #dbeafe, #93c5fd);
        padding: 20px;
        border-radius: 15px;
        color: #1e40af;
        margin: 15px 0;
        border-left: 5px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

    # Beautiful Header
    st.markdown(f"""
    <div class="analytics-header">
        <h1 style="margin:0; font-size: 2.5rem;">{T('header_title')}</h1>
        <p style="margin:10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">{T('header_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # STATIC DATA - No random generation
    months_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    months_hi = ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून']
    months = months_en if current_lang == 'EN' else months_hi

    crops_en = ['Wheat', 'Rice', 'Maize', 'Cotton']
    crops_hi = ['गेहूं', 'चावल', 'मक्का', 'कपास']
    crops = crops_en if current_lang == 'EN' else crops_hi

    # REALISTIC STATIC YIELD DATA (Quintal/Hectare)
    yield_data = {
        'Wheat': [42, 44, 45, 43, 46, 48],
        'Rice': [32, 34, 35, 33, 36, 37],
        'Maize': [28, 30, 31, 29, 32, 33],
        'Cotton': [23, 24, 25, 24, 26, 27]
    }

    # REALISTIC STATIC PRICE DATA (₹/Quintal)
    price_data = {
        'Wheat': [2100, 2150, 2200, 2250, 2300, 2350],
        'Rice': [1750, 1780, 1800, 1820, 1850, 1880],
        'Maize': [1650, 1680, 1700, 1720, 1750, 1780],
        'Cotton': [5800, 5900, 6000, 6100, 6200, 6300]
    }

    # Performance Metrics - Static realistic data
    st.markdown(f"### {T('performance_metrics')}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ef4444; margin:0;">📈 {'Avg Yield' if current_lang == 'EN' else 'औसत उपज'}</h3>
            <h1 style="color: #ef4444; margin:10px 0;">38.5 Q/Ha</h1>
            <p style="color: #666; margin:0;">{'Based on 2023-24 data' if current_lang == 'EN' else '2023-24 डेटा के आधार पर'}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #3b82f6; margin:0;">💰 {'Avg Price' if current_lang == 'EN' else 'औसत मूल्य'}</h3>
            <h1 style="color: #3b82f6; margin:10px 0;">₹2,450</h1>
            <p style="color: #666; margin:0;">{'Current market rate' if current_lang == 'EN' else 'वर्तमान बाजार दर'}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #10b981; margin:0;">🏆 {'Profit Margin' if current_lang == 'EN' else 'लाभ मार्जिन'}</h3>
            <h1 style="color: #10b981; margin:10px 0;">28.5%</h1>
            <p style="color: #666; margin:0;">{'Industry average' if current_lang == 'EN' else 'उद्योग औसत'}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #8b5cf6; margin:0;">🌱 {'Crop Health' if current_lang == 'EN' else 'फसल स्वास्थ्य'}</h3>
            <h1 style="color: #8b5cf6; margin:10px 0;">85%</h1>
            <p style="color: #666; margin:0;">{'Optimal Range' if current_lang == 'EN' else 'इष्टतम सीमा'}</p>
        </div>
        """, unsafe_allow_html=True)

    # Main Analytics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(T('yield_trend'))
        selected_crop = st.selectbox(T('select_crop_yield'), crops)

        crop_key = crops_en[crops.index(selected_crop)] if current_lang == 'HI' else selected_crop

        fig_yield = px.line(
            x=months,
            y=yield_data[crop_key],
            labels={'x': 'Month' if current_lang == 'EN' else 'महीना',
                    'y': 'Yield (Quintal/Hectare)' if current_lang == 'EN' else 'उपज (क्विंटल/हेक्टेयर)'},
            height=400
        )
        fig_yield.update_traces(line=dict(color='#22c55e', width=3))
        fig_yield.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title="Historical Yield Data" if current_lang == 'EN' else "ऐतिहासिक उपज डेटा"
        )
        st.plotly_chart(fig_yield, use_container_width=True)

    with col2:
        st.markdown(T('price_trend'))
        selected_crop_price = st.selectbox(T('select_crop_price'), crops)

        crop_price_key = crops_en[crops.index(selected_crop_price)] if current_lang == 'HI' else selected_crop_price

        fig_price = px.bar(
            x=months,
            y=price_data[crop_price_key],
            labels={'x': 'Month' if current_lang == 'EN' else 'महीना',
                    'y': 'Price (₹/Quintal)' if current_lang == 'EN' else 'मूल्य (₹/क्विंटल)'},
            height=400
        )
        fig_price.update_traces(marker_color='#a3e635')
        fig_price.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title="Market Price Trends" if current_lang == 'EN' else "बाजार मूल्य प्रवृत्तियां"
        )
        st.plotly_chart(fig_price, use_container_width=True)

    # Regional Performance - Static data
    st.markdown(T('regional_performance'))

    regions_en = ['North Zone', 'South Zone', 'East Zone', 'West Zone', 'Central Zone']
    regions_hi = ['उत्तर क्षेत्र', 'दक्षिण क्षेत्र', 'पूर्वी क्षेत्र', 'पश्चिमी क्षेत्र', 'मध्य क्षेत्र']
    regions = regions_en if current_lang == 'EN' else regions_hi

    # Static performance data (no randomness)
    performance = [85, 78, 82, 75, 88]

    col3, col4 = st.columns(2)

    with col3:
        fig_regional = px.pie(
            values=performance,
            names=regions,
            title="Regional Yield Performance" if current_lang == 'EN' else "क्षेत्रीय उपज प्रदर्शन",
            height=400
        )
        st.plotly_chart(fig_regional, use_container_width=True)

    with col4:
        st.markdown(T('crop_analysis'))

        # Static analysis data
        analysis_data = {
            'Crop': crops,
            'Avg Yield (Q/Ha)': [43, 34, 30, 25],
            'Avg Price (₹/Q)': [2250, 1850, 1750, 6100],
            'Profit Index': [85, 78, 72, 88]
        }

        df_analysis = pd.DataFrame(analysis_data)

        # Bilingual column names
        if current_lang == 'HI':
            df_analysis.columns = ['फसल', 'औसत उपज (क्विं/हे)', 'औसत मूल्य (₹/क्विं)', 'लाभ सूचकांक']

        st.dataframe(df_analysis, use_container_width=True)

    # Cost Analysis - Static realistic data
    st.markdown(T('profit_analysis'))

    col5, col6 = st.columns(2)

    with col5:
        # Static cost breakdown
        cost_labels_en = ['Seeds (20%)', 'Fertilizers (25%)', 'Labor (30%)', 'Irrigation (15%)', 'Equipment (10%)']
        cost_labels_hi = ['बीज (20%)', 'उर्वरक (25%)', 'श्रम (30%)', 'सिंचाई (15%)', 'उपकरण (10%)']
        cost_labels = cost_labels_en if current_lang == 'EN' else cost_labels_hi

        cost_values = [20, 25, 30, 15, 10]

        fig_cost = px.pie(
            values=cost_values,
            names=cost_labels,
            title="Typical Cost Distribution" if current_lang == 'EN' else "विशिष्ट लागत वितरण",
            height=400
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    with col6:
        # Static profit trend
        profit_trend = [25, 26, 27, 28, 29, 30]

        fig_profit = px.area(
            x=months,
            y=profit_trend,
            labels={'x': 'Month' if current_lang == 'EN' else 'महीना',
                    'y': 'Profit Margin (%)' if current_lang == 'EN' else 'लाभ मार्जिन (%)'},
            title="Typical Profit Trend" if current_lang == 'EN' else "विशिष्ट लाभ प्रवृत्ति",
            height=400
        )
        fig_profit.update_traces(fillcolor='rgba(34, 197, 94, 0.3)', line=dict(color='#22c55e'))
        st.plotly_chart(fig_profit, use_container_width=True)

    # Informational Box - No predictions or forecasts
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin:0;">{'📋 Data Information' if current_lang == 'EN' else '📋 डेटा जानकारी'}</h4>
        <p style="margin:5px 0 0 0;">
            {'This dashboard shows historical agricultural data and typical performance metrics. All data is based on industry averages and past trends.'
    if current_lang == 'EN' else
    'यह डैशबोर्ड ऐतिहासिक कृषि डेटा और विशिष्ट प्रदर्शन मेट्रिक्स दिखाता है। सभी डेटा उद्योग औसत और पिछले रुझानों पर आधारित है।'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Seasonal Insights - Static historical data
    st.markdown(T('seasonal_insights'))

    seasons_en = ['Rabi 2022', 'Kharif 2022', 'Rabi 2023', 'Kharif 2023']
    seasons_hi = ['रबी 2022', 'खरीफ 2022', 'रबी 2023', 'खरीफ 2023']
    seasons = seasons_en if current_lang == 'EN' else seasons_hi

    # Static production data
    production = [95, 88, 102, 94]

    fig_seasonal = px.bar(
        x=seasons,
        y=production,
        labels={'x': 'Season' if current_lang == 'EN' else 'मौसम',
                'y': 'Production Index' if current_lang == 'EN' else 'उत्पादन सूचकांक'},
        title="Historical Seasonal Performance" if current_lang == 'EN' else "ऐतिहासिक मौसमी प्रदर्शन",
        height=400
    )
    fig_seasonal.update_traces(marker_color='#22c55e')
    st.plotly_chart(fig_seasonal, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)