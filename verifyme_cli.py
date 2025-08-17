import sqlite3
import csv
import os
import random
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

DB_PATH = "verifyme.db"

TABLES = {
    "1": "cars",
    "2": "companies",
    "3": "houses",
    "4": "professions",
    "5": "stands"
}

# ----------------- Dynamic Verification Questions -----------------
VERIFICATION_QUESTIONS = {
    "professions": ["License Number","ID Number (last 4 digits only)","Full Name","Years of Operation","Registration with Professional Body","Status (Active/Suspended/Revoked)"],
    "cars": ["Number Plate","Chassis/VIN (partial)","Registered Owner Name (initials)","Make & Model","Registration Status"],
    "houses": ["House Number","Stand Number / Title Deed","Owner Name (partial)","Deed Verification Status"],
    "stands": ["Stand Number","Owner Name (partial)","Plot Size & General Location","Title Deed / Allocation Reference"],
    "companies": ["Company Name","Registration Number","Incorporation Date","Status (Active / Deregistered / In Liquidation)","Directors (initials only)","Tax Compliance Status"]
}

def get_dynamic_questions(category, num_questions=3):
    pool = VERIFICATION_QUESTIONS.get(category.lower(), [])
    return random.sample(pool, min(num_questions, len(pool)))

# --------------------- DB Utilities ---------------------
def connect_db(): return sqlite3.connect(DB_PATH)
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

# -------------------- Display ----------------------
def print_record_card(row, columns, table_name):
    header_color = Fore.WHITE + Style.BRIGHT
    value_color = Fore.WHITE
    record_id = row[0]
    header_text = f"{table_name.upper()} RECORD ID {record_id}"
    underline = "-" * len(header_text)
    print(Fore.CYAN + "=" * (len(header_text)+10))
    print(header_color + header_text)
    print(header_color + underline)
    for col, val in zip(columns[1:], row[1:]):
        label = col.replace("_"," ").title()
        sval = str(val)
        if sval.lower() in ["active","pending"]: val_display = Fore.LIGHTGREEN_EX + sval
        elif sval.lower() in ["not found","error","inactive"]: val_display = Fore.LIGHTRED_EX + sval
        else: val_display = value_color + sval
        print(f"{label:<25}: {val_display}")
    dynamic_qs = get_dynamic_questions(table_name)
    if dynamic_qs:
        print()
        q_header = "Verification Questions (Sample)"
        print(header_color + q_header)
        print(header_color + "-"*len(q_header))
        for q in dynamic_qs: print(Fore.WHITE + f"- {q}")
    print(Fore.CYAN + "=" * (len(header_text)+10))

def print_all_records(rows, table_name):
    if not rows: print(Fore.LIGHTRED_EX+"No records found.\n"); return
    columns = get_columns(table_name)
    for row in rows: print_record_card(row, columns, table_name)

def show_summary():
    parts=[]
    for name in TABLES.values(): parts.append(f"{name.capitalize()}: {len(fetch_all(name))}")
    summary="   "+"   |   ".join(parts)+"   "
    print(Fore.CYAN+"="*len(summary))
    print(Fore.WHITE+summary)
    print(Fore.CYAN+"="*len(summary))

# ---------------------- CRUD -----------------------
def add_record(table_name):
    cols=get_columns(table_name); values=[]
    print(Fore.WHITE+f"\n=== Adding new record to {table_name.upper()} ===")
    for col in cols:
        if col=="id": continue
        val=input(Fore.WHITE+f"{col.replace('_',' ').title()}: ")
        values.append(val)
    conn=connect_db(); cur=conn.cursor()
    try:
        placeholders=", ".join(["?"]*len(values))
        columns_str=", ".join([c for c in cols if c!="id"])
        cur.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", tuple(values))
        conn.commit()
        print(Fore.LIGHTGREEN_EX+"Record added successfully!\n")
    except sqlite3.Error as e: print(Fore.LIGHTRED_EX+f"Error: {e}")
    finally: conn.close()

