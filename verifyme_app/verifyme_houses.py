import sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Add House
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

# View Houses
def view_houses():
    cursor.execute("SELECT * FROM houses")
    rows = cursor.fetchall()
    print("\nHouses List:")
    for row in rows:
        print(row)
    print()

# Delete House
def delete_house():
    house_id = input("Enter House ID to delete: ")
    cursor.execute("DELETE FROM houses WHERE id = ?", (house_id,))
    conn.commit()
    print("House deleted successfully!\n")

# Search Houses
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

# Main menu loop
while True:
    print("1. Add House")
    print("2. View Houses")
    print("3. Delete House")
    print("4. Search Houses")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        add_house()
    elif choice == "2":
        view_houses()
    elif choice == "3":
        delete_house()
    elif choice == "4":
        search_houses()
    elif choice == "5":
        break
    else:
        print("Invalid choice, try again.\n")
