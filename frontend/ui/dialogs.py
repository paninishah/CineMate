# Exp 9 — Dialog windows (styled to match Letterboxd-like theme)
import tkinter as tk
from tkinter import messagebox
from frontend.services import db_service as dbs

# Match the theme constants
BG = "#0b0b0b"
PANEL = "#0f1110"
TEXT = "#eaf7ee"
ACCENT = "#2ecc71"
ENTRY_BG = "#121212"
MUTED = "#9aa39a"

class LoginDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login to CineMate")
        self.geometry("360x220")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.configure(bg=BG)

        tk.Label(self, text="CineMate Login", bg=BG, fg=ACCENT, font=("Helvetica", 14, "bold")).pack(pady=(12,6))

        # Username
        tk.Label(self, text="Username", bg=BG, fg=MUTED).pack(anchor="w", padx=24, pady=(6,0))
        self.username_entry = tk.Entry(self, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.username_entry.pack(fill="x", padx=24, pady=(0,6))

        # Password
        tk.Label(self, text="Password", bg=BG, fg=MUTED).pack(anchor="w", padx=24, pady=(6,0))
        self.password_entry = tk.Entry(self, show="*", bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.password_entry.pack(fill="x", padx=24, pady=(0,6))

        # Buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Login", bg=ACCENT, fg="black", width=12, relief="flat", command=self._on_login).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Create User", bg="#2b2b2b", fg=TEXT, width=12, relief="flat", command=self._on_create).pack(side="left")

        self.status_label = tk.Label(self, text="", bg=BG, fg="red")
        self.status_label.pack(pady=(4,0))

        self.username_entry.focus_set()
        self.result = False
        self.username = None

    def _on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Login", "Enter both username and password")
            return
        ok = dbs.validate_user(username, password)
        if ok:
            self.result = True
            self.username = username
            self.grab_release()
            self.destroy()
        else:
            self.status_label.config(text="Invalid credentials")

    def _on_create(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Create user", "Please provide username and password")
            return
        created = dbs.create_user(username, password)
        if created:
            messagebox.showinfo("Create user", f"User '{username}' created. You can now login.")
        else:
            messagebox.showerror("Create user", f"Could not create user '{username}'. It may already exist.")

class AddMovieDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Movie")
        self.geometry("460x420")
        self.resizable(False, False)
        self.transient(master)
        self.configure(bg=BG)

        tk.Label(self, text="Add a Movie", bg=BG, fg=ACCENT, font=("Helvetica", 13, "bold")).pack(pady=(12,6))

        # Title
        tk.Label(self, text="Title", bg=BG, fg=MUTED).pack(anchor="w", padx=20, pady=(8,0))
        self.title_entry = tk.Entry(self, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.title_entry.pack(fill="x", padx=20, pady=(0,6))

        # Year
        tk.Label(self, text="Year", bg=BG, fg=MUTED).pack(anchor="w", padx=20, pady=(8,0))
        self.year_entry = tk.Entry(self, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.year_entry.pack(fill="x", padx=20, pady=(0,6))

        # Genres
        tk.Label(self, text="Genres (comma-separated)", bg=BG, fg=MUTED).pack(anchor="w", padx=20, pady=(8,0))
        self.genres_entry = tk.Entry(self, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.genres_entry.pack(fill="x", padx=20, pady=(0,6))

        # Synopsis
        tk.Label(self, text="Synopsis", bg=BG, fg=MUTED).pack(anchor="w", padx=20, pady=(8,0))
        self.synopsis_text = tk.Text(self, height=6, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.synopsis_text.pack(fill="both", padx=20, pady=(0,8))

        # Buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Save", bg=ACCENT, fg="black", width=12, relief="flat", command=self._save).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", bg="#2b2b2b", fg=TEXT, width=12, relief="flat", command=self.destroy).pack(side="left")

    def _save(self):
        title = self.title_entry.get().strip()
        year = self.year_entry.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required")
            return
        movie = {"title": title, "year": year, "genres": self.genres_entry.get().strip(), "synopsis": self.synopsis_text.get("1.0","end").strip()}
        # Try saving via db service; it will fallback to in-memory if needed.
        new_id = dbs.add_movie(movie)
        if new_id:
            messagebox.showinfo("Saved", f"Movie '{title}' saved.")
        else:
            messagebox.showwarning("Save failed", "Could not save movie (placeholder).")
        self.destroy()
