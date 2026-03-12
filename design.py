import tkinter as tk
from tkinter import messagebox

class SeatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Room Designer")
        
        # Configuration
        self.rows = 6
        self.cols = 8
        self.seats = [] # To keep track of button objects

        # --- UI Setup ---
        self.header_label = tk.Label(root, text="Exam Seating Planner", font=("Times Square", 16, "bold"))
        self.header_label.pack(pady=10)

        # Control Frame
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        self.auto_btn = tk.Button(self.control_frame, text="Auto-Fill (Checkerboard)", command=self.auto_fill)
        self.auto_btn.grid(row=0, column=0, padx=5)

        self.reset_btn = tk.Button(self.control_frame, text="Reset Room", command=self.reset_room)
        self.reset_btn.grid(row=0, column=1, padx=5)

        # Grid Frame
        self.grid_frame = tk.Frame(root, bg="gray")
        self.grid_frame.pack(padx=20, pady=20)

        self.create_grid()

    def create_grid(self):
        """Generates the visual grid of buttons."""
        self.seats = []
        for r in range(self.rows):
            row_list = []
            for c in range(self.cols):
                btn = tk.Button(
                    self.grid_frame, 
                    text="Empty", 
                    width=8, 
                    height=2,
                    bg="white",
                    command=lambda r=r, c=c: self.toggle_seat(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_list.append(btn)
            self.seats.append(row_list)

    def toggle_seat(self, r, c):
        """Manual Placement: Toggles a seat between Occupied and Empty."""
        btn = self.seats[r][c]
        if btn.cget("text") == "Empty":
            btn.config(text="OCCUPIED", bg="#4CAF50", fg="white") # Green
        else:
            btn.config(text="Empty", bg="white", fg="black")

    def auto_fill(self):
        """Automatic Placement: Applies checkerboard logic."""
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.seats[r][c]
                # Logic: Place student if (row + col) is even
                if (r + c) % 2 == 0:
                    btn.config(text="OCCUPIED", bg="#2196F3", fg="white") # Blue
                else:
                    btn.config(text="Empty", bg="white", fg="black")

    def reset_room(self):
        """Clears all seats."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.seats[r][c].config(text="Empty", bg="white", fg="black")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingApp(root)
    root.mainloop()