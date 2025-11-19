from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Media:
    id: Optional[int]
    title: str
    year: Optional[int]
    tags: List[str]
    created_at: datetime

    def to_dict(self):
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        d['tags'] = ','.join(self.tags)
        return d

@dataclass
class Movie(Media):
    genres: List[str]
    synopsis: str
    poster_path: Optional[str] = None

    def to_dict(self):
        d = super().to_dict()
        d.update({
            'genres': ','.join(self.genres),
            'synopsis': self.synopsis,
            'poster_path': self.poster_path,
        })
        return d
