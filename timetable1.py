import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIMES = ['9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '2-3 PM', '3-4 PM']

SUBJECT_COLORS = {
    'Math': '#AED6F1',
    'Science': '#A9DFBF',
    'English': '#F9E79F',
    'History': '#F5B7B1',
    'Computer': '#D2B4DE',
}

DEFAULT_BG = '#F4F6F7'
CELL_BG = '#FFFFFF'
HEADER_BG = '#2E4053'
HEADER_FG = '#FDFEFE'

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Timetable with CSV Save")
        self.root.geometry("950x650")
        self.root.config(bg=DEFAULT_BG)

        self.entries = {}

        input_frame = tk.Frame(root, bg=DEFAULT_BG)
        input_frame.pack(pady=15, padx=15, fill='x')

        tk.Label(input_frame, text="Day:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.day_var = tk.StringVar(value=DAYS[0])
        tk.OptionMenu(input_frame, self.day_var, *DAYS).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Time:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.time_var = tk.StringVar(value=TIMES[0])
        tk.OptionMenu(input_frame, self.time_var, *TIMES).grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Subject:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=4, padx=5)
        self.subject_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.subject_entry.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Add Subject", font=("Helvetica", 12, 'bold'),
                  bg='#2874A6', fg='white', command=self.add_subject).grid(row=0, column=6, padx=10)

        # Submit button to save data to CSV
        tk.Button(input_frame, text="Submit & Save to CSV", font=("Helvetica", 12, 'bold'),
                  bg='#27AE60', fg='white', command=self.submit_to_csv).grid(row=0, column=7, padx=10)

        self.grid_frame = tk.Frame(root, bg=DEFAULT_BG)
        self.grid_frame.pack(padx=15, pady=10, fill='both', expand=True)

        self.build_grid()

        export_frame = tk.Frame(root, bg=DEFAULT_BG)
        export_frame.pack(padx=15, pady=10, fill='both')

        tk.Label(export_frame, text="Exported Timetable Preview:", bg=DEFAULT_BG,
                 font=("Helvetica", 14, 'bold')).pack(anchor='w')

        self.export_text = scrolledtext.ScrolledText(export_frame, width=100, height=10,
                                                     font=("Consolas", 12), bg='#EBF5FB')
        self.export_text.pack(pady=5, fill='both', expand=True)

        tk.Button(export_frame, text="Export as Text File", font=("Helvetica", 12, 'bold'),
                  bg='#117A65', fg='white', command=self.export_timetable).pack(pady=5)

    def build_grid(self):
        tk.Label(self.grid_frame, text="Time / Day", bg=HEADER_BG, fg=HEADER_FG,
                 font=("Helvetica", 12, 'bold'), relief='ridge', width=15, height=2).grid(row=0, column=0)

        for col, day in enumerate(DAYS):
            tk.Label(self.grid_frame, text=day, bg=HEADER_BG, fg=HEADER_FG,
                     font=("Helvetica", 12, 'bold'), relief='ridge', width=18, height=2).grid(row=0, column=col+1, sticky='nsew')

        for row, time in enumerate(TIMES):
            tk.Label(self.grid_frame, text=time, bg=HEADER_BG, fg=HEADER_FG,
                     font=("Helvetica", 11), relief='ridge', width=15, height=2).grid(row=row+1, column=0, sticky='nsew')
            for col in range(len(DAYS)):
                label = tk.Label(self.grid_frame, text="", bg=CELL_BG, relief="ridge",
                                 font=("Helvetica", 11), width=18, height=2, wraplength=120, justify='center')
                label.grid(row=row+1, column=col+1, sticky='nsew', padx=1, pady=1)
                self.entries[(DAYS[col], TIMES[row])] = label

        for i in range(len(TIMES)+1):
            self.grid_frame.rowconfigure(i, weight=1)
        for j in range(len(DAYS)+1):
            self.grid_frame.columnconfigure(j, weight=1)

    def add_subject(self):
        day = self.day_var.get()
        time = self.time_var.get()
        subject = self.subject_entry.get().strip()

        if not subject:
            messagebox.showwarning("Input Error", "Please enter a subject.")
            return

        label = self.entries[(day, time)]
        label.config(text=subject, bg=SUBJECT_COLORS.get(subject, "#D5D8DC"))

        self.subject_entry.delete(0, tk.END)
        self.update_export_text()

    def update_export_text(self):
        lines = ["Weekly Timetable\n"]
        header_line = "Time/Day\t" + "\t".join(DAYS)
        lines.append(header_line)

        for time in TIMES:
            row = [time]
            for day in DAYS:
                subject = self.entries[(day, time)].cget("text")
                row.append(subject if subject else "-")
            lines.append("\t".join(row))

        full_text = "\n".join(lines)
        self.export_text.delete(1.0, tk.END)
        self.export_text.insert(tk.END, full_text)

    def export_timetable(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")],
                                                title="Save Timetable As")
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(self.export_text.get(1.0, tk.END))
        messagebox.showinfo("Export Successful", "Timetable exported successfully!")

    def submit_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv")],
                                                title="Save Timetable As CSV")
        if not filename:
            return

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write header row
                writer.writerow(["Time / Day"] + DAYS)

                # Write timetable data
                for time in TIMES:
                    row = [time]
                    for day in DAYS:
                        subject = self.entries[(day, time)].cget("text")
                        row.append(subject if subject else "")
                    writer.writerow(row)

            messagebox.showinfo("Saved", f"Timetable saved as CSV file:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
