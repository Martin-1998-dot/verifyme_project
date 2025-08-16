import sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Add Profession
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

# View Professions
def view_professions():
    cursor.execute("SELECT * FROM professions")
    rows = cursor.fetchall()
    print("\nProfessions List:")
    for row in rows:
        print(row)
    print()

# Delete Profession
def delete_profession():
    prof_id = input("Enter Profession ID to delete: ")
    cursor.execute("DELETE FROM professions WHERE id = ?", (prof_id,))
    conn.commit()
    print("Profession deleted successfully!\n")

# Search Profession
def search_professions():
    term = input("Enter ID Number, License Number, School, College, or Specialization to search: ")
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

# Main menu loop
while True:
    print("1. Add Profession")
    print("2. View Professions")
    print("3. Delete Profession")
    print("4. Search Profession")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        add_profession()
    elif choice == "2":
        view_professions()
    elif choice == "3":
        delete_profession()
    elif choice == "4":
        search_professions()
    elif choice == "5":
        break
    else:
        print("Invalid choice, try again.\n")
