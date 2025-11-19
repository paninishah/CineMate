import tkinter as tk
from tkinter import ttk, messagebox

class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CineMate Lite")
        self.geometry("1100x650")
        self.configure(bg="white")

        self._build_menu()
        self._build_layout()

    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import CSV", command=self._import_csv)
        file_menu.add_command(label="Export JSON", command=self._export_json)
        menubar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menubar)

    def _build_layout(self):
        # Left panel – Movie list & search
        left = tk.Frame(self, width=300, bg="#f0f0f0")
        left.pack(side="left", fill="y")

        tk.Label(left, text="Search", bg="#f0f0f0").pack(pady=10)
        self.search_entry = tk.Entry(left)
        self.search_entry.pack(pady=5, padx=10, fill="x")

        self.movie_list = tk.Listbox(left)
        self.movie_list.pack(padx=10, pady=10, fill="both", expand=True)

        # Right panel – Movie details
        right = tk.Frame(self, bg="white")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Movie Details", font=("Arial", 16), bg="white").pack(pady=15)

        # Placeholder area
        self.details_label = tk.Label(right, text="Select a movie to see details", bg="white")
        self.details_label.pack(pady=20)

    # TODO functions — will link to Person C later
    def _import_csv(self):
        messagebox.showinfo("Import", "CSV import coming soon (linked to Person C).")

    def _export_json(self):
        messagebox.showinfo("Export", "JSON export coming soon (linked to Person C).")