import sqlite3

# Connect to database
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Add Car
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

# View Cars
def view_cars():
    cursor.execute("SELECT * FROM cars")
    rows = cursor.fetchall()
    print("\nCars List:")
    for row in rows:
        print(row)
    print()

# Delete Car
def delete_car():
    car_id = input("Enter Car ID to delete: ")
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    print("Car deleted successfully!\n")

# Search Cars
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

# Main menu loop
while True:
    print("1. Add Car")
    print("2. View Cars")
    print("3. Delete Car")
    print("4. Search Cars")
    print("5. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        add_car()
    elif choice == "2":
        view_cars()
    elif choice == "3":
        delete_car()
    elif choice == "4":
        search_cars()
    elif choice == "5":
        break
    else:
        print("Invalid choice, try again.\n")
