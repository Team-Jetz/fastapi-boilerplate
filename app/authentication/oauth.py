from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from settings.databases import get_db
from app.account import views as UserView

from settings.config import JWT as SettingsJWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()

  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=int(SettingsJWT['ACCESS_TOKEN_EXPIRE_MINUTES']))

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode,  SettingsJWT['SECRET_KEY'], algorithm= SettingsJWT['ALGORITHM'])

  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SettingsJWT['SECRET_KEY'], algorithms=SettingsJWT['ALGORITHM'])
    username: str = payload.get("username")

    if username is None:
      raise credentials_exception

  except JWTError:
    raise credentials_exception

  user = UserView.find_user_by_username(db, username)

  if not user:
    raise credentials_exception

  if not user.is_active:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, 
          detail="Please verify your email or contact your administrator to activate your account."
      )

  return user
