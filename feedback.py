import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv
import os

class FeedbackFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher/Course Feedback Form")
        self.root.geometry("800x750")
        self.root.configure(bg="#2C3E50")  # Dark blue background
        self.root.resizable(False, False)

        self.questions = [
            "Rate the teacher's clarity:",
            "Rate the course content:",
            "Was the pace of the class appropriate?",
            "Would you recommend this course/teacher?"
        ]

        self.ratings_vars = []
        self.yn_vars = []

        # Main container frame with padding and background
        main_frame = tk.Frame(root, bg="#34495E", padx=40, pady=30)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = tk.Label(main_frame, text="Teacher / Course Feedback Form",
                               font=("Segoe UI", 28, "bold"), fg="#ECF0F1", bg="#34495E")
        title_label.pack(pady=(0, 30))

        form_frame = tk.Frame(main_frame, bg="#34495E")
        form_frame.pack(fill='x')

        # Ratings 1-5 questions with sleek radio buttons
        for i, question in enumerate(self.questions[:2]):
            q_label = tk.Label(form_frame, text=question, font=("Segoe UI", 16), fg="#ECF0F1", bg="#34495E")
            q_label.pack(anchor='w', pady=(18, 8))

            rating_var = tk.IntVar(value=0)
            self.ratings_vars.append(rating_var)

            rating_frame = tk.Frame(form_frame, bg="#34495E")
            rating_frame.pack(anchor='w')

            for val in range(1, 6):
                rb = tk.Radiobutton(rating_frame, text=str(val), variable=rating_var, value=val,
                                    font=("Segoe UI", 14), bg="#34495E", fg="#ECF0F1",
                                    activebackground="#5DADE2", activeforeground="#1B4F72",
                                    selectcolor="#85C1E9", cursor="hand2", indicatoron=0,
                                    width=3, bd=0, relief='ridge')
                rb.pack(side='left', padx=10, pady=4)

        # Yes/No questions with radio buttons styled as toggle buttons
        for question in self.questions[2:]:
            q_label = tk.Label(form_frame, text=question, font=("Segoe UI", 16), fg="#ECF0F1", bg="#34495E")
            q_label.pack(anchor='w', pady=(25, 8))

            yn_var = tk.StringVar(value="")
            self.yn_vars.append(yn_var)

            yn_frame = tk.Frame(form_frame, bg="#34495E")
            yn_frame.pack(anchor='w')

            rb_yes = tk.Radiobutton(yn_frame, text="Yes", variable=yn_var, value="Yes",
                                    font=("Segoe UI", 14), bg="#34495E", fg="#ECF0F1",
                                    activebackground="#58D68D", activeforeground="#145A32",
                                    selectcolor="#58D68D", cursor="hand2", indicatoron=0,
                                    width=8, bd=0, relief='ridge')
            rb_yes.pack(side='left', padx=15, pady=5)

            rb_no = tk.Radiobutton(yn_frame, text="No", variable=yn_var, value="No",
                                   font=("Segoe UI", 14), bg="#34495E", fg="#ECF0F1",
                                   activebackground="#EC7063", activeforeground="#641E16",
                                   selectcolor="#EC7063", cursor="hand2", indicatoron=0,
                                   width=8, bd=0, relief='ridge')
            rb_no.pack(side='left', padx=15, pady=5)

        # Comments Label and Textbox with scrollbar, styled nicely
        comment_label = tk.Label(form_frame, text="Additional Comments:", font=("Segoe UI", 16), fg="#ECF0F1", bg="#34495E")
        comment_label.pack(anchor='w', pady=(30, 10))

        self.comments_text = tk.Text(form_frame, height=8, width=75, font=("Segoe UI", 14), wrap='word',
                                     bd=2, relief='sunken', bg="#ECF0F1", fg="#2C3E50", insertbackground="#2C3E50")
        self.comments_text.pack(pady=(0, 30))

        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg="#34495E")
        btn_frame.pack(fill='x', pady=(0, 25))

        submit_btn = tk.Button(btn_frame, text="Submit Feedback", font=("Segoe UI", 16, "bold"),
                               bg="#2980B9", fg="white", activebackground="#1B4F72",
                               padx=25, pady=12, command=self.submit_feedback, cursor="hand2", bd=0)
        submit_btn.pack(side='left', padx=15)

        export_btn = tk.Button(btn_frame, text="Export Feedback as .py", font=("Segoe UI", 16, "bold"),
                               bg="#27AE60", fg="white", activebackground="#196F3D",
                               padx=25, pady=12, command=self.export_feedback_py, cursor="hand2", bd=0)
        export_btn.pack(side='left', padx=15)

        clear_btn = tk.Button(btn_frame, text="Clear Form", font=("Segoe UI", 16, "bold"),
                              bg="#C0392B", fg="white", activebackground="#78281F",
                              padx=25, pady=12, command=self.reset_form, cursor="hand2", bd=0)
        clear_btn.pack(side='left', padx=15)

        # ScrolledText to show exported feedback preview (read-only)
        preview_label = tk.Label(main_frame, text="Exported Feedback Preview:",
                                 font=("Segoe UI", 20, "bold"),
                                 fg="#ECF0F1", bg="#34495E")
        preview_label.pack(anchor='w', pady=(0, 10))

        self.preview_text = scrolledtext.ScrolledText(main_frame, width=85, height=14,
                                                      font=("Consolas", 13), bg="#1B2631", fg="#D5D8DC",
                                                      state='disabled', bd=0)
        self.preview_text.pack()

    def submit_feedback(self):
        # Validate rating questions
        for idx, var in enumerate(self.ratings_vars):
            if var.get() == 0:
                messagebox.showwarning("Incomplete Form", f"Please rate: '{self.questions[idx]}'")
                return

        # Validate yes/no questions
        for idx, var in enumerate(self.yn_vars):
            if var.get() not in ("Yes", "No"):
                messagebox.showwarning("Incomplete Form", f"Please answer: '{self.questions[idx+2]}'")
                return

        data = {
            "Clarity Rating": self.ratings_vars[0].get(),
            "Content Rating": self.ratings_vars[1].get(),
            "Pace Appropriate": self.yn_vars[0].get(),
            "Recommend": self.yn_vars[1].get(),
            "Comments": self.comments_text.get("1.0", tk.END).strip()
        }

        file_exists = os.path.isfile("feedback_submissions.csv")
        with open("feedback_submissions.csv", "a", newline="", encoding='utf-8') as csvfile:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        messagebox.showinfo("Thank you!", "Your feedback has been submitted successfully.")
        self.reset_form()
        self.update_preview()

    def reset_form(self):
        for var in self.ratings_vars:
            var.set(0)
        for var in self.yn_vars:
            var.set("")
        self.comments_text.delete("1.0", tk.END)

    def update_preview(self):
        # Load CSV and format preview nicely
        if not os.path.isfile("feedback_submissions.csv"):
            self.preview_text.configure(state='normal')
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, "No feedback submissions yet.")
            self.preview_text.configure(state='disabled')
            return

        with open("feedback_submissions.csv", "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lines = []
            for idx, row in enumerate(reader, start=1):
                lines.append(f"Feedback Entry #{idx}")
                lines.append("-" * 60)
                for key, val in row.items():
                    lines.append(f"{key:<18}: {val}")
                lines.append("-" * 60)
                lines.append("")

        preview_text = "\n".join(lines)

        self.preview_text.configure(state='normal')
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, preview_text)
        self.preview_text.configure(state='disabled')

    def export_feedback_py(self):
        # Export preview content as .py file with formatted text in a Python string literal
        if not os.path.isfile("feedback_submissions.csv"):
            messagebox.showinfo("No Data", "No feedback submissions found to export.")
            return

        self.update_preview()

        preview_content = self.preview_text.get("1.0", tk.END).strip()
        if not preview_content:
            messagebox.showinfo("No Data", "No feedback submissions found to export.")
            return

        # Ask user to save file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py")],
            title="Save feedback as Python (.py) file"
        )

        if save_path:
            # Create a Python file containing the feedback preview as a variable
            with open(save_path, "w", encoding='utf-8') as f:
                f.write("# Exported Feedback Data\n")
                f.write("feedback_data = '''\n")
                f.write(preview_content)
                f.write("\n'''\n")

            messagebox.showinfo("Exported", f"Feedback exported successfully as Python file:\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackFormApp(root)
    app.update_preview()  # Show any existing data on startup
    root.mainloop()
