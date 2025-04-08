import sqlite3

conn = sqlite3.connect("database/health.db")
cursor = conn.cursor()

# Add test user
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))

# Add test doctor
cursor.execute("INSERT OR IGNORE INTO doctors (username, password) VALUES (?, ?)", ("testdoc", "testpass"))

conn.commit()
conn.close()
print("Test users added.")
