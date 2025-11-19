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
        ("Inception", 2010, ["Sci-Fi", "Action"], ["dream", "heist"], "A thief enters dreams to steal secrets.", None),
        ("The Dark Knight", 2008, ["Action", "Drama"], ["hero", "joker"], "Batman faces the Joker in Gotham City.", None),
        ("Interstellar", 2014, ["Sci-Fi", "Drama"], ["space", "time"], "Explorers travel through a wormhole.", None),
        ("Avengers: Endgame", 2019, ["Action", "Sci-Fi"], ["marvel", "thanos"], "Heroes unite to undo the Snap.", None),
        ("Parasite", 2019, ["Drama", "Thriller"], ["korea", "class"], "A poor family infiltrates a rich household.", None),
        ("The Shawshank Redemption", 1994, ["Drama"], ["prison", "hope"], "A man escapes after years in prison.", None),
        ("The Matrix", 1999, ["Sci-Fi", "Action"], ["simulation", "ai"], "A hacker learns reality is a simulation.", None),
        ("Joker", 2019, ["Drama", "Crime"], ["villain", "origin"], "The origin story of a troubled comedian.", None),
        ("Coco", 2017, ["Animation", "Family"], ["music", "mexico"], "A boy enters the Land of the Dead.", None),
        ("Lion King", 1994, ["Animation", "Drama"], ["lion", "disney"], "Simba learns the meaning of responsibility.", None),
        ("Whiplash", 2014, ["Drama"], ["music", "jazz"], "A drummer faces a brutal instructor.", None),
        ("Frozen", 2013, ["Animation", "Family"], ["disney", "magic"], "Two sisters confront magical powers.", None),
        ("Iron Man", 2008, ["Action", "Sci-Fi"], ["marvel", "suit"], "Tony Stark becomes Iron Man.", None),
        ("Dangal", 2016, ["Drama", "Sports"], ["india", "wrestling"], "A father trains daughters to become wrestlers.", None),
        ("3 Idiots", 2009, ["Comedy", "Drama"], ["india", "college"], "Three friends navigate engineering college.", None),
        ("Bahubali: The Beginning", 2015, ["Action", "Drama"], ["india", "epic"], "A warrior discovers his royal legacy.", None),
        ("Bahubali: The Conclusion", 2017, ["Action", "Drama"], ["india", "epic"], "The epic story continues to its climax.", None),
        ("Tenet", 2020, ["Sci-Fi", "Action"], ["time inversion", "spy"], "A secret agent manipulates time to stop a threat.", None),
        ("Oppenheimer", 2023, ["Drama", "History"], ["nuclear", "ww2"], "The story of J. Robert Oppenheimer.", None),
        ("KGF: Chapter 1", 2018, ["Action", "Drama"], ["india", "gangster"], "A man rises from poverty to power.", None),
    ]
    for title, year, genres, tags, synopsis, poster_path in sample_movies:
        lib.add_movie(title, year, genres, tags, synopsis, poster_path)

    movies = lib.list_movies()
    for i, m in enumerate(movies, start=1):
        lib.add_rating(movie_id=m.id, user_id=None, rating=6 + i)
    lib.close()
