# utils/helpers.py

TEXT = {
    "tagline": {
        "EN": "AI-powered climate insights & sustainable farming.",
        "HI": "एआई-संचालित जलवायु जानकारी व सतत खेती।",
    },
    "hero_cta": {"EN": "Get Started", "HI": "शुरू करें"},
    "farmers": {"EN": "Farmers Impacted", "HI": "लाभान्वित किसान"},
    "accuracy": {"EN": "Advisory Accuracy", "HI": "सलाह की सटीकता"},
    "coverage": {"EN": "State Coverage", "HI": "राज्य कवरेज"},
}

def T(key: str, lang: str):
    return TEXT.get(key, {}).get(lang, key)