def edit_record(table_name):
    rows=fetch_all(table_name)
    if not rows: print(Fore.LIGHTRED_EX+"No records found.\n"); return
    print_all_records(rows, table_name)
    record_id=input(Fore.WHITE+"Enter the ID of the record to edit: ").strip()
    cols=get_columns(table_name)
    conn=connect_db(); cur=conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name} WHERE id=?", (record_id,))
        old_row=cur.fetchone()
        if not old_row: print(Fore.LIGHTRED_EX+"Record not found.\n"); return
        new_values=[]
        print(Fore.WHITE+"Enter new values (leave blank to keep current value):")
        for i,col in enumerate(cols):
            if col=="id": continue
            val=input(Fore.WHITE+f"{col.replace('_',' ').title()} [{old_row[i]}]: ")
            if val=="": val=old_row[i]
            new_values.append(val)
        cur.execute(f"UPDATE {table_name} SET {', '.join([f'{col}=?' for col in cols if col!='id'])} WHERE id=?", tuple(new_values+[record_id]))
        conn.commit()
        print(Fore.LIGHTGREEN_EX+"Record updated successfully!\n")
    except sqlite3.Error as e: print(Fore.LIGHTRED_EX+f"Database error: {e}")
    finally: conn.close()

def delete_record(table_name):
    rows=fetch_all(table_name)
    if not rows: print(Fore.LIGHTRED_EX+"No records found.\n"); return
    print_all_records(rows, table_name)
    record_id=input(Fore.WHITE+"Enter the ID of the record to delete: ").strip()
    confirm=input(Fore.LIGHTRED_EX+f"Are you sure you want to delete record {record_id}? (y/n): ").strip()
    if confirm.lower()!="y": print(Fore.WHITE+"Delete cancelled.\n"); return
    conn=connect_db(); cur=conn.cursor()
    try: cur.execute(f"DELETE FROM {table_name} WHERE id=?", (record_id,)); conn.commit(); print(Fore.LIGHTGREEN_EX+"Record deleted successfully.\n")
    except sqlite3.Error as e: print(Fore.LIGHTRED_EX+f"Database error: {e}")
    finally: conn.close()

# -------------------- Export -----------------------
def export_to_csv(table_name):
    rows=fetch_all(table_name)
    if not rows: print(Fore.LIGHTRED_EX+"No records found to export.\n"); return
    columns=get_columns(table_name)
    timestamp=datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename=f"{table_name}_export_{timestamp}.csv"
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer=csv.writer(f); writer.writerow(columns); writer.writerows(rows)
        print(Fore.LIGHTGREEN_EX+f"Records exported successfully to {os.path.abspath(filename)} ({len(rows)} records)\n")
    except Exception as e: print(Fore.LIGHTRED_EX+f"Error exporting to CSV: {e}\n")

# ------------------ Table Picker -------------------
def choose_table(prompt):
    print(Fore.WHITE+"\n"+prompt)
    for num,name in TABLES.items(): print(Fore.WHITE+f"{num}. {name.capitalize()} ({len(fetch_all(name))} records)")
    choice=input(Fore.WHITE+"Enter choice number: ").strip()
    return TABLES.get(choice, None)

# --------------------- Main Menu -------------------
def main_menu():
    while True:
        print(Fore.WHITE+"\n================= VERIFY ME CLI =================")
        show_summary()
        print(Fore.WHITE+"1. View Records")
        print(Fore.WHITE+"2. Search Records")
        print(Fore.WHITE+"3. Add Record")
        print(Fore.WHITE+"4. Edit Record")
        print(Fore.WHITE+"5. Delete Record")
        print(Fore.WHITE+"6. Export Records to CSV")
        print(Fore.WHITE+"7. Exit")
        print(Fore.WHITE+"================================================")
        choice=input(Fore.WHITE+"Enter choice: ").strip()
        if choice=="1":
            table=choose_table("Select table to view:")
            if table: print_all_records(fetch_all(table), table)
        elif choice=="2":
            table=choose_table("Select table to search:")
            if table:
                term=input(Fore.WHITE+"Enter search term: ").strip()
                results=search_table(table, term)
                print_all_records(results, table)
        elif choice=="3":
            table=choose_table("Select table to add record to:")
            if table: add_record(table)
        elif choice=="4":
            table=choose_table("Select table to edit record:")
            if table: edit_record(table)
        elif choice=="5":
            table=choose_table("Select table to delete record from:")
            if table: delete_record(table)
        elif choice=="6":
            table=choose_table("Select table to export:")
            if table: export_to_csv(table)
        elif choice=="7":
            print(Fore.WHITE+"Exiting Verify Me CLI. Goodbye!"); break
        else: print(Fore.LIGHTRED_EX+"Invalid choice, try again.")

if __name__=="__main__":
    main_menu()
