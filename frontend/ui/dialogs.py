# Exp 9 — Dialog windows such as Login, Add/Edit Movie (Person B)
import tkinter as tk
from tkinter import ttk, messagebox
from frontend.services import db_service as dbs  # relative import via package structure

class LoginDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")
        self.geometry("350x200")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()  # modal

        # Username
        tk.Label(self, text="Username").pack(pady=(15, 4))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(fill="x", padx=20)

        # Password
        tk.Label(self, text="Password").pack(pady=(10, 4))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(fill="x", padx=20)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Login", width=10, command=self._on_login).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Create User", width=10, command=self._on_create).pack(side="left")

        # Status label
        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack(pady=(5,0))

        # focus
        self.username_entry.focus_set()
        self.result = False
        self.username = None

    def _on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password")
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
            messagebox.showwarning("Create user", "Please provide both username and password")
            return
        created = dbs.create_user(username, password)
        if created:
            messagebox.showinfo("Create user", f"User '{username}' created. You can now login.")
        else:
            messagebox.showerror("Create user", f"Could not create user '{username}'. It may already exist.")

# Keep the AddMovieDialog from previous starter (slightly updated)
class AddMovieDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Movie")
        self.geometry("420x380")
        self.resizable(False, False)
        self.transient(master)

        tk.Label(self, text="Title").pack(pady=6)
        self.title_entry = tk.Entry(self)
        self.title_entry.pack(fill="x", padx=20)

        tk.Label(self, text="Year").pack(pady=6)
        self.year_entry = tk.Entry(self)
        self.year_entry.pack(fill="x", padx=20)

        tk.Label(self, text="Genres (comma-separated)").pack(pady=6)
        self.genres_entry = tk.Entry(self)
        self.genres_entry.pack(fill="x", padx=20)

        tk.Label(self, text="Synopsis").pack(pady=6)
        self.synopsis_text = tk.Text(self, height=6)
        self.synopsis_text.pack(fill="both", padx=20, pady=(0,10))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Save", command=self._save).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left")

    def _save(self):
        # Placeholder: in future call db_service.add_movie()
        title = self.title_entry.get().strip()
        year = self.year_entry.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required")
            return
        # For now just print and close
        print("Saved movie:", title, year)
        messagebox.showinfo("Saved", f"Movie '{title}' saved (placeholder).")
        self.destroy()
