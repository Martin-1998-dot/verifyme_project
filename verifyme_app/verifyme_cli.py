import sqlite3
import csv
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

DB_PATH = "verifyme.db"

TABLES = {
    "1": "cars",
    "2": "companies",
    "3": "houses",
    "4": "professions"
}

# --------------------- DB Utilities ---------------------
def connect_db():
    return sqlite3.connect(DB_PATH)

def get_columns(table_name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [info[1] for info in cur.fetchall()]
    conn.close()
    return cols

def fetch_all(table_name):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name}")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(Fore.LIGHTRED_EX + f"Database error: {e}")
        return []
    finally:
        conn.close()

def search_table(table_name, term):
    cols = get_columns(table_name)
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT * FROM {table_name} WHERE " +
            " OR ".join([f"{col} LIKE ?" for col in cols]),
            tuple(f"%{term}%" for _ in cols)
        )
        return cur.fetchall()
    except sqlite3.Error as e:
        print(Fore.LIGHTRED_EX + f"Database error: {e}")
        return []
    finally:
        conn.close()

# ----------------- Questions (Step 1) -------------------
def ensure_questions_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            question_text TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def get_active_questions(table_name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, question_text FROM questions WHERE table_name=? AND active=1 ORDER BY id ASC",
                (table_name,))
    rows = cur.fetchall()
    conn.close()
    return rows

