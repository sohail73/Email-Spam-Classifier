from pathlib import Path
import streamlit as st


def load_css(file_name="style.css"):
    css = (Path(__file__).parent / file_name).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header():
    st.markdown(
        """<div class="title">Email &amp; SMS<br><span>Spam Classifier</span></div>
<div class="subtitle">Paste any message and find out in one click whether it is spam or not.</div>""",
        unsafe_allow_html=True,)


def render_result(is_spam, confidence=None):
    conf_html = ""
    if confidence is not None:
        conf_html = (
            f'<div class="conf">Model confidence: <b>{confidence:.1f}%</b>'
            f'<div class="bar"><div style="width:{confidence:.1f}%"></div></div></div>')

    if is_spam:
        css_class, icon, label = "spam", "&#10005;", "Spam"
        desc = "This message looks like spam. Avoid clicking any links in it."
    else:
        css_class, icon, label = "ham", "&#10003;", "Not Spam"
        desc = "This message looks safe."

    st.markdown(
        f'<div class="result {css_class}"><div class="icon">{icon}</div><div style="flex:1">'
        f'<p class="label">{label}</p><p class="desc">{desc}</p>{conf_html}</div></div>',
        unsafe_allow_html=True,)


def render_footer():
    st.markdown(
        """<div class="footer">
<div>Built by <b>Sohail Khan</b></div>
<div>
<a href="https://github.com/sohail73" target="_blank">GitHub</a>
<a href="https://www.linkedin.com/in/sohail-khan73/" target="_blank">LinkedIn</a>
</div>
</div>""",
        unsafe_allow_html=True,)
