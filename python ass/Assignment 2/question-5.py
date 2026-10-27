
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)
cur = db.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS contacts_db")
cur.execute("USE contacts_db")

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    category VARCHAR(30)
)
""")
db.commit()


def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_box.get()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Fill all fields")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showerror("Error", "Invalid email")
        return

    cur.execute(
        "INSERT INTO contacts (name,email,phone,category) VALUES (%s,%s,%s,%s)",
        (name, email, phone, category)
    )
    db.commit()
    messagebox.showinfo("Success", "Contact added")
    show_contacts()


def show_contacts():
    listbox.delete(0, tk.END)
    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        listbox.insert(tk.END, str(row))


def search_contact():
    keyword = search_entry.get().strip()
    cur.execute("""
        SELECT * FROM contacts
        WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    listbox.delete(0, tk.END)
    for row in cur.fetchall():
        listbox.insert(tk.END, str(row))


def delete_contact():
    try:
        selected = listbox.get(listbox.curselection())
        contact_id = int(selected.strip("()").split(",")[0])

        cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
        db.commit()
        show_contacts()
        print("Contact deleted")
    except (tk.TclError, ValueError):
        messagebox.showerror("Error", "Select a contact first")


def update_contact():
    try:
        selected = listbox.get(listbox.curselection())
        contact_id = int(selected.strip("()").split(",")[0])

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        category = category_box.get()

        if not name or not phone or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            messagebox.showerror("Error", "Enter valid contact details")
            return

        cur.execute("""
            UPDATE contacts
            SET name=%s, email=%s, phone=%s, category=%s
            WHERE id=%s
        """, (name, email, phone, category, contact_id))

        db.commit()
        show_contacts()
        print("Contact updated")
    except (tk.TclError, ValueError):
        messagebox.showerror("Error", "Select a contact first")


root = tk.Tk()
root.title("MySQL Contact Manager")
root.geometry("700x550")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=35)
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=35)
email_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root, width=35)
phone_entry.pack()

tk.Label(root, text="Category").pack()
category_box = ttk.Combobox(
    root, values=["Family", "Friends", "Work", "Other"],
    state="readonly"
)
category_box.set("Friends")
category_box.pack()

tk.Button(root, text="Add Contact", command=add_contact).pack(pady=3)
tk.Button(root, text="Update Contact", command=update_contact).pack(pady=3)
tk.Button(root, text="Delete Contact", command=delete_contact).pack(pady=3)

tk.Label(root, text="Search by name, email or phone").pack()
search_entry = tk.Entry(root, width=35)
search_entry.pack()

tk.Button(root, text="Search", command=search_contact).pack(pady=3)

listbox = tk.Listbox(root, width=90, height=12)
listbox.pack(pady=10)
listbox.bind("<Double-Button-1>", lambda event: fill_fields())

def fill_fields():
    try:
        row = listbox.get(listbox.curselection())
        contact_id, name, email, phone, category = eval(row)

        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        email_entry.delete(0, tk.END)
        email_entry.insert(0, email)
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, phone)
        category_box.set(category)
    except Exception:
        pass

show_contacts()
root.mainloop()

cur.close()
db.close()
