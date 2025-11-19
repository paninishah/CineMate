# Exp 9 — Main frames & layout (with login on startup)
import tkinter as tk
from tkinter import ttk, messagebox
from frontend.ui.dialogs import LoginDialog, AddMovieDialog
from frontend.services import db_service as dbs

class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CineMate Lite")
        self.geometry("1100x650")
        self.configure(bg="white")
        self.logged_in_user = None

        self._build_menu()
        self._build_layout()

        # Prompt login immediately
        self.after(100, self._show_login)

    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import CSV", command=self._import_csv)
        file_menu.add_command(label="Export JSON", command=self._export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Add Movie", command=self._open_add_movie)
        menubar.add_cascade(label="Actions", menu=actions_menu)

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
        self.movie_list.bind("<<ListboxSelect>>", self._on_movie_select)

        # Right panel – Movie details
        right = tk.Frame(self, bg="white")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Movie Details", font=("Arial", 16), bg="white").pack(pady=15)

        # Placeholder area
        self.details_label = tk.Label(right, text="Select a movie to see details", bg="white")
        self.details_label.pack(pady=20)

    def _show_login(self):
        dlg = LoginDialog(self)
        self.wait_window(dlg)
        if getattr(dlg, "result", False):
            self.logged_in_user = dlg.username
            self._post_login_setup()
        else:
            # If login cancelled/failed, we can allow guest or exit. Here we exit.
            messagebox.showinfo("Login", "Login required. Exiting.")
            self.quit()

    def _post_login_setup(self):
        # Update title with username
        self.title(f"CineMate Lite — Logged in as {self.logged_in_user}")
        # Load movies into listbox (from temporary db_service)
        movies = dbs.get_all_movies()
        self.movie_list.delete(0, tk.END)
        for m in movies:
            self.movie_list.insert(tk.END, f"{m.get('title')} ({m.get('year','n/a')})")

    def _open_add_movie(self):
        AddMovieDialog(self)

    def _import_csv(self):
        messagebox.showinfo("Import", "CSV import coming soon (linked to Person C).")

    def _export_json(self):
        messagebox.showinfo("Export", "JSON export coming soon (linked to Person C).")

    def _on_movie_select(self, evt):
        w = evt.widget
        if not w.curselection():
            return
        idx = int(w.curselection()[0])
        text = w.get(idx)
        self.details_label.config(text=f"Details for: {text}\n(Details are placeholders)")
