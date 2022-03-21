from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ValidationError, validator, EmailStr
from uuid import UUID



class UserBase(BaseModel):
    username: str
    password: str
    password2: str
    email: EmailStr

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserDisplay(BaseModel):
    id: UUID
    username: str
    password: str
    email: str
    registered_at: datetime
    is_active: bool
    is_admin: bool
    is_superuser: bool

    class Config():
        orm_mode = True
