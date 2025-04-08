# 🏥 DoC. Web App

**DoC.** is a modern, full-stack health assistant web application built with **Flask** that bridges the gap between users and doctors. From disease prediction to appointment booking, BMI calculation, AQI checking, and weather-related news — this app brings intelligent healthcare tools under one roof.

---

## 🚀 Features

- 👨‍⚕️ **Doctor & User Authentication**
  - Separate dashboards for users and doctors
  - Secure login and registration system

- 💬 **Disease Prediction Chatbot**
  - Uses KNN + TF-IDF NLP model to predict possible diseases based on user input

- 📅 **Doctor Availability Scheduling**
  - Doctors can add/edit/delete available slots
  - Users can book appointments

- 🧮 **BMI Calculator**
  - Simple calculator to compute BMI and categorize it

- 🌫️ **AQI Checker**
  - Uses the WAQI API to fetch and display real-time air quality index data

- 🌦️ **Weather Health News**
  - Fetches weather-related health news articles using NewsAPI based on city input

- 🌙 **Dark Mode**
  - Toggle between light and dark themes for a better visual experience

- 📱 **Responsive & Beautiful UI**
  - Clean, mobile-friendly layout with modern design, animations, and hover effects

---

## 🧠 Machine Learning: Disease Prediction

- **Model**: K-Nearest Neighbors (KNN)
- **Vectorizer**: TF-IDF (Term Frequency–Inverse Document Frequency)
- **Purpose**: Predicts disease based on user-described symptoms
- **Training**:
  - Input: Symptom descriptions
  - Output: Most likely disease
- **Files**:
  - `knn_model.pkl`: Trained KNN classifier
  - `tfidf_vectorizer.pkl`: Fitted TF-IDF vectorizer
- **Libraries Used**: `scikit-learn`, `joblib`, `spaCy`

---

## 📦 Tech Stack

- **Frontend**: HTML, CSS, Vanilla JavaScript (modern, animated UI)
- **Backend**: Python (Flask)
- **Database**: SQLite
- **ML Libraries**: scikit-learn, joblib, spaCy
- **APIs**:
  - WAQI API (Air Quality Index)
  - NewsAPI (Weather-based health news)

---


##📋 Requirements
All dependencies are listed in requirements.txt. Here's a quick overview:

- Flask==2.3.3
- scikit-learn==1.4.1
- joblib==1.3.2
- spacy==3.7.2
- requests==2.31.0
- newsapi-python==0.2.7
- gunicorn==21.2.0  # Optional, for deployment

## 🎥 Demo Video
👉 [https://youtu.be/dtGN0U8p_gw]


## 🔧 Installation & Setup
### Install Requirements
```bash
pip install -r requirements.txt
```

### Clone the Repository
```bash
git clone https://github.com/Anuj-m02/DoC..git
cd DoC.
```
### Run the App
```bash
python app.py
```