def list_all_questions(table_name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, question_text, active FROM questions WHERE table_name=? ORDER BY id ASC",
                (table_name,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_question(table_name, text):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions (table_name, question_text, active) VALUES (?, ?, 1)",
                (table_name, text))
    conn.commit()
    conn.close()

def toggle_question(question_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT active FROM questions WHERE id=?", (question_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    new_val = 0 if row[0] == 1 else 1
    cur.execute("UPDATE questions SET active=? WHERE id=?", (new_val, question_id))
    conn.commit()
    conn.close()
    return True

def delete_question(question_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (question_id,))
    conn.commit()
    conn.close()

def manage_questions_menu():
    while True:
        print(Fore.WHITE + "\n--- Manage Verification Questions ---")
        table = choose_table("Select table to manage questions:")
        if not table:
            print(Fore.LIGHTRED_EX + "Invalid choice.")
            return

        print(Fore.WHITE + f"\nCurrent questions for {table.capitalize()}:")
        all_qs = list_all_questions(table)
        if not all_qs:
            print(Fore.WHITE + "(none)")
        else:
            for qid, qtext, active in all_qs:
                status = Fore.LIGHTGREEN_EX + "Active" if active == 1 else Fore.LIGHTRED_EX + "Inactive"
                print(Fore.WHITE + f"[{qid}] {qtext}  -  {status}")

        print(Fore.WHITE + "\nOptions: 1) Add  2) Toggle Active  3) Delete  4) Back")
        opt = input(Fore.WHITE + "Enter option: ").strip()
        if opt == "1":
            text = input(Fore.WHITE + "Enter question text: ").strip()
            if text:
                add_question(table, text)
                print(Fore.LIGHTGREEN_EX + "Question added.")
        elif opt == "2":
            qid = input(Fore.WHITE + "Enter question ID to toggle: ").strip()
            if qid.isdigit() and toggle_question(int(qid)):
                print(Fore.LIGHTGREEN_EX + "Question toggled.")
            else:
                print(Fore.LIGHTRED_EX + "Invalid question ID.")
        elif opt == "3":
            qid = input(Fore.WHITE + "Enter question ID to delete: ").strip()
            if qid.isdigit():
                delete_question(int(qid))
                print(Fore.LIGHTGREEN_EX + "Question deleted.")
            else:
                print(Fore.LIGHTRED_EX + "Invalid question ID.")
        elif opt == "4":
            return
        else:
            print(Fore.LIGHTRED_EX + "Invalid choice.")

# -------------------- Display ----------------------
def print_record_card(row, columns, table_name):
    header_color = Fore.WHITE + Style.BRIGHT
    value_color = Fore.WHITE

    record_id = row[0]
    header_text = f"{table_name.upper()} RECORD ID {record_id}"
    underline = "-" * len(header_text)

    # Top border, header, underline
    print(Fore.CYAN + "=" * (len(header_text) + 10))
    print(header_color + header_text)
    print(header_color + underline)

    # Fields
    for col, val in zip(columns[1:], row[1:]):  # Skip ID
        label = col.replace("_", " ").title()
        sval = str(val)
        if sval.lower() in ["active", "pending"]:
            val_display = Fore.LIGHTGREEN_EX + sval
        elif sval.lower() in ["not found", "error", "inactive"]:
            val_display = Fore.LIGHTRED_EX + sval
        else:
            val_display = value_color + sval
        print(f"{label:<25}: {val_display}")

    # Active questions section
    qs = get_active_questions(table_name)
    if qs:
        print()  # spacing
        q_header = "Verification Questions"
        print(header_color + q_header)
        print(header_color + "-" * len(q_header))
        for _, qtext in qs:
            print(Fore.WHITE + f"- {qtext}")

    # Bottom border
    print(Fore.CYAN + "=" * (len(header_text) + 10))

def print_all_records(rows, table_name):
    if not rows:
        print(Fore.LIGHTRED_EX + "No records found.\n")
        return
    columns = get_columns(table_name)
    for row in rows:
        print_record_card(row, columns, table_name)

def show_summary():
    parts = []
    for name in TABLES.values():
        count = len(fetch_all(name))
        parts.append(f"{name.capitalize()}: {count}")
    # padded summary with subtle borders
    summary = "   " + "   |   ".join(parts) + "   "
    print(Fore.CYAN + "=" * len(summary))
    print(Fore.WHITE + summary)
    print(Fore.CYAN + "=" * len(summary))

# ---------------------- CRUD -----------------------
def add_record(table_name):
    cols = get_columns(table_name)
    values = []
    print(Fore.WHITE + f"\n=== Adding new record to {table_name.upper()} ===")
    for col in cols:
        if col == "id":
            continue
        val = input(Fore.WHITE + f"{col.replace('_', ' ').title()}: ")
        values.append(val)
    conn = connect_db()
    cur = conn.cursor()
    try:
        placeholders = ", ".join(["?"] * len(values))
        columns_str = ", ".join([c for c in cols if c != "id"])
        cur.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", tuple(values))
        conn.commit()
        print(Fore.LIGHTGREEN_EX + "Record added successfully!\n")
    except sqlite3.Error as e:
        print(Fore.LIGHTRED_EX + f"Error: {e}")
    finally:
        conn.close()

def edit_record(table_name):
    rows = fetch_all(table_name)
    if not rows:
        print(Fore.LIGHTRED_EX + "No records found.\n")
        return
    print_all_records(rows, table_name)
    record_id = input(Fore.WHITE + "Enter the ID of the record to edit: ").strip()
    cols = get_columns(table_name)
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name} WHERE id=?", (record_id,))
        old_row = cur.fetchone()
        if not old_row:
            print(Fore.LIGHTRED_EX + "Record not found.\n")
            return
        new_values = []
        print(Fore.WHITE + "Enter new values (leave blank to keep current value):")
        for i, col in enumerate(cols):
            if col == "id":
                new_values.append(record_id)
                continue
            val = input(Fore.WHITE + f"{col.replace('_', ' ').title()} [{old_row[i]}]: ")
            if val == "":
                val = old_row[i]
            new_values.append(val)
        cur.execute(
            f"UPDATE {table_name} SET {', '.join([f'{col}=?' for col in cols])} WHERE id=?",
            tuple(new_values + [record_id])
        )
        conn.commit()
        print(Fore.LIGHTGREEN_EX + "Record updated successfully!\n")
    except sqlite3.Error as e:
        print(Fore.LIGHTRED_EX + f"Database error: {e}")
    finally:
        conn.close()

def delete_record(table_name):
    rows = fetch_all(table_name)
    if not rows:
        print(Fore.LIGHTRED_EX + "No records found.\n")
        return
    print_all_records(rows, table_name)
    record_id = input(Fore.WHITE + "Enter the ID of the record to delete: ").strip()
    confirm = input(Fore.LIGHTRED_EX + f"Are you sure you want to delete record {record_id}? (y/n): ").strip()
    if confirm.lower() != "y":
        print(Fore.WHITE + "Delete cancelled.\n")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM {table_name} WHERE id=?", (record_id,))
        conn.commit()
        print(Fore.LIGHTGREEN_EX + "Record deleted successfully.\n")
    except sqlite3.Error as e:
        print(Fore.LIGHTRED_EX + f"Database error: {e}")
    finally:
        conn.close()

# -------------------- Export -----------------------
def export_to_csv(table_name):
    rows = fetch_all(table_name)
    if not rows:
        print(Fore.LIGHTRED_EX + "No records found to export.\n")
        return
    columns = get_columns(table_name)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"{table_name}_export_{timestamp}.csv"
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        print(Fore.LIGHTGREEN_EX + f"Records exported successfully to {os.path.abspath(filename)} ({len(rows)} records)\n")
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error exporting to CSV: {e}\n")

# ------------------ Table Picker -------------------
def choose_table(prompt):
    print(Fore.WHITE + "\n" + prompt)
    for num, name in TABLES.items():
        count = len(fetch_all(name))
        print(Fore.WHITE + f"{num}. {name.capitalize()} ({count} records)")
    choice = input(Fore.WHITE + "Enter choice number: ").strip()
    return TABLES.get(choice, None)

# --------------------- Main Menu -------------------
def main_menu():
    ensure_questions_table()  # make sure questions table exists
    while True:
        print(Fore.WHITE + "\n================= VERIFY ME CLI =================")
        show_summary()
        print(Fore.WHITE + "1. View Records")
        print(Fore.WHITE + "2. Search Records")
        print(Fore.WHITE + "3. Add Record")
        print(Fore.WHITE + "4. Edit Record")
        print(Fore.WHITE + "5. Delete Record")
        print(Fore.WHITE + "6. Exit")
        print(Fore.WHITE + "7. Export Records to CSV")
        print(Fore.WHITE + "8. Manage Verification Questions")
        print(Fore.WHITE + "================================================")
        choice = input(Fore.WHITE + "Enter choice: ").strip()

        if choice == "1":
            table = choose_table("Select table to view:")
            if table:
                rows = fetch_all(table)
                print_all_records(rows, table)
        elif choice == "2":
            table = choose_table("Select table to search:")
            if table:
                term = input(Fore.WHITE + "Enter search term: ")
                rows = search_table(table, term)
                print_all_records(rows, table)
        elif choice == "3":
            table = choose_table("Select table to add record:")
            if table:
                add_record(table)
        elif choice == "4":
            table = choose_table("Select table to edit record:")
            if table:
                edit_record(table)
        elif choice == "5":
            table = choose_table("Select table to delete record:")
            if table:
                delete_record(table)
        elif choice == "6":
            print(Fore.LIGHTGREEN_EX + "Exiting... Goodbye!\n")
            break
        elif choice == "7":
            table = choose_table("Select table to export:")
            if table:
                export_to_csv(table)
        elif choice == "8":
            manage_questions_menu()
        else:
            print(Fore.LIGHTRED_EX + "Invalid choice. Try again.\n")

if __name__ == "__main__":
    main_menu()
