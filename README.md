# 🏥 Health Chatbot Web App

A modern, full-stack health assistant web app built with Flask that helps users and doctors manage healthcare features like disease prediction, BMI calculation, AQI checks, appointment booking, and weather-related news.

---

## 🚀 Features

- 👨‍⚕️ Doctor & User Authentication (with separate dashboards)
- 💬 Disease Prediction Chatbot (KNN + TF-IDF NLP Model)
- 📅 Doctor Availability & Appointment Booking
- 🧮 BMI Calculator
- 🌫️ AQI (Air Quality Index) Checker using WAQI API
- 🌦️ Weather-Based Health News using NewsAPI
- 🌙 Dark Mode Toggle
- ✅ Clean & Responsive UI (Desktop & Mobile)

---

## 🧠 Machine Learning

- Disease prediction using a **KNN model** trained on symptom descriptions
- Text input is vectorized using **TF-IDF**
- Stored using `joblib` in `knn_model.pkl` and `tfidf_vectorizer.pkl`

---

## 📦 Tech Stack

- **Frontend:** HTML, CSS, Vanilla JS (modern, animated UI)
- **Backend:** Flask (Python)
- **Database:** SQLite
- **APIs Used:**  
  - [WAQI API](https://aqicn.org/api/) for Air Quality  
  - [NewsAPI](https://newsapi.org/) for Weather News

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/health-chatbot.git
cd health-chatbot
