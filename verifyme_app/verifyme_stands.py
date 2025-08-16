	mport sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Add Stand
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

# View Stands
def view_stands():
    cursor.execute("SELECT * FROM stands")
    rows = cursor.fetchall()
    print("\nStands List:")
    for row in rows:
        print(row)
    print()

# Delete Stand
def delete_stand():
    stand_id = input("Enter Stand ID to delete: ")
    cursor.execute("DELETE FROM stands WHERE id = ?", (stand_id,))
    conn.commit()
    print("Stand deleted successfully!\n")

# Search Stands
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

# Main menu loop
while True:
    print("1. Add Stand")
    print("2. View Stands")
    print("3. Delete Stand")
    print("4. Search Stands")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        add_stand()
    elif choice == "2":
        view_stands()
    elif choice == "3":
        delete_stand()
    elif choice == "4":
        search_stands()
    elif choice == "5":
        break
    else:
        print("Invalid choice, try again.\n")
