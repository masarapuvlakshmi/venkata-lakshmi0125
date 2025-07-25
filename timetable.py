import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIMES = ['9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '2-3 PM', '3-4 PM']

# Professional pastel colors for subjects
SUBJECT_COLORS = {
    'Math': '#AED6F1',       # Light blue
    'Science': '#A9DFBF',    # Light green
    'English': '#F9E79F',    # Soft yellow
    'History': '#F5B7B1',    # Soft pink
    'Computer': '#D2B4DE',   # Lavender
}

DEFAULT_BG = '#F4F6F7'  # Light grey background
CELL_BG = '#FFFFFF'     # White cell background
HEADER_BG = '#2E4053'   # Dark blue header background
HEADER_FG = '#FDFEFE'   # White text for header

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Weekly Timetable Maker")
        self.root.geometry("950x650")
        self.root.config(bg=DEFAULT_BG)

        self.entries = {}  # {(day, time): label widget}

        # Input Frame with padding and nicer background
        input_frame = tk.Frame(root, bg=DEFAULT_BG)
        input_frame.pack(pady=15, padx=15, fill='x')

        tk.Label(input_frame, text="Day:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.day_var = tk.StringVar(value=DAYS[0])
        tk.OptionMenu(input_frame, self.day_var, *DAYS).config(font=("Helvetica", 12))
        tk.OptionMenu(input_frame, self.day_var, *DAYS).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Time:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.time_var = tk.StringVar(value=TIMES[0])
        tk.OptionMenu(input_frame, self.time_var, *TIMES).config(font=("Helvetica", 12))
        tk.OptionMenu(input_frame, self.time_var, *TIMES).grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Subject:", bg=DEFAULT_BG, font=("Helvetica", 12)).grid(row=0, column=4, padx=5)
        self.subject_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.subject_entry.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Add Subject", font=("Helvetica", 12, 'bold'), bg='#2874A6', fg='white', command=self.add_subject).grid(row=0, column=6, padx=10)

        # Timetable Frame
        self.grid_frame = tk.Frame(root, bg=DEFAULT_BG)
        self.grid_frame.pack(padx=15, pady=10, fill='both', expand=True)

        self.build_grid()

        # Export Frame with scrollable text box & export button
        export_frame = tk.Frame(root, bg=DEFAULT_BG)
        export_frame.pack(padx=15, pady=10, fill='both')

        tk.Label(export_frame, text="Exported Timetable Preview:", bg=DEFAULT_BG, font=("Helvetica", 14, 'bold')).pack(anchor='w')

        self.export_text = scrolledtext.ScrolledText(export_frame, width=100, height=10, font=("Consolas", 12), bg='#EBF5FB')
        self.export_text.pack(pady=5, fill='both', expand=True)

        tk.Button(export_frame, text="Export as Text File", font=("Helvetica", 12, 'bold'), bg='#117A65', fg='white', command=self.export_timetable).pack(pady=5)

    def build_grid(self):
        # Header row
        tk.Label(self.grid_frame, text="Time / Day", bg=HEADER_BG, fg=HEADER_FG,
                 font=("Helvetica", 12, 'bold'), relief='ridge', width=15, height=2).grid(row=0, column=0)

        for col, day in enumerate(DAYS):
            tk.Label(self.grid_frame, text=day, bg=HEADER_BG, fg=HEADER_FG,
                     font=("Helvetica", 12, 'bold'), relief='ridge', width=18, height=2).grid(row=0, column=col+1, sticky='nsew')

        # Time rows + cells
        for row, time in enumerate(TIMES):
            tk.Label(self.grid_frame, text=time, bg=HEADER_BG, fg=HEADER_FG,
                     font=("Helvetica", 11), relief='ridge', width=15, height=2).grid(row=row+1, column=0, sticky='nsew')
            for col in range(len(DAYS)):
                label = tk.Label(self.grid_frame, text="", bg=CELL_BG, relief="ridge",
                                 font=("Helvetica", 11), width=18, height=2, wraplength=120, justify='center')
                label.grid(row=row+1, column=col+1, sticky='nsew', padx=1, pady=1)
                self.entries[(DAYS[col], TIMES[row])] = label

        # Configure grid weights for responsiveness
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
        color = SUBJECT_COLORS.get(subject, "#D5D8DC")  # default light gray if subject unknown
        label.config(text=subject, bg=color)

        self.subject_entry.delete(0, tk.END)
        self.update_export_text()

    def update_export_text(self):
        # Build export string
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
