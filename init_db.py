import sqlite3

conn = sqlite3.connect('verifyme.db')
c = conn.cursor()

# Professions table
c.execute('''
CREATE TABLE profession_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_number TEXT NOT NULL,
    license_number TEXT NOT NULL,
    full_name TEXT,
    profession TEXT,
    institution TEXT
)
''')

# Cars table
c.execute('''
CREATE TABLE car_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    full_name TEXT,
    car_model TEXT,
    registration_year TEXT
)
''')

# Houses table
c.execute('''
CREATE TABLE house_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stand_number TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    full_name TEXT,
    location TEXT,
    ownership_status TEXT
)
''')

conn.commit()
conn.close()
print("✅ New database and tables created successfully.")
