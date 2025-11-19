# Exp 9 — Reusable GUI widgets (styled)
import tkinter as tk

BG = "#0b0b0b"
ENTRY_BG = "#121212"
TEXT = "#eaf7ee"
MUTED = "#9aa39a"

class LabeledEntry(tk.Frame):
    def __init__(self, master, label, entry_width=30, **kwargs):
        super().__init__(master, bg=BG)
        tk.Label(self, text=label, bg=BG, fg=MUTED).pack(side="left", padx=(0,8))
        self.entry = tk.Entry(self, width=entry_width, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT, **kwargs)
        self.entry.pack(side="right", fill="x", expand=True)
