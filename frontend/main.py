import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CineMate Lite")
        self.geometry("1000x600")
        self.build_layout()

    def build_layout(self):
        # Left frame (movie list + search)
        left = tk.Frame(self, width=300, bg="#eee")
        left.pack(side="left", fill="y")

        # Right frame (details)
        right = tk.Frame(self, bg="white")
        right.pack(side="right", expand=True, fill="both")

if __name__ == "__main__":
    App().mainloop()