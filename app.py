from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from src.features import extract_features
from src.model import load_model, train

st.set_page_config(page_title="CSRF & XSS ML Detector", page_icon="🛡️", layout="wide")

st.title("🛡️ ML-Based CSRF & XSS Detection")
st.caption("Defensive academic prototype using Random Forest classification")

model_file = Path("models/random_forest.joblib")
if not model_file.exists():
    with st.spinner("Training the demo model..."):
        train("data/demo_web_requests.csv")

bundle = load_model()
model = bundle["model"]
feature_names = bundle["feature_names"]

@st.cache_data
def get_metrics():
    return train("data/demo_web_requests.csv")

metrics = get_metrics()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Accuracy", f"{metrics['accuracy']*100:.1f}%")
report = metrics["report"]
macro = report.get("macro avg", {})
m2.metric("Precision", f"{macro.get('precision',0)*100:.1f}%")
m3.metric("Recall", f"{macro.get('recall',0)*100:.1f}%")
m4.metric("F1 Score", f"{macro.get('f1-score',0)*100:.1f}%")

st.divider()
left, right = st.columns([1.1, 0.9])
with left:
    st.subheader("Request analysis")
    method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
    url = st.text_input("URL", "https://example.com/account")
    headers = st.text_area("Headers", "Origin: https://example.com\nReferer: https://example.com/\nCookie: session=abc123")
    payload = st.text_area("Request payload", "amount=100&recipient=user1")
    if st.button("Detect request", type="primary"):
        row = pd.DataFrame([{ "method": method, "url": url, "headers": headers, "payload": payload }])
        X = extract_features(row).reindex(columns=feature_names, fill_value=0)
        pred = model.predict(X)[0]
        probs = model.predict_proba(X)[0]
        confidence = float(max(probs))
        if pred == "BENIGN":
            st.success(f"Prediction: {pred} | Confidence: {confidence*100:.2f}%")
        else:
            st.error(f"Prediction: {pred} | Confidence: {confidence*100:.2f}%")
        st.json(dict(zip(model.classes_, [round(float(p),4) for p in probs])))

with right:
    st.subheader("Model overview")
    st.write("The model extracts lexical and structural indicators from HTTP request fields and classifies the request as BENIGN, CSRF, or XSS.")
    fi = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(6,4))
    fi.plot(kind="barh", ax=ax)
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    st.pyplot(fig, clear_figure=True)

st.divider()
st.subheader("Evaluation")
col1, col2 = st.columns(2)
with col1:
    st.write("Classification report")
    st.dataframe(pd.DataFrame(report).T.round(3), use_container_width=True)
with col2:
    st.write("Confusion matrix")
    cm = pd.DataFrame(metrics["confusion_matrix"], index=metrics["labels"], columns=metrics["labels"])
    st.dataframe(cm, use_container_width=True)

st.info("This repository uses a small demo dataset because the original project dataset/source code was not supplied with the paper. Replace the demo CSV with your actual labelled dataset for your real project results.")
