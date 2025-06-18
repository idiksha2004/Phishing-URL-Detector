import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

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

# Title
st.title("🔍 Phishing URL Classifier")

# Sidebar inputs
st.sidebar.header("🔧 Predict New URL Data")
input_data = {}
for feature in features:
    input_data[feature] = st.sidebar.number_input(feature, value=0)

# Predict button
if st.sidebar.button("Predict"):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    pred_label = "Phishing ⚠️" if prediction == 1 else "Legitimate ✅"
    st.subheader(f"Prediction: {pred_label}")

# Feature Importance
st.header("📌 Feature Importance (XGBoost)")
importances = model.feature_importances_
importance_df = pd.Series(importances, index=features).sort_values(ascending=False)
st.bar_chart(importance_df.head(10))

# Upload CSV
st.header("📁 Upload CSV for Batch Prediction")
uploaded_file = st.file_uploader("Choose a CSV file with the same structure", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    preds = model.predict(df[features])
    df["Prediction"] = preds
    df["Prediction Label"] = df["Prediction"].map({0: "Legitimate ✅", 1: "Phishing ⚠️"})
    st.dataframe(df.head())
