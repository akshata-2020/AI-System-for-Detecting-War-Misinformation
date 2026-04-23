import re
from datetime import datetime

# 🔥 KEYWORDS
HIGH_RISK = ["missile", "nuclear", "invasion", "bomb"]
MEDIUM_RISK = ["attack", "battle", "army", "conflict"]
LOW_RISK = ["tension", "protest", "discussion"]

EVENT_TYPES = {
    "Cyber Attack": ["cyber", "hack"],
    "Terrorism": ["blast", "terror"],
    "War": ["missile", "army", "attack"],
    "Political": ["government", "election"]
}

# 🧠 CLEAN TEXT
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

# 🚨 RISK SCORE
def calculate_risk(text):
    score = 0
    words = text.split()

    for word in words:
        if word in HIGH_RISK:
            score += 20
        elif word in MEDIUM_RISK:
            score += 10
        elif word in LOW_RISK:
            score += 5

    return min(score, 100)

# 🎯 EVENT TYPE
def classify_event(text):
    for event, keywords in EVENT_TYPES.items():
        if any(word in text for word in keywords):
            return event
    return "General"

# 📊 TREND ANALYSIS
def trend_analysis(history):
    if len(history) == 0:
        return "No data"

    high_count = sum(1 for h in history if h["risk"] > 70)

    if high_count > len(history) * 0.6:
        return "Increasing 📈"
    elif high_count < len(history) * 0.3:
        return "Decreasing 📉"
    else:
        return "Stable ➖"

# 🚨 ALERT GENERATION
def generate_alert(risk):
    if risk > 80:
        return "🔴 Critical Alert"
    elif risk > 50:
        return "🟡 Warning"
    else:
        return "🟢 Low Alert"

# 🧠 SIMPLE SUMMARY
def summarize(text):
    sentences = text.split('.')
    return sentences[0][:150]

# 🕵️ SOURCE TRUST
def source_trust(source):
    trusted = ["BBC", "CNN", "Reuters"]
    return 90 if source in trusted else 50

# 🧠 CORRELATION
def check_correlation(history):
    keywords = ["war", "attack", "missile"]

    count = 0
    for h in history:
        if any(k in h["text"] for k in keywords):
            count += 1

    if count > 5:
        return "⚠️ Escalation Pattern Detected"
    return "No strong pattern"

#------------------------
from textblob import TextBlob

# 🧠 SENTIMENT + INTENSITY
def sentiment_intensity(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1

    if polarity < -0.3:
        sentiment = "Negative"
        intensity = "High"
    elif polarity < 0:
        sentiment = "Slightly Negative"
        intensity = "Medium"
    else:
        sentiment = "Neutral/Positive"
        intensity = "Low"

    return sentiment, intensity, abs(polarity)

# 🚨 ADVANCED RISK SCORE (EARLY WARNING)
def advanced_risk_score(text):
    score = 0
    breakdown = {}

    words = text.split()

    for word in words:
        if word in ["missile", "nuclear"]:
            score += 40
            breakdown[word] = 40
        elif word in ["attack", "army"]:
            score += 30
            breakdown[word] = 30
        elif word in ["tension", "protest"]:
            score += 10
            breakdown[word] = 10

    sentiment, _, val = sentiment_intensity(text)
    sentiment_score = int(val * 20)

    score += sentiment_score
    breakdown["sentiment"] = sentiment_score

    return min(score, 100), breakdown

# 🌍 SIMPLE COUNTRY DETECTION
def detect_country(text):
    countries = ["india", "russia", "ukraine", "china", "usa"]
    for c in countries:
        if c in text:
            return c
    return "Unknown"

# 🌐 GEO IMPACT
def geo_impact(country):
    impact_map = {
        "india": "Pakistan, China",
        "russia": "Ukraine, Europe",
        "ukraine": "Russia, NATO",
        "china": "Taiwan, India",
        "usa": "Global Impact"
    }
    return impact_map.get(country, "General Impact")


def fake_news_detector(text):
    fake_words = ["rumor", "unconfirmed", "fake", "viral", "whatsapp"]
    real_words = ["official", "confirmed", "government", "reuters", "bbc"]

    score = 0

    for word in fake_words:
        if word in text.lower():
            score -= 1

    for word in real_words:
        if word in text.lower():
            score += 1

    if score >= 1:
        return "✅ Likely Real"
    elif score <= -1:
        return "❌ Likely Fake"
    else:
        return "⚠️ Uncertain"
