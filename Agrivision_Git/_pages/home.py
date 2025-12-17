# pages/home.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import os
from utils.helpers import T
from utils.assets import get_base64_of_bin_file
from components.video_section import render_video_section
from components.footer import render_footer


def render_home():
    # Apply CSS
    apply_styles()

    # Render ticker
    render_ticker()

    # Main content
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Show logo
    render_logo()

    # Hero section
    render_hero_section()

    # KPI section
    render_kpi_section()

    # Features section
    render_features_section()

    # Charts section
    render_charts_section()

    # Video section
    render_video_section()

    # Footer
    render_footer()

    st.markdown('</div>', unsafe_allow_html=True)


def apply_styles():
    try:
        bg_image_path = "assets/images/bg.jpg"
        encoded_bg = get_base64_of_bin_file(bg_image_path)
        if encoded_bg:
            bg_style = f"data:image/jpg;base64,{encoded_bg}"
        else:
            bg_style = "https://images.unsplash.com/photo-1591886800249-8115406b6d6e?auto=format&fit=crop&w=2070&q=80"
    except Exception:
        bg_style = "https://images.unsplash.com/photo-1591886800249-8115406b6d6e?auto=format&fit=crop&w=2070&q=80"

    css = f"""
    <style>
    :root {{
      --primary: #22c55e;
      --accent: #a3e635;
      --dark: #0b2416;
      --muted: #2a3f33;
    }}
    .stApp {{ 
        background: transparent; 
        margin-top: 40px !important;
    }}
    header[data-testid="stHeader"] {{ 
        background: transparent; 
        height: 40px;
        padding-top: 5px;
    }}
    section[data-testid="stSidebar"] > div {{
      background: rgba(0, 0, 0, 0.9);
      border-right: 1px solid #2b2b2b;
      margin-top: 40px;
    }}
    section[data-testid="stSidebar"] * {{ color: #fff !important; }}
    section[data-testid="stSidebar"] label {{ font-weight: 600; }}
    .app-bg {{ position: fixed; inset: 0; z-index: -10; background: url('{bg_style}') center/cover no-repeat; filter: blur(2px) brightness(0.85); }}
    .app-overlay {{ position: fixed; inset: 0; z-index: -5; background: linear-gradient(180deg, rgba(255,255,255,.2), rgba(255,255,255,.55)); }}
    .main {{ 
        background: rgba(255, 255, 255, 0.85); 
        border-radius: 16px; 
        padding: 18px;
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(255,255,255,.5);
        margin-top: 5px;
    }}
    .card {{ backdrop-filter: blur(12px); background: rgba(255,255,255,.9); border: 1px solid rgba(255,255,255,.6); border-radius: 16px; padding: 16px; transition: transform .25s ease, box-shadow .25s ease; box-shadow: 0 8px 30px rgba(0,0,0,.06); color: var(--dark); }}
    .card:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 20px 40px rgba(34,197,94,.25); }}
    .card h3 {{ margin: 0 0 6px 0; color: var(--dark) !important; }}
    .btn-primary {{ display:inline-block; padding: 12px 20px; border-radius: 14px; background: linear-gradient(45deg, var(--primary), var(--accent)); color:#062312; font-weight:700; text-decoration:none; transition: transform .2s ease, box-shadow .2s ease; border: 2px solid #0d3b1e; animation: pulse 2s infinite; }}
    .btn-primary:hover {{ transform: translateY(-2px) scale(1.05); box-shadow: 0 0 15px var(--accent); }}
    @keyframes pulse {{ 0%,100%{{box-shadow:0 0 0 rgba(34,197,94,0.35)}} 50%{{box-shadow:0 0 25px rgba(34,197,94,0.7)}} }}
    .fade-in {{ animation: fadeInUp .7s ease both; }}
    @keyframes fadeInUp {{ from{{opacity:0; transform:translateY(16px)}} to{{opacity:1; transform:none}} }}
    h1,h2,h3,h4,h5,h6 {{ color: var(--dark) !important; font-weight: 800 !important; }}
    h1.title-gradient {{
      font-size: clamp(1.8rem, 3.2vw + 1rem, 3.1rem) !important;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      -webkit-background-clip: text; background-clip: text; color: transparent;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.08);
      margin-top: 0px !important;
      margin-bottom: 5px !important;
    }}
    .subtitle {{ 
      color: var(--muted) !important; 
      font-weight: 600; 
      margin-top: 0px !important;
      margin-bottom: 15px !important;
    }}
    .kpi {{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
    .kpi .num {{ font-size: 2rem; font-weight: 900; color: var(--dark); }}
    .kpi .lbl {{ font-weight: 700; color: var(--muted); }}

    @keyframes ticker-scroll {{
        0% {{ transform: translateX(100vw); }}
        100% {{ transform: translateX(-100%); }}
    }}
    .ticker-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        overflow: hidden;
        background: linear-gradient(90deg, rgba(34,197,94,0.97), rgba(163,230,53,0.97));
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        padding: 8px 0;
        border-bottom: 2px solid #0d3b1e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        margin: 0;
    }}
    .ticker-content {{
        display: inline-block;
        white-space: nowrap;
        animation: ticker-scroll 25s linear infinite;
        padding-right: 100%;
        animation-delay: 0s !important;
    }}
    .ticker-content:hover {{
        animation-play-state: paused;
    }}
    .ticker-item {{
        display: inline-block;
        padding: 0 20px;
        position: relative;
    }}
    .ticker-item:after {{
        content: "•";
        position: absolute;
        right: -5px;
        color: rgba(255,255,255,0.7);
    }}
    .ticker-item:last-child:after {{
        content: "";
    }}
    .ticker-highlight {{
        color: #062312;
        text-shadow: 0 0 8px rgba(255,255,255,0.5);
        font-size: 1.3rem;
        font-weight: 900;
    }}
    .video-section {{
        margin-top: 40px;
        padding: 20px 0;
    }}
    .video-container-large {{
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0,0,0,0.25);
        border: 4px solid rgba(34,197,94,0.5);
        background: rgba(255,255,255,0.95);
        padding: 25px;
        margin: 0 auto;
        max-width: 1000px;
        width: 90%;
    }}
    .footer {{
        margin-top: 50px;
        padding: 25px 0;
        background: linear-gradient(90deg, rgba(34,197,94,0.1), rgba(163,230,53,0.1));
        border-top: 2px solid rgba(34,197,94,0.3);
        border-radius: 16px 16px 0 0;
    }}
    .footer-content {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }}
    .footer-text p {{
        margin: 5px 0;
        color: var(--muted);
        font-weight: 600;
    }}
    .footer-links span {{
        font-size: 1.5rem;
        margin: 0 8px;
        opacity: 0.8;
    }}
    .footer-links span:hover {{
        opacity: 1;
        transform: scale(1.1);
    }}
    @media (max-width: 768px) {{
        .footer-content {{
            flex-direction: column;
            text-align: center;
            gap: 15px;
        }}
    }}
    </style>
    <div class="app-bg"></div>
    <div class="app-overlay"></div>
    """
    st.markdown(css, unsafe_allow_html=True)



