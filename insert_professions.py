import sqlite3
conn = sqlite3.connect('verifyme.db')
cur = conn.cursor()

# Add more profession entries
cur.execute("INSERT INTO profession_ids (id_number, license) VALUES (?, ?)", ('ID99999999', 'LIC123456'))
cur.execute("INSERT INTO profession_ids (id_number, license) VALUES (?, ?)", ('ID11112222', 'LIC555555'))
conn.commit()
conn.close()
