import sqlite3

DB_PATH = "verifyme.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables_if_missing():
    conn = connect_db()
    cur = conn.cursor()

    tables_sql = {
        "cars": """CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number_plate TEXT,
                    vin TEXT,
                    owner_name TEXT,
                    make_model TEXT,
                    registration_status TEXT
                )""",
        "houses": """CREATE TABLE IF NOT EXISTS houses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    house_number TEXT,
                    stand_number TEXT,
                    owner_name TEXT,
                    deed_status TEXT
                )""",
        "professions": """CREATE TABLE IF NOT EXISTS professions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    school TEXT,
                    college_university TEXT,
                    license_number TEXT,
                    scandals TEXT,
                    years_of_operation TEXT
                )""",
        "stands": """CREATE TABLE IF NOT EXISTS stands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stand_number TEXT,
                    owner_name TEXT,
                    plot_size TEXT,
                    allocation_reference TEXT
                )""",
        "companies": """CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    registration_number TEXT,
                    incorporation_date TEXT,
                    status TEXT,
                    directors TEXT,
                    tax_compliance TEXT
                )"""
    }

    for name, sql in tables_sql.items():
        cur.execute(sql)

    conn.commit()
    conn.close()
    print("✅ All tables are ready (created if missing).")

# Run this function when starting the app
if __name__ == "__main__":
    create_tables_if_missing()
