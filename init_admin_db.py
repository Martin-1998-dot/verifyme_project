import sqlite3
import hashlib

conn = sqlite3.connect('verifyme.db')
c = conn.cursor()

# Create admin table
c.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

# Create a default admin user (username: admin, password: admin123)
password = 'admin123'
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Insert default admin if not exists
c.execute('''
INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)
''', ('admin', password_hash))

conn.commit()
conn.close()

print("✅ Admin table created and default admin added.")
