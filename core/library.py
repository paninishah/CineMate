import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import Movie
import os
import pytz

IST = pytz.timezone('Asia/Kolkata')

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'cine_mate.db'))

def _ensure_dir_exists(path: str):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)

class Library:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_PATH
        _ensure_dir_exists(self.db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genres TEXT,
            tags TEXT,
            synopsis TEXT,
            poster_path TEXT,
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            user_id INTEGER,
            rating INTEGER,
            created_at TEXT,
            FOREIGN KEY(movie_id) REFERENCES movies(id)
        );
        CREATE TABLE IF NOT EXISTS watchlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT
        );
        CREATE TABLE IF NOT EXISTS watchlist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            watchlist_id INTEGER,
            movie_id INTEGER
        );
        ''')
        self.conn.commit()

    def add_movie(self, title: str, year: Optional[int], genres: List[str], tags: List[str], synopsis: str, poster_path: Optional[str]) -> int:
        cur = self.conn.cursor()
        created_at = datetime.now(IST).isoformat()
        cur.execute(
            '''INSERT INTO movies (title, year, genres, tags, synopsis, poster_path, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (title, year, ','.join(genres), ','.join(tags), synopsis, poster_path, created_at)
        )
        self.conn.commit()
        return cur.lastrowid

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM movies WHERE id=?', (movie_id,))
        row = cur.fetchone()
        if not row:
            return None
        return Movie(
            id=row['id'],
            title=row['title'],
            year=row['year'],
            genres=row['genres'].split(',') if row['genres'] else [],
            tags=row['tags'].split(',') if row['tags'] else [],
            synopsis=row['synopsis'] or '',
            poster_path=row['poster_path'],
            created_at=datetime.fromisoformat(row['created_at'])
        )

    def update_movie(self, movie_id: int, **fields) -> bool:
        allowed = ['title', 'year', 'genres', 'tags', 'synopsis', 'poster_path']
        set_parts, values = [], []
        for k, v in fields.items():
            if k in allowed:
                set_parts.append(f"{k}=?")
                v = ','.join(v) if k in ('genres', 'tags') and isinstance(v, list) else v
                values.append(v)
        if not set_parts:
            return False
        values.append(movie_id)
        cur = self.conn.cursor()
        cur.execute(f"UPDATE movies SET {', '.join(set_parts)} WHERE id=?", values)
        self.conn.commit()
        return cur.rowcount > 0

    def delete_movie(self, movie_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute('DELETE FROM movies WHERE id=?', (movie_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def list_movies(self, filters: Optional[Dict[str, Any]] = None) -> List[Movie]:
        q = 'SELECT * FROM movies'
        params, clauses = [], []
        if filters:
            if 'title' in filters:
                clauses.append('title LIKE ?')
                params.append(f"%{filters['title']}%")
            if 'genre' in filters:
                clauses.append('genres LIKE ?')
                params.append(f"%{filters['genre']}%")
            if clauses:
                q += ' WHERE ' + ' AND '.join(clauses)
        q += ' ORDER BY created_at DESC'
        cur = self.conn.cursor()
        cur.execute(q, params)
        rows = cur.fetchall()
        return [
            Movie(
                id=row['id'],
                title=row['title'],
                year=row['year'],
                genres=row['genres'].split(',') if row['genres'] else [],
                tags=row['tags'].split(',') if row['tags'] else [],
                synopsis=row['synopsis'] or '',
                poster_path=row['poster_path'],
                created_at=datetime.fromisoformat(row['created_at'])
            ) for row in rows
        ]

    def add_rating(self, movie_id: int, user_id: Optional[int], rating: int) -> int:
        cur = self.conn.cursor()
        created_at = datetime.now(IST).isoformat()
        cur.execute(
            'INSERT INTO ratings (movie_id, user_id, rating, created_at) VALUES (?, ?, ?, ?)',
            (movie_id, user_id, rating, created_at)
        )
        self.conn.commit()
        return cur.lastrowid

    def get_ratings_for_movie(self, movie_id: int) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM ratings WHERE movie_id=?', (movie_id,))
        return [dict(r) for r in cur.fetchall()]

    def create_watchlist(self, user_id: int, name: str) -> int:
        cur = self.conn.cursor()
        cur.execute('INSERT INTO watchlists (user_id, name) VALUES (?, ?)', (user_id, name))
        self.conn.commit()
        return cur.lastrowid

    def add_to_watchlist(self, watchlist_id: int, movie_id: int) -> int:
        cur = self.conn.cursor()
        cur.execute('INSERT INTO watchlist_items (watchlist_id, movie_id) VALUES (?, ?)', (watchlist_id, movie_id))
        self.conn.commit()
        return cur.lastrowid

    def get_watchlist_items(self, watchlist_id: int) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            'SELECT m.* FROM movies m JOIN watchlist_items w ON w.movie_id = m.id WHERE w.watchlist_id=?',
            (watchlist_id,)
        )
        return [dict(r) for r in cur.fetchall()]

    def close(self):
        self.conn.close()
