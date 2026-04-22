
import streamlit as st
import joblib

st.set_page_config(
    page_title="War Misinformation Detector",
    page_icon="🔍",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load('model/pipeline.pkl')

pipeline = load_model()

st.title("🔍 War News Misinformation Detector")
st.markdown("Enter a news headline to check if it shows signs of misinformation.")
st.markdown("---")

headline = st.text_input(
    "📰 News Headline",
    placeholder="e.g. Government confirms ceasefire agreement signed"
)

if st.button("Analyze", type="primary"):
    if not headline.strip():
        st.warning("Please enter a headline.")
    else:
        prediction = pipeline.predict([headline])[0]
        confidence = pipeline.predict_proba([headline])[0]

        fake_conf = confidence[0] * 100
        real_conf = confidence[1] * 100

        st.markdown("---")

        if prediction == 0:
            st.error(f"⚠️ Likely Misinformation — {fake_conf:.1f}% confidence")
        else:
            st.success(f"✅ Likely Credible — {real_conf:.1f}% confidence")

        st.markdown("### Confidence Breakdown")
        st.markdown("**Fake probability**")
        st.progress(fake_conf / 100)
        st.caption(f"{fake_conf:.1f}%")

        st.markdown("**Real probability**")
        st.progress(real_conf / 100)
        st.caption(f"{real_conf:.1f}%")

        st.markdown("---")
        st.caption("📚 Academic NLP project. Always verify news through trusted sources. 🔍✅")

with st.sidebar:
    st.markdown("### About")
    st.markdown("Built with scikit-learn + Streamlit")
    st.markdown("**Model:** Logistic Regression")
    st.markdown("**Features:** TF-IDF (10,000 features)")
    st.markdown("---")
    st.markdown("### Try These Examples")
    st.code("SHOCKING: Army destroys entire city overnight")
    st.code("UN confirms humanitarian corridor opened")
