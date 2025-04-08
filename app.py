from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import pickle

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management

DB_PATH = "database/health.db"

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        table = 'users' if role == 'user' else 'doctors'

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['role'] = role
            return redirect(url_for('user_dashboard' if role == 'user' else 'doctor_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

import spacy.cli
spacy.cli.download("en_core_web_sm")

import joblib
import spacy
nlp = spacy.load("en_core_web_sm")


# Load KNN model and TF-IDF vectorizer
knn_model = joblib.load("models/knn_model.pkl")
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def preprocess_text(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if token.is_alpha and not token.is_stop]

@app.route("/predict_disease", methods=["GET"])
def chatbot_page():
    return render_template("disease_chatbot.html")


@app.route("/predict_disease", methods=["POST"])
def predict_disease():
    user_input = request.form['symptom']
    preprocessed = preprocess_text(user_input)
    symptom_text = ' '.join(preprocessed)

    symptom_vector = tfidf_vectorizer.transform([symptom_text])
    prediction = knn_model.predict(symptom_vector)

    return render_template("disease_chatbot.html", prediction=prediction[0], input=user_input)




@app.route('/user_dashboard')
def user_dashboard():
    if 'role' in session and session['role'] == 'user':
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch all doctors for dropdown
        cursor.execute("SELECT id, username FROM doctors")
        doctors = cursor.fetchall()

        # Fetch available slots
        cursor.execute("""
            SELECT schedules.id, doctors.username, schedules.date, schedules.time
            FROM schedules
            JOIN doctors ON schedules.doctor_id = doctors.id
            WHERE NOT EXISTS (
                SELECT 1 FROM appointments
                WHERE appointments.doctor_id = doctors.id
                AND appointments.date = schedules.date
                AND appointments.time = schedules.time
            )
        """)
        slots = cursor.fetchall()

        # Fetch user's booked appointments
        cursor.execute("""
            SELECT doctors.username, appointments.date, appointments.time
            FROM appointments
            JOIN doctors ON appointments.doctor_id = doctors.id
            WHERE appointments.user_id = ?
        """, (session['user_id'],))
        user_appointments = cursor.fetchall()

        conn.close()
        return render_template('user_dashboard.html', doctors=doctors, slots=slots, user_appointments=user_appointments)
    return redirect(url_for('login'))


@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'role' in session and session['role'] == 'doctor':
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch doctor's own schedule
        cursor.execute("SELECT date, time FROM schedules WHERE doctor_id = ?", (session['user_id'],))
        schedule_list = cursor.fetchall()

        conn.close()
        return render_template('doctor_dashboard.html', schedule_list=schedule_list)
    return redirect(url_for('login'))

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    if 'role' in session and session['role'] == 'user':
        height = float(request.form['height']) / 100  # convert cm to meters
        weight = float(request.form['weight'])
        bmi = round(weight / (height * height), 2)

        # Classify BMI
        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            status = "Normal weight"
        elif 25 <= bmi < 29.9:
            status = "Overweight"
        else:
            status = "Obesity"

        # Re-render user dashboard with BMI
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username FROM doctors")
        doctors = cursor.fetchall()

        cursor.execute("""
            SELECT schedules.id, doctors.username, schedules.date, schedules.time
            FROM schedules
            JOIN doctors ON schedules.doctor_id = doctors.id
            WHERE NOT EXISTS (
                SELECT 1 FROM appointments
                WHERE appointments.doctor_id = doctors.id
                AND appointments.date = schedules.date
                AND appointments.time = schedules.time
            )
        """)
        slots = cursor.fetchall()

        cursor.execute("""
            SELECT doctors.username, appointments.date, appointments.time
            FROM appointments
            JOIN doctors ON appointments.doctor_id = doctors.id
            WHERE appointments.user_id = ?
        """, (session['user_id'],))
        user_appointments = cursor.fetchall()

        conn.close()

        return render_template(
            'user_dashboard.html',
            doctors=doctors,
            slots=slots,
            user_appointments=user_appointments,
            bmi=bmi,
            bmi_status=status
        )

    return redirect(url_for('login'))

@app.route('/aqi')
def show_aqi_form():
    return render_template("aqi.html")


import requests
from flask import request, render_template

WAQI_TOKEN = "9be63fc5bd91464104d72cf96372c6da4df40cac"  # replace this with your actual token

@app.route('/check_aqi', methods=['POST'])
def check_aqi():
    city = request.form['city'].strip().lower()
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['status'] != 'ok':
            return render_template("aqi.html", aqi="N/A", quality="City not found or data unavailable 😕")

        aqi_value = data['data']['aqi']

        # AQI rating scale
        if aqi_value <= 50:
            quality = "Good 😊"
        elif aqi_value <= 100:
            quality = "Moderate 😐"
        elif aqi_value <= 150:
            quality = "Unhealthy for Sensitive Groups 😷"
        elif aqi_value <= 200:
            quality = "Unhealthy 😷"
        elif aqi_value <= 300:
            quality = "Very Unhealthy 🤢"
        else:
            quality = "Hazardous ☠️"

        return render_template("aqi.html", aqi=aqi_value, quality=quality)

    except Exception as e:
        print("AQI Error:", e)
        return render_template("aqi.html", aqi="N/A", quality="An error occurred while fetching data ⚠️")


import requests

NEWS_API_KEY = "f63c29a6eebd4f6eb29b3bb4e136f910"  # Replace with your real key

@app.route('/weather_news', methods=['GET'])
def weather_news():
    city = request.args.get('city')
    if not city:
        return render_template('weather_news.html', city=city, articles=[])

    query = f"weather AND {city}"
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()
    all_articles = data.get('articles', [])

    # Filter articles to keep only those with actual weather context
    filtered_articles = []
    keywords = ["temperature", "forecast", "rain", "storm", "weather", "climate", "snow", "heat", "air quality", "flood"]

    for article in all_articles:
        description = article.get('description', '').lower()
        title = article.get('title', '').lower()

        if any(word in description or word in title for word in keywords):
            filtered_articles.append(article)

    return render_template('weather_news.html', city=city, articles=filtered_articles)


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register_user.html', error="Username already exists")

    return render_template('register_user.html')


@app.route('/schedule', methods=['POST'])
def schedule():
    if 'role' in session and session['role'] == 'doctor':
        date = request.form['date']
        time = request.form['time']
        doctor_id = session['user_id']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedules (doctor_id, date, time) VALUES (?, ?, ?)", (doctor_id, date, time))
        conn.commit()
        conn.close()

        return render_template('doctor_dashboard.html', message="Availability added successfully!")
    return redirect(url_for('login'))

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'role' in session and session['role'] == 'user':
        user_id = session['user_id']
        slot_id = request.form['slot_id']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get slot info from schedules table
        cursor.execute("SELECT doctor_id, date, time FROM schedules WHERE id=?", (slot_id,))
        slot = cursor.fetchone()
        if slot:
            doctor_id, date, time = slot
            # Save appointment
            cursor.execute("""
                INSERT INTO appointments (user_id, doctor_id, date, time)
                VALUES (?, ?, ?, ?)
            """, (user_id, doctor_id, date, time))
            conn.commit()

        conn.close()
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))


@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO doctors (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register_doctor.html', error="Username already exists")

    return render_template('register_doctor.html')


# --------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
