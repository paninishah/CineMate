import csv
import json
from typing import List, Dict, Any
import os
from functools import reduce

def normalize_title(title: str) -> str:
    return ' '.join(title.strip().split()).title()

def extract_genre_counts(movies: List[Dict[str, Any]]) -> Dict[str, int]:
    all_genres = list(
        reduce(lambda acc, gstr: acc + (gstr.split(',') if gstr else []),
               map(lambda m: m.get('genres', ''), movies),
               [])
    )
    cleaned = [s.strip().lower() for s in all_genres if s]
    counts = {}
    for g in cleaned:
        counts[g] = counts.get(g, 0) + 1
    return counts

def export_movies_to_csv(movies: List[Dict[str, Any]], path: str):
    if not movies:
        return
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(movies[0].keys()))
            writer.writeheader()
            for m in movies:
                writer.writerow(m)
    except Exception as e:
        raise RuntimeError(f"Failed to write CSV: {str(e)}")

def import_movies_from_csv(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [dict(r) for r in reader]
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV: {str(e)}")

def export_to_json(obj: Any, path: str):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"Failed to write JSON: {str(e)}")

def import_from_json(path: str) -> Any:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read JSON: {str(e)}")

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def scan_folder_for_posters(folder_path: str) -> List[str]:
    results = []
    if not os.path.exists(folder_path):
        return results

    def _scan(path: str):
        try:
            for entry in os.listdir(path):
                full = os.path.join(path, entry)
                if os.path.isdir(full):
                    _scan(full)
                else:
                    _, ext = os.path.splitext(entry)
                    if ext.lower() in IMAGE_EXTS:
                        results.append(full)
        except PermissionError:
            return  

    _scan(folder_path)
    return results
