import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import sqlite3

# --- BACKEND SECTION ---
class DatabaseManager:
    def __init__(self, db_name="exam_room.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_table()

    def setup_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS seating (
                row_idx INTEGER, col_idx INTEGER, status TEXT,
                PRIMARY KEY (row_idx, col_idx)
            )
        ''')
        self.conn.commit()

    def save_layout(self, grid_data):
        self.cursor.execute("DELETE FROM seating")
        for entry in grid_data:
            self.cursor.execute(
                "INSERT INTO seating (row_idx, col_idx, status) VALUES (?, ?, ?)",
                (entry['row'], entry['col'], entry['status'])
            )
        self.conn.commit()

    def load_layout(self):
        self.cursor.execute("SELECT row_idx, col_idx, status FROM seating")
        return self.cursor.fetchall()

# --- FRONTEND SECTION ---
class SeatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Designer: All-in-One")
        self.db = DatabaseManager()
        
        self.rows, self.cols = 6, 8
        self.seats = []

        # UI Layout
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = tk.LabelFrame(self.main_container, text=" Student Management ", padx=10, pady=10)
        self.sidebar.pack(side="left", fill="y", padx=5)
        
        tk.Label(self.sidebar, text="Student Name:").pack(anchor="w")
        self.name_entry = tk.Entry(self.sidebar)
        self.name_entry.pack(fill="x", pady=5)
        
        tk.Button(self.sidebar, text="Add Manually", command=self.add_manual_student).pack(fill="x")
        tk.Button(self.sidebar, text="Import Excel", command=self.import_excel, bg="#fff9c4").pack(fill="x", pady=10)
        
        self.queue_listbox = tk.Listbox(self.sidebar, height=15)
        self.queue_listbox.pack(fill="x", pady=5)

        # Grid Side
        self.grid_container = tk.Frame(self.main_container)
        self.grid_container.pack(side="right", fill="both", expand=True)
        
        ctrl_frame = tk.Frame(self.grid_container)
        ctrl_frame.pack(fill="x", pady=5)
        tk.Button(ctrl_frame, text="Auto-Fill", command=self.auto_fill).pack(side="left", padx=2)
        tk.Button(ctrl_frame, text="Save", command=self.save_to_db).pack(side="left", padx=2)
        tk.Button(ctrl_frame, text="Load", command=self.load_from_db).pack(side="left", padx=2)
        tk.Button(ctrl_frame, text="Clear", command=self.reset_room).pack(side="left", padx=2)

        self.grid_frame = tk.Frame(self.grid_container, bg="gray80")
        self.grid_frame.pack(padx=10, pady=10)
        self.create_grid()

    def create_grid(self):
        for r in range(self.rows):
            row_list = []
            for c in range(self.cols):
                btn = tk.Button(self.grid_frame, text="Empty", width=10, height=2, bg="white",
                                command=lambda r=r, c=c: self.assign_student_to_seat(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_list.append(btn)
            self.seats.append(row_list)

    def add_manual_student(self):
        name = self.name_entry.get().strip()
        if name:
            self.queue_listbox.insert(tk.END, name)
            self.name_entry.delete(0, tk.END)

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                # 1. Clear the existing listbox first so data doesn't mix
                self.queue_listbox.delete(0, tk.END) 
                
                # 2. Read the new file
                df = pd.read_excel(file_path)
                
                # 3. Add the new names
                for name in df.iloc[:, 0].dropna().tolist():
                    self.queue_listbox.insert(tk.END, str(name))
                
                messagebox.showinfo("Success", "New student list loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read Excel: {e}")

    def assign_student_to_seat(self, r, c):
        selection = self.queue_listbox.curselection()
        btn = self.seats[r][c]
        if selection:
            name = self.queue_listbox.get(selection[0])
            btn.config(text=name, bg="#C8E6C9")
            self.queue_listbox.delete(selection[0])
        elif btn.cget("text") != "Empty":
            self.queue_listbox.insert(tk.END, btn.cget("text"))
            btn.config(text="Empty", bg="white")

    def auto_fill(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r + c) % 2 == 0 and self.queue_listbox.size() > 0:
                    name = self.queue_listbox.get(0)
                    self.seats[r][c].config(text=name, bg="#BBDEFB")
                    self.queue_listbox.delete(0)

    def save_to_db(self):
        data = [{'row': r, 'col': c, 'status': self.seats[r][c].cget("text")} 
                for r in range(self.rows) for c in range(self.cols)]
        self.db.save_layout(data)
        messagebox.showinfo("Done", "Saved!")

    def load_from_db(self):
        data = self.db.load_layout()
        for r, c, status in data:
            if status != "Empty":
                self.seats[r][c].config(text=status, bg="#C8E6C9")
            else:
                self.seats[r][c].config(text="Empty", bg="white")

    def reset_room(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.seats[r][c]
                if btn.cget("text") != "Empty":
                    self.queue_listbox.insert(tk.END, btn.cget("text"))
                    btn.config(text="Empty", bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingApp(root)
    root.mainloop()