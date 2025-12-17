# pages/weather.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json


def render_weather():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Get current language
    current_lang = st.session_state.get('lang', 'EN')

    # Bilingual text dictionary
    TEXT = {
        'header_title': {
            'EN': "🌤️ Smart Weather Insights",
            'HI': "🌤️ स्मार्ट मौसम जानकारी"
        },
        'header_subtitle': {
            'EN': "Real-time weather intelligence for smarter farming decisions",
            'HI': "स्मार्ट खेती के फैसलों के लिए रीयल-टाइम मौसम जानकारी"
        },
        'location_label': {
            'EN': "📍 **Enter Your Location**",
            'HI': "📍 **अपना स्थान दर्ज करें**"
        },
        'location_placeholder': {
            'EN': "e.g., Mumbai, Maharashtra",
            'HI': "जैसे, मुंबई, महाराष्ट्र"
        },
        'start_date_label': {
            'EN': "📅 **Start Date**",
            'HI': "📅 **प्रारंभ तिथि**"
        },
        'forecast_days_label': {
            'EN': "📆 **Forecast Days**",
            'HI': "📆 **पूर्वानुमान दिन**"
        }
    }

    def T(key):
        return TEXT.get(key, {}).get(current_lang, key)

    # BEST CSS - Perfectly visible description boxes
    st.markdown("""
    <style>
    .weather-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
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
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    /* PERFECT DESCRIPTION BOXES - Highly Visible */
    .description-box {
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #0ea5e9;
        margin: 15px 0;
        font-size: 15px;
        color: #0369a1;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.2);
        position: relative;
        overflow: hidden;
    }
    .description-box::before {
        content: "💡";
        position: absolute;
        top: 18px;
        left: 20px;
        font-size: 24px;
        opacity: 0.9;
    }
    .description-box-content {
        margin-left: 45px;
        padding-right: 10px;
    }
    .description-box h4 {
        color: #0369a1;
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 700;
    }
    .description-box p {
        color: #0c4a6e;
        margin: 0;
        line-height: 1.6;
        font-weight: 500;
    }

    .alert-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #dc2626;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
    }
    .info-card {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #0d9488;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Beautiful Header
    st.markdown(f"""
    <div class="weather-header">
        <h1 style="margin:0; font-size: 2.5rem;">{T('header_title')}</h1>
        <p style="margin:10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">{T('header_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Location input with better styling
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            location = st.text_input(T('location_label'),
                                     value="Sonipat, Haryana",
                                     placeholder=T('location_placeholder'),
                                     help="Enter city and state for accurate weather forecasts" if current_lang == 'EN' else "सटीक मौसम पूर्वानुमान के लिए शहर और राज्य दर्ज करें")
        with col2:
            start = st.date_input(T('start_date_label'),
                                  value=datetime.today().date(),
                                  help="Select forecast start date" if current_lang == 'EN' else "पूर्वानुमान प्रारंभ तिथि चुनें")
        with col3:
            days = st.selectbox(T('forecast_days_label'),
                                options=[3, 5, 7],
                                index=2,
                                help="Choose forecast duration" if current_lang == 'EN' else "पूर्वानुमान अवधि चुनें")

    # Real-time weather data function
    def get_real_weather_data(location, days):
        try:
            # Replace with your actual OpenWeatherMap API key
            API_KEY = "*******"  # ← PUT YOUR KEY HERE

            # Geocoding API to get coordinates
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
            geo_response = requests.get(geo_url, timeout=10)

            if geo_response.status_code == 200 and geo_response.json():
                geo_data = geo_response.json()[0]
                lat, lon = geo_data['lat'], geo_data['lon']
                city_name = geo_data.get('name', location)
                country = geo_data.get('country', '')

                # Weather forecast API
                weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                weather_response = requests.get(weather_url, timeout=10)

                if weather_response.status_code == 200:
                    weather_data = weather_response.json()

                    # Process hourly data for detailed analysis
                    dates, temps, humidity, rain, pressures, winds, descriptions, icons = [], [], [], [], [], [], [], []

                    for item in weather_data['list'][:days * 8]:  # 8 readings per day
                        dates.append(datetime.fromtimestamp(item['dt']))
                        temps.append(item['main']['temp'])
                        humidity.append(item['main']['humidity'])
                        rain.append(item.get('rain', {}).get('3h', 0))
                        pressures.append(item['main']['pressure'])
                        winds.append(item['wind']['speed'])
                        descriptions.append(item['weather'][0]['description'].title())
                        icons.append(item['weather'][0]['icon'])

                    # Create detailed DataFrame
                    df = pd.DataFrame({
                        'DateTime': dates,
                        'Temperature (°C)': temps,
                        'Humidity (%)': humidity,
                        'Rain (mm)': rain,
                        'Pressure (hPa)': pressures,
                        'Wind Speed (m/s)': winds,
                        'Conditions': descriptions,
                        'Icon': icons
                    })

                    # Add date column for daily aggregation
                    df['Date'] = df['DateTime'].dt.date

                    return df, True, city_name, country

            return generate_realistic_demo_data(location, days), False, location, ""

        except Exception as e:
            st.sidebar.warning(f"⚠️ Using demo data. API Error: {str(e)}")
            return generate_realistic_demo_data(location, days), False, location, ""

    def generate_realistic_demo_data(location, days):
        """Generate realistic demo data when API is unavailable"""
        dates = pd.date_range(datetime.today(), periods=days * 8, freq="3H")

        # Location-based variations
        if 'haryana' in location.lower() or 'punjab' in location.lower():
            base_temp = np.random.uniform(25, 38)
            base_humidity = 45
        elif 'kerala' in location.lower() or 'tamilnadu' in location.lower():
            base_temp = np.random.uniform(28, 32)
            base_humidity = 75
        else:
            base_temp = np.random.uniform(20, 35)
            base_humidity = 60

        # Generate realistic time-series data
        time_points = len(dates)
        time_idx = np.arange(time_points)

        # Temperature with daily cycle
        temps = base_temp + 8 * np.sin(2 * np.pi * time_idx / 8 - np.pi / 2) + np.random.normal(0, 2, time_points)

        # Other parameters
        humidity = np.clip(base_humidity + 20 * np.sin(2 * np.pi * time_idx / 8) + np.random.normal(0, 10, time_points),
                           30, 95)
        rain = np.clip(np.random.exponential(0.5, time_points), 0, 15)
        pressure = 1013 + 10 * np.sin(2 * np.pi * time_idx / 16) + np.random.normal(0, 3, time_points)
        wind = np.clip(np.random.exponential(2, time_points), 0, 12)

        # Weather conditions based on parameters
        conditions = []
        icons = []
        for i in range(time_points):
            if rain[i] > 5:
                conditions.append('Heavy Rain')
                icons.append('10d')
            elif rain[i] > 1:
                conditions.append('Light Rain')
                icons.append('09d')
            elif humidity[i] > 80:
                conditions.append('Cloudy')
                icons.append('04d')
            else:
                conditions.append('Clear Sky')
                icons.append('01d')

        df = pd.DataFrame({
            'DateTime': dates,
            'Temperature (°C)': np.round(temps, 1),
            'Humidity (%)': np.round(humidity, 0),
            'Rain (mm)': np.round(rain, 1),
            'Pressure (hPa)': np.round(pressure, 1),
            'Wind Speed (m/s)': np.round(wind, 1),
            'Conditions': conditions,
            'Icon': icons,
            'Date': [d.date() for d in dates]
        })

        return df

    # Get weather data
    weather_df, is_real_data, city_name, country = get_real_weather_data(location, days)

    # Bilingual descriptions dictionary
    DESCRIPTIONS = {
        'live_data': {
            'EN': "📍 **Live Data for**: {}",
            'HI': "📍 **लाइव डेटा के लिए**: {}"
        },
        'demo_data': {
            'EN': "📍 **Demo Data for**: {} (Add API key for real-time data)",
            'HI': "📍 **डेमो डेटा के लिए**: {} (रीयल-टाइम डेटा के लिए API key जोड़ें)"
        },
        'current_summary': {
            'EN': "### 🎯 Current Weather Summary",
            'HI': "### 🎯 वर्तमान मौसम सारांश"
        },
        'temp_description': {
            'EN': "Shows current temperature and average for the forecast period",
            'HI': "वर्तमान तापमान और पूर्वानुमान अवधि का औसत दिखाता है"
        },
        'humidity_description': {
            'EN': "Current humidity level and average moisture in air",
            'HI': "वर्तमान आर्द्रता स्तर और हवा में औसत नमी"
        },
        'rain_description': {
            'EN': "Total rainfall expected during the forecast period",
            'HI': "पूर्वानुमान अवधि के दौरान कुल वर्षा की संभावना"
        },
        'wind_description': {
            'EN': "Current wind speed and average wind conditions",
            'HI': "वर्तमान हवा की गति और औसत हवा की स्थिति"
        },
        'overview_chart': {
            'EN': "### 📊 Quick Weather Overview",
            'HI': "### 📊 त्वरित मौसम अवलोकन"
        },
        'overview_description': {
            'EN': "This chart shows daily temperature ranges. The shaded area represents the temperature variation throughout each day.",
            'HI': "यह चार्ट दैनिक तापमान रेंज दिखाता है। छायांकित क्षेत्र प्रत्येक दिन तापमान में बदलाव को दर्शाता है।"
        },
        'analytics_tab': {
            'EN': "### 📈 Advanced Weather Analytics",
            'HI': "### 📈 उन्नत मौसम विश्लेषण"
        },
        'heatmap_title': {
            'EN': "#### 🌡️ Temperature Heatmap",
            'HI': "#### 🌡️ तापमान हीटमैप"
        },
        'heatmap_description': {
            'EN': "This heatmap shows temperature patterns throughout the day. Darker red colors indicate warmer temperatures, while blue shows cooler periods.",
            'HI': "यह हीटमैप पूरे दिन तापमान पैटर्न दिखाता है। गहरे लाल रंग गर्म तापमान दर्शाते हैं, जबकि नीला ठंडे समय को दिखाता है।"
        },
        'radar_title': {
            'EN': "#### 📊 Weather Parameters Radar",
            'HI': "#### 📊 मौसम पैरामीटर रडार"
        },
        'radar_description': {
            'EN': "The radar chart compares different weather parameters. A larger area means more balanced weather conditions.",
            'HI': "रडार चार्ट विभिन्न मौसम पैरामीटर की तुलना करता है। बड़ा क्षेत्र अधिक संतुलित मौसम स्थितियों को दर्शाता है।"
        },
        'wind_analysis': {
            'EN': "#### 💨 Wind & Pressure Analysis",
            'HI': "#### 💨 हवा और दबाव विश्लेषण"
        },
        'wind_rose_description': {
            'EN': "Wind rose shows wind patterns from different directions. Longer bars mean stronger winds from that direction.",
            'HI': "विंड रोज अलग-अलग दिशाओं से हवा के पैटर्न दिखाता है। लंबी बार उस दिशा से तेज हवाओं को दर्शाती है।"
        },
        'pressure_description': {
            'EN': "Pressure trend helps predict weather changes. Rising pressure often means improving weather.",
            'HI': "दबाव ट्रेंड मौसम परिवर्तन की भविष्यवाणी में मदद करता है। बढ़ता दबाव अक्सर बेहतर मौसम का संकेत देता है।"
        },
        'farm_advice': {
            'EN': "### 🌱 Smart Farming Recommendations",
            'HI': "### 🌱 स्मार्ट खेती सिफारिशें"
        },
        'critical_alerts': {
            'EN': "#### ⚠️ Critical Alerts",
            'HI': "#### ⚠️ महत्वपूर्ण अलर्ट"
        },
        'favorable_conditions': {
            'EN': "#### ✅ Favorable Conditions",
            'HI': "#### ✅ अनुकूल परिस्थितियां"
        },
        'crop_specific': {
            'EN': "#### 🌾 Crop-Specific Recommendations",
            'HI': "#### 🌾 फसल-विशिष्ट सिफारिशें"
        },
        'detailed_forecast': {
            'EN': "### 📋 Detailed Hourly Forecast",
            'HI': "### 📋 विस्तृत घंटावार पूर्वानुमान"
        }
    }

    def D(key):
        return DESCRIPTIONS.get(key, {}).get(current_lang, key)

    # Display location info
    if is_real_data:
        st.success(D('live_data').format(f"{city_name}, {country}"))
    else:
        st.info(D('demo_data').format(location))

    # Create interactive tabs with bilingual labels
    tab_labels = {
        'EN': ["🌡️ Dashboard", "📈 Analytics", "🌱 Farm Advice", "📋 Detailed Forecast"],
        'HI': ["🌡️ डैशबोर्ड", "📈 विश्लेषण", "🌱 खेती सलाह", "📋 विस्तृत पूर्वानुमान"]
    }

    tab1, tab2, tab3, tab4 = st.tabs(tab_labels[current_lang])

    with tab1:
        # Current weather summary
        st.markdown(D('current_summary'))

        # Calculate current metrics (latest reading)
        current_data = weather_df.iloc[0]
        avg_temp = weather_df['Temperature (°C)'].mean()
        total_rain = weather_df['Rain (mm)'].sum()
        avg_humidity = weather_df['Humidity (%)'].mean()
        avg_wind = weather_df['Wind Speed (m/s)'].mean()

        # Metric cards in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #ef4444; margin:0;">🌡️ {'Temperature' if current_lang == 'EN' else 'तापमान'}</h3>
                <h1 style="color: #ef4444; margin:10px 0;">{current_data['Temperature (°C)']:.1f}°C</h1>
                <p style="color: #666; margin:0;">{'Avg' if current_lang == 'EN' else 'औसत'}: {avg_temp:.1f}°C</p>
            </div>
            """, unsafe_allow_html=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('temp_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #3b82f6; margin:0;">💧 {'Humidity' if current_lang == 'EN' else 'आर्द्रता'}</h3>
                <h1 style="color: #3b82f6; margin:10px 0;">{current_data['Humidity (%)']:.0f}%</h1>
                <p style="color: #666; margin:0;">{'Avg' if current_lang == 'EN' else 'औसत'}: {avg_humidity:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('humidity_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #10b981; margin:0;">🌧️ {'Rainfall' if current_lang == 'EN' else 'वर्षा'}</h3>
                <h1 style="color: #10b981; margin:10px 0;">{total_rain:.1f}mm</h1>
                <p style="color: #666; margin:0;">{'Total' if current_lang == 'EN' else 'कुल'} {days} {'days' if current_lang == 'EN' else 'दिन'}</p>
            </div>
            """, unsafe_allow_html=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('rain_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #8b5cf6; margin:0;">💨 {'Wind' if current_lang == 'EN' else 'हवा'}</h3>
                <h1 style="color: #8b5cf6; margin:10px 0;">{current_data['Wind Speed (m/s)']:.1f} m/s</h1>
                <p style="color: #666; margin:0;">{'Avg' if current_lang == 'EN' else 'औसत'}: {avg_wind:.1f} m/s</p>
            </div>
            """, unsafe_allow_html=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('wind_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Quick weather chart
        st.markdown(D('overview_chart'))

        # Daily aggregated data for overview
        daily_data = weather_df.groupby('Date').agg({
            'Temperature (°C)': ['mean', 'min', 'max'],
            'Rain (mm)': 'sum',
            'Humidity (%)': 'mean'
        }).round(1)
        daily_data.columns = ['Avg Temp', 'Min Temp', 'Max Temp', 'Total Rain', 'Avg Humidity']
        daily_data = daily_data.reset_index()

        fig_overview = go.Figure()

        # Temperature range
        fig_overview.add_trace(go.Scatter(
            x=daily_data['Date'], y=daily_data['Max Temp'],
            mode='lines', line=dict(width=0), showlegend=False,
            name='Max Temp'
        ))
        fig_overview.add_trace(go.Scatter(
            x=daily_data['Date'], y=daily_data['Min Temp'],
            mode='lines', line=dict(width=0),
            fill='tonexty', fillcolor='rgba(255, 107, 107, 0.2)',
            name='Temperature Range'
        ))
        fig_overview.add_trace(go.Scatter(
            x=daily_data['Date'], y=daily_data['Avg Temp'],
            mode='lines+markers', line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8), name='Average Temp'
        ))

        fig_overview.update_layout(
            title='Daily Temperature Range',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            height=300
        )

        st.plotly_chart(fig_overview, use_container_width=True)
        # PERFECT DESCRIPTION BOX
        st.markdown(f"""
        <div class='description-box'>
            <div class='description-box-content'>
                <p>{D('overview_description')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(D('analytics_tab'))

        col1, col2 = st.columns(2)

        with col1:
            # Interactive temperature heatmap
            st.markdown(D('heatmap_title'))

            # Create hourly heatmap data
            weather_df['Hour'] = weather_df['DateTime'].dt.hour
            weather_df['Day'] = weather_df['DateTime'].dt.date

            heatmap_data = weather_df.pivot_table(
                values='Temperature (°C)',
                index='Hour',
                columns='Day',
                aggfunc='mean'
            ).round(1)

            fig_heatmap = px.imshow(
                heatmap_data,
                labels=dict(x="Date", y="Hour of Day", color="Temperature (°C)"),
                color_continuous_scale="RdYlBu_r",
                aspect="auto"
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('heatmap_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Weather parameters radar chart
            st.markdown(D('radar_title'))

            # Normalize parameters for radar chart
            params = ['Temperature (°C)', 'Humidity (%)', 'Rain (mm)', 'Wind Speed (m/s)', 'Pressure (hPa)']
            max_vals = [40, 100, 20, 15, 1040]  # Maximum expected values
            normalized = []

            for param, max_val in zip(params, max_vals):
                val = weather_df[param].mean()
                normalized.append((val / max_val) * 100)

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=normalized,
                theta=params,
                fill='toself',
                fillcolor='rgba(34, 197, 94, 0.3)',
                line=dict(color='#22c55e', width=2),
                name='Current Conditions'
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig_radar, use_container_width=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('radar_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Wind and Pressure analysis
        st.markdown(D('wind_analysis'))

        col3, col4 = st.columns(2)

        with col3:
            # Wind rose chart
            wind_data = weather_df[['Wind Speed (m/s)', 'Conditions']].copy()
            fig_wind = px.bar_polar(
                wind_data,
                r='Wind Speed (m/s)',
                theta='Conditions',
                color='Wind Speed (m/s)',
                template='plotly_white',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            fig_wind.update_layout(height=300)
            st.plotly_chart(fig_wind, use_container_width=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('wind_rose_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            # Pressure trend
            fig_pressure = px.line(
                weather_df,
                x='DateTime',
                y='Pressure (hPa)',
                title='Atmospheric Pressure Trend',
                line_shape='spline'
            )
            fig_pressure.update_traces(
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=4)
            )
            fig_pressure.update_layout(height=300)
            st.plotly_chart(fig_pressure, use_container_width=True)
            # PERFECT DESCRIPTION BOX
            st.markdown(f"""
            <div class='description-box'>
                <div class='description-box-content'>
                    <p>{D('pressure_description')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown(D('farm_advice'))

        # Calculate farming metrics
        avg_temp = weather_df['Temperature (°C)'].mean()
        total_rain = weather_df['Rain (mm)'].sum()
        avg_humidity = weather_df['Humidity (%)'].mean()
        max_temp = weather_df['Temperature (°C)'].max()
        min_temp = weather_df['Temperature (°C)'].min()

        # Bilingual farming recommendations
        FARMING_TIPS = {
            'heat_alert': {
                'EN': ("🔥 Heat Stress Alert",
                       "High temperatures can stress crops. Increase irrigation frequency and consider shade nets for sensitive plants."),
                'HI': ("🔥 गर्मी का तनाव अलर्ट",
                       "उच्च तापमान फसलों को तनाव में डाल सकता है। सिंचाई की आवृत्ति बढ़ाएं और संवेदनशील पौधों के लिए शेड नेट्स पर विचार करें।")
            },
            'cold_alert': {
                'EN': ("❄️ Cold Stress Warning",
                       "Low temperatures may affect crop growth. Consider protective covers and adjust planting schedules."),
                'HI': ("❄️ ठंड का तनाव चेतावनी",
                       "कम तापमान फसल वृद्धि को प्रभावित कर सकता है। सुरक्षात्मक कवर पर विचार करें और रोपण कार्यक्रम समायोजित करें।")
            },
            'temp_optimal': {
                'EN': "✅ Temperature range is optimal for most crops",
                'HI': "✅ अधिकांश फसलों के लिए तापमान रेंज इष्टतम है"
            },
            'heavy_rain': {
                'EN': ("🌧️ Heavy Rainfall Alert",
                       "Ensure proper drainage. Delay fertilizer application and protect against soil erosion."),
                'HI': ("🌧️ भारी वर्षा अलर्ट",
                       "उचित जल निकासी सुनिश्चित करें। उर्वरक अनुप्रयोग में देरी करें और मिट्टी के कटाव से बचाव करें।")
            },
            'irrigation_needed': {
                'EN': ("🏜️ Irrigation Needed",
                       "Low rainfall expected. Schedule irrigation and consider drought-resistant varieties."),
                'HI': ("🏜️ सिंचाई की आवश्यकता",
                       "कम वर्षा की संभावना है। सिंचाई का समय निर्धारित करें और सूखा-प्रतिरोधी किस्मों पर विचार करें।")
            },
            'rain_adequate': {
                'EN': "✅ Rainfall levels are adequate for most crops",
                'HI': "✅ अधिकांश फसलों के लिए वर्षा का स्तर पर्याप्त है"
            }
        }

        def F(key):
            return FARMING_TIPS.get(key, {}).get(current_lang, key)

        # Generate farming recommendations
        recommendations = []
        alerts = []

        # Temperature-based recommendations
        if avg_temp > 35:
            alerts.append(F('heat_alert'))
        elif avg_temp < 15:
            alerts.append(F('cold_alert'))
        else:
            recommendations.append(F('temp_optimal'))

        # Rainfall-based recommendations
        if total_rain > 30:
            alerts.append(F('heavy_rain'))
        elif total_rain < 10:
            alerts.append(F('irrigation_needed'))
        else:
            recommendations.append(F('rain_adequate'))

        # Display alerts
        if alerts:
            st.markdown(D('critical_alerts'))
            for title, message in alerts:
                st.markdown(f"""
                <div class="alert-card">
                    <h4 style="margin:0;">{title}</h4>
                    <p style="margin:5px 0 0 0;">{message}</p>
                </div>
                """, unsafe_allow_html=True)

        # Display recommendations
        if recommendations:
            st.markdown(D('favorable_conditions'))
            for rec in recommendations:
                st.markdown(f"""
                <div class="info-card">
                    <p style="margin:0;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)

        # Crop-specific advice
        st.markdown(D('crop_specific'))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Wheat & Cereals**" if current_lang == 'EN' else "**गेहूं और अनाज**")
            if 15 <= avg_temp <= 25:
                st.success(
                    "Ideal conditions for wheat growth" if current_lang == 'EN' else "गेहूं की वृद्धि के लिए आदर्श स्थितियां")
            else:
                st.warning("Monitor for temperature stress" if current_lang == 'EN' else "तापमान तनाव की निगरानी करें")

            st.markdown("**Vegetables**" if current_lang == 'EN' else "**सब्जियां**")
            if 20 <= avg_temp <= 30 and total_rain < 20:
                st.success("Good for most vegetables" if current_lang == 'EN' else "अधिकांश सब्जियों के लिए अच्छा")
            else:
                st.info(
                    "Adjust irrigation based on rainfall" if current_lang == 'EN' else "वर्षा के आधार पर सिंचाई समायोजित करें")

        with col2:
            st.markdown("**Rice & Paddy**" if current_lang == 'EN' else "**चावल और धान**")
            if avg_temp > 25 and total_rain > 15:
                st.success("Suitable for rice cultivation" if current_lang == 'EN' else "चावल की खेती के लिए उपयुक्त")
            else:
                st.warning(
                    "Ensure adequate water supply" if current_lang == 'EN' else "पर्याप्त पानी की आपूर्ति सुनिश्चित करें")

            st.markdown("**Fruits**" if current_lang == 'EN' else "**फल**")
            if 18 <= avg_temp <= 32:
                st.success("Favorable for fruit crops" if current_lang == 'EN' else "फलों की फसलों के लिए अनुकूल")
            else:
                st.info("Protect from extreme temperatures" if current_lang == 'EN' else "चरम तापमान से बचाव करें")

    with tab4:
        st.markdown(D('detailed_forecast'))

        # FIXED: Use actual DataFrame column names for multiselect
        # Default columns that exist in the DataFrame
        default_columns = ['DateTime', 'Temperature (°C)', 'Conditions', 'Rain (mm)', 'Humidity (%)']

        # Interactive dataframe with filters
        col1, col2 = st.columns(2)
        with col1:
            show_columns = st.multiselect(
                "Select columns to display:" if current_lang == 'EN' else "प्रदर्शित करने के लिए कॉलम चुनें:",
                options=weather_df.columns.tolist(),
                default=default_columns
            )
        with col2:
            rows_to_show = st.slider(
                "Number of rows to display:" if current_lang == 'EN' else "प्रदर्शित करने के लिए पंक्तियों की संख्या:",
                10, 100, 24
            )

        # Display filtered dataframe
        if show_columns:  # Only display if columns are selected
            display_df = weather_df[show_columns].head(rows_to_show)

            # Style the dataframe
            styled_df = display_df.style.format({
                'Temperature (°C)': '{:.1f}°C',
                'Humidity (%)': '{:.0f}%',
                'Rain (mm)': '{:.1f}mm',
                'Wind Speed (m/s)': '{:.1f} m/s',
                'Pressure (hPa)': '{:.1f} hPa'
            }).background_gradient(subset=['Temperature (°C)'], cmap='YlOrRd') \
                .background_gradient(subset=['Rain (mm)'], cmap='Blues') \
                .background_gradient(subset=['Humidity (%)'], cmap='GnBu')

            st.dataframe(styled_df, use_container_width=True, height=400)
        else:
            st.info(
                "Please select at least one column to display" if current_lang == 'EN' else "कृपया प्रदर्शित करने के लिए कम से कम एक कॉलम चुनें")

        # Download option with bilingual label
        csv = weather_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Weather Data (CSV)" if current_lang == 'EN' else "📥 मौसम डेटा डाउनलोड करें (CSV)",
            data=csv,
            file_name=f"weather_forecast_{location.replace(',', '_')}.csv",
            mime="text/csv"
        )

    # API key reminder in sidebar
    if not is_real_data:
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            "### 🔑 Get Real Weather Data" if current_lang == 'EN' else "### 🔑 असली मौसम डेटा प्राप्त करें")
        st.sidebar.info("""
        1. Visit [OpenWeatherMap](https://openweathermap.org/api)
        2. Sign up for free account  
        3. Get your API key
        4. Replace `YOUR_ACTUAL_OPENWEATHER_API_KEY` in the code
        """ if current_lang == 'EN' else """
        1. [OpenWeatherMap](https://openweathermap.org/api) पर जाएं
        2. मुफ्त खाते के लिए साइन अप करें
        3. अपनी API key प्राप्त करें
        4. कोड में `YOUR_ACTUAL_OPENWEATHER_API_KEY` को बदलें
        """)

    st.markdown('</div>', unsafe_allow_html=True)