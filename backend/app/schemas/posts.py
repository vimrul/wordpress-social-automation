from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class Post(BaseModel):
    id: int
    date: datetime
    title: str
    excerpt: Optional[str]
    link: HttpUrl
    seo_description: Optional[str]
    featured_image: Optional[HttpUrl]

class PostsResponse(BaseModel):
    count: int
    posts: List[Post]
