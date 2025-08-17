import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to your database
DB_PATH = "verifyme.db"

def query_table(table_name):
    """Fetch all rows from a table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return []

# GUI setup
root = tk.Tk()
root.title("Verify Me App - Desktop GUI")
root.geometry("800x500")

# Tabs for Cars, Companies, Houses, Professions
tab_control = ttk.Notebook(root)
tabs = {}
for name in ["Cars", "Companies", "Houses", "Professions"]:
    frame = ttk.Frame(tab_control)
    tab_control.add(frame, text=name)
    tabs[name] = frame

tab_control.pack(expand=1, fill="both")

# Function to populate a table in a tab
def populate_tab(tab_name):
    frame = tabs[tab_name]
    for widget in frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame)
    tree.pack(expand=1, fill="both")
    
    # Get data
    rows = query_table(tab_name.lower())
    if not rows:
        return

    # Set columns
    tree["columns"] = [f"col{i}" for i in range(len(rows[0]))]
    tree["show"] = "headings"
    for i in range(len(rows[0])):
        tree.heading(f"col{i}", text=f"Col {i+1}")
        tree.column(f"col{i}", width=100)

    for row in rows:
        tree.insert("", "end", values=row)

# Add a refresh button to each tab
for name in tabs:
    btn = ttk.Button(tabs[name], text="Load Data", command=lambda n=name: populate_tab(n))
    btn.pack(side="top", pady=5)

root.mainloop()
