import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import ui
st.set_page_config(page_title="Email & SMS Spam Classifier",page_icon="📩", layout="centered")


# NLP
@st.cache_resource
def setup_nltk():
    for pkg in ["punkt", "punkt_tab", "stopwords"]:
        nltk.download(pkg, quiet=True)
    return set(stopwords.words("english"))


STOP_WORDS = setup_nltk()
ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        if i not in STOP_WORDS and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@st.cache_resource
def load_model():
    tfidf = pickle.load(open("vectorizer.pkl", "rb"))
    model = pickle.load(open("model.pkl", "rb"))
    return tfidf, model


tfidf, model = load_model()

# Page
ui.load_css()
ui.render_header()

input_sms = st.text_area("Enter the message", height=170, placeholder="Paste your email or SMS here...")

if st.button("Predict", type="primary"):
    if not input_sms.strip():
        st.warning("Please enter a message first.")
    else:
        # 1. preprocess
        transform_sms = transform_text(input_sms)
        # 2. vectorize
        vector_input = tfidf.transform([transform_sms])
        # 3. predict
        result = model.predict(vector_input)[0]

        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = float(model.predict_proba(vector_input)[0].max()) * 100

        # 4. display
        ui.render_result(result == 1, confidence)

ui.render_footer()
