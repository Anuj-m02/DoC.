import sqlite3

# Connect to SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("database/health.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# Create doctors table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# Create doctor schedules table
cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""")

# Create appointments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
""")

print("Database and tables created successfully.")
conn.commit()
conn.close()
