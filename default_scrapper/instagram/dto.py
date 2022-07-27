from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List
from datetime import datetime

class InstagramMediaType(Enum):
    IMAGE = 1
    VIDEO = 2
    CAROUSEL_IMAGE = 8

@dataclass
class InstagramDataclassInterface:
    _data: Dict = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        if len(self._data) > 0:
            data = {k.lower(): v for k, v in self._data.items() if k.lower() in self.__dict__.keys()}
            self.__dict__.update(data)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != "_data"}

@dataclass
class InstagramUser(InstagramDataclassInterface):
    pk: int = field(default=None)
    username: str = field(default=None)
    full_name: str = field(default=None)
    is_private: bool = field(default=None)
    profile_pic_url: str = field(default=None)

@dataclass
class InstagramCaption(InstagramDataclassInterface):
    pk: int = field(default=None)
    user: InstagramUser = field(default=None)
    text: str = field(default=None)
    type: int = field(default=None)
    created_at: datetime = field(default=None)
    content_type: str = field(default=None)
    status: str = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        self.user = InstagramUser(self.user)

@dataclass
class InstagramImage(InstagramDataclassInterface):
    width: int = field(default=None)
    height: int = field(default=None)
    url: str = field(default=None)

@dataclass
class InstagramContent(InstagramDataclassInterface):
    pk: int = field(default=None)
    id: int = field(default=None)
    taken_at: datetime = field(default=None)
    media_type: InstagramMediaType = field(default=None)
    code: str = field(default=None)
    comment_count: int = field(default=None)
    user: InstagramUser = field(default=None)
    like_count: int = field(default=None)
    caption: InstagramCaption = field(default=None)
    accessibility_caption: str = field(default=None)
    original_width: int = field(default=None)
    original_height: int = field(default=None)
    images: List[InstagramImage] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.media_type = InstagramMediaType(self.media_type)
        self.user = InstagramUser(self.user)
        self.caption = InstagramCaption(self.caption)
        if "image_versions2" in self._data:
            self.images = [InstagramImage(image) for image in self._data['image_versions2']['candidates']]
        elif "carousel_media" in self._data:
            self.images = []
            for media in self._data['carousel_media']:
                self.images += [InstagramImage(image) for image in media['image_versions2']['candidates']]
