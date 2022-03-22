from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from uuid import UUID


class UserLogin(BaseModel):
    username: str
    password: str


class UserAuth(BaseModel):
    id: UUID
    username: str
    email: EmailStr


class ForgotPassword(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    reset_code: UUID
    new_password: str
    confirm_new_password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str


class ActivateEmail(BaseModel):
    email: EmailStr


class ConfirmAccountActivation(BaseModel):
    activation_code: UUID
