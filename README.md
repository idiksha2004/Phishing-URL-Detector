# 🛡️ Phishing URL Detector

A powerful and interactive **Streamlit** app to detect **phishing URLs** using a machine learning model trained on URL-based features.  
Whether you're uploading batches, analyzing single URLs, or previewing link content — this tool gives you a complete security-check experience.

---

## 🚀 Features

### 🔍 Phishing Detection
- Classify URLs as **Phishing ⚠️** or **Legitimate ✅** based on structural attributes.
- Supports **manual input**, **URL-based feature extraction**, and **batch upload via CSV**.

### 📁 Batch Prediction
- Upload datasets and get predictions with explanation labels.
- Works with pre-formatted `.csv` files matching model features.

### 🌐 URL Parsing + Whitelist
- Enter any URL and get it automatically analyzed.
- Known safe domains (like `microsoft.com`, `google.com`) are skipped with a trust flag.

### 🔎 Link Preview
- Scrape the **title** and **meta description** of any public URL.
- Includes a browser-style user-agent header to avoid simple blocks.

---

## 🧪 Demo Screenshots

![UI Screenshot 1](https://via.placeholder.com/800x400?text=Manual+Input+Tab)
![UI Screenshot 2](https://via.placeholder.com/800x400?text=URL+Classifier+Tab)
![UI Screenshot 3](https://via.placeholder.com/800x400?text=CSV+Batch+Prediction)

---

## 🧰 Tech Stack

- **Streamlit** – Interactive UI
- **XGBoost** – Phishing classification model
- **Pandas / Joblib** – Data handling and model I/O
- **BeautifulSoup + Requests** – For fetching link previews
- **Matplotlib** – For visualizing feature importances

---

## 📦 Setup Locally

```bash
git clone https://github.com/your-username/Phishing-URL-Detector.git
cd Phishing-URL-Detector
pip install -r requirements.txt
streamlit run streamlit_app_final.py
```

---

## 📂 Sample Files

- `xgboost_phishing_model.pkl` – Pretrained model file
- `sample_phishing_input.csv` – Test dataset with phishing/legit rows

---

## 🌐 Live Deployment

> 🔗 App is hosted live on [Streamlit Cloud](https://your-app-link.streamlit.app)

---

## 🤝 Contributors

- 👤 [Your Name](https://github.com/your-username) – Developer & Designer

---

## 📄 License

Licensed under MIT — free to use, modify, and distribute.

---

