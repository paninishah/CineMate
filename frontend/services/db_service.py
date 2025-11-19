# Exp 9 — temporary DB service for frontend login (Person B)
# Tries to use data/cine_mate.db's users table if available, otherwise uses an in-memory fallback.
import os
import hashlib
import sqlite3
from contextlib import closing

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "cine_mate.db")
DB_PATH = os.path.normpath(DB_PATH)

# In-memory fallback user store: username -> password_hash
_inmemory_users = {}

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def _init_inmemory():
    # seed a test user
    if "testuser" not in _inmemory_users:
        _inmemory_users["testuser"] = _hash_password("pass123")
        # also a second user
        _inmemory_users["alice"] = _hash_password("alicepwd")

def using_sqlite():
    # returns True if DB file and users table likely exist
    if not os.path.exists(DB_PATH):
        return False
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            return cur.fetchone() is not None
    except Exception:
        return False

# --------- Public API ---------

def create_user(username: str, password: str) -> bool:
    """
    Create a user. Returns True on success.
    If sqlite users table exists, insert there. Otherwise add to in-memory store.
    """
    pwd_hash = _hash_password(password)
    if using_sqlite():
        try:
            with closing(sqlite3.connect(DB_PATH)) as conn:
                cur = conn.cursor()
                cur.execute("""INSERT INTO users(username, email, password_hash) VALUES(?, ?, ?)""",
                            (username, "", pwd_hash))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False
    else:
        _init_inmemory()
        if username in _inmemory_users:
            return False
        _inmemory_users[username] = pwd_hash
        return True

def validate_user(username: str, password: str) -> bool:
    """
    Validate username/password.
    Checks sqlite users table if available, otherwise checks in-memory store.
    """
    pwd_hash = _hash_password(password)
    if using_sqlite():
        try:
            with closing(sqlite3.connect(DB_PATH)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
                row = cur.fetchone()
                if not row:
                    return False
                return row[0] == pwd_hash
        except Exception:
            # If something goes wrong, fallback to in-memory
            pass

    # fallback
    _init_inmemory()
    return _inmemory_users.get(username) == pwd_hash

def list_users():
    """Debug helper — returns list of usernames available (for UI testing only)."""
    if using_sqlite():
        try:
            with closing(sqlite3.connect(DB_PATH)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT username FROM users LIMIT 100")
                return [r[0] for r in cur.fetchall()]
        except Exception:
            pass
    _init_inmemory()
    return list(_inmemory_users.keys())
