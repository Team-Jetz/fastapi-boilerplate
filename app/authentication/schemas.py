from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class UserLogin(BaseModel):
    username: str
    password: str


class UserAuth(BaseModel):
    id: UUID
    username: str
    email: str