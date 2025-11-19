import tkinter as tk
from tkinter import ttk

class AddMovieDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Movie")
        self.geometry("400x350")

        tk.Label(self, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.pack(pady=5)

        tk.Label(self, text="Year").pack(pady=5)
        self.year_entry = tk.Entry(self)
        self.year_entry.pack(pady=5)

        tk.Button(self, text="Save", command=self._save).pack(pady=20)

    def _save(self):
        # TODO: connect to db_service.add_movie()
        print("Movie saved (placeholder)")
        self.destroy()