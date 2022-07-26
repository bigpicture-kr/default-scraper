from dataclasses import dataclass
from enum import Enum
from typing import List
from datetime import datetime

class InstagramMediaType(Enum):
    IMAGE = 1
    VIDEO = 2
    CAROUSEL_IMAGE = 8

@dataclass
class InstagramUser:
    PK: int
    username: str
    full_name: str
    is_private: bool
    profile_pic_url: str

@dataclass
class InstagramCaption:
    PK: int
    user: InstagramUser
    text: str
    type: int
    created_at: datetime
    content_type: str
    status: str

@dataclass
class InstagramImage:
    width: int
    height: int
    url: str

@dataclass
class InstagramContent:
    PK: int
    ID: int
    taken_at: datetime
    media_type: InstagramMediaType
    code: str
    comment_count: int
    user: InstagramUser
    like_count: int
    caption: InstagramCaption
    accessibility_caption: str
    images: List[InstagramImage]
    original_width: int
    original_height: int