def render_ticker():
    ticker_html = """
    <div class="ticker-container">
        <div class="ticker-content">
            <span class="ticker-item"><span class="ticker-highlight">🌾 Welcome to AGRIVISION</span> — AI-Powered Climate Insights & Sustainable Farming Platform</span>
            <span class="ticker-item">🌱 Real-time weather monitoring & crop advisory</span>
            <span class="ticker-item">💧 Smart irrigation recommendations</span>
            <span class="ticker-item">📈 Data-driven farming insights</span>
            <span class="ticker-item">🌍 Serving farmers across India</span>
            <span class="ticker-item">🚜 Empowering farmers with technology</span>
            <span class="ticker-item">📱 Download our mobile app for real-time alerts</span>
        </div>
    </div>
    """
    st.markdown(ticker_html, unsafe_allow_html=True)


def render_logo():
    logo_path = "assets/images/agrivision.png"
    if os.path.exists(logo_path):
        logo_base64 = get_base64_of_bin_file(logo_path)
        if logo_base64:
            st.markdown(
                f"""
                <style>
                @keyframes softpulse {{
                    0% {{ transform: scale(1); opacity: 0.9; }}
                    50% {{ transform: scale(1.04); opacity: 1; }}
                    100% {{ transform: scale(1); opacity: 0.9; }}
                }}
                .hero-logo {{
                    position: absolute;
                    top: 50px;
                    right: 14vw;
                    z-index: 50;
                    animation: softpulse 5s ease-in-out infinite;
                }}
                .hero-logo img {{
                    width: 20vw;
                    max-width: 150px;
                    min-width: 100px;
                }}
                @media (max-width: 992px) {{
                    .hero-logo {{
                        top: 60px;
                        right: 5vw;
                    }}
                    .hero-logo img {{
                        width: 15vw;
                        max-width: 130px;
                    }}
                }}
                @media (max-width: 600px) {{
                    .hero-logo {{
                        top: 50px;
                        right: 3vw;
                    }}
                    .hero-logo img {{
                        width: 25vw;
                        max-width: 120px;
                    }}
                }}
                </style>
                <div class="hero-logo fade-in">
                    <img src="data:image/png;base64,{logo_base64}">
                </div>
                """,
                unsafe_allow_html=True
            )


