import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
from utils import *
import matplotlib.pyplot as plt

st.set_page_config(page_title="Conflict Intelligence System", layout="wide")


st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #00FFAA;
}
.stButton>button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
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

    st.markdown("### 📥 Input Sources: Text / File / URL/ Social")

# 📂 FILE UPLOAD
    uploaded_file = st.file_uploader("Upload News File (txt)")

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.write("📄 Uploaded Content Preview:")
        st.write(content[:200])
        user_input = content

# 🔗 URL INPUT (NEW FEATURE)
    link = st.text_input("Paste News URL")

    if link:
        if "instagram.com" in link:
            st.warning("⚠️ Instagram content cannot be fetched. Please paste the caption text.")
        else:
            try:
                from bs4 import BeautifulSoup

                page = requests.get(link)
                soup = BeautifulSoup(page.content, "html.parser")

                text_data = " ".join([p.text for p in soup.find_all("p")])

                st.write("📄 Extracted Content Preview:")
                st.write(text_data[:200])

                user_input = text_data

            except:
                st.error("Unable to fetch content from link")
        # 📱 SOCIAL MEDIA TEXT INPUT (OPTION 1)
    social_input = st.text_area("Paste Social Media Post")

    if social_input:
        user_input = social_input

    # 📌 SMALL LABEL (EXTRA FEATURE)
    st.caption("Supports news websites. Social media links require manual text input.")


    # 📂 FILE UPLOAD (NEW FEATURE)
    # uploaded_file = st.file_uploader("Upload News File (txt)")

    # if uploaded_file:
    #     content = uploaded_file.read().decode("utf-8")
    #     st.write("📄 Uploaded Content Preview:")
    #     st.write(content[:200])

    # 👉 Replace user input with file content
    # user_input = content

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
        # st.write("Result:", fake_result)

        if "Fake" in fake_result:
            st.error(fake_result)
        elif "Real" in fake_result:
            st.success(fake_result)
        else:
            st.warning(fake_result)
        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Risk Score", risk)
        col2.metric("🎯 Event", event)
        col3.metric("⚡ Intensity", intensity)

        # 🧠 EXPLAINABLE AI
        st.subheader("🧠 Explainable AI")
        for k, v in breakdown.items():
            st.write(f"{k} → +{v}")
        st.info(f"🧠 AI Insight: This event indicates {event} with {intensity} intensity and potential escalation risk.")

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

    risks = [h["risk"] for h in history]

    fig, ax = plt.subplots()
    ax.plot(risks)
    ax.set_title("Risk Trend Over Time")

    st.pyplot(fig)

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

# def fake_news_detector(text):
#     fake_words = ["rumor", "unconfirmed", "fake", "viral", "whatsapp forward"]
#     real_words = ["official", "confirmed", "government", "reuters", "bbc"]

#     score = 0

#     for word in fake_words:
#         if word in text:
#             score -= 1

#     for word in real_words:
#         if word in text:
#             score += 1

#     if score >= 1:
#         return "✅ Likely Real"
#     elif score <= -1:
#         return "❌ Likely Fake"
#     else:
#         return "⚠️ Uncertain"
