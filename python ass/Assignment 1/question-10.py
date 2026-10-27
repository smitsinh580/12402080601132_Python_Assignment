
import tkinter as tk
from tkinter import messagebox
import json
import csv
import os

file = "submissions.json"

if os.path.exists(file):
    with open(file, "r") as f:
        data = json.load(f)
else:
    data = []

def save():
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def add():
    name = name_entry.get().strip()
    assignment = assignment_entry.get().strip()
    marks = marks_entry.get().strip()

    if not name or not assignment:
        messagebox.showerror("Error", "Enter name and assignment")
        return

    if marks:
        try:
            marks = float(marks)
            if marks < 0 or marks > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Marks must be 0 to 100")
            return
    else:
        marks = ""

    data.append({
        "name": name,
        "assignment": assignment,
        "marks": marks,
        "status": "Completed" if marks != "" else "Pending"
    })

    save()
    show()
    name_entry.delete(0, tk.END)
    assignment_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def show():
    listbox.delete(0, tk.END)
    status = filter_var.get()

    for i, item in enumerate(data):
        if status == "All" or item["status"] == status:
            listbox.insert(
                tk.END,
                f"{i} | {item['name']} | {item['assignment']} | "
                f"{item['marks']} | {item['status']}"
            )

def update_marks():
    try:
        selected = listbox.get(listbox.curselection())
        index = int(selected.split("|")[0].strip())
        marks = float(marks_entry.get())

        if not 0 <= marks <= 100:
            raise ValueError

        data[index]["marks"] = marks
        data[index]["status"] = "Completed"
        save()
        show()

    except (ValueError, IndexError):
        messagebox.showerror("Error", "Select a record and enter marks from 0 to 100")

def export_csv():
    with open("report.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "assignment", "marks", "status"]
        )
        writer.writeheader()
        writer.writerows(data)

    messagebox.showinfo("Success", "Report exported to report.csv")

root = tk.Tk()
root.title("Assignment Tracker")
root.geometry("650x500")

tk.Label(root, text="Student Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Assignment").pack()
assignment_entry = tk.Entry(root)
assignment_entry.pack()

tk.Label(root, text="Marks").pack()
marks_entry = tk.Entry(root)
marks_entry.pack()

tk.Button(root, text="Add Submission", command=add).pack(pady=5)
tk.Button(root, text="Update Marks", command=update_marks).pack(pady=5)

filter_var = tk.StringVar(value="All")
tk.Label(root, text="Filter Status").pack()

tk.OptionMenu(
    root, filter_var, "All", "Pending", "Completed",
    command=lambda _: show()
).pack()

listbox = tk.Listbox(root, width=80, height=12)
listbox.pack(pady=10)

tk.Button(root, text="Export CSV", command=export_csv).pack()

show()
root.mainloop()
