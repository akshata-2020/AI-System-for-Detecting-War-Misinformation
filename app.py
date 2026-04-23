import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
from utils import *

st.set_page_config(page_title="Conflict Intelligence System", layout="wide")

# 🌍 SIDEBAR
st.sidebar.title("🌍 Navigation")

page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "🔍 Analysis",
    "📊 Dashboard",
    "🚨 Alerts"
])

# 📰 FETCH NEWS
def fetch_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "war OR attack OR conflict",
        "apiKey": "41cfe961c15f468797932f807be6c561"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    news = []

    for article in data.get("articles", [])[:5]:
        news.append({
            "text": article.get("title", ""),
            "source": article.get("source", {}).get("name", "Unknown")
        })

    return news

# 📂 LOAD HISTORY
try:
    with open("data/news_history.json", "r") as f:
        history = json.load(f)
except:
    history = []

# 🏠 HOME
if page == "🏠 Home":
    st.title("🌍 AI Conflict Intelligence System")
    st.write("Real-time conflict monitoring system")

# 🔍 ANALYSIS (🔥 ALL NEW FEATURES HERE)
elif page == "🔍 Analysis":

    st.header("🔍 Advanced News Analysis")

    user_input = st.text_area("Enter News Text")

    if st.button("Analyze") and user_input.strip() != "":# 🧠 FAKE NEWS DETECTION
        text = preprocess(user_input)

        # 🔥 EARLY WARNING SCORE
        risk, breakdown = advanced_risk_score(text)

        # 🎯 EVENT TYPE
        event = classify_event(text)

        # 🚨 ALERT
        alert = generate_alert(risk)

        # 🧾 SUMMARY
        summary = summarize(user_input)

        

        # 🧬 SENTIMENT + INTENSITY
        sentiment, intensity, _ = sentiment_intensity(text)

        # 🌍 LOCATION + GEO IMPACT
        country = detect_country(text)
        impact = geo_impact(country)
        fake_result = fake_news_detector(text)

        # SAVE WITH TIMESTAMP
        result = {
            "text": text,
            "risk": risk,
            "event": event,
            "time": str(datetime.now())
        }

        history.append(result)

        with open("data/news_history.json", "w") as f:
            json.dump(history, f)

        # ✅ OUTPUT SECTION
        st.subheader("📊 Result")

        st.write("🔥 Conflict Escalation Score:", risk)
        st.write("🎯 Event Type:", event)
        st.write("🚨 Alert:", alert)
        st.write("🧾 Summary:", summary)

        st.write("🧬 Sentiment:", sentiment)
        st.write("⚡ Intensity:", intensity)

        st.write("🌍 Location:", country)
        st.write("🌐 Geo Impact:", impact)
        
        st.subheader("📰 Fake News Detection")
        st.write("Result:", fake_result)

        if "Fake" in fake_result:
            st.error(fake_result)
        elif "Real" in fake_result:
            st.success(fake_result)
        else:
            st.warning(fake_result)

        # 🧠 EXPLAINABLE AI
        st.subheader("🧠 Explainable AI")
        for k, v in breakdown.items():
            st.write(f"{k} → +{v}")

# 📊 DASHBOARD (ALL ADVANCED VISUALS)
elif page == "📊 Dashboard":

    st.header("📊 Conflict Dashboard")

    if history:

        # 📈 TREND
        st.subheader("📈 Trend Analysis")
        st.write(trend_analysis(history))

        # 🧠 CORRELATION
        st.subheader("🧠 Multi-News Correlation")
        st.write(check_correlation(history))

        # 📅 TIMELINE
        st.subheader("📅 Conflict Timeline")
        for h in history[-10:]:
            st.write(f"{h['time']} → {h['event']} (Risk {h['risk']})")

        # 🚨 ANOMALY DETECTION
        if len(history) > 10:
            recent = history[-10:]
            high = sum(1 for h in recent if h["risk"] > 70)

            if high > 6:
                st.error("🚨 Sudden Conflict Spike Detected")

        # 🌍 MAP
        st.subheader("🌍 Conflict Map")

        map_data = []

        for h in history:
            if "india" in h["text"]:
                map_data.append([20.59, 78.96])
            elif "russia" in h["text"]:
                map_data.append([61.52, 105.31])
            elif "ukraine" in h["text"]:
                map_data.append([48.37, 31.16])

        if map_data:
            df = pd.DataFrame(map_data, columns=["lat", "lon"])
            st.map(df)

    else:
        st.write("No data yet")

# 🚨 ALERTS (REAL-TIME SYSTEM)
elif page == "🚨 Alerts":

    st.header("🚨 Real-Time Conflict Alerts")

    news = fetch_news()

    if news:
        for n in news:
            text = preprocess(n["text"])

            # 🔥 USE ADVANCED SCORE
            risk, _ = advanced_risk_score(text)

            alert = generate_alert(risk)

            trust = source_trust(n["source"])

            st.write(f"{alert} → {n['text']}")
            st.write(f"🔥 Risk: {risk} | 🕵️ Trust: {trust}%")

    else:
        st.write("No live news")

# 🔄 AUTO REFRESH
import time
# time.sleep(10)
# st.rerun()

def fake_news_detector(text):
    fake_words = ["rumor", "unconfirmed", "fake", "viral", "whatsapp forward"]
    real_words = ["official", "confirmed", "government", "reuters", "bbc"]

    score = 0

    for word in fake_words:
        if word in text:
            score -= 1

    for word in real_words:
        if word in text:
            score += 1

    if score >= 1:
        return "✅ Likely Real"
    elif score <= -1:
        return "❌ Likely Fake"
    else:
        return "⚠️ Uncertain"
