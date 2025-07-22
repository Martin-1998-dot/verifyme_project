import sqlite3

conn = sqlite3.connect('verifyme.db')
c = conn.cursor()

# Table for IDs
c.execute('''
CREATE TABLE IF NOT EXISTS ids (
    id_number TEXT PRIMARY KEY,
    full_name TEXT
)
''')

# Table for profession verification
c.execute('''
CREATE TABLE IF NOT EXISTS profession (
    id_number TEXT,
    license_number TEXT,
    profession TEXT
)
''')

# Table for cars
c.execute('''
CREATE TABLE IF NOT EXISTS cars (
    plate_number TEXT PRIMARY KEY,
    owner_id TEXT,
    model TEXT
)
''')

# Table for houses/stands
c.execute('''
CREATE TABLE IF NOT EXISTS properties (
    stand_number TEXT PRIMARY KEY,
    owner_id TEXT,
    location TEXT
)
''')

conn.commit()
conn.close()
print("✅ Database initialized.")
