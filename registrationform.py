import tkinter as tk
from tkinter import messagebox
import csv
import os

CSV_FILE = "course_registration.csv"

courses = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science"]

def register():
    name = name_var.get().strip()
    student_id = id_var.get().strip()
    selected_courses = [course for course, var in course_vars.items() if var.get() == 1]

    if not name or not student_id:
        messagebox.showwarning("Input Error", "Please enter Student Name and ID.")
        return

    if not selected_courses:
        messagebox.showwarning("Input Error", "Please select at least one course.")
        return

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Student Name", "Student ID", "Courses Registered"])
        writer.writerow([name, student_id, "; ".join(selected_courses)])

    messagebox.showinfo("Success", f"{name} registered for courses successfully!")

    # Clear inputs
    name_var.set("")
    id_var.set("")
    for var in course_vars.values():
        var.set(0)

root = tk.Tk()
root.title("Course Registration Form")
root.geometry("400x400")

# Variables
name_var = tk.StringVar()
id_var = tk.StringVar()
course_vars = {course: tk.IntVar() for course in courses}

# Labels and Entries
tk.Label(root, text="Student Name").pack(pady=5)
tk.Entry(root, textvariable=name_var).pack()

tk.Label(root, text="Student ID").pack(pady=5)
tk.Entry(root, textvariable=id_var).pack()

tk.Label(root, text="Available Courses").pack(pady=5)

# Checkboxes for courses
for course in courses:
    cb = tk.Checkbutton(root, text=course, variable=course_vars[course])
    cb.pack(anchor='w')

# Register button
tk.Button(root, text="Register", command=register, bg="green", fg="white").pack(pady=20)

root.mainloop()
