import sqlite3

conn = sqlite3.connect('verifyme.db')
c = conn.cursor()

# Sample profession
c.execute('''
INSERT INTO profession_ids (id_number, license_number, full_name, profession, institution)
VALUES ('123456', 'LIC001', 'Dr. Musa Ncube', 'Medical Doctor', 'Parirenyatwa Hospital')
''')

# Sample car
c.execute('''
INSERT INTO car_records (plate_number, owner_id, full_name, car_model, registration_year)
VALUES ('ABZ1234', '567890', 'Thandiwe Dube', 'Toyota Corolla', '2018')
''')

# Sample house
c.execute('''
INSERT INTO house_records (stand_number, owner_id, full_name, location, ownership_status)
VALUES ('ST123', '9101112', 'Blessing Moyo', 'Bulawayo', 'Owned')
''')

conn.commit()
conn.close()
print("✅ Sample data inserted successfully.")
