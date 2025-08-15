import sqlite3

conn = sqlite3.connect("app_data.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    registration_number TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS professions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stand_number TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL
)
""")

conn.commit()
conn.close()
print("Database and tables created!")
