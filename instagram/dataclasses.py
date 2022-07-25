from dataclasses import dataclass
from typing import List

@dataclass
class InstagramComment:
    author: str
    author_full_name: str
    like_count: int
    result: str

@dataclass
class InstagramImage:
    width: int
    height: int
    url: str

@dataclass
class InstagramContent:
    PK: int
    ID: int
    content_url: str
    images: List[InstagramImage]
    original_width: int
    original_height: int
    author: str
    author_full_name: str
    like_count: int
    result: str
    comments: List[InstagramComment] = []
