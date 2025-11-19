import tkinter as tk

class LabeledEntry(tk.Frame):
    def __init__(self, master, label, **kwargs):
        super().__init__(master)
        tk.Label(self, text=label).pack(side="left")
        self.entry = tk.Entry(self, **kwargs)
        self.entry.pack(side="right", fill="x", expand=True)