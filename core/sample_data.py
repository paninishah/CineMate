from .library import Library
from datetime import datetime
from typing import Optional

def seed_sample(db_path: Optional[str] = None):
    lib = Library(db_path)
    cur = lib.conn.cursor()
    cur.execute('DELETE FROM movies')
    cur.execute('DELETE FROM ratings')
    lib.conn.commit()

    sample_movies = [
        ("The Silent Dawn", 2018, ["Drama", "Indie"], ["quiet", "award-winning"], "A slow-burning drama.", None),
        ("Space Runners", 2021, ["Sci-Fi", "Action"], ["space", "fast"], "Futuristic space action.", None),
        ("Laugh Lines", 2016, ["Comedy"], ["funny"], "A small comedy about friends.", None),
    ]
    for title, year, genres, tags, synopsis, poster_path in sample_movies:
        lib.add_movie(title, year, genres, tags, synopsis, poster_path)

    movies = lib.list_movies()
    for i, m in enumerate(movies, start=1):
        lib.add_rating(movie_id=m.id, user_id=None, rating=6 + i)
    lib.close()
