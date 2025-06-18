import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Load trained model
model = joblib.load('xgboost_phishing_model.pkl')

# Define features (must match training order)
features = [
    "NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash", 
    "NumDashInHostname", "AtSymbol", "TildeSymbol", "NumUnderscore", "NumPercent",
    "NumQueryComponents", "NumAmpersand", "NumHash", "NumNumericChars", "NoHttps",
    "RandomString", "IpAddress", "DomainInSubdomains", "DomainInPaths", "HttpsInHostname",
    "HostnameLength", "PathLength", "QueryLength", "DoubleSlashInPath", "NumSensitiveWords",
    "EmbeddedBrandName", "PctExtHyperlinks", "PctExtResourceUrls", "ExtFavicon",
    "InsecureForms", "RelativeFormAction", "ExtFormAction", "AbnormalFormAction",
    "PctNullSelfRedirectHyperlinks", "FrequentDomainNameMismatch", "FakeLinkInStatusBar",
    "RightClickDisabled", "PopUpWindow", "SubmitInfoToEmail", "IframeOrFrame",
    "MissingTitle", "ImagesOnlyInForm", "SubdomainLevelRT", "UrlLengthRT",
    "PctExtResourceUrlsRT", "AbnormalExtFormActionR", "ExtMetaScriptLinkRT",
    "PctExtNullSelfRedirectHyperlinksRT"
]

# Title and description
st.set_page_config(page_title="Phishing URL Detector", layout="wide")
st.title("🛡️ Phishing URL Detector")
st.markdown("""
Welcome to the **Phishing URL Detector**!  
This app allows you to:
- Detect phishing links via manual input or URL analysis
- Upload CSV files for batch predictions
- View feature importances from the trained model
- Preview metadata from any URL  
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Manual Input", "📁 Batch Upload", "🌐 URL Classifier", "🔎 Link Preview"])

# Tab 1: Manual feature input
with tab1:
    st.header("📊 Predict from Manual Input")
    st.sidebar.header("🔧 Enter Feature Values")
    input_data = {feature: st.sidebar.number_input(feature, value=0) for feature in features}

    if st.sidebar.button("Predict"):
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        if prediction == 1:
            st.error("⚠️ This input is classified as **Phishing**.")
        else:
            st.success("✅ This input is classified as **Legitimate**.")

        # Feature importance chart
        st.subheader("📌 Top 10 Feature Importances")
        importances = model.feature_importances_
        importance_df = pd.Series(importances, index=features).sort_values(ascending=False)
        st.bar_chart(importance_df.head(10))

# Tab 2: Batch Upload
with tab2:
    st.header("📁 Upload CSV for Batch Prediction")
    uploaded_file = st.file_uploader("Choose a CSV file with the same structure", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        preds = model.predict(df[features])
        df["Prediction"] = preds
        df["Prediction Label"] = df["Prediction"].map({0: "Legitimate ✅", 1: "Phishing ⚠️"})
        st.dataframe(df.head())

# Tab 3: URL Parsing and Prediction
def extract_basic_url_features(url):
    parsed = urlparse(url)
    return {
        "UrlLength": len(url),
        "NumDots": url.count('.'),
        "NumDash": url.count('-'),
        "AtSymbol": int("@" in url),
        "TildeSymbol": int("~" in url),
        "NumUnderscore": url.count('_'),
        "NumPercent": url.count('%'),
        "NumQueryComponents": len(parsed.query.split('&')) if parsed.query else 0,
        "PathLevel": len(parsed.path.split('/')) - 1,
        "HostnameLength": len(parsed.hostname) if parsed.hostname else 0,
        "PathLength": len(parsed.path),
    }

with tab3:
    st.header("🌐 Predict from URL Input")
    url_to_test = st.text_input("Paste a URL to classify")

    if url_to_test:
        features_extracted = extract_basic_url_features(url_to_test)
        input_df = pd.DataFrame([features_extracted])

        for f in features:
            if f not in input_df.columns:
                input_df[f] = 0

        prediction = model.predict(input_df)[0]
        if prediction == 1:
            st.error("⚠️ This URL is classified as **Phishing**.")
        else:
            st.success("✅ This URL is classified as **Legitimate**.")

# Tab 4: Link Preview
with tab4:
    st.header("🔎 Link Preview Checker")
    url_input = st.text_input("Enter a URL to preview")

    if url_input:
        try:
            response = requests.get(url_input, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string if soup.title else "No title found"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc else "No description found"

            st.markdown(f"**Title**: {title}")
            st.markdown(f"**Description**: {description}")

        except Exception as e:
            st.error(f"Failed to load preview: {e}")
