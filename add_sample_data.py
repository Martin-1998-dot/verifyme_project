import sqlite3

conn = sqlite3.connect('verifyme.db')
c = conn.cursor()

# Insert sample profession records
c.execute("INSERT OR IGNORE INTO profession (id_number, license_number, profession) VALUES (?, ?, ?)",
          ('123456789', 'PROF001', 'Engineer'))
c.execute("INSERT OR IGNORE INTO profession (id_number, license_number, profession) VALUES (?, ?, ?)",
          ('987654321', 'PROF002', 'Doctor'))

# Insert sample cars
c.execute("INSERT OR IGNORE INTO cars (plate_number, owner_id, model) VALUES (?, ?, ?)",
          ('ABC123', '123456789', 'Toyota Corolla'))
c.execute("INSERT OR IGNORE INTO cars (plate_number, owner_id, model) VALUES (?, ?, ?)",
          ('XYZ789', '987654321', 'Honda Civic'))

# Insert sample properties
c.execute("INSERT OR IGNORE INTO properties (stand_number, owner_id, location) VALUES (?, ?, ?)",
          ('STAND001', '123456789', 'Bulawayo'))
c.execute("INSERT OR IGNORE INTO properties (stand_number, owner_id, location) VALUES (?, ?, ?)",
          ('STAND002', '987654321', 'Harare'))

conn.commit()
conn.close()

print("✅ Sample data added.")
