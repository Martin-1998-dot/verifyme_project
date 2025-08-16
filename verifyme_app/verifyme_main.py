import sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# ================== Professions ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS professions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_number TEXT,
    license_number TEXT,
    school TEXT,
    college TEXT,
    scandals TEXT,
    years_in_profession INTEGER,
    specialization TEXT,
    current_employer TEXT
)
""")
conn.commit()

def add_profession():
    id_number = input("ID Number: ")
    license_number = input("License Number: ")
    school = input("School: ")
    college = input("College: ")
    scandals = input("Scandals: ")
    years = input("Years in profession: ")
    specialization = input("Specialization: ")
    employer = input("Current Employer: ")
    cursor.execute("""
        INSERT INTO professions (id_number, license_number, school, college, scandals, years_in_profession, specialization, current_employer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_number, license_number, school, college, scandals, years, specialization, employer))
    conn.commit()
    print("Profession added successfully!\n")

def view_professions():
    cursor.execute("SELECT * FROM professions")
    rows = cursor.fetchall()
    print("\nProfessions List:")
    for row in rows:
        print(row)
    print()

def delete_profession():
    prof_id = input("Enter Profession ID to delete: ")
    cursor.execute("DELETE FROM professions WHERE id = ?", (prof_id,))
    conn.commit()
    print("Profession deleted successfully!\n")

def search_professions():
    term = input("Enter ID, License, School, College, or Specialization to search: ")
    cursor.execute("""
        SELECT * FROM professions
        WHERE id_number LIKE ? OR license_number LIKE ? OR school LIKE ? OR college LIKE ? OR specialization LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(row)
    else:
        print("No records found.")
    print()


# ================== Cars ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id TEXT,
    model TEXT,
    color TEXT,
    reg_number TEXT,
    insurance TEXT,
    year INTEGER
)
""")
conn.commit()

def add_car():
    owner_id = input("Owner ID: ")
    model = input("Car Model: ")
    color = input("Color: ")
    reg_number = input("Registration Number: ")
    insurance = input("Insurance Details: ")
    year = input("Year of Manufacture: ")
    cursor.execute("""
        INSERT INTO cars (owner_id, model, color, reg_number, insurance, year)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (owner_id, model, color, reg_number, insurance, year))
    conn.commit()
    print("Car added successfully!\n")

def view_cars():
    cursor.execute("SELECT * FROM cars")
    rows = cursor.fetchall()
    print("\nCars List:")
    for row in rows:
        print(row)
    print()

def delete_car():
    car_id = input("Enter Car ID to delete: ")
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    print("Car deleted successfully!\n")

def search_cars():
    term = input("Enter Owner ID, Model, Color, Reg Number, Insurance, or Year to search: ")
    cursor.execute("""
        SELECT * FROM cars
        WHERE owner_id LIKE ? OR model LIKE ? OR color LIKE ? OR reg_number LIKE ? OR insurance LIKE ? OR year LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(row)
    else:
        print("No records found.")
    print()


# ================== Stands ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS stands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id TEXT,
    stand_number TEXT,
    conflict TEXT,
    next_of_kin TEXT
)
""")
conn.commit()

def add_stand():
    owner_id = input("Owner ID: ")
    stand_number = input("Stand Number: ")
    conflict = input("Conflict: ")
    next_of_kin = input("Next of Kin: ")
    cursor.execute("""
        INSERT INTO stands (owner_id, stand_number, conflict, next_of_kin)
        VALUES (?, ?, ?, ?)
    """, (owner_id, stand_number, conflict, next_of_kin))
    conn.commit()
    print("Stand added successfully!\n")

def view_stands():
    cursor.execute("SELECT * FROM stands")
    rows = cursor.fetchall()
    print("\nStands List:")
    for row in rows:
        print(row)
    print()

def delete_stand():
    stand_id = input("Enter Stand ID to delete: ")
    cursor.execute("DELETE FROM stands WHERE id = ?", (stand_id,))
    conn.commit()
    print("Stand deleted successfully!\n")

def search_stands():
    term = input("Enter Owner ID, Stand Number, Conflict, or Next of Kin to search: ")
    cursor.execute("""
        SELECT * FROM stands
        WHERE owner_id LIKE ? OR stand_number LIKE ? OR conflict LIKE ? OR next_of_kin LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(row)
    else:
        print("No records found.")
    print()


# ================== Houses ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id TEXT,
    house_number TEXT,
    next_of_kin TEXT,
    location TEXT,
    size TEXT
)
""")
conn.commit()

def add_house():
    owner_id = input("Owner ID: ")
    house_number = input("House Number: ")
    next_of_kin = input("Next of Kin: ")
    location = input("Location: ")
    size = input("Size (e.g., 2BHK, 3BHK): ")
    cursor.execute("""
        INSERT INTO houses (owner_id, house_number, next_of_kin, location, size)
        VALUES (?, ?, ?, ?, ?)
    """, (owner_id, house_number, next_of_kin, location, size))
    conn.commit()
    print("House added successfully!\n")

def view_houses():
    cursor.execute("SELECT * FROM houses")
    rows = cursor.fetchall()
    print("\nHouses List:")
    for row in rows:
        print(row)
    print()

def delete_house():
    house_id = input("Enter House ID to delete: ")
    cursor.execute("DELETE FROM houses WHERE id = ?", (house_id,))
    conn.commit()
    print("House deleted successfully!\n")

def search_houses():
    term = input("Enter Owner ID, House Number, Next of Kin, Location, or Size to search: ")
    cursor.execute("""
        SELECT * FROM houses
        WHERE owner_id LIKE ? OR house_number LIKE ? OR next_of_kin LIKE ? OR location LIKE ? OR size LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(row)
    else:
        print("No records found.")
    print()


# ================== Companies ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_name TEXT,
    company_name TEXT,
    years_of_operation INTEGER,
    current_ceo TEXT,
    scandals TEXT,
    location TEXT
)
""")
conn.commit()

def add_company():
    owner_name = input("Owner Name: ")
    company_name = input("Company Name: ")
    years = input("Years of Operation: ")
    ceo = input("Current CEO: ")
    scandals = input("Scandals: ")
    location = input("Location: ")
    cursor.execute("""
        INSERT INTO companies (owner_name, company_name, years_of_operation, current_ceo, scandals, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (owner_name, company_name, years, ceo, scandals, location))
    conn.commit()
    print("Company added successfully!\n")

def view_companies():
    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    print("\nCompanies List:")
    for row in rows:
        print(row)
    print()

def delete_company():
    company_id = input("Enter Company ID to delete: ")
    cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    print("Company deleted successfully!\n")

def search_companies():
    term = input("Enter Owner Name, Company Name, CEO, Scandals, or Location to search: ")
    cursor.execute("""
        SELECT * FROM companies
        WHERE owner_name LIKE ? OR company_name LIKE ? OR current_ceo LIKE ? OR scandals LIKE ? OR location LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%
