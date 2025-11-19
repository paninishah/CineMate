import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from .library import Library
from typing import Optional

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analytics_output'))

def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def genre_count_plot(db_path: Optional[str] = None) -> str:
    _ensure_output_dir()
    lib = Library(db_path)
    movies = lib.list_movies()
    lib.close()
    output_file = os.path.join(OUTPUT_DIR, 'genre_counts.png')
    if not movies:
        plt.figure()
        plt.text(0.5, 0.5, 'No data', ha='center', va='center')
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        return output_file

    rows = [{'id': m.id, 'title': m.title, 'genres': m.genres, 'created_at': m.created_at} for m in movies]
    df = pd.DataFrame(rows)
    df['genres'] = df['genres'].apply(lambda g: g.split(',') if isinstance(g, str) else g)
    df = df.explode('genres')
    df['genres'] = df['genres'].str.strip().str.lower()
    genre_counts = df['genres'].value_counts()
    ax = genre_counts.plot(kind='bar')
    ax.set_title('Genre Counts')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Count')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file

def rating_histogram(db_path: Optional[str] = None) -> str:
    _ensure_output_dir()
    lib = Library(db_path)
    cur = lib.conn.cursor()
    cur.execute('SELECT rating FROM ratings')
    ratings = [r['rating'] for r in cur.fetchall()]
    lib.close()

    output_file = os.path.join(OUTPUT_DIR, 'rating_histogram.png')
    plt.figure()
    if not ratings:
        plt.text(0.5, 0.5, 'No ratings', ha='center', va='center')
        plt.axis('off')
        plt.savefig(output_file)
        plt.close()
        return output_file
    arr = np.array(ratings)
    plt.hist(arr, bins=np.arange(0, 11) - 0.5, edgecolor='black')
    plt.title('Ratings Histogram')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.xticks(range(0, 11))
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file

def monthly_additions(db_path: Optional[str] = None) -> str:
    _ensure_output_dir()
    lib = Library(db_path)
    movies = lib.list_movies()
    lib.close()
    output_file = os.path.join(OUTPUT_DIR, 'monthly_additions.png')
    if not movies:
        plt.figure()
        plt.text(0.5, 0.5, 'No data', ha='center', va='center')
        plt.axis('off')
        plt.savefig(output_file)
        plt.close()
        return output_file

    rows = [{'title': m.title, 'created_at': m.created_at} for m in movies]
    df = pd.DataFrame(rows)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month'] = df['created_at'].dt.to_period('M')
    monthly_counts = df.groupby('month').size()
    monthly_counts.index = monthly_counts.index.to_timestamp()
    ax = monthly_counts.plot()
    ax.set_title('Monthly Additions')
    ax.set_xlabel('Month')
    ax.set_ylabel('Count')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file