def render_hero_section():
    lang = st.session_state.get('lang', 'EN')

    c1, c2 = st.columns([7, 5], vertical_alignment="center")
    with c1:
        st.markdown(
            f"<h1 class='title-gradient fade-in'>AgriVision · एग्रीविजन</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<h3 class='subtitle fade-in'>{T('tagline', lang)}</h3>", unsafe_allow_html=True)
        st.markdown('<a class="btn-primary" href="#quick">' + T("hero_cta", lang) + "</a>", unsafe_allow_html=True)
    with c2:
        try:
            from streamlit_lottie import st_lottie
            import requests

            @st.cache_data(show_spinner=False)
            def load_lottie(url: str):
                try:
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        return r.json()
                except Exception:
                    return None
                return None

            lottie = load_lottie("https://assets4.lottiefiles.com/packages/lf20_S9bY9A.json")
            if lottie:
                st_lottie(lottie, height=240, speed=0.9, loop=True)
        except:
            st.markdown("""
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 4rem;"></div>
            </div>
            """, unsafe_allow_html=True)


def render_kpi_section():
    lang = st.session_state.get('lang', 'EN')

    if "_did_kpi_anim" not in st.session_state:
        st.session_state._did_kpi_anim = False

    def animated_kpi(target: int, label: str, suffix: str = ""):
        box = st.empty()
        steps = 50
        dur = 0.5
        delay = dur / steps
        if not st.session_state._did_kpi_anim:
            for i in range(0, target + 1, max(target // steps, 1)):
                display_val = f"{i}{suffix}" if target < 1000 else f"{i // 1000}k+"
                box.markdown(
                    f"<div class='card kpi fade-in'><div class='num'>{display_val}</div><div class='lbl'>{label}</div></div>",
                    unsafe_allow_html=True)
                time.sleep(delay)
        display_val = f"{target}{suffix}" if target < 1000 else f"{target // 1000}k+"
        box.markdown(f"<div class='card kpi'><div class='num'>{display_val}</div><div class='lbl'>{label}</div></div>",
                     unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1:
        animated_kpi(120000, T("farmers", lang))
    with k2:
        animated_kpi(92, T("accuracy", lang), suffix="%")
    with k3:
        animated_kpi(28, T("coverage", lang))
    st.session_state._did_kpi_anim = True


def render_features_section():
    lang = st.session_state.get('lang', 'EN')

    st.markdown("### 🌟 Why AgriVision is Different")
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<div class='card fade-in'><h3>🌱 {'AI-driven Farming' if lang == 'EN' else 'एआई आधारित खेती'}</h3><div>{'Smart crop & soil insights' if lang == 'EN' else 'स्मार्ट फसल और मिट्टी की जानकारी'}</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='card fade-in'><h3>🌤️ {'Live Weather Insights' if lang == 'EN' else 'रीयल-टाइम मौसम'}</h3><div>{'Timely irrigation & risk alerts' if lang == 'EN' else 'समय पर सिंचाई व जोखिम चेतावनी'}</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='card fade-in'><h3>🛰️ {'Local + Global View' if lang == 'EN' else 'स्थानीय + वैश्विक दृष्टि'}</h3><div>{'Serving farmers across India' if lang == 'EN' else 'भारतभर सेवा'}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_charts_section():
    st.markdown("### 📈 Climate & Crop Demo Analytics")

    # First row of charts
    left, right = st.columns([6, 5])
    with left:
        rng = pd.date_range("2024-06-01", "2026-03-31", freq="D")
        base = np.sin(np.linspace(0, 3 * np.pi, len(rng))) * 20
        noise = np.random.normal(0, 5, len(rng))
        anomaly = base + noise
        df_line = pd.DataFrame({"date": rng, "Rainfall Anomaly (mm)": anomaly})
        fig_line = px.line(df_line, x="date", y="Rainfall Anomaly (mm)", title="Monsoon Rainfall Anomaly — Demo")
        fig_line.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300)
        st.plotly_chart(fig_line, use_container_width=True)

    with right:
        crops = ["Wheat", "Rice", "Maize", "Cotton", "Soybean", "Sugarcane"]
        risk = np.clip(np.random.normal(55, 18, len(crops)), 10, 95)
        df_bar = pd.DataFrame({"Crop": crops, "Risk Index": risk})
        fig_bar = px.bar(df_bar, x="Crop", y="Risk Index", title="Top Crops — Risk Index (Demo)")
        fig_bar.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div id="quick"></div>', unsafe_allow_html=True)

    # Second row of info boxes
    left, right = st.columns([6, 5])

    def render_rainfall_anomaly_info():
        lang = st.session_state.get('lang', 'EN')  # Default to English
        st.markdown("<h2>🌧️ Rainfall Anomaly </h2>",
                    unsafe_allow_html=True)

        if lang == "EN":
            st.markdown(
                """
                <div style='background-color:#d9f0ff; padding:20px; border-radius:12px; border-left: 8px solid #0078d7; color:black; '>
                <p><b>Rainfall anomaly</b> means how much the rainfall is different from the normal rainfall.</p>
                <ul>
                  <li>📈 <b>Positive anomaly</b> → More rain than usual.  
                  ➤ Farmers can plan <b>water management</b> and grow <b>rice, sugarcane, or jute</b>.</li>
                  <li>📉 <b>Negative anomaly</b> → Less rain than usual.  
                  ➤ Farmers should <b>save water</b> and prefer <b>millets, pulses, or oilseeds</b>.</li>
                </ul>
                <p>This helps farmers to plan <b>crop selection, irrigation, and fertilizer use</b> according to the rainfall pattern.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:  # Hindi
            st.markdown(
                """
                <div style='background-color:#d9f0ff; padding:20px; border-radius:12px; border-left: 8px solid #0078d7; color:black; '>
                <p><b>रेनफॉल एनॉमली</b> का मतलब है – इस बार की बारिश <b>सामान्य से कितनी अलग</b> है।</p>
                <ul>
                  <li>📈 <b>पॉज़िटिव एनॉमली</b> → सामान्य से ज़्यादा बारिश।  
                  ➤ किसान <b>पानी निकासी</b> की तैयारी करें और <b>धान, गन्ना या जूट</b> जैसी फसलें लगाएँ।</li>
                  <li>📉 <b>नेगेटिव एनॉमली</b> → सामान्य से कम बारिश।  
                  ➤ किसान <b>पानी बचाएँ</b> और <b>बाजरा, दालें या तिलहन</b> जैसी फसलें लगाएँ।</li>
                </ul>
                <p>इससे किसान <b>फसल, सिंचाई और खाद</b> की योजना मौसम के हिसाब से बना सकते हैं।</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def render_crop_risk_info():
        lang = st.session_state.get('lang', 'EN')  # Default to English
        st.markdown("<h2 style='text-align:center;'>📊 Top Crops — Risk Index</h2>", unsafe_allow_html=True)
        # Description box
        if lang == "EN":
            st.markdown(
                """
                <div style='background-color:#fff1b8; padding:20px; border-radius:12px; border-left: 8px solid #ff8c00; color:black; '>
                <p>This chart shows the <b>Risk Index</b> for the top crops based on demo data.</p>
                <ul style='text-align:left; display:inline-block;'>
                    <li>🌾 Higher risk → Crop may be more affected by weather or pests.</li>
                    <li>🌾 Lower risk → Crop is more stable and less affected.</li>
                </ul>
                <p>Farmers can use this information to <b>plan crop selection</b> and <b>risk management</b>.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:  # Hindi
            st.markdown(
                """
                <div style='background-color:#fff1b8; padding:20px; border-radius:12px; border-left: 8px solid #ff8c00; color:black;'>
                <p>यह चार्ट <b>टॉप फसलों के रिस्क इंडेक्स</b> को दिखाता है (डेमो डेटा के आधार पर)।</p>
                <ul style='text-align:left; display:inline-block;'>
                    <li>🌾 उच्च रिस्क → फसल मौसम या कीटों से अधिक प्रभावित हो सकती है।</li>
                    <li>🌾 कम रिस्क → फसल अधिक स्थिर और कम प्रभावित।</li>
                </ul>
                <p>किसान इस जानकारी का उपयोग करके <b>फसल चयन</b> और <b>रिस्क प्रबंधन</b> कर सकते हैं।</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Render the info boxes in the second row
    with left:
        render_rainfall_anomaly_info()

    with right:
        render_crop_risk_info()