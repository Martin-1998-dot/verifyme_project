import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("verifyme.db")
cursor = conn.cursor()

# Create professions table if it doesn't exist
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

# -------------------------------
# GUI SETUP
# -------------------------------
root = Tk()
root.title("Verify Me App - Professions")
root.geometry("800x500")
root.configure(bg="#E3F2FD")  # Soft blue for trust

# Styles
font_large = ("Helvetica", 12)
font_heading = ("Helvetica", 14, "bold")
button_style = {"font": font_large, "bg": "#4CAF50", "fg": "white", "width": 12}

# -------------------------------
# FUNCTIONS
# -------------------------------
def add_profession():
    def save():
        cursor.execute("""
        INSERT INTO professions (id_number, license_number, school, college, scandals, years_in_profession, specialization, current_employer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_number_var.get(), license_var.get(), school_var.get(), college_var.get(),
            scandals_var.get(), years_var.get(), specialization_var.get(), employer_var.get()
        ))
        conn.commit()
        messagebox.showinfo("Success", "Profession added successfully!")
        add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add Profession")
    add_window.geometry("400x400")
    add_window.configure(bg="#FFF3E0")

    id_number_var = StringVar()
    license_var = StringVar()
    school_var = StringVar()
    college_var = StringVar()
    scandals_var = StringVar()
    years_var = IntVar()
    specialization_var = StringVar()
    employer_var = StringVar()

    labels = ["ID Number", "License Number", "School", "College", "Scandals", "Years", "Specialization", "Employer"]
    vars = [id_number_var, license_var, school_var, college_var, scandals_var, years_var, specialization_var, employer_var]

    for i, (label_text, var) in enumerate(zip(labels, vars)):
        Label(add_window, text=label_text, bg="#FFF3E0", font=font_large).grid(row=i, column=0, padx=10, pady=5, sticky=W)
        Entry(add_window, textvariable=var, font=font_large).grid(row=i, column=1, padx=10, pady=5)

    Button(add_window, text="Save", command=save, **button_style).grid(row=len(labels), column=0, columnspan=2, pady=15)

def view_professions():
    cursor.execute("SELECT * FROM professions")
    records = cursor.fetchall()
    view_window = Toplevel(root)
    view_window.title("View Professions")
    view_window.geometry("900x400")
    view_window.configure(bg="#E8F5E9")

    tree = ttk.Treeview(view_window, columns=("id","id_number","license","school","college","scandals","years","specialization","employer"), show="headings")
    headings = ["ID","ID Number","License","School","College","Scandals","Years","Specialization","Employer"]
    for h in headings:
        tree.heading(h, text=h)
        tree.column(h, width=100)
    for row in records:
        tree.insert("", END, values=row)
    tree.pack(fill=BOTH, expand=True)

def delete_profession():
    def remove():
        cursor.execute("DELETE FROM professions WHERE id = ?", (id_var.get(),))
        conn.commit()
        messagebox.showinfo("Deleted", "Profession deleted successfully!")
        del_window.destroy()

    del_window = Toplevel(root)
    del_window.title("Delete Profession")
    del_window.geometry("300x150")
    del_window.configure(bg="#FFEBEE")
    id_var = IntVar()
    Label(del_window, text="Profession ID to delete:", bg="#FFEBEE", font=font_large).pack(pady=10)
    Entry(del_window, textvariable=id_var, font=font_large).pack(pady=5)
    Button(del_window, text="Delete", command=remove, **button_style).pack(pady=10)

# -------------------------------
# MAIN MENU
# -------------------------------
Label(root, text="Verify Me App - Professions", bg="#E3F2FD", font=("Helvetica", 18, "bold")).pack(pady=20)

menu_frame = Frame(root, bg="#E3F2FD")
menu_frame.pack(pady=10)

Button(menu_frame, text="Add Profession", command=add_profession, **button_style).grid(row=0, column=0, padx=10, pady=5)
Button(menu_frame, text="View Professions", command=view_professions, **button_style).grid(row=0, column=1, padx=10, pady=5)
Button(menu_frame, text="Delete Profession", command=delete_profession, **button_style).grid(row=0, column=2, padx=10, pady=5)

root.mainloop()
