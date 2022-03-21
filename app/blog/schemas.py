from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint
from uuid import UUID


class Author(BaseModel):
    id: UUID
    username: str

    class Config():
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    # author_id: Optional[UUID]
    image_url: Optional[str]


class PostBaseUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    image_url: Optional[str]
    remove_image: bool = False

class PostDisplay(BaseModel):
    id: UUID
    title: str
    content: str
    image_url: Optional[str]
    published: bool
    created_at: datetime

    author: Optional[Author]

    class Config():
        orm_mode = True


class VoteBase(BaseModel):
    post_id: UUID
    # dir: conint(le=1,ge=0)
