# Exp 9 — Main frames & layout (Letterboxd-style theme)
import tkinter as tk
from tkinter import messagebox
from frontend.ui.dialogs import LoginDialog, AddMovieDialog
from frontend.services import db_service as dbs

# Theme (Letterboxd-like)
BG = "#0b0b0b"
PANEL = "#0f1110"
TEXT = "#eaf7ee"
ACCENT = "#2ecc71"
ENTRY_BG = "#121212"
MUTED = "#9aa39a"

class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CineMate Lite")
        self.geometry("1100x650")
        self.configure(bg=BG)
        self.logged_in_user = None

        self._build_menu()
        self._build_layout()

        # Prompt login shortly after startup
        self.after(100, self._show_login)

    def _build_menu(self):
        menubar = tk.Menu(self, bg=PANEL, fg=TEXT)
        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        file_menu.add_command(label="Import CSV", command=self._import_csv)
        file_menu.add_command(label="Export JSON", command=self._export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        actions_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        actions_menu.add_command(label="Add Movie", command=self._open_add_movie)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        # Add a simple account label/menu
        account_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        account_menu.add_command(label="Logout", command=self._logout)
        menubar.add_cascade(label="Account", menu=account_menu)

        self.config(menu=menubar)

    def _build_layout(self):
        # Left panel – Movie list & search
        left = tk.Frame(self, width=320, bg=PANEL)
        left.pack(side="left", fill="y")

        tk.Label(left, text="CineMate", bg=PANEL, fg=ACCENT, font=("Helvetica", 16, "bold")).pack(pady=(12,6))
        tk.Label(left, text="Search", bg=PANEL, fg=MUTED).pack(pady=(6,2))
        self.search_entry = tk.Entry(left, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
        self.search_entry.pack(pady=6, padx=12, fill="x")

        # Buttons row
        btn_row = tk.Frame(left, bg=PANEL)
        btn_row.pack(padx=12, pady=(0,8), fill="x")
        tk.Button(btn_row, text="Search", bg=ACCENT, fg="black", relief="flat", command=self._on_search).pack(side="left", padx=(0,6))
        tk.Button(btn_row, text="Clear", bg="#2b2b2b", fg=TEXT, relief="flat", command=self._on_clear).pack(side="left")

        # Movie list
        self.movie_list = tk.Listbox(left, bg=ENTRY_BG, fg=TEXT, selectbackground=ACCENT, activestyle="none")
        self.movie_list.pack(padx=12, pady=6, fill="both", expand=True)
        self.movie_list.bind("<<ListboxSelect>>", self._on_movie_select)

        # Right panel – Movie details
        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        header = tk.Frame(right, bg=BG)
        header.pack(fill="x", pady=12)
        self.title_label = tk.Label(header, text="Movie Details", font=("Helvetica", 16, "bold"), bg=BG, fg=TEXT)
        self.title_label.pack(side="left", padx=12)

        # Details area
        body = tk.Frame(right, bg=BG)
        body.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # Poster placeholder (left) and text on right
        poster_frame = tk.Frame(body, bg=PANEL, width=220, height=320)
        poster_frame.pack(side="left", padx=(0,12), pady=6)
        poster_frame.pack_propagate(False)
        self.poster_label = tk.Label(poster_frame, text="Poster\n(placeholder)", bg=PANEL, fg=MUTED)
        self.poster_label.pack(expand=True)

        info_frame = tk.Frame(body, bg=BG)
        info_frame.pack(side="right", fill="both", expand=True)

        self.details_label = tk.Label(info_frame, text="Select a movie from the left to see details.", bg=BG, fg=TEXT, justify="left", wraplength=600)
        self.details_label.pack(anchor="nw", pady=(6,0))

        # Bottom status bar
        self.status_var = tk.StringVar(value="Not logged in")
        status_bar = tk.Label(self, textvariable=self.status_var, bg=PANEL, fg=MUTED)
        status_bar.pack(side="bottom", fill="x")

    # ----- Login / session -----
    def _show_login(self):
        dlg = LoginDialog(self)
        self.wait_window(dlg)
        if getattr(dlg, "result", False):
            self.logged_in_user = dlg.username
            self._post_login_setup()
        else:
            messagebox.showinfo("Login", "Login required. Exiting.")
            self.quit()

    def _post_login_setup(self):
        self.title(f"CineMate Lite — {self.logged_in_user}")
        self.status_var.set(f"Logged in as {self.logged_in_user}")
        self._load_movies()

    def _logout(self):
        self.logged_in_user = None
        self.status_var.set("Logged out")
        # Re-show login
        self.after(100, self._show_login)

    # ----- Movie list & actions -----
    def _load_movies(self):
        movies = dbs.get_all_movies()
        self.movie_list.delete(0, tk.END)
        for m in movies:
            display = f"{m.get('title', 'Untitled')} ({m.get('year','n/a')})"
            self.movie_list.insert(tk.END, display)

    def _on_search(self):
        q = self.search_entry.get().strip().lower()
        if not q:
            self._load_movies()
            return
        # simple client-side search over placeholder list
        movies = dbs.get_all_movies()
        filtered = [m for m in movies if q in m.get("title","").lower() or q in (m.get("genres") or "").lower()]
        self.movie_list.delete(0, tk.END)
        for m in filtered:
            self.movie_list.insert(tk.END, f"{m.get('title')} ({m.get('year','n/a')})")

    def _on_clear(self):
        self.search_entry.delete(0, tk.END)
        self._load_movies()

    def _open_add_movie(self):
        dlg = AddMovieDialog(self)
        self.wait_window(dlg)
        # If AddMovieDialog stored a flag or printed, reload movies:
        self._load_movies()

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
        # For now show placeholder details — later fetch by id
        self.details_label.config(text=f"Details for: {text}\n\n(Details are placeholders)")
