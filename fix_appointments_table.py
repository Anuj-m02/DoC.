import sqlite3
import os

# Adjust path if needed
DB_PATH = os.path.join("database", "health.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop and recreate the appointments table
cursor.execute("DROP TABLE IF EXISTS appointments")

cursor.execute("""
    CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
""")

conn.commit()
conn.close()

print("✅ appointments table has been recreated successfully.")
