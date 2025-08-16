import sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Add Company
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

# View Companies
def view_companies():
    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    print("\nCompanies List:")
    for row in rows:
        print(row)
    print()

# Delete Company
def delete_company():
    company_id = input("Enter Company ID to delete: ")
    cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    print("Company deleted successfully!\n")

# Search Companies
def search_companies():
    term = input("Enter Owner Name, Company Name, CEO, Scandals, or Location to search: ")
    cursor.execute("""
        SELECT * FROM companies
        WHERE owner_name LIKE ? OR company_name LIKE ? OR current_ceo LIKE ? OR scandals LIKE ? OR location LIKE ?
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
    print("1. Add Company")
    print("2. View Companies")
    print("3. Delete Company")
    print("4. Search Companies")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        add_company()
    elif choice == "2":
        view_companies()
    elif choice == "3":
        delete_company()
    elif choice == "4":
        search_companies()
    elif choice == "5":
        break
    else:
        print("Invalid choice, try again.\n")
