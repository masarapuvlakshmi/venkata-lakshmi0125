import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

CSV_FILE = "attendance.csv"
students = ["Alice", "Bob", "Charlie", "David", "Eva"]

def mark_attendance(status):
    date = date_entry.get()
    student = student_var.get()
    if not student:
        messagebox.showwarning("Input Error", "Please select a student.")
        return
    
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Student", "Attendance"])
        writer.writerow([date, student, status])
    
    messagebox.showinfo("Success", f"{student} marked as {status} on {date}")
    student_var.set('')  # clear selection

root = tk.Tk()
root.title("Attendance Marker")
root.geometry("350x250")

tk.Label(root, text="Select Date").pack(pady=5)
date_entry = DateEntry(root, width=18, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
date_entry.pack(pady=5)

tk.Label(root, text="Select Student").pack(pady=5)
student_var = tk.StringVar()
student_dropdown = ttk.Combobox(root, textvariable=student_var, values=students, state="readonly")
student_dropdown.pack(pady=5)

tk.Button(root, text="Mark Present", bg="green", fg="white", width=15,
          command=lambda: mark_attendance("Present")).pack(pady=10)

tk.Button(root, text="Mark Absent", bg="red", fg="white", width=15,
          command=lambda: mark_attendance("Absent")).pack()

root.mainloop()
