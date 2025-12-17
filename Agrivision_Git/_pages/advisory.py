import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def render_advisory():
    # Get current language
    current_lang = st.session_state.get('lang', 'EN')

    # Bilingual text dictionary
    TEXT = {
        'header_title': {
            'EN': "🌱 Smart Crop Advisory",
            'HI': "🌱 स्मार्ट फसल सलाह"
        },
        'header_subtitle': {
            'EN': "Your Personal Farming Assistant 🚜",
            'HI': "आपका व्यक्तिगत खेती सहायक 🚜"
        },
        'header_description': {
            'EN': "Get easy-to-understand, visual guidance for better crop management",
            'HI': "बेहतर फसल प्रबंधन के लिए आसानी से समझ में आने वाली, दृश्य मार्गदर्शन प्राप्त करें"
        },
        'quick_start': {
            'EN': "🎯 Quick Start - Choose Your Crop & Soil",
            'HI': "🎯 त्वरित प्रारंभ - अपनी फसल और मिट्टी चुनें"
        },
        'select_crop': {
            'EN': "**Select Your Crop**",
            'HI': "**अपनी फसल चुनें**"
        },
        'select_soil': {
            'EN': "**Soil Type**",
            'HI': "**मिट्टी का प्रकार**"
        },
        'select_region': {
            'EN': "**Your Region**",
            'HI': "**आपका क्षेत्र**"
        },
        'crop_journey': {
            'EN': "📊 Your Crop's Journey",
            'HI': "📊 आपकी फसल की यात्रा"
        },
        'growth_stage': {
            'EN': "**Where is your crop right now?**",
            'HI': "**आपकी फसल अभी कहाँ है?**"
        },
        'days_planted': {
            'EN': "📅 Days Planted",
            'HI': "📅 लगाए गए दिन"
        },
        'days_harvest': {
            'EN': "⏳ Days to Harvest",
            'HI': "⏳ कटाई तक दिन"
        },
        'crop_health': {
            'EN': "💚 Crop Health",
            'HI': "💚 फसल स्वास्थ्य"
        },
        'soil_temp': {
            'EN': "🌡️ Soil Temp",
            'HI': "🌡️ मिट्टी का तापमान"
        },
        'farming_guide': {
            'EN': "📚 Your Farming Guide",
            'HI': "📚 आपका खेती मार्गदर्शक"
        },
        'basic_guide': {
            'EN': "🎯 Basic Guide",
            'HI': "🎯 बुनियादी मार्गदर्शन"
        },
        'water_needs': {
            'EN': "💧 Water Needs",
            'HI': "💧 पानी की जरूरत"
        },
        'plant_food': {
            'EN': "🌱 Food for Plants",
            'HI': "🌱 पौधों के लिए भोजन"
        },
        'soil_care': {
            'EN': "🏞️ Soil Care",
            'HI': "🏞️ मिट्टी की देखभाल"
        },
        'success_tips': {
            'EN': "💡 Top 3 Success Tips",
            'HI': "💡 शीर्ष 3 सफलता टिप्स"
        },
        'save_plan': {
            'EN': "📥 Save Your Plan",
            'HI': "📥 अपनी योजना सहेजें"
        },
        'save_pdf': {
            'EN': "📄 Save as PDF",
            'HI': "📄 PDF के रूप में सहेजें"
        },
        'pro_tip': {
            'EN': "💡 **Pro Tip:** Take screenshots of this page to save your personalized farming guide!",
            'HI': "💡 **प्रो टिप:** अपनी व्यक्तिगत खेती मार्गदर्शक को सहेजने के लिए इस पृष्ठ की स्क्रीनशॉट लें!"
        },
        'happy_farming': {
            'EN': "🌱 Happy Farming! 🚜",
            'HI': "🌱 सफल खेती! 🚜"
        },
        'footer_quote': {
            'EN': "Remember: Good farmers grow food, great farmers grow soil!",
            'HI': "याद रखें: अच्छे किसान भोजन उगाते हैं, महान किसान मिट्टी उगाते हैं!"
        }
    }

    def T(key):
        return TEXT.get(key, {}).get(current_lang, key)

    # Custom CSS with vibrant colors and animations
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .crop-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 15px 0px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .soil-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin: 10px 0px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .water-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin: 10px 0px;
    }
    .fert-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin: 10px 0px;
    }
    .progress-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 20px;
        margin: 10px 0px;
    }
    .icon-box {
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 15px;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: rgba(255,255,255,0.9);
        padding: 15px;
        border-radius: 15px;
        margin: 8px 0px;
        text-align: center;
    }
    .description-box {
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #0ea5e9;
        margin: 10px 0;
        font-size: 14px;
        color: #0369a1;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Beautiful Header
    st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5rem;">{T('header_title')}</h1>
        <p style="margin:10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">{T('header_subtitle')}</p>
        <p style="margin:5px 0 0 0; font-size: 1rem; opacity: 0.8;">{T('header_description')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Start Guide with Icons
    st.markdown(f"### {T('quick_start')}")

    # Visual selection section
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 🌾")
        crop_type = st.selectbox(
            T('select_crop'),
            ["Wheat", "Rice", "Maize", "Cotton", "Soybean", "Sugarcane"],
            help="Choose what you want to grow" if current_lang == 'EN' else "चुनें कि आप क्या उगाना चाहते हैं"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 🏞️")
        soil_type = st.selectbox(
            T('select_soil'),
            ["Loamy", "Sandy", "Clay", "Silt", "Peaty"],
            help="What type of soil do you have?" if current_lang == 'EN' else "आपके पास किस प्रकार की मिट्टी है?"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="icon-box">', unsafe_allow_html=True)
        st.markdown("### 🗺️")
        region = st.selectbox(
            T('select_region'),
            ["North Zone", "South Zone", "East Zone", "West Zone", "Central Zone"],
            help="Where is your farm located?" if current_lang == 'EN' else "आपका खेत कहाँ स्थित है?"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual Progress Tracker
    st.markdown(f"### {T('crop_journey')}")

    # Growth stage visualization
    growth_stages_en = ["🌱 Planning", "🪴 Sowing", "🌿 Growing", "🌸 Flowering", "🍎 Harvest"]
    growth_stages_hi = ["🌱 योजना", "🪴 बुवाई", "🌿 बढ़ रहा", "🌸 फूल आना", "🍎 कटाई"]

    growth_stages = growth_stages_en if current_lang == 'EN' else growth_stages_hi

    current_stage = st.select_slider(
        T('growth_stage'),
        options=growth_stages,
        value=growth_stages[2]
    )

    # Show progress bar
    stage_progress = (growth_stages.index(current_stage) + 1) / len(growth_stages)
    st.progress(stage_progress)
    st.caption(f"{'Progress' if current_lang == 'EN' else 'प्रगति'}: {int(stage_progress * 100)}% complete")

    # Colorful metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(T('days_planted'), "45")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(T('days_harvest'), "75")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(T('crop_health'), "Good" if current_lang == 'EN' else "अच्छा")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric(T('soil_temp'), "24°C")
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Information in Colorful Tabs
    st.markdown(f"### {T('farming_guide')}")

    # Bilingual tab labels
    tab_labels_en = [T('basic_guide'), T('water_needs'), T('plant_food'), T('soil_care')]
    tab_labels_hi = [T('basic_guide'), T('water_needs'), T('plant_food'), T('soil_care')]

    tab_labels = tab_labels_en if current_lang == 'EN' else tab_labels_hi

    tab1, tab2, tab3, tab4 = st.tabs(tab_labels)

    with tab1:
        st.markdown(f'<div class="crop-card">', unsafe_allow_html=True)

        # Bilingual crop information
        CROP_INFO = {
            'growing_calendar': {
                'EN': f"### {crop_type} Growing Calendar",
                'HI': f"### {crop_type} उगाने का कैलेंडर"
            },
            'sow_time': {
                'EN': "#### 🌱 Sow Time",
                'HI': "#### 🌱 बुवाई का समय"
            },
            'grow_time': {
                'EN': "#### 🌿 Grow Time",
                'HI': "#### 🌿 बढ़ने का समय"
            },
            'harvest_time': {
                'EN': "#### 🎉 Harvest Time",
                'HI': "#### 🎉 कटाई का समय"
            },
            'easy_steps': {
                'EN': "### 👣 Easy Steps to Follow:",
                'HI': "### 👣 अनुसरण करने के लिए आसान चरण:"
            }
        }

        def C(key):
            return CROP_INFO.get(key, {}).get(current_lang, key)

        st.markdown(C('growing_calendar'))

        # Timeline data with bilingual months
        timeline_data = {
            "Wheat": {
                "sow": "Nov-Dec" if current_lang == 'EN' else "नवंबर-दिसंबर",
                "grow": "Dec-Feb" if current_lang == 'EN' else "दिसंबर-फरवरी",
                "harvest": "Mar-Apr" if current_lang == 'EN' else "मार्च-अप्रैल"
            },
            "Rice": {
                "sow": "Jun-Jul" if current_lang == 'EN' else "जून-जुलाई",
                "grow": "Jul-Sep" if current_lang == 'EN' else "जुलाई-सितंबर",
                "harvest": "Oct-Nov" if current_lang == 'EN' else "अक्टूबर-नवंबर"
            },
            "Maize": {
                "sow": "Jun-Jul" if current_lang == 'EN' else "जून-जुलाई",
                "grow": "Jul-Aug" if current_lang == 'EN' else "जुलाई-अगस्त",
                "harvest": "Sep-Oct" if current_lang == 'EN' else "सितंबर-अक्टूबर"
            },
        }

        timeline = timeline_data.get(crop_type, timeline_data["Wheat"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(C('sow_time'))
            st.info(f"**{timeline['sow']}**")
        with col2:
            st.markdown(C('grow_time'))
            st.warning(f"**{timeline['grow']}**")
        with col3:
            st.markdown(C('harvest_time'))
            st.success(f"**{timeline['harvest']}**")

        # Simple steps in bilingual
        st.markdown(C('easy_steps'))

        simple_steps_en = {
            "Wheat": [
                "🛌 Prepare bed in October",
                "🌱 Sow seeds in Nov-Dec",
                "💧 Water 4-5 times",
                "🍃 Add plant food",
                "✂️ Harvest in March"
            ],
            "Rice": [
                "💦 Flood field in May",
                "🌱 Plant baby plants in Jun-Jul",
                "💧 Keep 2-3 inch water",
                "🌾 Add special food",
                "🎑 Harvest in October"
            ],
            "Maize": [
                "🛌 Prepare land in May",
                "🌱 Sow seeds in June",
                "💧 Water every 10 days",
                "🌿 Remove weeds",
                "🌽 Harvest in September"
            ]
        }

        simple_steps_hi = {
            "Wheat": [
                "🛌 अक्टूबर में बिस्तर तैयार करें",
                "🌱 नवंबर-दिसंबर में बीज बोएं",
                "💧 4-5 बार पानी दें",
                "🍃 पौधे का भोजन डालें",
                "✂️ मार्च में कटाई करें"
            ],
            "Rice": [
                "💦 मई में खेत में पानी भरें",
                "🌱 जून-जुलाई में पौधे लगाएं",
                "💧 2-3 इंच पानी रखें",
                "🌾 विशेष भोजन डालें",
                "🎑 अक्टूबर में कटाई करें"
            ],
            "Maize": [
                "🛌 मई में जमीन तैयार करें",
                "🌱 जून में बीज बोएं",
                "💧 हर 10 दिन में पानी दें",
                "🌿 खरपतवार हटाएं",
                "🌽 सितंबर में कटाई करें"
            ]
        }

        simple_steps = simple_steps_en if current_lang == 'EN' else simple_steps_hi
        steps = simple_steps.get(crop_type, simple_steps["Wheat"])

        for step in steps:
            st.markdown(f"- {step}")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="water-card">', unsafe_allow_html=True)

        # Bilingual water schedule
        WATER_TEXT = {
            'water_schedule': {
                'EN': "### 💧 Water Schedule Made Easy",
                'HI': "### 💧 पानी का समय सारणी आसान बनाया"
            },
            'when_to_water': {
                'EN': "#### 💦 When to Water:",
                'HI': "#### 💦 कब पानी दें:"
            },
            'water_calculator': {
                'EN': "#### 🧮 Water Calculator",
                'HI': "#### 🧮 पानी कैलकुलेटर"
            },
            'field_size': {
                'EN': "Your field size (acres)",
                'HI': "आपके खेत का आकार (एकड़)"
            },
            'total_water': {
                'EN': "Total Water Needed",
                'HI': "कुल पानी की आवश्यकता"
            }
        }

        def W(key):
            return WATER_TEXT.get(key, {}).get(current_lang, key)

        st.markdown(W('water_schedule'))
        st.markdown(W('when_to_water'))

        water_schedule_en = {
            "Wheat": ["🚰 After planting", "🚰 3 weeks later", "🚰 When flowering", "🚰 When grains form"],
            "Rice": ["🌊 Keep field flooded", "🌊 Change water monthly", "🌊 Dry before harvest"],
            "Maize": ["💧 After planting", "💧 When knee-high", "💧 When making flowers", "💧 When making corn"],
        }

        water_schedule_hi = {
            "Wheat": ["🚰 रोपण के बाद", "🚰 3 सप्ताह बाद", "🚰 फूल आने पर", "🚰 अनाज बनने पर"],
            "Rice": ["🌊 खेत में पानी भरा रखें", "🌊 महीने में एक बार पानी बदलें", "🌊 कटाई से पहले सुखाएं"],
            "Maize": ["💧 रोपण के बाद", "💧 घुटने तक ऊंचा होने पर", "💧 फूल बनने पर", "💧 मक्का बनने पर"],
        }

        water_schedule = water_schedule_en if current_lang == 'EN' else water_schedule_hi
        schedule = water_schedule.get(crop_type, water_schedule["Wheat"])

        for i, when in enumerate(schedule, 1):
            st.markdown(f"{i}. {when}")

        # Simple water calculator
        st.markdown("---")
        st.markdown(W('water_calculator'))

        col1, col2 = st.columns(2)
        with col1:
            field_size = st.slider(W('field_size'), 1, 20, 5)
            st.metric("📏 Field Size" if current_lang == 'EN' else "📏 खेत का आकार", f"{field_size} acres")

        with col2:
            water_needs = {
                "Wheat": 500, "Rice": 1200, "Maize": 600,
                "Cotton": 800, "Soybean": 500, "Sugarcane": 1500
            }
            total_water = water_needs.get(crop_type, 500) * field_size

            st.metric(W('total_water'), f"{total_water:,} liters")
            st.caption("For entire growing season" if current_lang == 'EN' else "पूरे बढ़ते मौसम के लिए")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown(f'<div class="fert-card">', unsafe_allow_html=True)

        # Bilingual fertilizer information
        FERT_TEXT = {
            'plant_food_guide': {
                'EN': "### 🌱 Plant Food Guide",
                'HI': "### 🌱 पौधे के भोजन का मार्गदर्शक"
            },
            'what_to_feed': {
                'EN': "#### 🥪 What to Feed Your Plants:",
                'HI': "#### 🥪 अपने पौधों को क्या खिलाएं:"
            },
            'green_food': {
                'EN': "##### 🍃 Green Food",
                'HI': "##### 🍃 हरा भोजन"
            },
            'root_food': {
                'EN': "##### 🏔️ Root Food",
                'HI': "##### 🏔️ जड़ का भोजन"
            },
            'strong_food': {
                'EN': "##### 💪 Strong Food",
                'HI': "##### 💪 मजबूत भोजन"
            },
            'when_to_add': {
                'EN': "#### 🕒 When to Add Food:",
                'HI': "#### 🕒 भोजन कब डालें:"
            }
        }

        def F(key):
            return FERT_TEXT.get(key, {}).get(current_lang, key)

        st.markdown(F('plant_food_guide'))
        st.markdown(F('what_to_feed'))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(F('green_food'))
            st.metric("Nitrogen", "120 kg")
            st.caption("Makes leaves green" if current_lang == 'EN' else "पत्तियों को हरा बनाता है")

        with col2:
            st.markdown(F('root_food'))
            st.metric("Phosphorus", "60 kg")
            st.caption("Helps roots grow" if current_lang == 'EN' else "जड़ों को बढ़ने में मदद करता है")

        with col3:
            st.markdown(F('strong_food'))
            st.metric("Potassium", "40 kg")
            st.caption("Makes plants strong" if current_lang == 'EN' else "पौधों को मजबूत बनाता है")

        # Simple application guide
        st.markdown(F('when_to_add'))

        feed_times_en = {
            "Wheat": [
                "📅 At planting: 50% of food",
                "📅 After 1 month: 25% more",
                "📅 After 2 months: 25% rest"
            ],
            "Rice": [
                "📅 Before planting: 50% of food",
                "📅 After 3 weeks: 25% more",
                "📅 After 6 weeks: 25% rest"
            ]
        }

        feed_times_hi = {
            "Wheat": [
                "📅 रोपण पर: 50% भोजन",
                "📅 1 महीने बाद: 25% और",
                "📅 2 महीने बाद: 25% बाकी"
            ],
            "Rice": [
                "📅 रोपण से पहले: 50% भोजन",
                "📅 3 सप्ताह बाद: 25% और",
                "📅 6 सप्ताह बाद: 25% बाकी"
            ]
        }

        feed_times = feed_times_en if current_lang == 'EN' else feed_times_hi
        feed_schedule = feed_times.get(crop_type, feed_times["Wheat"])

        for feed_time in feed_schedule:
            st.markdown(f"- {feed_time}")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown(f'<div class="soil-card">', unsafe_allow_html=True)

        # Bilingual soil care information
        SOIL_TEXT = {
            'soil_care': {
                'EN': f"### 🏞️ Your {soil_type} Soil Care",
                'HI': f"### 🏞️ आपकी {soil_type} मिट्टी की देखभाल"
            },
            'soil_health_check': {
                'EN': "#### 🩺 Soil Health Check",
                'HI': "#### 🩺 मिट्टी स्वास्थ्य जांच"
            }
        }

        def S(key):
            return SOIL_TEXT.get(key, {}).get(current_lang, key)

        st.markdown(S('soil_care'))

        # Soil type visualization with bilingual descriptions
        soil_icons_en = {
            "Loamy": "⭐ Gold Soil!",
            "Sandy": "🏖️ Sandy Soil",
            "Clay": "🧱 Clay Soil",
            "Silt": "🌊 Silt Soil",
            "Peaty": "🍂 Rich Soil"
        }

        soil_icons_hi = {
            "Loamy": "⭐ सोने जैसी मिट्टी!",
            "Sandy": "🏖️ रेतीली मिट्टी",
            "Clay": "🧱 चिकनी मिट्टी",
            "Silt": "🌊 गाद मिट्टी",
            "Peaty": "🍂 समृद्ध मिट्टी"
        }

        soil_icons = soil_icons_en if current_lang == 'EN' else soil_icons_hi
        st.markdown(f"#### {soil_icons.get(soil_type, '⭐')}")

        # Simple soil tips in bilingual
        soil_tips_en = {
            "Loamy": [
                "✅ You have the best soil!",
                "💧 Water normally",
                "🌿 Add compost once a year",
                "🔄 Change crops each season"
            ],
            "Sandy": [
                "⚠️ Soil dries quickly",
                "💧 Water little but often",
                "🍂 Add lots of compost",
                "🌱 Use mulch to keep wet"
            ],
            "Clay": [
                "⚠️ Soil gets waterlogged",
                "💧 Water less frequently",
                "🏗️ Add sand for drainage",
                "🛌 Make raised beds"
            ]
        }

        soil_tips_hi = {
            "Loamy": [
                "✅ आपके पास सबसे अच्छी मिट्टी है!",
                "💧 सामान्य रूप से पानी दें",
                "🌿 साल में एक बार कम्पोस्ट डालें",
                "🔄 हर मौसम में फसलें बदलें"
            ],
            "Sandy": [
                "⚠️ मिट्टी जल्दी सूख जाती है",
                "💧 कम लेकिन अक्सर पानी दें",
                "🍂 बहुत सारा कम्पोस्ट डालें",
                "🌱 गीला रखने के लिए मल्च का उपयोग करें"
            ],
            "Clay": [
                "⚠️ मिट्टी में पानी भर जाता है",
                "💧 कम बार पानी दें",
                "🏗️ जल निकासी के लिए रेत डालें",
                "🛌 उठे हुए बिस्तर बनाएं"
            ]
        }

        soil_tips = soil_tips_en if current_lang == 'EN' else soil_tips_hi
        tips = soil_tips.get(soil_type, soil_tips["Loamy"])

        for tip in tips:
            st.markdown(f"- {tip}")

        # Soil health check
        st.markdown("---")
        st.markdown(S('soil_health_check'))

        last_check = st.date_input(
            "When did you last test soil?" if current_lang == 'EN' else "आपने आखिरी बार मिट्टी की जांच कब की थी?",
            datetime.now() - timedelta(days=180)
        )
        days_ago = (datetime.now().date() - last_check).days

        if days_ago > 365:
            st.error(
                "🚨 Test your soil now! It's been over a year." if current_lang == 'EN' else "🚨 अब अपनी मिट्टी की जांच करें! एक साल से अधिक हो गया है।")
        elif days_ago > 180:
            st.warning("⚠️ Time to test soil soon" if current_lang == 'EN' else "⚠️ जल्द ही मिट्टी की जांच का समय")
        else:
            st.success("✅ Your soil test is recent!" if current_lang == 'EN' else "✅ आपकी मिट्टी की जांच हाल की है!")

        st.markdown('</div>', unsafe_allow_html=True)

    # Success Tips Section
    st.markdown(f"### {T('success_tips')}")

    success_tips_en = {
        "Wheat": [
            "🎯 Plant at right time (Nov-Dec)",
            "💧 Water at flowering stage",
            "🌾 Harvest when grains are hard"
        ],
        "Rice": [
            "🎯 Keep field flooded",
            "🌱 Use healthy baby plants",
            "🕒 Harvest when 80% grains yellow"
        ],
        "Maize": [
            "🎯 Plant in rows",
            "💧 Water when making flowers",
            "🌽 Harvest when husks are dry"
        ]
    }

    success_tips_hi = {
        "Wheat": [
            "🎯 सही समय पर लगाएं (नवंबर-दिसंबर)",
            "💧 फूल आने के चरण में पानी दें",
            "🌾 जब अनाज सख्त हों तो कटाई करें"
        ],
        "Rice": [
            "🎯 खेत में पानी भरा रखें",
            "🌱 स्वस्थ छोटे पौधों का उपयोग करें",
            "🕒 जब 80% अनाज पीले हों तो कटाई करें"
        ],
        "Maize": [
            "🎯 पंक्तियों में लगाएं",
            "💧 फूल बनते समय पानी दें",
            "🌽 जब भूसी सूख जाए तो कटाई करें"
        ]
    }

    success_tips = success_tips_en if current_lang == 'EN' else success_tips_hi
    tips = success_tips.get(crop_type, success_tips["Wheat"])

    col1, col2, col3 = st.columns(3)
    for i, tip in enumerate(tips):
        with [col1, col2, col3][i]:
            st.markdown(f'<div class="icon-box">', unsafe_allow_html=True)
            st.markdown(f"**{'Tip' if current_lang == 'EN' else 'टिप'} {i + 1}**")
            st.markdown(f"{tip}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Download Section
    st.markdown("---")
    st.markdown(f"### {T('save_plan')}")

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button(T('save_pdf'), type="primary", use_container_width=True):
            st.balloons()
            st.success(
                "✅ Your farming plan is ready! (PDF feature coming soon)" if current_lang == 'EN' else "✅ आपकी खेती की योजना तैयार है! (PDF सुविधा जल्द आ रही है)")

    with col2:
        st.info(T('pro_tip'))

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: gray;'>
        <p>{T('happy_farming')}</p>
        <p>{T('footer_quote')}</p>
    </div>
    """, unsafe_allow_html=True)


# Helper function for simple explanations
def explain_term(term, lang='EN'):
    """Simple explanations for farming terms in bilingual"""
    explanations_en = {
        "Nitrogen": "Green food for leaves",
        "Phosphorus": "Root food for strong roots",
        "Potassium": "Strong food for healthy plants",
        "pH": "How sour or sweet your soil is",
        "Irrigation": "Giving water to plants"
    }

    explanations_hi = {
        "Nitrogen": "पत्तियों के लिए हरा भोजन",
        "Phosphorus": "मजबूत जड़ों के लिए जड़ का भोजन",
        "Potassium": "स्वस्थ पौधों के लिए मजबूत भोजन",
        "pH": "आपकी मिट्टी कितनी खट्टी या मीठी है",
        "Irrigation": "पौधों को पानी देना"
    }

    explanations = explanations_en if lang == 'EN' else explanations_hi
    return explanations.get(term, term)