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
    url_to_test = st.text_input("Paste a URL to classify", key="url_classify")

    if url_to_test:
        parsed_url = urlparse(url_to_test)
        domain = parsed_url.hostname.lower() if parsed_url.hostname else ""

        whitelist_domains = ['microsoft.com', 'google.com', 'amazon.com', 'wikipedia.org', 'openai.com', 'linkedin.com']
        if any(whitelist in domain for whitelist in whitelist_domains):
            st.info("⚪ This is a known safe domain. Prediction skipped.")
        else:
            features_extracted = extract_basic_url_features(url_to_test)
            complete_input = {f: features_extracted.get(f, 0) for f in features}
            input_df = pd.DataFrame([complete_input])

            prediction = model.predict(input_df)[0]
            if prediction == 1:
                st.error("⚠️ This URL is classified as **Phishing**.")
            else:
                st.success("✅ This URL is classified as **Legitimate**.")

# Tab 4: Link Preview
with tab4:
    st.header("🔎 Link Preview Checker")
    url_input = st.text_input("Enter a URL to preview", key="link_preview")

    if url_input:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            response = requests.get(url_input, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string if soup.title else "No title found"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc else "No description found"

            st.markdown(f"**Title**: {title}")
            st.markdown(f"**Description**: {description}")

        except Exception as e:
            st.error(f"Failed to load preview: {e}")
