import streamlit as st
import pandas as pd
from src.features import extract_features, explain_url
from src.model import load_model

st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="centered")
st.title("🛡️ PhishGuard AI")
st.subheader("Explainable phishing URL risk checker")
st.write("Enter a URL to estimate whether its URL structure resembles phishing links. The app does not open or visit the URL.")

url = st.text_input("Website URL", placeholder="https://example.com/login")
if st.button("Analyse URL", type="primary", disabled=not url.strip()):
    try:
        bundle = load_model()
        model = bundle["model"]
        row = pd.DataFrame([extract_features(url)])
        prediction = int(model.predict(row)[0])
        probability = model.predict_proba(row)[0]
        phishing_index = list(model.classes_).index(1)
        risk = float(probability[phishing_index])
        if prediction == 1:
            st.error(f"Potential phishing URL — estimated model score: {risk:.1%}")
        else:
            st.success(f"Lower-risk URL pattern — estimated model score: {risk:.1%}")
        st.progress(risk, text="Model-estimated phishing score")
        st.markdown("**Why you should inspect it**")
        for note in explain_url(url):
            st.write("• " + note)
        with st.expander("View extracted ML features"):
            st.dataframe(row.T.rename(columns={0: "Value"}), use_container_width=True)
        st.caption("This is a machine-learning estimate, not a security guarantee. Do not enter passwords on unfamiliar sites.")
    except FileNotFoundError as exc:
        st.warning(str(exc))
        st.code("python train.py")
    except Exception as exc:
        st.error(f"Could not analyse this input: {exc}")

st.divider()
st.caption("Academic portfolio project • Python • scikit-learn • Streamlit")
